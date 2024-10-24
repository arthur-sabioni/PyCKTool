from output_handler.output_handler import OutputHandler
from parser.folder_parser import FolderParser
from metrics.metrics import Metrics

def run(path: str, output_format: str= 'csv') -> None:

    fp = FolderParser(path)
    fp.parse_path()

    metrics = Metrics(fp.parser.classes, fp.parser.inheritances)
    results = metrics.calculate_metrics()

    OutputHandler.save_results(results, 'results', output_format)

    print('')

if __name__ == "__main__":

    path = 'F:\\CEFET\\TCC\\PyCKTools\\pycktools\\example' 
    run(path, 'csv')