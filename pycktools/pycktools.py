from parser.folder_parser import FolderParser
from metrics.metrics import Metrics

def run(path: str) -> None:

    fp = FolderParser(path)
    fp.parse_path()

    metrics = Metrics(fp.parser.classes, fp.parser.inheritances)
    results = metrics.calculate_metrics()

    print('')

if __name__ == "__main__":

    path = 'F:\\CEFET\\TCC\\PyCKTools\\pycktools\\example' 
    run(path)