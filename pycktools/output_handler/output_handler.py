import os
from output_handler.csv_output import CSVOutput
from output_handler.json_output import JSONOutput

class OutputHandler:

    @staticmethod
    def save_results(
        data: dict, file_name: str, output_format: str= 'csv'
    ) -> None:
        path = os.path.join(os.getcwd(), file_name)
        if output_format == 'csv':
            CSVOutput.save_results_csv(data, path)
        elif output_format == 'json':
            JSONOutput.save_results(data, path)
        