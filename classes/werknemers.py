from .read_files import json_file as jf
from .read_files import csv_file as csv
from .locaties import Locaties

class Werknemers:
    def __init__(self, path='data/werknemers.json'):
        self.interne_medewerkers = []
        self.externe_medewerkers = []
        self.inwerkers = []
        self.medewerkers = []
        self.path = path
        self.retreive_from_file()

    def save_to_file(self):
        """If the instance has a path bound to it, it will save the data
        of the instance to that file."""

        if self.path:
            self.sort("personeelsnummer")
            self.reverse()
            
            werknemers_list = self.to_list()
            locatie_list = Locaties('data/locaties.json')

            list = [[ "Personeelsnummer", "Naam" ]]
            for i in locatie_list.locaties:
                list[0].append(f"{i.naam} ({i.id})")
            
            for i in werknemers_list:
                ingewerkte_locaties = i.pop('ingewerkte_locaties')
                list.append([i['personeelsnummer'], i['naam']])
                list[-1].extend(["x" if j in ingewerkte_locaties else ""
                                for j in range(1,len(list[0])-1)])
            
            jf.write(self.path, werknemers_list)
            csv.write('data/ingewerkte_locaties.csv', list)

    def retreive_from_file(self):
        """If the instance has a path bound to it, it will retreive the data
        of the file to the instance."""

        if self.path:
            werknemers_list = jf.read(self.path)
            if werknemers_list:
                self.to_class(werknemers_list)

    def get_index_by_id(self, id, search_list):
        for i in range(len(search_list)):
            if id == search_list[i].personeelsnummer:
                return i

    def delete_werknemer(self, werknemer, save_file=False):
        personeelsnummer = werknemer.personeelsnummer

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
        
        del self.medewerkers[self.get_index_by_id(
            personeelsnummer, self.medewerkers
        )]

    def add_inwerker(self, inwerker, save_file=False):
        """Adds an inwerker to the medewerker instance. Takes either
        a dictionary or an inwerker and adds it to both the inwerkers list
        and the full list of medewerkers. By default doesn't save to the file
        if it has one, but if specified that it must be saved, it will
        be saved."""

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
        """Adds an interne medewerker to the medewerker instance. Takes
        either a dictionary or an interne_medewerker and adds it to
        both the interne_medewerkers list and the full list of medewerkers.
        By default doesn't save to the file if it has one, but if specified
        that it must be saved, it will be saved."""

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
        """Adds an externe medewerker to the medewerker instance. Takes
        either a dictionary or an externe_medewerker and adds it to
        both the externe_medewerkers list and the full list of medewerkers.
        By default doesn't save to the file if it has one, but if specified
        that it must be saved, it will be saved."""

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
        """Is used to add a list of dictionaries or a list of
        Extern_medewerker, Intern_medewerker or Inwerker through
        the add functions."""
        
        for i in werknemers:
            if type(i) == dict:
                if not i["intern"]:
                    self.add_externe_medewerker(i)
                elif i["inwerker"]:
                    self.add_inwerker(i)
                else:
                    self.add_interne_medewerker(i)
            else:
                if type(i) == Extern_medewerker:
                    self.add_externe_medewerker(i)
                elif type(i) == Inwerker:
                    self.add_inwerker(i)
                elif type(i) == Intern_medewerker:
                    self.add_interne_medewerker(i)

    def to_list(self):
        """Returns a list with dictionaries to make saving to json files
        easier."""

        return [medewerker.to_dict() for medewerker in self.medewerkers]

    def to_inwerker(self):
        pass

    def to_intern(self):
        pass

    def set_sort_by(self, to_set, key):
        for locatie in to_set:
            locatie.sorted_by = key

    def sort(self, key):
        if key in ["personeelsnummer", "inwerk_probability"]:
            self.set_sort_by(self.interne_medewerkers, key)
            self.set_sort_by(self.externe_medewerkers, key)
            self.set_sort_by(self.inwerkers, key)
            self.set_sort_by(self.medewerkers, key)

            self.interne_medewerkers.sort()
            self.externe_medewerkers.sort()
            self.inwerkers.sort()
            self.medewerkers.sort()
            self.reverse()

    def reverse(self):
        self.interne_medewerkers.reverse()
        self.externe_medewerkers.reverse()
        self.inwerkers.reverse()
        self.medewerkers.reverse()

class Ingeplanden(Werknemers):
    def __init__(self, path=""):
        super().__init__("data/ingeplanden/"+path)
        self.absenten = []

    def save_to_file(self):
        """If the instance has a path bound to it, it will save the data
        of the instance to that file."""

        if self.path:
            self.sort("personeelsnummer")
            self.reverse()

            werknemers_list = self.to_list()
            for i in werknemers_list:
                i.pop('ingewerkte_locaties')
            jf.write(self.path, werknemers_list)

class medewerker_format:
    def __init__(self, intern, inwerker):
        """Initialise werknemer_format class."""
        self.personeelsnummer = self.get_new_personeelsnummer()
        self.naam = ""
        self.ingewerkte_locaties = [] # List of locations the employee is trained for
        self.voorkeuren = {}  # Dictionary of preferred locations or tasks
        self.ongeschikte_locaties = []  # List of unsuitable locations
        self.intern = intern  # Boolean indicating if the employee is internal
        self.inwerker = inwerker  # Boolean indicating if the employee is a trainer
        self.fysieke_kracht = 5  # Integer representing physical strength level
        self.sorted_by = "personeelsnummer"
        self.inwerk_probability = 0
    
    def get_ingewerkte_locaties(self, personeelsnummer:int):
        rows = csv.read('data/ingewerkte_locaties.csv')
        if not rows:
            return []
        
        for row in rows[1:]:
            if (int(row[0]) == personeelsnummer):
                locaties:list = row[2:]
                ingewerkte_locaties = []

                while 'x' in locaties:
                    x = locaties.index('x')
                    ingewerkte_locaties.append(x+1)
                    locaties[x] = ''
                
                return ingewerkte_locaties
        return []

    def get_new_personeelsnummer(self):
        werknemers_list = jf.read('data/werknemers.json')
        if werknemers_list:
            return (werknemers_list[-1]["personeelsnummer"] + 1)
        else:
            return 1
    
    def to_class(self, dictionary:dict):
        self.personeelsnummer = dictionary.get('personeelsnummer',
                                               self.personeelsnummer)
        self.naam = dictionary.get('naam', self.naam)
        self.ingewerkte_locaties = dictionary.get('ingewerkte_locaties',
                                                  self.get_ingewerkte_locaties(
                                                      self.personeelsnummer))
        self.voorkeuren = dictionary.get('voorkeuren', self.voorkeuren)
        self.ongeschikte_locaties = dictionary.get('ongeschikte_locaties',
                                                   self.ongeschikte_locaties)
        self.fysieke_kracht = dictionary.get('fysieke_kracht',
                                             self.fysieke_kracht)
        self.inwerk_probability = self.get_inwerk_probability()

    def to_dict(self):
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
        if self.sorted_by == "personeelsnummer":
            return self.personeelsnummer < other.personeelsnummer
        elif self.sorted_by == "inwerk_probability":
            return self.inwerk_probability < other.inwerk_probability
        else:
            raise ValueError

    def __le__(self, other):
        if self.sorted_by == "personeelsnummer":
            return self.personeelsnummer <= other.personeelsnummer
        elif self.sorted_by == "inwerk_probability":
            return self.inwerk_probability <= other.inwerk_probability
        else:
            raise ValueError

    def __eq__(self, other):
        if self.sorted_by == "personeelsnummer":
            return self.personeelsnummer == other.personeelsnummer
        elif self.sorted_by == "inwerk_probability":
            return self.inwerk_probability == other.inwerk_probability
        else:
            raise ValueError

    def __ne__(self, other):
        if self.sorted_by == "personeelsnummer":
            return self.personeelsnummer != other.personeelsnummer
        elif self.sorted_by == "inwerk_probability":
            return self.inwerk_probability != other.inwerk_probability
        else:
            raise ValueError

    def __gt__(self, other):
        if self.sorted_by == "personeelsnummer":
            return self.personeelsnummer > other.personeelsnummer
        elif self.sorted_by == "inwerk_probability":
            return self.inwerk_probability > other.inwerk_probability
        else:
            raise ValueError

    def __ge__(self, other):
        if self.sorted_by == "personeelsnummer":
            return self.personeelsnummer >= other.personeelsnummer
        elif self.sorted_by == "inwerk_probability":
            return self.inwerk_probability >= other.inwerk_probability
        else:
            raise ValueError

    def get_inwerk_probability(self):
        pass

class Intern_medewerker(medewerker_format):
    def __init__(self):
        super().__init__(True, False)
        self.__pity = 0

    def first_pick(self):
        self.__pity = 0

    def not_first_pick(self):
        self.__pity += 1

    def get_inwerk_probability(self):
        locations = Locaties('data/locaties.json')

        total_locations = len(locations.locaties)
        locations_ingewerkt = len(self.ingewerkte_locaties)
        locations_to_go = total_locations - locations_ingewerkt

        return locations_to_go / total_locations * 100

class Extern_medewerker(medewerker_format):
    def __init__(self):
        super().__init__(False, False)
    
    def get_inwerk_probability(self):
        if self.ingewerkte_locaties:
            return 0
        return 100.0

class Inwerker(medewerker_format):
    def __init__(self):
        super().__init__(True, True)
    
    def get_inwerk_probability(self):
        return 0.0