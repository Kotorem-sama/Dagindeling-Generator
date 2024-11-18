from .read_files import json_file as jf

class Werknemers:
    def __init__(self):
        self.interne_medewerkers = []
        self.externe_medewerkers = []
        self.inwerkers = []
        self.medewerkers = []

    def add_inwerker(self, inwerker):
        if type(inwerker) == dict:
            inwerker = [inwerker]
        if type(inwerker) == list:
            for i in inwerker:
                new_inwerker = Inwerker()
                new_inwerker.to_class(i)
                self.inwerkers.append(new_inwerker)
                self.medewerkers.append(new_inwerker)
        elif type(inwerker) == Inwerker:
            self.inwerkers.append(inwerker)
            self.medewerkers.append(inwerker)

    def add_interne_medewerker(self, intern):
        if type(intern) == dict:
            intern = [intern]
        if type(intern) == list:
            for i in intern:
                new_werknemer = Intern_medewerker()
                new_werknemer.to_class(i)
                self.interne_medewerkers.append(new_werknemer)
                self.medewerkers.append(new_werknemer)
        elif type(intern) == Intern_medewerker:
            self.interne_medewerkers.append(intern)
            self.medewerkers.append(intern)

    def add_externe_medewerker(self, extern):
        if type(extern) == dict:
            extern = [extern]
        if type(extern) == list:
            for i in extern:
                new_extern = Extern_medewerker()
                new_extern.to_class(i)
                self.externe_medewerkers.append(new_extern)
                self.medewerkers.append(new_extern)
        elif type(extern) == Extern_medewerker:
            self.externe_medewerkers.append(extern)
            self.medewerkers.append(extern)

    def get_werknemers(self, path):
        werknemers_dict = jf.read(path)
        self.to_class(werknemers_dict)

    def to_class(self, werknemers):
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

    def to_inwerker(self):
        pass

    def to_intern(self):
        pass

    def sort(self):
        pass

class medewerker_format:
    def __init__(self, intern, inwerker):
        """Initialise werknemer class."""
        self.personeelsnummer = self.get_new_personeelsnummer()
        self.naam = ""
        self.ingewerkte_locaties = [] # List of locations the employee is trained for
        self.voorkeuren = {}  # Dictionary of preferred locations or tasks
        self.ongeschikte_locaties = []  # List of unsuitable locations
        self.intern = intern  # Boolean indicating if the employee is internal
        self.inwerker = inwerker  # Boolean indicating if the employee is a trainer
        self.fysieke_kracht = 5  # Integer representing physical strength level
    
    def get_new_personeelsnummer(self):
        werknemers_dict = jf.read('data/werknemers.json')
        return (werknemers_dict[-1]["personeelsnummer"] + 1)
    
    def to_class(self, dictionary:dict):
        self.personeelsnummer = dictionary.get('personeelsnummer', self.personeelsnummer)
        self.naam = dictionary.get('naam', self.naam)
        self.ingewerkte_locaties = dictionary.get('ingewerkte_locaties', self.ingewerkte_locaties)
        self.voorkeuren = dictionary.get('voorkeuren', self.voorkeuren)
        self.ongeschikte_locaties = dictionary.get('ongeschikte_locaties', self.ongeschikte_locaties)
        self.fysieke_kracht = dictionary.get('fysieke_kracht', self.fysieke_kracht)

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

class Intern_medewerker(medewerker_format):
    def __init__(self):
        super().__init__(True, False)

    def get_inwerk_probability(self):
        amount_ingewerkt = len(self.ingewerkte_locaties)
        locaties_dict = jf.read('data/locaties.json')

class Extern_medewerker(medewerker_format):
    def __init__(self):
        super().__init__(False, False)

class Inwerker(medewerker_format):
    def __init__(self):
        super().__init__(True, True)