import pypandoc
import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials

def create_folder(currentFolder, name):  
    _path = os.path.join(currentFolder,name)
    if not os.path.exists(_path):
        os.mkdir(_path)
        return _path
    else:
        return _path
    

def get_files_paths(inputFolderPath,filesToIgnore):
    _f = []
    for _file in os.listdir(inputFolderPath):
        if os.path.isfile(os.path.join(inputFolderPath, _file)) and "." +_file.rsplit('.',1)[1] not in filesToIgnore:
            _f.append(_file)

    return _f
    
def generate_name_for_output_file(outputFolderPath,fileName):
     return os.path.join(outputFolderPath,fileName.rsplit('.',1)[0])+ "(" + fileName.rsplit('.',1)[1]+ ")" + ".md"
        
def convert_files_to_md(inputFiles, inputFolderPath, outputFolderPath):
    if len(inputFiles)  > 0: 
            for _file in inputFiles:
                pypandoc.convert_file(source_file =os.path.join(inputFolderPath,_file), to = 'rst' , outputfile =generate_name_for_output_file(outputFolderPath,_file) ,cworkdir= outputFolderPath)
                print(_file + " converted")
    else:
            print("0 files in input folder")

def get_folder_id(service, folder_name):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(q=query, spaces='drive').execute()
    folders = results.get('files', [])
    if not folders:
        raise FileNotFoundError(f"No folder found with the name '{folder_name}'")
    return folders[0]['id']

def download_docx_files(service, folder_id, download_path):
    # Query for all files in the folder
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    files = results.get('files', [])
    
    if not files:
        print("No files found in the folder.")
        return

    

    for file in files:
        file_id = file['id']
        file_name = file['name']
        mime_type = file['mimeType']

        if mime_type == 'application/vnd.google-apps.document':
            # Export Google Docs as .docx
            request = service.files().export_media(
                fileId=file_id, 
                mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            file_name += ".docx"  # Append .docx to the filename
        else:
            print(f"Skipping unsupported file: {file_name} (MIME Type: {mime_type})")
            continue

        file_path = os.path.join(download_path, file_name)
        with io.FileIO(file_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Downloading {file_name}: {int(status.progress() * 100)}%")
    print("Download complete.")

if __name__ == '__main__':
    SERVICE_ACCOUNT_FILE =  os.path.expanduser("~") + "/Downloads/"+"quiet-antler-442510-n5-895e32a3d7d7.json" # REPLACE "quiet-antler..." WITH YOUR FILE 
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    FOLDER_NAME = 'docs'
    filesToIgnore = [".DS_Store", ".txt", ".pdf"]
    inputFolderName = "input"
    outputFolderName = "output"
    inputFolderPath  = create_folder(os.getcwd(), inputFolderName)
    DOWNLOAD_PATH = inputFolderPath
    outputFolderPath = create_folder(os.getcwd(), outputFolderName)
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    try:
        folder_id = get_folder_id(service, FOLDER_NAME)
        download_docx_files(service, folder_id, DOWNLOAD_PATH)

    except Exception as e:
        print(f"-------------------------------ERROR-------------------------------\n: {e}")

    inputFiles = get_files_paths(inputFolderPath,filesToIgnore)
    convert_files_to_md(inputFiles, inputFolderPath, outputFolderPath)


#epub rtf problems
#todo:
# import TED and connect with pandoc
