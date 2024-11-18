from pathlib import Path
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
        if new_path.exists():
            data = json.dumps(information)
            new_path.write_text(data)