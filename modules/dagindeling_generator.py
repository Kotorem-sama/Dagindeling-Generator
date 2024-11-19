from classes.werknemers import Ingeplanden
from classes.locaties import Locaties

def generator(ingeplanden:Ingeplanden, locaties:Locaties):
    locaties.sort("belang")
    ingeplanden.sort("inwerk_probability")
    priority = [i for i in ingeplanden.medewerkers
                if i.inwerk_probability == 100]
    