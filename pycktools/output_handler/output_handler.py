import os
from output_handler.csv_output import CSVOutput
from output_handler.json_output import JSONOutput

class OutputHandler:

    @staticmethod
    def save_results(
        classes_data: dict, methods_data: dict, file_name: str, 
        output_format: str= 'csv'
    ) -> None:
        #TODO: Improve this copy paste
        path_classes = file_name + '-classes.' + output_format
        path_classes = os.path.join(os.getcwd(), path_classes)

        path_methods = file_name + '-methods.' + output_format
        path_methods = os.path.join(os.getcwd(), path_methods)
        if output_format == 'csv':
            CSVOutput.save_results(classes_data, path_classes)
            CSVOutput.save_results(methods_data, path_methods)
        elif output_format == 'json':
            JSONOutput.save_results(classes_data, path_classes)
            JSONOutput.save_results(methods_data, path_methods)
        