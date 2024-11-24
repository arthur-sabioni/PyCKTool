import os
from pycktools.output_handler.csv_output import CSVOutput
from pycktools.output_handler.json_output import JSONOutput

class OutputHandler:

    @staticmethod
    def save_results(
        classes_data: dict, methods_data: dict, file_name: str, 
        output_format: str= 'csv'
    ) -> None:
        """
        Saves the results of the metrics extraction to a CSV or JSON file.
        """
        #TODO: Improve this copy paste
        path_classes = file_name + '-classes.' + output_format
        path_classes = os.path.join(os.getcwd(), path_classes)

        path_methods = file_name + '-methods.' + output_format
        path_methods = os.path.join(os.getcwd(), path_methods)
        if output_format == 'csv':
            formatted_classes_data = CSVOutput.format_class_results(classes_data)
            CSVOutput.save_results(formatted_classes_data, path_classes)
            formatted_methods_data = CSVOutput.format_method_results(methods_data)
            CSVOutput.save_results(formatted_methods_data, path_methods)
        elif output_format == 'json':
            JSONOutput.save_results(classes_data, path_classes)
            JSONOutput.save_results(methods_data, path_methods)
        