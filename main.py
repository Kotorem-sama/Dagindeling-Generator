from classes.werknemers import Werknemers, Ingeplanden
from classes.locaties import Locaties
from modules.dagindeling_generator import generator
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

totaal = 0
for i in locatie_list.locaties:
    totaal += i.maximale_medewerkers

print(totaal)

# aanwezigen = Ingeplanden("Vandaag.json")
# aanwezigen.to_class(randomise_list(werknemers.to_list()[:], 50))
# generator(aanwezigen, locatie_list)
# aanwezigen.save_to_file()