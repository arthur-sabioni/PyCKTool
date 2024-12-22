import os
import glob
import chardet

from pycktools.model.class_model import Class
from pycktools.parser.code_parser import CodeParser

class FolderParser:

    def __init__(self, path) -> None:

        self.path = path
        self.parser = CodeParser()
        
    @staticmethod
    def _guess_file_encode(file_path):
        """
        Guess the encoding of a file using chardet library.
        If undefined, utf-8 is default
        """
        file_encoding = ""
        with open(file_path, 'rb') as file:
            file_encoding = chardet.detect(file.read())['encoding']
        if file_encoding is None:
            return 'utf-8'
        return file_encoding
    
    def parse_path(self) -> dict[str, Class]:

        """
        Parses all the python files in the folder and its subfolders.

        Returns:
            dict: The extracted data.
        """
        #TODO: Modularize this code
        for file_path in glob.iglob(os.path.join(self.path, '**', '*.py'), recursive=True):
            current_code = ""
            try:
                with open(file_path, 'r', encoding='utf_8_sig') as file:
                    current_code = file.read()
            except UnicodeDecodeError:
                # Try to detect file encoding
                try:
                    file_encoding = self._guess_file_encode(file_path)
                    with open(file_path, 'r', encoding=file_encoding) as file:
                        current_code = file.read()
                except Exception as e:
                    print('Failed to read file: ', file_path)
            try:
                self.parser.extract_code_data(current_code, file_path)
            except Exception as e:
                print('Failed to parse file content: ', file_path)

        self.parser.process_possible_coupled_classes()
            
        return self.parser.classes

if __name__ == "__main__":

    path = 'F:\\CEFET\\TCC\\PyCKTools\\pycktools\\example' 
    fp = FolderParser(path)
    fp.parse_path()