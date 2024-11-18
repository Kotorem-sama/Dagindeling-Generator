from pathlib import Path
import json

class json_file:
    def read(path:str):
        """Returns the information stored in a JSON file via a path."""
        new_path = Path(__file__).parent.parent / path
        if new_path.exists():
            contents = new_path.read_text()
            information:dict = json.loads(contents)
            return information
        else:
            return None