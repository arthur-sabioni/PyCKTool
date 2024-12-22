import json

class JSONOutput:

    @staticmethod
    def save_results(results: dict, path: str) -> None:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(results, file, indent=4)