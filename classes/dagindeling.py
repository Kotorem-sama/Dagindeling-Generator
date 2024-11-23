import os
from classes.werknemers import Ingeplanden, Inwerker
from classes.locaties import Locaties, Locatie
from classes.werknemers import Extern_medewerker, Intern_medewerker
from classes.werknemers import Werknemers, Inwerker, medewerker_format
from classes.read_files import date as get_date
from classes.read_files import json_file as jf
from classes.read_files import csv_file as csv

class Dagindeling:
    """Een dagindeling class die bestaat uit verschillende dictionaries om
    makkelijk werknemers en inwerkers uit elkaar te kunnen houden."""

    def __init__(self):
        """De initialisatie van de class dagindeling. Zet een path neer voor
        json en csv bestand met de geselecteerde datum. Daarna wordt start_up
        uitgevoerd."""

        self.dagindeling = {}
        self.inwerkers = {}
        self.json = f"data/ingeplanden/{get_date.get()[0]}_dagindeling.json"
        self.csv = f"dagindelingen/{get_date.get()[0]}.csv"
        self.start_up()
    
    def start_up(self):
        """Een functie die checkt of een csv bestand bestaat. Zo ja wordt deze
        geladen. Zo nee runt het de generator en wordt deze opgeslagen in
        de backup_json."""

        if csv.path_exists(self.csv):
            self.load_csv()
        else:
            self.generator()
            self.save_backup_json()

    def delete_csv(self):
        """Een functie die probeert het CSV-bestand te verwijderen die staat
        opgeslagen in het pad self.csv."""
        try:
            os.remove(self.csv)
        except:
            pass

    def delete(self):
        """Een functie die probeert het JSON-bestand te verwijderen die staat
        opgeslagen in het pad self.json. Hierna probeert de functie het
        CSV-bestand te verwijderen."""
        try:
            os.remove(self.json)
        except:
            pass

        self.delete_csv()

    def save_csv(self):
        """Een functie die de dagindeling opslaat in het CSV-bestand waarvan de
        path is opgeslagen in self.csv."""

        # Maakt een lijst met lijsten aan voor het csv bestand waarbij de
        # eerste lijst de kolomkopken zijn.
        csv_list = [[ "Locaties", "", "", "", "Inwerkers" ]]

        # Laad alle locaties in via het pad.
        path = f"data/ingeplanden/{get_date.get()[0]}_locaties.json"
        locations = Locaties(path)

        # Per key wordt de locatie opgeslagen en dan wordt er een lijst
        # aangemaakt met als eerste item de locatie id en naam.
        for key, value in self.dagindeling.items():
            locatie = locations.get_location_by_id(int(key))
            line = [f"{locatie.id}.{locatie.naam}"]
            
            # Elke value is een lijst met medewerkers. Hier wordt gecheckt of
            # er een werknemer in de lijst zit. Zo ja wordt de naam en
            # personeelsnummer toegevoegd aan de lijst en zo nee wordt een lege
            # string toegevoegd.
            for index in range(3):
                if index < len(value):
                    employee = value[index]
                    msg = f"{employee.naam} ({employee.personeelsnummer})"
                    line.append(msg)
                else:
                    line.append("")
            
            # Hier wordt gecheckt met dezelfde key (locatie_id) of er inwerkers
            # in de dictionary staan. Zo ja wordt deze toegevoegd aan de lijst,
            # zo nee wordt een lege string toegevoegd.
            if self.inwerkers[str(key)]:
                inwerker = self.inwerkers[str(key)][0]
                try:
                    line.append(f"{inwerker.naam} ({inwerker.personeelsnummer})")
                except:
                    line.append("")
            else:
                line.append("")
            
            # De lijn lijst wordt toegevoegd aan de lijst voor het CSV-bestand.
            csv_list.append(line)

        # Slaat het CSV-bestand op met het pad in de instance en de
        # gecreerde lijst.
        csv.write(self.csv, csv_list)

    def load_csv(self):
        """Een functie die de dagindeling inlaad in het CSV-bestand waarvan de
        path is opgeslagen in self.csv."""

        # Werknemers en ingeplanden worden ingeladen met de geselecteerde datum.
        werknemers = Werknemers()
        ingeplanden = Ingeplanden(f"{get_date.get()[0]}_ingeplanden.json")

        # Het CSV-bestand wordt uitgelezen en return none als de lees functie
        # niets of een lege lijst terug stuurt.
        rows = csv.read(self.csv)
        if not rows:
            return

        # In rows wordt de eerste rij overgeslagen, sinds hier de kolomkop
        # wordt bewaard. De eerste kolom bevat de locatie id, dus wordt deze
        # met string manipulatie er uit gehaald. Daarna wordt er per locatie_id
        # een nieuwe lijst toegevoegd in voor de medewerkers en inwerkers
        # dictionary in de dagindeling.
        for row in rows[1:]:
            locatie_id = row[0].split(".")[0]
            self.dagindeling[str(locatie_id)] = []
            self.inwerkers[str(locatie_id)] = []

            # Elke rij bevat 3 kolommen met een werknemer. Hier wordt per
            # kolom gecheckt of de kolom niet leeg is. Zo niet wordt het
            # personeelsnummer eruit gehaald (Voorbeeld: 'Rick Slingerland (1)')
            # met string manipulatie. Personeelsnummer staat als id om het kort
            # te houden.
            for index in range(3):
                if not row[1+index] == "":
                    column = row[1+index]
                    split_column = column.split("(")
                    id = int(split_column[-1].replace(")", ""))

                    # Hier wordt gecheckt of het personeelnummer in de lijst van
                    # ingeplanden zit zodat afgemelde werknemers niet worden
                    # toegevoegd aan de dagindeling. Daarna toegevoegd aan de
                    # dagindeling.
                    if ingeplanden.is_employee_in_list(id):
                        inwerker = werknemers.get_employee_by_id(id)
                        self.dagindeling[str(locatie_id)].append(inwerker)
            
            # Als kolom met index 4 niet leeg is, betekent het dat een inwerker
            # is ingepland. Ook hier wordt het personeelsnummer verkregen door
            # string manipulatie. En wordt het afgekort naar id.
            if not row[4] == "":
                column = row[4]
                split_column = column.split("(")
                id = int(split_column[-1].replace(")", ""))

                # Hier wordt gecheckt of het personeelnummer in de lijst van
                # ingeplanden zit zodat afgemelde inwerkers niet worden
                # toegevoegd aan de dagindeling. Daarna toegevoegd aan de
                # dagindeling.
                if ingeplanden.is_employee_in_list(int(id)):
                    employee = werknemers.get_employee_by_id(int(id))
                    self.inwerkers[str(locatie_id)].append(employee)

    def save_backup_json(self):
        """Deze functie slaat de dagindeling op in het JSON-bestand in het
        pad self.json."""
        dagindeling = self.to_list()
        jf.write(self.json, dagindeling)

    def load_backup_json(self):
        """Deze functie laad de dagindeling in vanuit het backup JSON-bestand
        in het pad self.json."""
        
        json_content = jf.read(self.json)

        # Checkt of de functie content bevat en zorgt ervoor dat de werknemers
        # en inwerkers dictionaries worden gereset.
        if json_content:
            self.dagindeling = {}
            self.inwerkers = {}
            self.to_class(json_content)

    def open_locatie(self, id):
        """Deze functie opent een locatie en voegt voor beide de werknemers en
        de inwerkers een nieuwe lijst met die locatie id."""
        self.dagindeling[str(id)] = []
        self.inwerkers[str(id)] = []

        # Sorteert de werknemers en inwerkers dagindeling dictionaries.
        self.dagindeling = sorted(self.dagindeling)
        self.inwerkers = sorted(self.inwerkers)

        self.generator()
        self.save_csv()

    def sluit_locatie(self, id):
        """Deze functie sluit een locatie, verwijderd de dagindeling voor beide
        de werknemers en de inwerkers en roept dan de generator op."""
        del self.dagindeling[str(id)]
        del self.inwerkers[str(id)]

        self.generator()
        self.save_csv()

    def absentie_medewerker(self, id:int):
        """Deze functie verwijderd absente medewerkers van de dagindeling en de
        inwerkers lijst. Verwijderd eerst de employee met hetzelfde
        personeelsnummer in de dagindeling lijst waarna het de inwerkers lijst
        checkt. Als laatst wordt de generator opgeroepen en wordt het bestand
        weer opgeslagen."""

        for id, employees in self.dagindeling.items():
            for index in range(len(employees)):
                if employees[index].personeelsnummer == id:
                    employees.pop(index)
                    
                    # Als de werknemer ingepland stond om ingewerkt te worden,
                    # wordt de inwerker ook uit de lijst gegooid.
                    if self.inwerkers[str(index)]:
                        self.inwerkers[str(index)].pop()
        
        for id, inwerkers in self.dagindeling.items():
            for index in range(len(inwerkers)):
                if inwerkers[index].personeelsnummer == id:
                    inwerkers.pop(index)

                    # Als de inwerker ingepland stond om in te werken, wordt de
                    # lijst met medewerkers verwijderd.
                    if self.dagindeling[str(index)]:
                        self.dagindeling[str(index)] = []

        # Als laatst wordt de generator aangeroepen om opnieuw de gepopte
        # medewerkers in te plannen waarna het wordt opgeslagen in de csv.
        self.generator()
        self.save_csv()        

    def to_medewerker(self, werknemer:dict):
        """Deze functie wordt gebruikt om een dictionary variant van een
        werknemer om te zetten in een medewerker class."""

        if type(werknemer) == dict:
            
            # Als de werknemer niet een intern is wordt er een externe
            # medewerker class gemaakt en wordt de data hier aan toegevoegd.
            if not werknemer["intern"]:
                new_extern = Extern_medewerker()
                new_extern.to_class(werknemer)
                return new_extern
            
            # Als de werknemer een inwerker is wordt er een inwerker class
            # gemaakt en wordt de data hier aan toegevoegd.
            elif werknemer["inwerker"]:
                new_inwerker = Inwerker()
                new_inwerker.to_class(werknemer)
                return new_inwerker
            
            # Als het geen van bovenstaande categorieen is wordt er een interne
            # medewerker class aangemaakt en de data er aan toegevoegd.
            else:
                new_intern = Intern_medewerker()
                new_intern.to_class(werknemer)
                return new_intern

    def to_class(self, dagindeling:list):
        """Wordt gebruikt om een lijst met 2 dictionaries toe te voegen aan de
        dagindeling lijsten."""

        # Elke key is een personeelsnummer en elke value is een lijst met
        # werknemer dictionaries die omgezet wordt in een werknemer via de
        # to_medewerker functie en wordt dan toegevoegd aan de dagindeling
        # dictionary.
        for key, value in dagindeling[0].items():
            self.dagindeling[str(key)] = []
            for person in value:
                employee = self.to_medewerker(person)
                self.dagindeling[str(key)].append(employee)
        
        # Elke key is een personeelsnummer en elke value is een lijst met een
        # inwerker dictionary die omgezet wordt in een inwerker via de
        # to_medewerker functie en wordt dan toegevoegd aan de dagindeling
        # dictionary.
        for key, value in dagindeling[1].items():
            self.dagindeling[str(key)] = []
            for person in value:
                employee = self.to_medewerker(person)
                self.dagindeling[str(key)].append(employee)

    def to_list(self):
        """Deze functie zet de dagindeling en inwerkers dictionaries met
        werknemers classes om naar dictionaries met werknemer dictionaries om
        het makkelijker te kunnen opslaan."""

        dict_dagindeling = {}

        # Voor elke key (locatie id) in de dagindeling wordt de key toegevoegd
        # aan de nieuwe dictionary.
        for key, value in self.dagindeling.items():
            dict_dagindeling[str(key)] = []

            # Voor elke werknemer in value (lijst met werknemers) wordt de
            # werknemer omgezet in een werknemer dictionary en toegevoegd aan
            # de lijst in de nieuwe dictionary. Ook wordt de ingewerkte locatie
            # verwijderd uit de werknemer dictionary.
            for person in value:
                employee = person.to_dict()
                del employee["ingewerkte_locaties"]
                dict_dagindeling[str(key)].append(employee)

        dict_inwerkers = {}

        # Voor elke key (locatie id) in de inwerkers dictionary wordt de key
        # toegevoegd aan de nieuwe dictionary.
        for key, value in self.dagindeling.items():
            dict_inwerkers[str(key)] = []

            # Voor elke inwerker in value (lijst van werknemers) wordt de
            # inwerker omgezet in een inwerker dictionary en toegevoegd aan de
            # lijst in de nieuwe dictionary. Ook worden de ingewerkte locaties
            # verwijderd uit deze dictionary.
            for person in value:
                employee = person.to_dict()
                del employee["ingewerkte_locaties"]
                dict_inwerkers[str(key)].append(employee)

        # Een lijst van de 2 dictionaries wordt terug gestuurd.
        return [dict_dagindeling, dict_inwerkers]

    def get_employees_per_location(
            self, locatie_id:int, search_list:list, absenten:list):
            """Deze functie returnt een lijst met werknemers die zijn ingewerkt
            op de locatie en die wordt gepakt vanuit de locatie id, genoeg
            fysieke kracht hebben om er te worden ingeroosterd gesorteerd op
            voorkeur. Zoekt in search_list voor de werknemers en zoekt absenten
            in de absenten lijst."""

            # Maakt nieuwe lijsten om werknemers toe te voegen.
            employees_per_location = []
            sort_with_voorkeur = []

            # Voor elke werknemer in de lijst wordt gezocht of de werknemer is
            # ingewerkt op de locatie, of de werknemer ongeschikt om op de
            # locatie ingeroosterd te worden, en of de werknemer niet absent is.
            for employee in search_list:
                if locatie_id in employee.ingewerkte_locaties and (
                    locatie_id not in employee.ongeschikte_locaties) and (
                        employee not in absenten):
                    
                    # Als de locatie_id is toegevoegd in de voorkeuren
                    # dictionary van de werknemer, wordt het cijfer (1 tot 10)
                    # bewaard in de variabele voorkeur. Anders wordt het cijfer
                    # 6 onthouden.
                    if locatie_id in employee.voorkeuren.keys():
                        voorkeur = employee.voorkeuren[locatie_id]
                    else:
                        voorkeur = 6
                    
                    # Hier wordt een dictionary gemaakt met de int voorkeur en
                    # de medewerker class employee die wordt toegevoegd aan de
                    # lijst.
                    add_dict = { "voorkeur": voorkeur, "medewerker": employee }
                    sort_with_voorkeur.append(add_dict)

            # Als de voorkeurs lijst niet leeg is, wordt de lijst gesorteerd
            # op voorkeur met een lambda.
            if sort_with_voorkeur:
                sort_with_voorkeur = sorted(
                    sort_with_voorkeur, key=lambda d: d['voorkeur'])
                
                # Voor elke medewerker in de voorkeurslijst wordt de medewerker
                # uit de dictionary gehaald en in de lijst gestopt.
                for employee in sort_with_voorkeur:
                    employees_per_location.append(employee["medewerker"])

            return employees_per_location

    def get_employees_per_group(self, loc_ids:list, s_list:list, absenten:list):
        """Een functie die mensen zoekt die op alle locaties is ingewerkt in
        een groep. Loc_ids is een lijst met locatie ids van de groep. s_list
        is kort voor search list en de absenten lijst spreekt voor zich. Returnt
        een lijst met medewerkers die is ingewerkt op alle locaties."""

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
        """Deze functie zoekt een lijst met mogelijke werknemers door of ze
        sterk genoege fysieke kracht hebben voor de locatie."""
        too_weak = []

        # Per werknemer in mogelijkheden wordt de werknemer toegevoegd als de
        # fysieke kracht lager is dan de nodige fysieke kracht.
        for employee in possibilities:
            if employee.fysieke_kracht < location.fysieke_kracht:
                too_weak.append(employee)

        # Returnt een lijst met werknemers die te zwak zijn.
        return too_weak

    def schedule_rest_employees(
            self, locations:Locaties, dagindeling:list, ingeplanden:Ingeplanden,
            medewerkers_list, minimum_or_maximum:bool):
        """Een functie die vraagt om de beschikbare locaties, de dagindeling
        voor hoever hij nu bestaat, de ingeplanden medewerkers lijst, een lijst
        met alle medewerkers en een boolean waar wordt gespecificeerd of er
        gekeken moet worden naar minimale of maximale medewerkers bij een
        locatie. Returnt een aangevulde dagindeling."""

        # Per geopende locatie. wordt er eerst gekeken er nog
        # medewerkers nodig zijn per locatie.
        for location in locations.open_locaties:

            # Als de boolean True is wordt er gekeken naar de minimum
            # medewerkers per locatie. Als het aantal ingeplanden hoger of
            # gelijk aan het minimum is, wordt de locatie overgeslagen.
            if minimum_or_maximum:
                minimum = location.minimale_medewerkers
                if len(dagindeling[str(location.id)]) >= minimum:
                    continue
            
            # Als de boolean False is wordt er gekeken naar de maximum
            # medewerkers per locaite. Als het aantal ingeplanden hoger of
            # gelijk aan het maximum, wordt de locatie overgeslagen.
            else:
                maximum = location.maximale_medewerkers
                if len(dagindeling[str(location.id)]) >= maximum:
                    continue
            
            # Er wordt gezocht naar medewerkers die zijn ingewerkt op de
            # locatie. Als er niemand is ingewerkt, wordt de locatie
            # overgeslagen.
            possibilities = self.get_employees_per_location(
                location.id, medewerkers_list, ingeplanden.absenten)
            if not possibilities:
                continue
            
            # Per werknemer wordt er gekeken of ze sterk genoeg zijn voor de
            # locatie. Als er niemand meer overblijft, wordt de locatie
            # overgeslagen.
            lower_fysical_power = self.get_lower_fysical_power(
                possibilities, location)
            remaining = [ employee for employee in possibilities if employee not
                         in lower_fysical_power ]
            if not remaining:
                continue
            
            # Als het aantal werknemers in de lijst van mogelijkheden groter is
            # dan 1, wordt de persoon gepakt met het minst aantal ingewerkte
            # locaties. Anders wordt de laatst overgebleven werknemer
            # geselecteerd.
            if len(remaining) > 1:
                employee = self.get_least_locations(possibilities)
            else:
                employee = remaining[0]
            
            # De werknemer wordt verwijderd uit de ingeplanden lijst en
            # toegevoegd aan de dagindeling.
            ingeplanden.delete_werknemer(employee)
            dagindeling[str(location.id)].append(employee)

        return dagindeling

    def get_least_locations(self, possibilities:list):
        """Deze functie wordt gebruikt om uit een lijst de werknemer terug te
        krijgen met de minst ingewerkte locaties"""

        amount_list = [
            len(employee.ingewerkte_locaties) for employee in possibilities
            ]
        return possibilities[amount_list.index(min(amount_list))]

    def get_inwerker(self, ingeplanden:Ingeplanden):
        """Deze functie wordt gebruikt om uit de lijst van ingeplanden een
        inwerker terug te krijgen. Als dit niet lukt wordt een supervisor
        meegegeven."""

        try:
            inwerker = ingeplanden.inwerkers[0]
            ingeplanden.delete_werknemer(inwerker)
        except:
            inwerker = "Supervisor"
        return inwerker

    def is_type_in_list(self, search_list:list, types):
        """Deze functie wordt gebruikt om een boolean terug te krijgen of een
        meegegeven class zich bevind in de search_list."""
        for item in search_list:
            if type(item) == types:
                return True
        return False

    def generator(self):
        """Deze functie genereert de dagindeling en zet ze neer in de class."""

        # Hier worden de ingeplanden en locaties van de geselecteerde dag
        # ingeladen en worden de ingeplanden gesorteerd op kans van inwerken.
        ingeplanden = Ingeplanden(f"{get_date.get()[0]}_ingeplanden.json")
        locations = Locaties(f"data/ingeplanden/{get_date.get()[0]}_locaties.json")
        ingeplanden.sort("inwerk_probability")

        # # Checkt per ingeplande werknemer of ze al in de dagindeling staan.
        # # Zo ja worden ze verwijderd van de ingeplanden lijst.
        # for employees in self.dagindeling.values():
        #     for index in range(len(employees)):
        #         ingeplanden.delete_werknemer(employees[index])

        # # Checkt per ingeplande inwerker of ze al in de dagindeling staan.
        # # Zo ja worden ze verwijderd van de ingeplanden lijst.
        # for inwerkers in self.inwerkers.values():
        #     for index in range(len(inwerkers)):
        #         ingeplanden.delete_werknemer(inwerkers[index])

        # Per locatie wordt er in de dictionaries voor medewerkers en inwerkers
        # een lijst aangemaakt met als key de locatie id.
        for location in locations.open_locaties:
            self.dagindeling[str(location.id)] = []
            self.inwerkers[str(location.id)] = []

        # Maakt een lijst met alle nieuwe werknemers.
        priority_list = [ employee for employee in ingeplanden.medewerkers if
                employee.inwerk_probability == 100 and employee not
                in ingeplanden.absenten ]
        
        # Per groep die de locaties deel van zijn worden hier een inwerker
        # ingedeeld en (als het kan) 3 nieuwe medewerkers. Deze locaties
        # worden gezien als beginner locaties.
        for group in locations.groepen.values():
            
            # Als er nieuwe medewerkers zijn. Wordt er een inwerker ingepland
            # per groep.
            if priority_list:
                inwerker = self.get_inwerker(ingeplanden)
            
            # Per locatie in de groep wordt er een nieuwe werknemer ingedeeld.
            # De loop wordt gestopt wanneer de prioriteitenlijst leeg is of de
            # locatie id niet in de dagindeling staat.
            for location in group:
                if not priority_list or self.dagindeling.get(location,"") == "":
                    break

                # De werknemer wordt verwijderd uit de prioriteiten lijst en de
                # werknemers lijst.
                employee = priority_list.pop(0)
                ingeplanden.delete_werknemer(employee)

                # Hier word per locatie de inwerker ingedeeld en de nieuwe
                # werknemer.
                self.dagindeling[str(location)].extend([employee])
                self.inwerkers[str(location)] = [inwerker]
        
        # Sorteert de locaties lijst op moeilijkheidsgraad, en zorgt ervoor dat
        # de makkelijkste locaties vooraan komen te staan.
        locations.sort("moeilijkheidsgraad")
        locations.reverse()

        # Tot de prioriteitenlijst leeg is en de index onder hetaantal geopende
        # locaties blijft, zal het programma een medewerker proberen in te
        # roosteren.
        index = 0
        while priority_list and index < len(locations.open_locaties):

            # Als de volgende locatie nog niet met maximale bemanning staat,
            # wordt er 1 toegevoegd bij de index.
            next_location = locations.open_locaties[index]
            if not len(self.dagindeling[str(next_location.id)]) <= (
                next_location.maximale_medewerkers):
                index += 1

            # Als de dagindeling op de volgende locatie geen medewerkers heeft
            # ingepland, wordt er een nieuwe medewerker toegevoegd.
            if len(self.dagindeling[str(next_location.id)]) < (
                next_location.maximale_medewerkers):
                employee = priority_list.pop(0)
                ingeplanden.delete_werknemer(employee)
                
                # Als er al een inwerker staat ingedeeld ingepland, wordt alleen
                # de nieuwe medewerker toegevoegd aan de dagindeling. Anders
                # wordt er een nieuwe inwerker gepakt en die ingedeeld.
                if self.inwerkers[str(next_location.id)]:
                    self.dagindeling[str(next_location.id)].extend([employee])
                else:
                    inwerker = self.get_inwerker(ingeplanden)
                    self.inwerkers[str(next_location.id)] = [inwerker]
                    self.dagindeling[str(next_location.id)].extend([employee])

        # Als er nog inwerkers over zijn, worden de personen met de hoogste
        # inwerk kans als eerste ingepland. De locaties worden gesorteerd op
        # belang. Ook wordt de index gereset.
        locations.sort("belang")
        index = 0
        priority_list = [ employee for employee in ingeplanden.medewerkers if
                employee.inwerk_probability != 100 and employee not in
                ingeplanden.absenten and employee not in ingeplanden.inwerkers ]
        while len(ingeplanden.inwerkers) > 0 and index < len(
            locations.open_locaties) and len(priority_list) > 0:

            next_location = locations.open_locaties[index]
            index += 1

            # Als het maximum medewerkers nog niet is bereikt, wordt er een
            # medewerker ingepland.
            if len(self.dagindeling[str(next_location.id)]) < (
                next_location.maximale_medewerkers):
                employee = priority_list.pop(0)
                ingeplanden.delete_werknemer(employee)
                
                # Als er al een inwerker staat ingedeeld ingepland, wordt alleen
                # de nieuwe medewerker toegevoegd aan de dagindeling. Anders
                # wordt er een nieuwe inwerker gepakt en die ingedeeld.
                if self.inwerkers[str(next_location.id)]:
                    self.dagindeling[str(next_location.id)].extend([employee])
                else:
                    inwerker = self.get_inwerker(ingeplanden)
                    self.inwerkers[str(next_location.id)] = [inwerker]
                    self.dagindeling[str(next_location.id)].extend([employee])

        # Als laatste worden alle overgebleven medewerkers ingedeeld via de
        # schedule_rest_employees functie. Inwerkers gaan als eerst. Er wordt nu
        # nog gekeken naar het minimale medewerkers, vandaar de True.
        self.dagindeling = self.schedule_rest_employees(locations,
            self.dagindeling, ingeplanden, ingeplanden.interne_medewerkers,True)
        
        # Daarna worden alle externe medewerkers ingedeeld via de
        # schedule_rest_employees functie. Er wordt nu nog gekeken naar het
        # minimale medewerkers, vandaar de True.
        self.dagindeling = self.schedule_rest_employees(locations,
            self.dagindeling, ingeplanden, ingeplanden.externe_medewerkers,True)
        
        # Wanneer er geen interne of externe medewerkers over zijn, worden de
        # inwerkers ingepland.
        if not ingeplanden.interne_medewerkers and not (
            ingeplanden.externe_medewerkers) and ingeplanden.inwerkers:
            self.dagindeling = self.schedule_rest_employees(
                locations, self.dagindeling, ingeplanden, ingeplanden.inwerkers,
                True)
            
        # Als er nog interne medewerkers of externe medewerkers over zijn,
        # worden die ingedeeld als 2e of 3e man als dit mogelijk is.
        if ingeplanden.interne_medewerkers or ingeplanden.externe_medewerkers:

            # Eerst de interne medewerkers.
            self.dagindeling = self.schedule_rest_employees(locations,
                self.dagindeling, ingeplanden, ingeplanden.interne_medewerkers,
                False)
            
            # Als tweede de externe medewerkers.
            self.dagindeling = self.schedule_rest_employees(locations,
                self.dagindeling, ingeplanden, ingeplanden.externe_medewerkers,
                False)
            
            # Als er dan nog inwerkers over zijn, worden deze ingedeeld als 2e
            # man.
            if not ingeplanden.interne_medewerkers and not (
                ingeplanden.externe_medewerkers) and len(
                    ingeplanden.inwerkers) > 0:
                
                self.dagindeling = self.schedule_rest_employees(locations,
                    self.dagindeling, ingeplanden, ingeplanden.inwerkers, False)