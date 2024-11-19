from classes.werknemers import Ingeplanden
from classes.locaties import Locaties

def get_employees_per_location(locatie_id:int, search_list:list):
        employees_per_location = []
        sort_with_voorkeur = []

        for employee in search_list:
            if locatie_id in employee.ingewerkte_locaties and (
                        locatie_id not in employee.ongeschikte_locaties):
                
                if locatie_id in employee.voorkeuren.keys():
                    voorkeur = employee.voorkeuren[locatie_id]
                else:
                    voorkeur = 6
                
                add_dict = { "voorkeur": voorkeur, "medewerker": employee }
                sort_with_voorkeur.append(add_dict)

        if sort_with_voorkeur:
            sort_with_voorkeur = sorted(sort_with_voorkeur,
                                            key=lambda d: d['voorkeur'])
            for employee in sort_with_voorkeur:
                employees_per_location.append(employee["medewerker"])

        return employees_per_location

def generator(ingeplanden:Ingeplanden, locaties:Locaties):
    locaties.sort("belang")
    ingeplanden.sort("inwerk_probability")
    priority = [i for i in ingeplanden.medewerkers
                if i.inwerk_probability == 100]
    
    dagindeling = {}
    for locatie in locaties.open_locaties:
        possibilities = get_employees_per_location(locatie.id,
                                            ingeplanden.interne_medewerkers)
        
        