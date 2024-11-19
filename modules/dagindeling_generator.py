from classes.werknemers import Ingeplanden
from classes.locaties import Locaties

def generator(ingeplanden:Ingeplanden, locaties:Locaties):

    if len(ingeplanden.medewerkers) < locaties:
        pass