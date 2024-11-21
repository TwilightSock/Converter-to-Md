# Import necessary library
import re
import pypandoc
import os

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
                pypandoc.convert_file(source_file =os.path.join(inputFolderPath,_file), to = 'md' , outputfile =generate_name_for_output_file(outputFolderPath,_file) ,cworkdir= outputFolderPath)
                print(_file + " converted")
    else:
            print("0 files in input folder")



filesToIgnore = [".DS_Store", ".txt", ".pdf"]
inputFolderName = "input"
outputFolderName = "output"
inputFolderPath  = create_folder(os.path.abspath(__file__), inputFolderName)
outputFolderPath = create_folder(os.path.abspath(__file__), outputFolderName)

inputFiles = get_files_paths(inputFolderPath,filesToIgnore)

convert_files_to_md(inputFiles, inputFolderPath, outputFolderPath)

print(os.defpath)

#epub rtf problems
#todo:
# import TED and connect with pandoc