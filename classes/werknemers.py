from .read_files import json_file as jf
from .read_files import csv_file as csv
from .locaties import Locaties
import os

class Werknemers:
    """Een class die bestaat uit verschillende lijsten om makkelijk bij te
    houden welke medewerkers er zijn en wat voor medewerker ze zijn."""

    def __init__(self, path='data/werknemers.json'):
        """De initialisatie van de werknemers class. Vraagt om een path, maar
        heeft als default de locatie waar alle werknemers staan opgeslagen."""

        self.interne_medewerkers = []
        self.externe_medewerkers = []
        self.inwerkers = []
        self.medewerkers = []
        self.path = path

        # Probeert data te krijgen van het bestand. Als het bestand niet het
        # standaard pad heeft, slaat het deze op.
        self.retreive_from_file()
        if path != 'data/werknemers.json':
            self.save_to_file()
    
    def delete(self):
        """Een functie die probeert om de json die opgeslagen staat op
        self.path te verwijderen."""
        try:
            os.remove(self.path)
        except:
            pass
        

    def save_to_file(self):
        """Als de instance een pad heeft dat eraan is gebonden, worden de
        gegevens van de instance in dat bestand opgeslagen. De ingewerkte
        locaties worden gepopt en opgeslagen in een apart csv-bestand."""

        if self.path:
            # De lijst wordt gesorteert op personeelsnummer.
            self.sort("personeelsnummer")
            self.reverse()
            
            # De werknemer wordt omgezet naar een lijst met dictionaries en de
            # locaties worden ingeladen.
            werknemers_list = self.to_list()
            locatie_list = Locaties('data/locaties.json')

            # De lijst met lijsten voor de csv file begint in de eerste regel
            # met personeelsnummer en naam. Daarna worden de namen met tussen
            # haakjes het id van locaties toegevoegd aan de lijst.
            csv_list = [[ "Personeelsnummer", "Naam" ]]
            for locatie in locatie_list.locaties:
                csv_list[0].append(f"{locatie.naam} ({locatie.id})")
            
            # Per werknemer wordt er een nieuwe lijst gecreeert en de
            # ingewerkte locaties worden weg gehaald zodat deze niet worden
            # opgeslagen in de json. Voor elke attractie wordt er in de lijst
            # iets toegevoegd. x voor wel ingewerkt, niets voor niet ingewerkt.
            for werknemer in werknemers_list:
                werknemer_id = werknemer['personeelsnummer']
                werknemer_naam = werknemer['naam']
                csv_list.append([werknemer_id, werknemer_naam])
                
                ingewerkte_locaties = werknemer.pop('ingewerkte_locaties')
                csv_list[-1].extend(["x" if j in ingewerkte_locaties else ""
                                for j in range(1,len(csv_list[0])-1)])
            
            # Hieronder worden de json_file (jf) en csv_file (csv) opgeslagen.
            jf.write(self.path, werknemers_list)
            csv.write('data/ingewerkte_locaties.csv', csv_list)

    def retreive_from_file(self):
        """Als er een pad aan de instance is gekoppeld, worden de gegevens van
        het bestand opgeslagen in de instance."""
        if self.path:
            werknemers_list = jf.read(self.path)
            if werknemers_list:
                self.to_class(werknemers_list)

    def is_employee_in_list(self, id):
        """Checkt of een werknemer in de class is toegevoegd via het meegeven
        van een id. Returnt een boolean."""
        for employee in self.medewerkers:
            if employee.personeelsnummer == id:
                return True
        return False

    def get_employee_by_id(self, id):
        """Checkt of een werknemer in de class is toegevoegd via het meegeven
        van een id. Returnt de werknemer als deze gevonden is."""
        for employee in self.medewerkers:
            if employee.personeelsnummer == id:
                return employee

    def get_index_by_id(self, id:int, search_list:list):
        """Zoekt in search_list voor de meegegeven personeelsnummer. Als deze
        gevonden is, stuurt het de index terug."""
        for index in range(len(search_list)):
            if id == search_list[index].personeelsnummer:
                return index

    def delete_werknemer(self, werknemer):
        """Verwijdert een werknemer uit de class lijsten. Als een id wordt
        meegegeven wordt de werknemer verwijderd met die personeelsnummer."""
        if type(werknemer) == int:
            werknemer = self.medewerkers[self.get_index_by_id(
            werknemer, self.medewerkers
        )]
        
        # Selecteert personeelsnummer
        personeelsnummer = werknemer.personeelsnummer

        # Probeert de werknemer uit de medewerkers lijst te verwijderen.
        try:
            del self.medewerkers[self.get_index_by_id(
                personeelsnummer, self.medewerkers
            )]
        except:
            pass
        
        # Probeert de werknemer te verwijderen uit de specifieke lijsten. Als
        # het een inwerker is, wordt de werknemer verwijderd uit de inwerkers
        # lijst. Als het een externe medewerker is, wordt de werknemer
        # verwijderd uit de externe medewerkers lijst. Als het een interne
        # medewerker is, wordt de werknemer verwijderd uit de interne
        # medewerkers lijst.
        try:
            if type(werknemer) == Inwerker:
                del self.inwerkers[self.get_index_by_id(
                    personeelsnummer, self.inwerkers
                )]
            elif type(werknemer) == Intern_medewerker:
                del self.interne_medewerkers[self.get_index_by_id(
                    personeelsnummer, self.interne_medewerkers
                )]
            else:
                del self.externe_medewerkers[self.get_index_by_id(
                    personeelsnummer, self.externe_medewerkers
                )]
        except:
            pass

    def add_inwerker(self, inwerker, save_file=False):
        """Voegt een inwerker toe aan de medewerker instance. Neemt een
        dictionary of een inwerker en voegt deze toe aan zowel de
        inwerkerslijst als de volledige lijst met medewerkers. Standaard
        wordt het bestand niet opgeslagen als het er een heeft, maar als is
        opgegeven dat het moet worden opgeslagen, wordt het opgeslagen.
        Save_file wordt niet gebruikt, maar dit kan handig zijn wanneer
        werknemers worden toegevoegd via de app in de toekomst."""

        if type(inwerker) == dict:
            new_inwerker = Inwerker()
            new_inwerker.to_class(inwerker)

            self.inwerkers.append(new_inwerker)
            self.medewerkers.append(new_inwerker)

        elif type(inwerker) == Inwerker:
            self.inwerkers.append(inwerker)
            self.medewerkers.append(inwerker)
        
        if save_file:
            self.save_to_file()

    def add_interne_medewerker(self, intern, save_file=False):
        """Voegt een interne medewerker toe aan de medewerker instance. Neemt
        een dictionary of een interne_medewerker en voegt deze toe aan zowel de
        interne_medewerkers-lijst als de volledige lijst met medewerkers.
        Standaard wordt het bestand niet opgeslagen als het er een heeft, maar
        als is opgegeven dat het moet worden opgeslagen, wordt het opgeslagen.
        Save_file wordt niet gebruikt, maar dit kan handig zijn wanneer
        werknemers worden toegevoegd via de app in de toekomst."""

        if type(intern) == dict:
            new_werknemer = Intern_medewerker()
            new_werknemer.to_class(intern)

            self.interne_medewerkers.append(new_werknemer)
            self.medewerkers.append(new_werknemer)

        elif type(intern) == Intern_medewerker:
            self.interne_medewerkers.append(intern)
            self.medewerkers.append(intern)
        
        if save_file:
            self.save_to_file()

    def add_externe_medewerker(self, extern, save_file=False):
        """Voegt een externe medewerker toe aan de medewerker instance. Neemt
        een dictionary of een externe_medewerker en voegt deze toe aan zowel
        de externe_medewerkers-lijst als de volledige lijst met medewerkers.
        Standaard wordt het bestand niet opgeslagen als het er een heeft, maar
        als is opgegeven dat het moet worden opgeslagen, wordt het opgeslagen.
        Save_file wordt niet gebruikt, maar dit kan handig zijn wanneer
        werknemers worden toegevoegd via de app in de toekomst."""

        if type(extern) == dict:
            new_extern = Extern_medewerker()
            new_extern.to_class(extern)

            self.externe_medewerkers.append(new_extern)
            self.medewerkers.append(new_extern)

        elif type(extern) == Extern_medewerker:
            self.externe_medewerkers.append(extern)
            self.medewerkers.append(extern)
        
        if save_file:
            self.save_to_file()            

    def to_class(self, werknemers:list):
        """Wordt gebruikt om een lijst met dictionaries of een lijst met
        Extern_medewerker, Intern_medewerker of Inwerker objecten toe te voegen
        via de add-functies. Checkt of de item in de lijst een medewerker type
        is, of een dictionary."""
        
        for werknemer in werknemers:
            if type(werknemer) == dict:
                if not werknemer["intern"]:
                    self.add_externe_medewerker(werknemer)
                elif werknemer["inwerker"]:
                    self.add_inwerker(werknemer)
                else:
                    self.add_interne_medewerker(werknemer)
            else:
                if type(werknemer) == Extern_medewerker:
                    self.add_externe_medewerker(werknemer)
                elif type(werknemer) == Inwerker:
                    self.add_inwerker(werknemer)
                elif type(werknemer) == Intern_medewerker:
                    self.add_interne_medewerker(werknemer)

    def to_list(self):
        """Returnt een lijst met dictionaries, zodat je deze gemakkelijker in
        JSON-bestanden kunt opslaan."""
        return [medewerker.to_dict() for medewerker in self.medewerkers]

    def set_sort_by(self, to_set, key):
        """Om een lijst te kunnen sorteren moet er eerst per werknemer het
        soort sorteren worden gespecificeerd, sinds de lijsten op verschillende
        manieren gesorteerd kunnen worden."""
        for employee in to_set:
            employee.sorted_by = key

    def sort(self, key):
        """Deze functie sorteert de medewerker lijsten op key die wordt mee
        gegeven. Het kan gesorteerd worden op personeelsnummer en
        inwerk_probability."""

        if key in ["personeelsnummer", "inwerk_probability"]:

            # Eerst wordt voor elke werknemer in elke lijst de manier van
            # sorteren gewijzigd.
            self.set_sort_by(self.interne_medewerkers, key)
            self.set_sort_by(self.externe_medewerkers, key)
            self.set_sort_by(self.inwerkers, key)
            self.set_sort_by(self.medewerkers, key)

            # Dan wordt de sorteer functie uitgevoerd.
            self.interne_medewerkers.sort()
            self.externe_medewerkers.sort()
            self.inwerkers.sort()
            self.medewerkers.sort()

            # Als de key gelijk is aan inwerk_probability, wordt de lijst
            # omgedraaid sinds het de bedoeling is dat de hoogste waarde
            # eerst komt.
            if key == "inwerk_probability":
                self.reverse()

    def reverse(self):
        """Een functie om alle lijsten om te draaien."""
        self.interne_medewerkers.reverse()
        self.externe_medewerkers.reverse()
        self.inwerkers.reverse()
        self.medewerkers.reverse()

class Ingeplanden(Werknemers):
    """Een class die werknemers inherit met een standaart path, een eigen manier
    van opslaan en een lijst voor absenten."""

    def __init__(self, path):
        """De initialisatie van de Ingeplanden class. Vraagt om een path waar
        'data/ingeplanden/' wordt toegevoegd sinds dit standaard is."""
        super().__init__("data/ingeplanden/"+path)
        self.absenten = []

    def save_to_file(self):
        """Deze functie slaat de lijst met werknemers op in de JSON-file waar
        de self.path naar verwijst. Sorteert eerst op personeelsnummer en
        verwijderd daarna de ingewerkte locaties."""

        self.sort("personeelsnummer")
        self.reverse()

        werknemers_list = self.to_list()
        for werknemer in werknemers_list:
            werknemer.pop('ingewerkte_locaties')
        
        jf.write(self.path, werknemers_list)

class medewerker_format:
    """Een class voor alle medewerkers om te inheritten met een aantal basis
    dingen zodat de class niet uitmaakt en ik wel de functies kan gebruiken."""

    def __init__(self, intern:bool, inwerker:bool):
        """medewerker_format wordt geinitialiseerd. Neemt 2 booleans."""

        self.personeelsnummer = self.get_new_personeelsnummer()
        self.naam = ""
        self.ingewerkte_locaties = []
        self.voorkeuren = {}  # lijst met als key een locatie id en een nummer van 0 tot 10
        self.ongeschikte_locaties = []
        self.intern = intern  # Boolean
        self.inwerker = inwerker  # Boolean
        self.fysieke_kracht = 5  # Int met een waarde van max 5 minimaal 0
        self.sorted_by = "personeelsnummer" # Waarmee de vergelijkingen worden gemaakt.
        self.inwerk_probability = 0 # Int met een waarde van max 100 minimaal 0
    
    def get_ingewerkte_locaties(self, personeelsnummer:int):
        """Een functie die met een personeelsnummer neemt en kijkt in de
        ingewerkte locaties csv of de persoon in de lijst staat en waar de
        persoon is ingewerkt."""

        rows = csv.read('data/ingewerkte_locaties.csv')

        # Als het bestand niet is gevonden, wordt een lege lijst terug gestuurd.
        if not rows:
            return []
        
        # Het bestand start altijd met een rij met kolom kopjes, dus start het
        # met de eerst volgende rij. Wanneer de persoon is gevonden via de
        # personeelsnummer, wordt er een lijst aangemaakt genaamd locaties,
        # omdat de eerste 2 rijen de naam en personeelsnummer bevatten. Ook
        # wordt er een lijst aangemaakt met ingewerkte locaties.
        for row in rows[1:]:
            if (int(row[0]) == personeelsnummer):
                locaties:list = row[2:]
                ingewerkte_locaties = []

                # Als er een 'x' wordt gevonden in de locaties zal de code
                # hieronder doorgaan totdat er geen 'x' meer in zit. Van elke x
                # wordt de index gezocht en daarna toegevoegd aan de lijst en
                # wordt de x veranderd in een lege ruimte zodat de lijst
                # indexen niet veranderen.
                while 'x' in locaties:
                    x = locaties.index('x')
                    ingewerkte_locaties.append(x+1)
                    locaties[x] = ''
                
                return ingewerkte_locaties
        # Als het personeelsnummer niet wordt gevonden, wordt een lege lijst
        # terug gestuurd.
        return []

    def get_new_personeelsnummer(self):
        """Deze functie zoekt door de werknemers.json voor het hoogste
        personeelsnummer. Returnt de hoogste + 1 of een 1 als het niets vind."""
        werknemers_list = jf.read('data/werknemers.json')
        if werknemers_list:
            return (werknemers_list[-1]["personeelsnummer"] + 1)
        else:
            return 1
    
    def to_class(self, dictionary:dict):
        """Neemt een dictionary en verandert het naar een werknemer class.
        Voegt alle waardes aan zichzelf toe. Als de key niet wordt gevonden
        in de dictionary blijft de waarde hetzelfde."""

        self.personeelsnummer = dictionary.get(
            'personeelsnummer', self.personeelsnummer)
        
        self.naam = dictionary.get('naam', self.naam)

        self.ingewerkte_locaties = dictionary.get(
            'ingewerkte_locaties', self.get_ingewerkte_locaties(
                self.personeelsnummer))
        
        self.voorkeuren = dictionary.get('voorkeuren', self.voorkeuren)

        self.ongeschikte_locaties = dictionary.get(
            'ongeschikte_locaties', self.ongeschikte_locaties)
        
        self.fysieke_kracht = dictionary.get(
            'fysieke_kracht', self.fysieke_kracht)
        
        self.inwerk_probability = self.get_inwerk_probability()

    def to_dict(self):
        """Verandert de class naar een dictionary om het makkelijker op te
        slaan als JSON-bestand."""
        return {
            "personeelsnummer" : self.personeelsnummer,
            "naam" : self.naam,
            "ingewerkte_locaties": self.ingewerkte_locaties,
            "voorkeuren": self.voorkeuren,
            "ongeschikte_locaties": self.ongeschikte_locaties,
            "intern": self.intern,
            "inwerker": self.inwerker,
            "fysieke_kracht": self.fysieke_kracht
        }
    
    def __lt__(self, other):
        """Een dunder om andere objecten te vergelijken met zichzelf. Dit staat voor kleiner dan."""
        if self.sorted_by == "personeelsnummer":
            return self.personeelsnummer < other.personeelsnummer
        elif self.sorted_by == "inwerk_probability":
            return self.inwerk_probability < other.inwerk_probability
        else:
            raise ValueError

    def __le__(self, other):
        """Een dunder om andere objecten te vergelijken met zichzelf. Dit staat voor kleiner dan of gelijk aan."""
        if self.sorted_by == "personeelsnummer":
            return self.personeelsnummer <= other.personeelsnummer
        elif self.sorted_by == "inwerk_probability":
            return self.inwerk_probability <= other.inwerk_probability
        else:
            raise ValueError

    def __eq__(self, other):
        """Een dunder om andere objecten te vergelijken met zichzelf. Dit staat voor gelijk aan."""
        if self.sorted_by == "personeelsnummer":
            return self.personeelsnummer == other.personeelsnummer
        elif self.sorted_by == "inwerk_probability":
            return self.inwerk_probability == other.inwerk_probability
        else:
            raise ValueError

    def __ne__(self, other):
        """Een dunder om andere objecten te vergelijken met zichzelf. Dit staat voor niet gelijk aan."""
        if self.sorted_by == "personeelsnummer":
            return self.personeelsnummer != other.personeelsnummer
        elif self.sorted_by == "inwerk_probability":
            return self.inwerk_probability != other.inwerk_probability
        else:
            raise ValueError

    def __gt__(self, other):
        """Een dunder om andere objecten te vergelijken met zichzelf. Dit staat voor groter dan."""
        if self.sorted_by == "personeelsnummer":
            return self.personeelsnummer > other.personeelsnummer
        elif self.sorted_by == "inwerk_probability":
            return self.inwerk_probability > other.inwerk_probability
        else:
            raise ValueError

    def __ge__(self, other):
        """Een dunder om andere objecten te vergelijken met zichzelf. Dit staat voor groter dan of gelijk aan."""
        if self.sorted_by == "personeelsnummer":
            return self.personeelsnummer >= other.personeelsnummer
        elif self.sorted_by == "inwerk_probability":
            return self.inwerk_probability >= other.inwerk_probability
        else:
            raise ValueError

    def get_inwerk_probability(self):
        """Een placeholder voor de functie die uitrekent hoe groot de kans is
        dat je wordt ingedeeld die verschilt per soort medewerker."""
        pass

class Intern_medewerker(medewerker_format):
    """Een class voor de interne medewerkers die medewerker_format inheritten.
    Heeft een eigen (ongebruikte) variabele genaamd pity."""

    def __init__(self):
        """De initialisatie van intern_medewerker die een true voor intern
        terug stuurt naar medewerker_format en een false voor inwerker."""
        super().__init__(True, False)
        self.__pity = 0

    def first_pick(self):
        """Een (ongebruikte) functie die de pity reset naar 0. Zou gebruikt
        worden wanneer je een voorkeur hebt voor een locatie en daar wordt
        neergezet."""
        self.__pity = 0

    def not_first_pick(self):
        """Een (ongebruikte) functie die pity omhoog gooit met 1. Zou gebruikt
        worden wanneer je niet wordt gekozen voor een locatie naar voorkeur,
        of wordt neergezet bij een locatie met negatieve voorkeurscore."""
        self.__pity += 1

    def get_inwerk_probability(self):
        """Deze functie stuurt een percentage terug van hoe groot de kans op
        inwerken is. Pakt het totaal aantal locaties, haalt daar de ingewerkte
        locaties vanaf en deelt dat door het totaal en doet keer 100. Simpel
        deel/geheel * 100."""

        locations = Locaties('data/locaties.json')

        total_locations = len(locations.locaties)
        locations_ingewerkt = len(self.ingewerkte_locaties)
        locations_to_go = total_locations - locations_ingewerkt

        return locations_to_go / total_locations * 100

class Extern_medewerker(medewerker_format):
    """Een class voor externe medewerkers die inherrit van medewerker_format."""
    def __init__(self):
        """De initialisatie van de externe medewerker class. Stuurt een false
        voor beide inwerker en intern terug naar medewerker_format. Externe
        medewerkers kunnen geen inwerkers zijn namelijk."""
        super().__init__(False, False)
    
    def get_inwerk_probability(self):
        """Deze functie stuurt een percentage terug van hoe groot de kans op
        inwerken is. Als de externe medewerker al is ingewerkt ergens, is er
        een grote kans dat deze niet meer wordt ingewerkt."""

        if self.ingewerkte_locaties:
            return 0
        return 100.0

class Inwerker(medewerker_format):
    """Een class van inwerkers die inherriten van medewerker_format."""
    def __init__(self):
        """De initialisatie van de inwerker class. Stuurt een true naar
        medewerker_format voor beide inwerker en intern, sinds alleen
        interne medewerkers inwerkers kunnen zijn."""
        super().__init__(True, True)
    
    def get_inwerk_probability(self):
        """Deze functie stuurt een percentage terug van hoe groot de kans op
        inwerken is. Stuurt 0 terug sinds inwerkers niet ingewerkt kunnen
        worden."""
        return 0.0