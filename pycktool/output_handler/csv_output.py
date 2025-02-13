import csv

class CSVOutput:
    
    @staticmethod
    def format_class_results(data: dict) -> dict:
        """
        Formats class results into a dictionary suitable for CSV output.

        This function takes a dictionary where each key is a class name and each value
        is a dictionary of results associated with that class. It processes this data 
        to produce a new dictionary with keys being CSV columns, and values being
        column lines.
        """
        if not len(data) or not len(list(data.values())[0]):
            return dict()
        
        # Gets the list of method results identifications
        results_headers = list(list(data.values())[0].keys())
        class_header = 'class'
        
        full_headers = [class_header, *results_headers]
        
        formatted_dict = dict()
        for header in full_headers:
            formatted_dict[header] = list()
            
        for class_name in data.keys():
            formatted_dict[class_header].append(class_name)
            for result_name in data[class_name].keys():
                formatted_dict[result_name].append(data[class_name][result_name])
                
        return formatted_dict
    
    @staticmethod
    def format_method_results(data: dict) -> dict:
        """
        Formats method results into a dictionary suitable for CSV output.

        This function takes a dictionary where each key is a class name and each value
        is a dictionary of results associated with that class. It processes this data 
        to produce a new dictionary with keys being CSV columns, and values being
        column lines.
        """
    
        if not len(data) or not len(list(data.values())[0]):
            return dict()
        
        # Gets the list of method results identifications
        results_headers = list(list(next(iter(data.values())).values())[0].keys())
        class_header = 'class'
        method_header = 'method'
        
        full_headers = [class_header, method_header,*results_headers]
        
        formatted_dict = dict()
        for header in full_headers:
            formatted_dict[header] = list()
            
        for class_name in data.keys():
            for method_name in data[class_name].keys():
                formatted_dict[class_header].append(class_name)
                formatted_dict[method_header].append(method_name)
                for result_name in data[class_name][method_name].keys():
                    formatted_dict[result_name].append(data[class_name][method_name][result_name])
                
        return formatted_dict

    @staticmethod
    def save_results(data: dict, path: str) -> None:
        """
        Saves the results of the metrics extraction to a CSV file.

        This function takes a dictionary with keys as class names and values as
        column lines.
        """

        headers = data.keys()

        with open(path, 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)

            # Write the header to the CSV
            writer.writerow(headers)

            # Write the rows to the CSV (zipping values together)
            writer.writerows(zip(*data.values()))

    