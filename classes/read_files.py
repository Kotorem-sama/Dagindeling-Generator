from pathlib import Path
import csv
import json

class json_file:
    def read(path:str):
        """Returns the information stored in a JSON file via a path."""
        new_path = Path(__file__).parent.parent / path
        if new_path.exists():
            contents = new_path.read_text()
            information:list = json.loads(contents)
            return information
        else:
            return None
    
    def write(path:str, information):
        """Saves the information given to a provided JSON file"""
        new_path = Path(__file__).parent.parent / path
        new_path.parent.mkdir(exist_ok=True)
        data = json.dumps(information)
        new_path.write_text(data)

class csv_file:
    def read(path:str):
        new_path = Path(__file__).parent.parent / path
        if new_path.exists():
            with new_path.open("r", encoding="utf-8") as file:
                reader = csv.reader(file, delimiter=';')
                return [row for row in reader if row]

    def write(path:str, information:list):
        new_path = Path(__file__).parent.parent / path
        new_path.parent.mkdir(exist_ok=True)
        with new_path.open("w", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=';')
            for info in information:
                    writer.writerow(info)