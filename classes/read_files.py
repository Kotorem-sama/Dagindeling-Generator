from pathlib import Path
import csv
import json
import datetime

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
        new_path.parent.mkdir(exist_ok=True, parents=True)
        data = json.dumps(information)
        new_path.write_text(data)

class csv_file:
    def read(path:str):
        new_path = Path(__file__).parent.parent / path
        if new_path.exists():
            with new_path.open("r", encoding="utf-8", newline="") as file:
                reader = csv.reader(file, delimiter=';')
                return [row for row in reader if row and row[0]]
                

    def write(path:str, information:list):
        new_path = Path(__file__).parent.parent / path
        new_path.parent.mkdir(exist_ok=True, parents=True)
        with new_path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(information)

class date:
    def get():
        work_date = json_file.read('data/work_date.json')
        if work_date:
            return work_date
        else:
            today = datetime.date.today()
            today = today.strftime("%Y/%m/%d")
            date.set(today)

    def set(date:str):
        json_file.write('data/work_date.json', [date])