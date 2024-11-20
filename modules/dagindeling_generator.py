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

def get_employees_per_group(loc_ids:list, s_list:list, absenten:list):
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
    ingeplanden.sort("inwerk_probability")
    total_inwerkers = len(ingeplanden.inwerkers)

    dagindeling = {}
    for location in locations.open_locaties:
        dagindeling[location.id] = []

    # Gets a list of all the new employees
    priority_list = [ i for i in ingeplanden.medewerkers if i.inwerk_probability
                == 100 and i not in ingeplanden.absenten ]
    
    # First fill the groups (beginner locations) with new employees
    for group in locations.groepen.values():
        if priority_list:
            total_inwerkers -= 1
        for location in group:
            if not priority_list or dagindeling.get(location, "No") == "No":
                break
            employee = priority_list.pop(0)
            ingeplanden.delete_werknemer(employee)
            dagindeling[location].append(employee)
    
    # If there's more new employees, the while loop will continue till every
    # new employee has a spot.
    locations.sort("moeilijkheidsgraad")
    index = 0
    while priority_list and index < len(locations.open_locaties):
        next_location = locations.open_locaties[index]
        index += 1

        # If the dagindeling doesnt have any employees scheduled in
        # the next location, it will add a new employee.
        if len(dagindeling[next_location.id]) == 0:
            total_inwerkers -= 1
            employee = priority_list.pop(0)
            ingeplanden.delete_werknemer(employee)
            dagindeling[next_location.id].append(employee)

    locations.sort("belang")
    index = 0
    priority_list = [ i for i in ingeplanden.medewerkers if
            i.inwerk_probability != 100 and i not in ingeplanden.absenten ]
    while total_inwerkers > 0 and index < len(locations.open_locaties):

        next_location = locations.open_locaties[index]
        index += 1

        if len(dagindeling[next_location.id]) < next_location.minimale_medewerkers:
            total_inwerkers -= 1
            employee = priority_list.pop(0)
            ingeplanden.delete_werknemer(employee)
            dagindeling[next_location.id].append(employee)

    for location in locations.open_locaties:
        minimum = location.minimale_medewerkers
        if len(dagindeling[location.id]) == minimum:
            continue
        
        possibilities = get_employees_per_location(location.id,
                                            ingeplanden.interne_medewerkers,
                                            ingeplanden.absenten)
        if not possibilities:
            continue
        
        lower_fysical_power = get_lower_fysical_power(possibilities, location)
        remaining = [i for i in possibilities if i not in lower_fysical_power]
        if not remaining:
            continue
        
        if len(remaining) > 1:
            employee = get_least_locations(possibilities)
        else:
            employee = remaining[0]
        
        ingeplanden.delete_werknemer(employee)
        dagindeling[location.id].append(employee)