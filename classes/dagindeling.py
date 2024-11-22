import os
from classes.werknemers import Ingeplanden, Inwerker
from classes.locaties import Locaties, Locatie
from classes.werknemers import Extern_medewerker, Intern_medewerker, Inwerker, Werknemers
from classes.read_files import date as get_date
from classes.read_files import json_file as jf
from classes.read_files import csv_file as csv

class Dagindeling:
    def __init__(self):
        self.dagindeling = {}
        self.inwerkers = {}
        self.json = f"data/ingeplanden/{get_date.get()[0]}_dagindeling.json"
        self.csv = f"dagindelingen/{get_date.get()[0]}.csv"
        self.start_up()
    
    def start_up(self):
        file_check = csv.read(self.csv)
        if file_check:
            self.load_csv()
        else:
            self.generator()
            self.save_backup_json()

    def delete_csv(self):
        try:
            os.remove(self.csv)
        except:
            pass

    def delete(self):
        try:
            os.remove(self.json)
        except:
            pass

        self.delete_csv()

    def save_csv(self):
        csv_list = [[ "Locaties", "", "", "", "Inwerkers" ]]
        locations = Locaties(f"data/ingeplanden/{get_date.get()[0]}_locaties.json")

        for key, value in self.dagindeling.items():
            line = []
            locatie = locations.get_location_by_id(int(key))
            line.append(f"{locatie.id}.{locatie.naam}")

            for index in range(3):
                if index < len(value):
                    msg = f"{value[index].naam} ({value[index].personeelsnummer})"
                    line.append(msg)
                else:
                    line.append("")
                    
            if self.inwerkers[key]:
                msg = f"{self.inwerkers[key][0].naam} ({self.inwerkers[key][0].personeelsnummer})"
                line.append(msg)
            else:
                line.append("")
            
            csv_list.append(line)

        csv.write(self.csv, csv_list)

    def load_csv(self):
        werknemers = Werknemers()
        ingeplanden = Ingeplanden(f"{get_date.get()[0]}_ingeplanden.json")

        rows = csv.read(self.csv)
        if not rows:
            return

        for row in rows[1:]:
            self.dagindeling[row[0].split(".")[0]] = []
            self.inwerkers[row[0].split(".")[0]] = []

            for index in range(3):
                if not row[1+index] == "":
                    personeelsnummer = row[1+index].split("(")[-1].replace(")", "")
                    if ingeplanden.is_employee_in_list(int(personeelsnummer)):
                        employee = werknemers.get_employee_by_id(int(personeelsnummer))
                        self.dagindeling[row[0].split(".")[0]].append(employee)
                    
            if not row[4] == "":
                personeelsnummer = row[4].split("(")[-1].replace(")", "")
                if ingeplanden.is_employee_in_list(int(personeelsnummer)):
                    employee = werknemers.get_employee_by_id(int(personeelsnummer))
                    self.inwerkers[row[0].split(".")[0]].append(employee)

    def save_backup_json(self):
        dagindeling = self.to_list()
        jf.write(self.json, dagindeling)

    def load_backup_json(self):
        json_content = jf.read(self.json)
        self.dagindeling = {}
        self.inwerkers = {}
        self.to_class(json_content)

    def to_medewerker(self, werknemer):
        if type(werknemer) == dict:
            if not werknemer["intern"]:
                new_extern = Extern_medewerker()
                new_extern.to_class(werknemer)
                return new_extern
            elif werknemer["inwerker"]:
                new_inwerker = Inwerker()
                new_inwerker.to_class(werknemer)
                return new_inwerker
            else:
                new_intern = Intern_medewerker()
                new_intern.to_class(werknemer)
                return new_intern

    def to_class(self, dagindeling:list):
        for key, value in dagindeling[0].items():
            self.dagindeling[key] = []
            for person in value:
                employee = self.to_medewerker(person)
                self.dagindeling[key].append(employee)
        
        for key, value in dagindeling[1].items():
            self.dagindeling[key] = []
            for person in value:
                employee = self.to_medewerker(person)
                self.dagindeling[key].append(employee)

    def to_list(self):
        dict_dagindeling = {}
        for key, value in self.dagindeling.items():
            dict_dagindeling[key] = []
            for person in value:
                employee = person.to_dict()
                del employee["ingewerkte_locaties"]
                dict_dagindeling[key].append(employee)

        dict_inwerkers = {}
        for key, value in self.dagindeling.items():
            dict_inwerkers[key] = []
            for person in value:
                employee = person.to_dict()
                del employee["ingewerkte_locaties"]
                dict_inwerkers[key].append(employee)
        return [dict_dagindeling, dict_inwerkers]

    def get_employees_per_location(self, locatie_id:int, search_list:list,
                                absenten:list):
            employees_per_location = []
            sort_with_voorkeur = []

            for employee in search_list:
                if locatie_id in employee.ingewerkte_locaties and (locatie_id
                                not in employee.ongeschikte_locaties) and (
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

    def get_employees_per_group(self, loc_ids:list, s_list:list, absenten:list):
        employees_per_locations = [ self.get_employees_per_location(locatie,
                                    s_list, absenten) for locatie in loc_ids ]
        employees_per_group = []
        if employee_list[0]:
            for employee in employee_list[0]:
                for employee_list in employees_per_locations[1:]:
                    if employee in employee_list:
                        employees_per_group.append(employee)
        
        return employees_per_group

    def get_lower_fysical_power(self, possibilities:list, location:Locatie):
        too_weak = []
        for employee in possibilities:
            if employee.fysieke_kracht < location.fysieke_kracht:
                too_weak.append(employee)

        return too_weak

    def schedule_rest_employees(self, locations:Locaties, dagindeling:list,
                                ingeplanden:Ingeplanden, medewerkers_list,
                                minormax:bool):
        for location in locations.open_locaties:
            if minormax:
                minimum = location.minimale_medewerkers
                if len(dagindeling[location.id]) >= minimum:
                    continue
            else:
                maximum = location.maximale_medewerkers
                if len(dagindeling[location.id]) == maximum:
                    continue
            
            possibilities = self.get_employees_per_location(
                location.id, medewerkers_list, ingeplanden.absenten)
            if not possibilities:
                continue
            
            lower_fysical_power = self.get_lower_fysical_power(
                possibilities,location)
            remaining = [
                i for i in possibilities if i not in lower_fysical_power
                ]
            if not remaining:
                continue
            
            if len(remaining) > 1:
                employee = self.get_least_locations(possibilities)
            else:
                employee = remaining[0]
            
            ingeplanden.delete_werknemer(employee)
            dagindeling[location.id].append(employee)

        return dagindeling

    def get_least_locations(self, possibilities:list):
        amount_list = [len(i.ingewerkte_locaties) for i in possibilities]
        return possibilities[amount_list.index(min(amount_list))]

    def get_inwerker(self, ingeplanden:Ingeplanden):
        try:
            inwerker = ingeplanden.inwerkers[0]
            ingeplanden.delete_werknemer(inwerker)
        except:
            inwerker = "Supervisor"
        return inwerker

    def is_type_in_list(self, search_list:list, types):
        for i in search_list:
            if type(i) == types:
                return True
        return False

    def generator(self):
        ingeplanden = Ingeplanden(f"{get_date.get()[0]}_ingeplanden.json")
        locations = Locaties(f"data/ingeplanden/{get_date.get()[0]}_locaties.json")
        ingeplanden.sort("inwerk_probability")

        for location in locations.open_locaties:
            self.dagindeling[location.id] = []
            self.inwerkers[location.id] = []

        # Gets a list of all the new employees
        priority_list = [ i for i in ingeplanden.medewerkers if
                i.inwerk_probability == 100 and i not in ingeplanden.absenten 
                ]
        
        # First fill the groups (beginner locations) with new employees
        for group in locations.groepen.values():
            if priority_list:
                inwerker = self.get_inwerker(ingeplanden)
            for location in group:
                if not priority_list or self.dagindeling.get(location,"No")=="No":
                    break
                employee = priority_list.pop(0)
                ingeplanden.delete_werknemer(employee)
                self.dagindeling[location].extend([employee])
                self.inwerkers[location] = [inwerker]
        
        # If there's more new employees, the while loop will continue till every
        # new employee has a spot.
        locations.sort("moeilijkheidsgraad")
        locations.reverse()

        index = 0
        while priority_list and index < len(locations.open_locaties):
            next_location = locations.open_locaties[index]
            if not len(self.dagindeling[next_location.id]) < (
                next_location.maximale_medewerkers):

                index += 1

            # If the dagindeling doesnt have any employees scheduled in
            # the next location, it will add a new employee.
            if len(self.dagindeling[next_location.id]) < (
                next_location.maximale_medewerkers):
                employee = priority_list.pop(0)
                ingeplanden.delete_werknemer(employee)
                
                if self.inwerkers[next_location.id]:
                    self.dagindeling[next_location.id].extend([employee])
                else:
                    inwerker = self.get_inwerker(ingeplanden)
                    self.inwerkers[next_location.id] = [inwerker]
                    self.dagindeling[next_location.id].extend([employee])

        # If theres inwerkers left, people with the highest inwerk_probability
        # will be scheduled first.
        locations.sort("belang")
        index = 0
        priority_list = [ i for i in ingeplanden.medewerkers if
                i.inwerk_probability != 100 and i not in ingeplanden.absenten
                and i not in ingeplanden.inwerkers ]
        while len(ingeplanden.inwerkers) > 0 and index < len(
            locations.open_locaties) and len(priority_list) > 0:

            next_location = locations.open_locaties[index]
            index += 1

            if len(self.dagindeling[next_location.id]) < (
                next_location.maximale_medewerkers):
                employee = priority_list.pop(0)
                ingeplanden.delete_werknemer(employee)
                
                if self.inwerkers[next_location.id]:
                    self.dagindeling[next_location.id].extend([employee])
                else:
                    inwerker = self.get_inwerker(ingeplanden)
                    self.inwerkers[next_location.id] = [inwerker]
                    self.dagindeling[next_location.id].extend([employee])

        # All internal employees are added to the dagindeling
        self.dagindeling = self.schedule_rest_employees(locations,
            self.dagindeling, ingeplanden, ingeplanden.interne_medewerkers,True)
        self.dagindeling = self.schedule_rest_employees(locations,
            self.dagindeling, ingeplanden, ingeplanden.externe_medewerkers,True)
        if not ingeplanden.interne_medewerkers and (
            not ingeplanden.externe_medewerkers) and not ingeplanden.inwerkers:
            self.dagindeling = self.schedule_rest_employees(
                locations, self.dagindeling, ingeplanden, ingeplanden.inwerkers,
                True)
        if ingeplanden.interne_medewerkers or ingeplanden.externe_medewerkers:
            self.dagindeling = self.schedule_rest_employees(locations,
                self.dagindeling, ingeplanden, ingeplanden.interne_medewerkers,
                False)
            self.dagindeling = self.schedule_rest_employees(locations,
                self.dagindeling, ingeplanden, ingeplanden.externe_medewerkers,
                False)
            if not ingeplanden.interne_medewerkers and (
                not ingeplanden.externe_medewerkers) and len(
                    ingeplanden.inwerkers) > 0:
                self.dagindeling = self.schedule_rest_employees(locations,
                    self.dagindeling, ingeplanden, ingeplanden.inwerkers, False)