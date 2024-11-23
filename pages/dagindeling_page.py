from tkinter import *
from tkinter.font import *
from tkinter import messagebox
from .widgets import SearchableComboBox
from classes.werknemers import Ingeplanden
from classes.read_files import date as get_date
from classes.locaties import Locaties
from classes.dagindeling import Dagindeling

class Dagindeling_Page(Frame):
    """Pagina of frame die de gegenereerde dagindeling laat zien waar je ook de
    dagindeling kan aanpassen, opslaan, verwijderen en opnieuw kan genereren."""

    def __init__(self, parent, controller):
        """Initialiseerd de frame en stuurt zichzelf naar de parent (app class
        die alles beheert). Controller is de frame waar functies aan gebonden
        zijn die je kan terug lezen in main."""
        Frame.__init__(self, parent)

        # Checkt of de json voor de geselecteerde datum bestaat of niet. Maakt
        # een nieuw bestand aan met de huidige datum als het niet bestaat.
        get_date.get()
        
        # Creeert van tevoren alle frames die het scherm verdelen.
        topFrame = Frame(self)
        middleFrame = Frame(self)
        leftFrame = Frame(middleFrame)
        rightFrame = Frame(middleFrame)
        
        # Voegt alle frames toe die hiermee op het scherm verschijnen.
        topFrame.pack(side = TOP)
        middleFrame.pack(fill=BOTH, expand=TRUE)
        leftFrame.place(x=0, y=0, relwidth=0.7, relheight=1)
        rightFrame.place(relx=0.7, y=0, relwidth=0.3, relheight=1)

        # Creeert de titel dat leest Gegenereerde Dagindeling. Heeft eigen font.
        # Staat in de topframe.
        title_font = Font(self.master, size=36, weight=BOLD)
        dagindeling_label = Label(topFrame, text="Gegenereerde Dagindeling",
                                  font=title_font)
        dagindeling_label.grid(row=0, column=0)

        # Laad alle ingeplanden en locaties in van de geselecteerde dag.
        ingeplanden = Ingeplanden(f"{get_date.get()[0]}_ingeplanden.json")
        locations_path = f"data/ingeplanden/{get_date.get()[0]}_locaties.json"
        locations = Locaties(locations_path)
        
        # Voegt alle werknemers toe aan werknemer_options voor de searchable
        # comboboxes.
        werknemer_options = [""]
        for werknemer in ingeplanden.medewerkers:
            option = f"{werknemer.naam} ({werknemer.personeelsnummer})"
            werknemer_options.append(option)

        # Voegt alle inwerkers toe aan de inwerker_options voor de searchable
        # comboboxes.
        inwerker_options = [""]
        for inwerker in ingeplanden.inwerkers:
            option = f"{inwerker.naam} ({inwerker.personeelsnummer})"
            inwerker_options.append(option)

        # De dagindeling class wordt gemaakt en genereerd hierbij direct de
        # dagindeling.
        dagindeling = Dagindeling()

        # Maakt dictionaries aan om aanpassingen in de dagindeling in op te
        # slaan.
        changed_dagindeling = {}
        changed_inwerkers = {}

        # Index voor de row waar de locatie frame te staan komt.
        grid_row = 0

        # Een forloop die door de dagindeling heen gaat om elke geopende locatie
        # toe te voegen aan het scherm met de werknemers en inwerkers die
        # worden neergezet in een searchable combobox.
        for key, values in dagindeling.dagindeling.items():

            # Creeert een apart frame voor elke locatie zodat alles in de grid
            # op zijn minst allignt met zijn eigen regel.
            location_frame = Frame(leftFrame)
            location_frame.grid(row=1+grid_row, column=0)

            # Voor de key in de dagindeling wordt een locatie gezocht in de
            # locatie lijst.
            location = locations.get_location_by_id(int(key))

            # Creeert labels voor de locatie id en de locatie naam.
            Label(location_frame, text=location.id).grid(row=0, column=0)
            Label(location_frame, text=location.naam+":").grid(row=0, column=1)
            
            # Creert een lijst voor alle searchable comboboxes.
            list_of_comboboxes = []
            
            # Probeert met een for loop 3 werknemers te pakken uit de
            # dagindeling lijst. Elke dagindeling gebruikt namelijk een int key
            # en een list value. Als het een error krijg, is employee leeg.
            for index in range(3):
                try:
                    employee_name = values[index].naam
                    employee_id = values[index].personeelsnummer
                    employee = f"{employee_name} ({employee_id})"
                except:
                    employee = ""

                # Maakt per locatie 3 werknemer comboboxes met de waarde van
                # employee als default. Voegt deze dan toe aan de lijst van
                # comboboxes om later de waardes ervan te kunnen lezen.
                werknemer_combobox = SearchableComboBox(
                    location_frame, werknemer_options)
                werknemer_combobox.set(employee)
                werknemer_combobox.grid(row=0, column=2+index)
                list_of_comboboxes.append(werknemer_combobox)
            
            # Verandert de lijst in de veranderde dagindeling naar de lijst van
            # comboboxes.
            changed_dagindeling[key] = list_of_comboboxes

            # Voegt voor elke locatie 1 inwerker combobox toe.
            inwerker_combobox = SearchableComboBox(
                location_frame, inwerker_options)

            # Checkt of de dagindeling een inwerker heeft ingepland op deze
            # locatie. Zo ja voegt het de naam met personeelsnummer toe als
            # waarde van de combobox.
            if dagindeling.inwerkers[key]:
                try:
                    inwerker = dagindeling.inwerkers[key][0]
                    inwerker_naam = inwerker.naam
                    inwerker_id = inwerker.personeelsnummer
                    inwerker_combobox.set(f"{inwerker_naam} ({inwerker_id})")
                except:
                    pass

            inwerker_combobox.grid(row=0, column=6, padx=50)

            # Voegt de combobox van de inwerker toe aan de changed_inwerkers
            # lijst.
            changed_inwerkers[key] = [inwerker_combobox]

            # Voegt waarde van 1 toe aan grid_row zodat alle locatie frames
            # niet op elkaar komen te staan.
            grid_row += 1

        def opslaan():
            """Functie voor het opslaan van de dagindeling. Slaat een back_up
            json op voor het geval foute keuzes zijn gemaakt en slaat een csv
            bestand op die elke keer wordt geladen."""

            # Voor elk item in de changed_dagindeling dictionary pakt deze
            # forloop de waarde van de geselecteerden.
            for key, values in changed_dagindeling.items():
                dagindeling.dagindeling[str(key)] = []
                dagindeling.inwerkers[str(key)] = []

                # Deze for loop checkt of de comboboxes in de lijst een
                # persoon bevatten. Gaat door wanneer dit niet zo is. Gebruikt
                # als het wel zo is string manipulatie om het personeelsnummer
                # te verkrijgen. Voegt daarna de persoon toe aan de dagindeling.
                for value in values:
                    try:
                        person = value.get()
                        id = int(person.split()[-1].strip("(").strip(")"))
                        employee = ingeplanden.get_employee_by_id(id)
                        dagindeling.dagindeling[str(key)].append(employee)
                    except:
                        pass
                
                # Deze code geeft een error wanneer de combobox leeg is sinds
                # het niet de werknemer kan vinden met lege id integer, maar
                # voegt de inwerker toe aan de dagindeling als deze is gevonden.
                try:
                    person = changed_inwerkers[str(key)][0].get()
                    id = int(person.split()[-1].strip("(").strip(")"))
                    employee = ingeplanden.get_employee_by_id(id)
                    dagindeling.inwerkers[str(key)].append(employee)
                except:
                    pass
            
            # Slaat de dagindeling op in een csv bestand met de geselecteerde
            # datum als naam. Stuurt je daarna terug naar de generatie pagina.
            dagindeling.save_csv()
            controller.show_generation_page()

        def opnieuw_genereren():
            """Deze functie vraagt de gebruiker met een messagebox of ze door
            willen gaan. Zo ja wordt de dagindeling csv verwijderd en wordt de
            dagindeling pagina gerefresht."""

            message = "Weet u zeker dat u opnieuw wilt genereren?"
            message = f"{message} De csv wordt hierbij verwijderd."

            waarschuwing = messagebox.askyesno("Waarschuwing", message)
            if waarschuwing:
                dagindeling.delete_csv()
                controller.show_generated_dagindeling()

        def verwijderen():
            """Deze functie vraagt de gebruiker met een messagebox of ze door
            willen gaan. Zo ja wordt alles dat stond opgeslagen met de
            geselecteerde datum verwijderd."""

            message = "Weet u zeker dat u de dagindeling wil verwijderen?"
            message = f"{message} Alle bestanden van de dag worden verwijderd."

            waarschuwing = messagebox.askyesno("Waarschuwing", message)
            if waarschuwing:
                dagindeling.delete()
                ingeplanden.delete()
                locations.delete()
                controller.show_generation_page()

        # Creeert een opslaan knop die de dagindeling opslaat.
        terug_button = Button(rightFrame, text="Opslaan", command=opslaan)
        terug_button.pack()

        # Creeert een opnieuw genereren knop die de dagindeling opnieuw
        # genereerd.
        regerenerate_button = Button(rightFrame, text="Opnieuw genereren",
                                    command=opnieuw_genereren)
        regerenerate_button.pack()

        # Creeert een verwijderen knop die alles verwijderd met de
        # geselecteerde datum.
        delete_button = Button(rightFrame, text="Verwijderen",
                                    command=verwijderen)
        delete_button.pack()

        # Creeert een terug knop om terug te gaan naar de generatie pagina.
        command=lambda:controller.show_generation_page()
        terug_button = Button(rightFrame, text="Terug", command=command)
        terug_button.pack()