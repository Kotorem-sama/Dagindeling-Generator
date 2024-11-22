from .read_files import json_file as jf
import os

class Locaties:
    def __init__(self, path:str):
        self.gesloten_locaties = []
        self.open_locaties = []
        self.locaties = []
        self.groepen = {}
        self.path = path
        self.retreive_from_file()

    def get_index_by_id(self, id, search_list):
        for i in range(len(search_list)):
            if id == search_list[i].id:
                return i
            
    def get_location_by_id(self, id):
        for location in self.locaties:
            if location.id == id:
                return location
            
    def is_location_closed(self, id):
        for i in self.gesloten_locaties:
            if id == i.id:
                return True
        return False

    def close_location(self, id:int):
        for location in self.locaties:
            if id == location.id:
                location.beschikbaarheid = False
                break

        for index in range(len(self.open_locaties)):
            if id == self.open_locaties[index].id:
                self.gesloten_locaties.append(self.open_locaties.pop(index))
                break

    def open_location(self, id:int):
        for location in self.locaties:
            if id == location.id:
                location.beschikbaarheid = True
                break
        
        for index in range(len(self.gesloten_locaties)):
            if id == self.gesloten_locaties[index].id:
                self.open_locaties.append(self.gesloten_locaties.pop(index))
                break

    def set_sort_by(self, to_set, key):
        for locatie in to_set:
            locatie.sorted_by = key

    def reverse(self):
        self.gesloten_locaties.reverse()
        self.open_locaties.reverse()
        self.locaties.reverse()

    def sort(self, key:str):
        if key in ["moeilijkheidsgraad","id","fysieke_kracht","belang"]:
            self.set_sort_by(self.gesloten_locaties, key)
            self.set_sort_by(self.open_locaties, key)
            self.set_sort_by(self.locaties, key)

            self.gesloten_locaties.sort()
            self.open_locaties.sort()
            self.locaties.sort()
            self.reverse()

    def delete(self):
        try:
            os.remove(self.path)
        except:
            pass
    
    def save_to_file(self):
        """If the instance has a path bound to it, it will save the data
        of the instance to that file."""

        if self.path:
            self.sort("id")
            self.reverse()
            locaties_list = self.to_list()
            jf.write(self.path, locaties_list)

    def retreive_from_file(self):
        """If the instance has a path bound to it, it will retreive the data
        of the file to the instance."""

        if self.path:
            locaties_list = jf.read(self.path)
            if locaties_list:
                self.to_class(locaties_list)

    def add_attraction(self, attractie, save_file=False):
        if type(attractie) == dict:
            new_attraction = Attractie()
            new_attraction.to_class(attractie)
            self.locaties.append(new_attraction)

        elif type(attractie) == Attractie:
            self.locaties.append(attractie)

        if save_file:
            self.save_to_file()
    
    def add_shop(self, shop, save_file=False):
        if type(shop) == dict:
            new_show = Winkel()
            new_show.to_class(shop)
            self.locaties.append(new_show)

        elif type(shop) == Attractie:
            self.locaties.append(shop)

        if save_file:
            self.save_to_file()

    def to_class(self, locaties:list):

        # Adds attractie and winkel classes to locaties list.
        for i in locaties:
            if type(i) == dict:
                if i["categorie"] == "attractie":
                    self.add_attraction(i)
                else:
                    self.add_shop(i)
            else:
                if type(i) == Attractie:
                    self.add_attraction(i)
                elif type(i) == Winkel:
                    self.add_shop(i)
        
        for locatie in self.locaties:
            # Adds location to open_locaties or gesloten_locaties.
            if locatie.beschikbaarheid:
                self.open_locaties.append(locatie)
            else:
                self.gesloten_locaties.append(locatie)
            
            # Adds location to the groepen dictionary if it has a group.
            if locatie.groep:
                if self.groepen.get(locatie.groep):
                    self.groepen[locatie.groep].append(locatie.id)
                else:
                    self.groepen[locatie.groep] = [locatie.id]

    def to_list(self):
        return [locatie.to_dict() for locatie in self.locaties]

class Locatie:
    def __init__(self, categorie):
        self.id = 0
        self.naam = ""
        self.categorie = categorie
        self.groep = ""
        self.minimale_medewerkers = 1
        self.maximale_medewerkers = 1
        self.moeilijkheidsgraad = 1
        self.beschikbaarheid = True
        self.belang = 1
        self.fysieke_kracht = 1
        self.sorted_by = "id"

    def __lt__(self, other):
        if self.sorted_by == "id":
            return self.id < other.id
        elif self.sorted_by == "moeilijkheidsgraad":
            return self.moeilijkheidsgraad < other.moeilijkheidsgraad
        elif self.sorted_by == "belang":
            return self.belang < other.belang
        elif self.sorted_by == "fysieke_kracht":
            return self.fysieke_kracht < other.fysieke_kracht
        else:
            raise ValueError

    def __le__(self, other):
        if self.sorted_by == "id":
            return self.id <= other.id
        elif self.sorted_by == "moeilijkheidsgraad":
            return self.moeilijkheidsgraad <= other.moeilijkheidsgraad
        elif self.sorted_by == "belang":
            return self.belang <= other.belang
        elif self.sorted_by == "fysieke_kracht":
            return self.fysieke_kracht <= other.fysieke_kracht
        else:
            raise ValueError

    def __eq__(self, other):
        if self.sorted_by == "id":
            return self.id == other.id
        elif self.sorted_by == "moeilijkheidsgraad":
            return self.moeilijkheidsgraad == other.moeilijkheidsgraad
        elif self.sorted_by == "belang":
            return self.belang == other.belang
        elif self.sorted_by == "fysieke_kracht":
            return self.fysieke_kracht == other.fysieke_kracht
        else:
            raise ValueError

    def __ne__(self, other):
        if self.sorted_by == "id":
            return self.id != other.id
        elif self.sorted_by == "moeilijkheidsgraad":
            return self.moeilijkheidsgraad != other.moeilijkheidsgraad
        elif self.sorted_by == "belang":
            return self.belang != other.belang
        elif self.sorted_by == "fysieke_kracht":
            return self.fysieke_kracht != other.fysieke_kracht
        else:
            raise ValueError

    def __gt__(self, other):
        if self.sorted_by == "id":
            return self.id > other.id
        elif self.sorted_by == "moeilijkheidsgraad":
            return self.moeilijkheidsgraad > other.moeilijkheidsgraad
        elif self.sorted_by == "belang":
            return self.belang > other.belang
        elif self.sorted_by == "fysieke_kracht":
            return self.fysieke_kracht > other.fysieke_kracht
        else:
            raise ValueError

    def __ge__(self, other):
        if self.sorted_by == "id":
            return self.id >= other.id
        elif self.sorted_by == "moeilijkheidsgraad":
            return self.moeilijkheidsgraad >= other.moeilijkheidsgraad
        elif self.sorted_by == "belang":
            return self.belang >= other.belang
        elif self.sorted_by == "fysieke_kracht":
            return self.fysieke_kracht >= other.fysieke_kracht
        else:
            raise ValueError

    def to_class(self, dictionary:dict):
        self.id = dictionary.get('id', self.id)
        self.naam = dictionary.get('naam', self.naam)
        self.groep = dictionary.get('groep', self.groep)
        self.minimale_medewerkers = dictionary.get('minimale_medewerkers', self.minimale_medewerkers)
        self.maximale_medewerkers = dictionary.get('maximale_medewerkers', self.maximale_medewerkers)
        self.moeilijkheidsgraad = dictionary.get('moeilijkheidsgraad', self.moeilijkheidsgraad)
        self.beschikbaarheid = dictionary.get('beschikbaarheid', self.beschikbaarheid)
        self.belang = dictionary.get('belang', self.belang)
        self.fysieke_kracht = dictionary.get('fysieke_kracht', self.fysieke_kracht)

    def to_dict(self):
        return {
            "id": self.id,
            "naam": self.naam,
            "categorie": self.categorie,
            "groep": self.groep,
            "minimale_medewerkers": self.minimale_medewerkers,
            "maximale_medewerkers": self.maximale_medewerkers,
            "moeilijkheidsgraad": self.moeilijkheidsgraad,
            "beschikbaarheid": self.beschikbaarheid,
            "belang": self.belang,
            "fysieke_kracht": self.fysieke_kracht
        }
    
class Attractie(Locatie):
    def __init__(self):
        super().__init__("attractie")

class Winkel(Locatie):
    def __init__(self):
        super().__init__("winkel")