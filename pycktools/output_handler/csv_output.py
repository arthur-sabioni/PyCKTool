import csv

class CSVOutput:

    @staticmethod
    def save_results_csv(data: dict, path: str) -> None:
        headers = data.keys()

        with open(path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)

            # Write the header to the CSV
            writer.writeheader()

            # Write the rows to the CSV (zipping values together)
            rows = [dict(zip(headers, row)) for row in zip(*data.values())]
            writer.writerows(rows)
