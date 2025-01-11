from pycktool.output_handler.output_handler import OutputHandler
from pycktool.parser.folder_parser import FolderParser
from pycktool.metrics.metrics import Metrics

class PyCKTool:

    @staticmethod
    def run(path: str, output_format: str= 'csv', prefix: str= '') -> None:

        fp = FolderParser(path)
        fp.parse_path()

        metrics = Metrics(fp.parser.classes)
        results_class, results_methods = metrics.calculate_all_metrics()

        OutputHandler.save_results(
            results_class, results_methods, 'results', output_format, prefix
        )

        print('PyCKTool execution completed')

if __name__ == "__main__":

    path = r'F:\CEFET\TCC\repositorios\PyCKTool' 
    PyCKTool.run(path, 'csv')