from classes.werknemers import Werknemers, Ingeplanden
from classes.locaties import Locaties
from classes.dagindeling import Dagindeling
from random import *
from tkinter import *

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
werknemers.save_to_file()

locatie_list = Locaties('data/locaties.json')
locatie_list.save_to_file()

dd = Dagindeling()
dd.save_csv()
dd.load_csv()
print(dd.inwerkers)