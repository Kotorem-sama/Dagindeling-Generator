from classes.werknemers import Ingeplanden
from classes.locaties import Locaties, Locatie

def get_employees_per_location(locatie_id:int, search_list:list, absenten:list):
        employees_per_location = []
        sort_with_voorkeur = []

        for employee in search_list:
            if locatie_id in employee.ingewerkte_locaties and (
                        locatie_id not in employee.ongeschikte_locaties) and (
                            employee not in absenten):
                
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

def get_employees_per_afwisseling(loc_ids:list, s_list:list, absenten:list):
    employees_per_locations = [ get_employees_per_location(locatie, s_list,
                                absenten) for locatie in loc_ids ]
    employees_per_group = []
    if employee_list[0]:
        for employee in employee_list[0]:
            for employee_list in employees_per_locations[1:]:
                if employee in employee_list:
                    employees_per_group.append(employee)
    
    return employees_per_group

def get_lower_fysical_power(possibilities:list, location:Locatie):
    too_weak = []
    for employee in possibilities:
        if employee.fysieke_kracht < location.fysieke_kracht:
            too_weak.append(employee)

    return too_weak

def get_least_locations(possibilities:list):
    amount_list = [len(i.ingewerkte_locaties) for i in possibilities]
    return possibilities[amount_list.index(min(amount_list))]

def generator(ingeplanden:Ingeplanden, locations:Locaties):
    locations.sort("belang")
    ingeplanden.sort("inwerk_probability")
    priority = [i for i in ingeplanden.medewerkers
                if i.inwerk_probability == 100]
    
    dagindeling = {}
    afwisselings_groups = []
    for location in locations.open_locaties:
        dagindeling[location.id] = []

        if location.afwisseling > 0 and (
            location.afwisseling not in afwisselings_groups):
            afwisselings_groups.append(location.afwisseling)

    for location in locations.open_locaties:
        possibilities = get_employees_per_location(location.id,
                                            ingeplanden.interne_medewerkers,
                                            ingeplanden.absenten)
        if not possibilities:
            dagindeling[location.id] = ["0_ingewerkt"]
            continue
        
        lower_fysical_power = get_lower_fysical_power(possibilities, location)
        remaining = [i for i in possibilities if i not in lower_fysical_power]
        if not remaining:
            dagindeling[location.id] = ["0_strong"]
            continue
        
        if len(remaining) > 1:
            first_pick = get_least_locations(possibilities)
            index = ingeplanden.interne_medewerkers.index(first_pick)
        else:
            index = ingeplanden.interne_medewerkers.index(remaining[0])
        
        employee = ingeplanden.interne_medewerkers.pop(index)
        dagindeling[location.id].append(employee)
    
    print(len(ingeplanden.interne_medewerkers))