from pathlib import Path
import csv
import json
import datetime

class json_file:
    """Een class gemaakt specifiek voor het lezen en wegschrijven naar een
    JSON-bestand."""
    def read(path:str):
        """Geeft de informatie die is opgeslagen in een JSON-bestand in een
        meegegeven pad terug."""

        # Maakt eerst een path aan die altijd start bij de folder
        # "dagindeling generator".
        new_path = Path(__file__).parent.parent / path

        # Als het pad bestaat leest het de informatie uit en stuurt het dat
        # terug. Als het pad niet bestaat stuurt het None terug.
        if new_path.exists():
            contents = new_path.read_text()
            information:list = json.loads(contents)
            return information
        else:
            return None
    
    def write(path:str, information):
        """Slaat de meegegeven informatie op in een JSON-bestand via een
        meegegeven pad."""

        # Maakt eerst een path aan die altijd start bij de folder
        # "dagindeling generator".
        new_path = Path(__file__).parent.parent / path

        # Creert de folders in de path als ze niet bestaan.
        new_path.parent.mkdir(exist_ok=True, parents=True)

        # Verandert de data in json format en schrijft het naar het bestand.
        data = json.dumps(information)
        new_path.write_text(data)

class csv_file:
    """Een class gemaakt specifiek voor het lezen en wegschrijven naar een
    CSV-bestand."""

    def read(path:str):
        """Geeft de informatie die is opgeslagen in een CSV-bestand in een
        meegegeven pad terug."""

        # Maakt eerst een path aan die altijd start bij de folder
        # "dagindeling generator".
        new_path = Path(__file__).parent.parent / path

        # Als het pad bestaat leest het de informatie uit en stuurt het dat
        # terug als list. Als het pad niet bestaat stuurt het None terug.
        if new_path.exists():
            with new_path.open("r", newline="") as file:
                reader = csv.reader(file, delimiter=';')
                return [row for row in reader if row]
                

    def write(path:str, information:list):
        """Slaat de meegegeven informatie op in een CSV-bestand via een
        meegegeven pad."""

        # Maakt eerst een path aan die altijd start bij de folder
        # "dagindeling generator".
        new_path = Path(__file__).parent.parent / path

        # Creert de folders in de path als ze niet bestaan.
        new_path.parent.mkdir(exist_ok=True, parents=True)

        # Opent het csv bestand met een writer en schrijft alle regels naar
        # het bestand.
        with new_path.open("w", newline="") as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(information)

class date:
    """Een class die de werk_datum, ookwel de geselecteerde datum, uitleest uit
    een json bestand. Als dit bestand niet bestaat maakt het een nieuw bestand
    aan met de huidige datum."""

    def get():
        """Een functie waarmee de datum wordt terug gegeven. Als de datum niet
        bestaat wordt de dag van vandaag opgeslagen."""
        work_date = json_file.read('data/work_date.json')
        if work_date:
            return work_date
        else:
            today = datetime.date.today()
            today = today.strftime("%Y/%m/%d")
            date.set(today)

    def set(date:str):
        """Een functie waarmee de geselecteerde datum wordt opgeslagen in
        'work_date.json'"""
        json_file.write('data/work_date.json', [date])