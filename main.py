from classes.read_files import json_file
from random import *
from classes.werknemers import Werknemers

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

werknemers = Werknemers()
werknemers.get_werknemers('data/werknemers.json')

locaties_path = 'data/locaties.json'
locaties_dict = json_file.read(locaties_path)

dagindeling = {}
for locatie in locaties_dict:
    if locatie["beschikbaarheid"]:
        dagindeling[locatie["id"]] = 0

aanwezigen = Werknemers()
aanwezigen.to_class(randomise_list(werknemers.medewerkers[:], 35))
