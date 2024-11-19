from classes.werknemers import Ingeplanden
from classes.locaties import Locaties

def generator(ingeplanden:Ingeplanden, locaties:Locaties):
    locaties.sort("belang")
    locaties.reverse()
    priority = []
    