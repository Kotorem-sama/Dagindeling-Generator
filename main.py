import json
from pathlib import Path
from random import *

def get_stored_information(path:Path):
    """Returns the information stored in a JSON file via a path."""
    if path.exists():
        contents = path.read_text()
        information:dict = json.loads(contents)
        return information
    else:
        return None

def seperate_inwerkers(given_list:list):
    """Takes a list of 'werknemer dictionaries' and returns 2 lists with
    'inwerkers' seperated from 'werknemers'."""
    inwerkers = []
    werknemers = []
    for i in range(len(given_list)):
        if given_list[i]["inwerker"]:
            inwerkers.append(given_list[i])
        else:
            werknemers.append(given_list[i])
    given_list = werknemers
    return inwerkers, werknemers

def randomise_list(given_list:list, total:int):
    """Returns a randomised list with a set total. Makes sure there are no
    duplicates and returns None if the list has a smaller size than the total
    parameter."""
    if total > len(given_list):
        return None
    
    random_list = []
    for i in range(total):
        random_number = randint(0, len(given_list)-1)
        random_list.append(given_list[random_number])
        del given_list[random_number]
    return random_list
    
werknemers_path = Path(__file__).parent / 'data/werknemers.json'
werknemers_dict = get_stored_information(werknemers_path)

locaties_path = Path(__file__).parent / 'data/locaties.json'
locaties_dict = get_stored_information(locaties_path)

dagindeling = {}
for locatie in locaties_dict:
    if locatie["beschikbaarheid"]:
        dagindeling[locatie["id"]] = ""

aanwezigen = randomise_list(werknemers_dict[:], 35)
inwerkers, werknemers = seperate_inwerkers(aanwezigen)