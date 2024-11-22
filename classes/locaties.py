from .read_files import json_file as jf
import os

class Locaties:
    """Een class met lijsten en groepen om makkelijk locaties te
    onderscheiden."""

    def __init__(self, path:str):
        """De initialisatie van de locaties class. Vraagt om een path en
        gebruikt daarna retreive from file om de gegevens in te laden."""

        self.gesloten_locaties = []
        self.open_locaties = []
        self.locaties = []
        self.groepen = {}
        self.path = path
        self.retreive_from_file()

    def get_index_by_id(self, id, search_list):
        """Een functie die de index van een locatie op basis van een id
        zoekt in search_list. De search_list moet een lijst zijn met locatie
        objecten."""
        for i in range(len(search_list)):
            if id == search_list[i].id:
                return i
            
    def get_location_by_id(self, id:int):
        """Een functie die de locatie zoekt in locaties op basis van een id.
        Stuurt een locatie object terug."""
        for location in self.locaties:
            if location.id == id:
                return location
            
    def is_location_closed(self, id:int):
        """Een functie die de gesloten locaties lijst doorzoekt op basis van
        een id om te bepalen of een locatie gesloten is of niet. Stuurt een
        bool terug."""
        for i in self.gesloten_locaties:
            if id == i.id:
                return True
        return False

    def close_location(self, id:int):
        """Een functie om een locatie op basis van een id te sluiten in de
        locaties lijst. Ook verplaatst het de locatie van de open locaties
        lijst naar de gesloten locatie lijst."""

        # Doorzoekt de locaties lijst en zet de beschikbaarheid op false.
        # Stopt de forloop wanneer de locatie is gevonden.
        for location in self.locaties:
            if id == location.id:
                location.beschikbaarheid = False
                break
        
        # Doorzoekt open locaties lijst, popt de locatie en voegt die toe aan
        # de gesloten locaties lijst. Stopt de forloop wanneer de locatie is
        # gevonden.
        for index in range(len(self.open_locaties)):
            if id == self.open_locaties[index].id:
                self.gesloten_locaties.append(self.open_locaties.pop(index))
                break

    def open_location(self, id:int):
        """Een functie om een locatie op basis van een id te sluiten in de
        locaties lijst. Ook verplaatst het de locatie van de gesloten locaties
        lijst naar de open locaties lijst."""

        # Doorzoekt de locaties lijst en zet de beschikbaarheid op true. Stopt
        # de forloop wanneer de locatie is gevonden.
        for location in self.locaties:
            if id == location.id:
                location.beschikbaarheid = True
                break
        
        # Doorzoekt de gesloten locaties lijst, popt de locatie en voegt die
        # toe aan de open locaties lijst. Stopt de forloop wanneer de locatie
        # is gevonden.
        for index in range(len(self.gesloten_locaties)):
            if id == self.gesloten_locaties[index].id:
                self.open_locaties.append(self.gesloten_locaties.pop(index))
                break

    def set_sort_by(self, to_set, key):
        """Om een lijst te kunnen sorteren moet er eerst per locatie het
        soort sorteren worden gespecificeerd, sinds de lijsten op verschillende
        manieren gesorteerd kunnen worden."""
        for locatie in to_set:
            locatie.sorted_by = key

    def sort(self, key:str):
        """Deze functie sorteert de locatie lijsten op key die wordt mee
        gegeven. Het kan gesorteerd worden op moeilijkheidsgraad, id,
        fysieke_kracht en belang."""

        if key in ["moeilijkheidsgraad","id","fysieke_kracht","belang"]:

            # Eerst wordt voor elke locatie in elke lijst de manier van
            # sorteren gewijzigd.
            self.set_sort_by(self.gesloten_locaties, key)
            self.set_sort_by(self.open_locaties, key)
            self.set_sort_by(self.locaties, key)

            # Dan wordt de sorteer functie uitgevoerd. Daarna wordt de lijst
            # omgedraaid.
            self.gesloten_locaties.sort()
            self.open_locaties.sort()
            self.locaties.sort()
            self.reverse()

    def reverse(self):
        """Een functie om alle lijsten om te draaien."""
        self.gesloten_locaties.reverse()
        self.open_locaties.reverse()
        self.locaties.reverse()

    def delete(self):
        """Een functie die probeert om de json die opgeslagen staat op
        self.path te verwijderen."""
        try:
            os.remove(self.path)
        except:
            pass
    
    def save_to_file(self):
        """Als de instantie een pad heeft dat is gekoppeld, worden de gegevens
        van de instantie in dat bestand opgeslagen. Eerst wordt het gesorteerd
        op id en omgedraaid zodat het begint bij id '1'."""

        if self.path:
            self.sort("id")
            self.reverse()

            # De class wordt omgezet naar een lijst om makkelijker op te slaan
            # in json.
            locaties_list = self.to_list()

            jf.write(self.path, locaties_list)

    def retreive_from_file(self):
        """Als de instantie een pad heeft dat eraan is gekoppeld, worden de
        gegevens van het bestand naar de instantie opgehaald met de to_class
        functie."""
        if self.path:
            locaties_list = jf.read(self.path)
            if locaties_list:
                self.to_class(locaties_list)

    def add_attraction(self, attractie):
        """Voegt een locatie type attractie toe aan de lijst. Neemt of een
        dictionary aan en zet het om naar een attractie class, of neemt een
        attractie class aan en zet het in de lijst."""

        if type(attractie) == dict:
            new_attraction = Attractie()
            new_attraction.to_class(attractie)
            self.locaties.append(new_attraction)
        elif type(attractie) == Attractie:
            self.locaties.append(attractie)
    
    def add_shop(self, shop):
        """Voegt een locatie type winkel toe aan de lijst. Neemt of een
        dictionary aan en zet het om naar een winkel class, of neemt een
        winkel class aan en zet het in de lijst."""
        if type(shop) == dict:
            new_show = Winkel()
            new_show.to_class(shop)
            self.locaties.append(new_show)
        elif type(shop) == Winkel:
            self.locaties.append(shop)

    def to_class(self, locaties:list):
        """Wordt gebruikt om een lijst met dictionaries of een lijst met
        Winkel en Attractie objecten toe te voegen via de add-functies. Checkt
        of de item in de lijst een locatie class is, of een dictionary."""

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
        
        # Checkt per locatie in de locaties lijst of deze beschikbaar is of
        # niet. Zo ja wordt hij toegevoegd aan de open locaties lijst, zo nee
        # wordt het toegevoegd aan de gesloten locaties lijst.
        for locatie in self.locaties:
            if locatie.beschikbaarheid:
                self.open_locaties.append(locatie)
            else:
                self.gesloten_locaties.append(locatie)
            
            # Voegt locaties to aan de groepen dictionary als een locatie
            # deelmaakt van een locatiegroep.
            if locatie.groep:
                if self.groepen.get(locatie.groep):
                    self.groepen[locatie.groep].append(locatie.id)
                else:
                    self.groepen[locatie.groep] = [locatie.id]

    def to_list(self):
        """Returnt een lijst met dictionaries, zodat je deze gemakkelijker in
        JSON-bestanden kunt opslaan."""
        return [locatie.to_dict() for locatie in self.locaties]

class Locatie:
    """Een """
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