from classes.read_files import csv_file
from classes.werknemers import Werknemers
from classes.locaties import locaties
from random import *

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

werknemers = Werknemers('data/werknemers.json')
# werknemers.save_to_file()

# locatie_list = locaties('data/locaties.json')
# locatie_list.save_to_file()

# aanwezigen = Werknemers()
# aanwezigen.to_class(randomise_list(werknemers.medewerkers[:], 35))

