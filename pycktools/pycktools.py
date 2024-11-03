from pycktools.output_handler.output_handler import OutputHandler
from pycktools.parser.folder_parser import FolderParser
from pycktools.metrics.metrics import Metrics

def run(path: str, output_format: str= 'csv') -> None:

    fp = FolderParser(path)
    fp.parse_path()

    metrics = Metrics(fp.parser.classes, fp.parser.inheritances)
    results_class, results_methods = metrics.calculate_all_metrics()

    OutputHandler.save_results(
        results_class, results_methods, 'results', output_format
    )

    print('')

if __name__ == "__main__":

    path = 'C:\\CEFET\\TCC\\PyCKTools\\pycktools\\example' 
    run(path, 'csv')