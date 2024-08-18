import os
import glob

from parser.code_parser import CodeParser

class FolderParser:

    def __init__(self, path) -> None:

        self.path = path
        self.parser = CodeParser()

    def build_full_code_string(self):
        full_code = ""
        for file_path in glob.iglob(os.path.join(self.path, '**', '*.py'), recursive=True):
            with open(file_path, 'r', encoding='utf-8') as file:
                full_code += file.read() + '\n'
        return full_code
    
    def parse_path(self) -> dict:

        code = self.build_full_code_string()

        self.parser.extract_classes_and_methods(code)

        print('')

if __name__ == "__main__":

    path = 'F:\\CEFET\\TCC\\PyCKTools\\pycktools\\example' 
    fp = FolderParser(path)
    fp.parse_path()