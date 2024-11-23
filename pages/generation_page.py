from tkinter import *
from tkinter.font import *
from classes.werknemers import Werknemers, Ingeplanden
from classes.locaties import Locaties
from classes.read_files import date as get_date
from pathlib import *
from .widgets import SearchableComboBox
from classes.read_files import csv_file as csv
from classes.dagindeling import Dagindeling

class Gesloten_Locaties_Frame:
    """Class voor de gesloten locaties frame om locaties te selecteren en
    weer te geven."""

    def __init__(self, frame, master):
        """Initialisatie van de class waarbij locaties van de werk_date
        worden gelezen."""

        self.frame = frame
        self.master = master
        self.path = f"data/ingeplanden/{get_date.get()[0]}_locaties.json"
        self.gesloten_locaties = Locaties(self.path)
        self.initialise_file()

        # De text wat leest gesloten locaties. Heeft een eigen font.
        categories_font = Font(self.master, size=24, weight=BOLD)
        label_gesloten_locaties = Label(self.frame, text="Gesloten Locaties:",
                                    font=categories_font, padx=20)
        label_gesloten_locaties.grid(row=0, column=0, sticky="nsew",
                                    columnspan=3, pady=10)

        # Laad opties in voor het toevoegen van mogelijke locaties in de
        # searchable combobox.
        options = []
        for locatie in self.gesloten_locaties.locaties:
            options.append(f"{locatie.naam} ({locatie.id})")
        
        # Checkt of de locaties lijst json voor de geselecteerde dag al
        # bestaat. Zo niet slaat het programma een nieuwe op. En haalt de
        # locaties uit de generale locatieslijst.
        locatie_list = Locaties('data/locaties.json')
        if not self.gesloten_locaties.locaties:
            self.gesloten_locaties.to_class(locatie_list.to_list())
            self.gesloten_locaties.save_to_file()

        # Searchable combobox die options gebruikt als mogelijke selecties.
        search_gesloten_locaties = SearchableComboBox(self.frame, options)
        search_gesloten_locaties.set(options[0])
        search_gesloten_locaties.grid(1, 0)

        def remove():
            """Een functie die de geselecteerde locatie verwijderd uit de
            listbox en direct de locatie aanpast naar open of gesloten."""

            value = gesloten_locaties_listbox.curselection()
            if value:
                val = gesloten_locaties_listbox.get(value[0])
                
                # Gebruikt wat string manipulatie om de id van de locatie te
                # krijgen en opent direct de attractie waarna hij het bestand
                # opslaat.
                locatie_id = int(val.split()[-1].strip("(").strip(")"))
                locatie_list.open_location(locatie_id)
                locatie_list.save_to_file()

                # Gebruikt de locatie id om ook de locatie te openen in het
                # locaties bestand van de geselecteerde dag.
                self.gesloten_locaties.open_location(locatie_id)
                self.gesloten_locaties.save_to_file()

                # Verwijdert de locatie uit de listbox.
                gesloten_locaties_listbox.delete(value)

                # Past het aantal locaties die geopend zijn aan naar het nieuwe
                # aantal geopende locaties.
                opened_text = f"Open Locaties: {len(
                    self.gesloten_locaties.open_locaties)}"
                open_label.config(text=opened_text)

                # Past het aantal locaties die gesloten zijn aan naar het nieuwe
                # aantal gesloten locaties.
                close_text = f"Gesloten Locaties: {len(
                    self.gesloten_locaties.gesloten_locaties)}"
                closed_label.config(text=close_text)

        def get():
            """Een functie die de geselecteerde locatie uit de searchable
            combobox toevoegd aan de gesloten locaties lijst en ze in de
            bestanden aanpast."""

            value = search_gesloten_locaties.get()
            if value:
                
                # Gebruikt wat string manipulatie om de id van de locatie te
                # krijgen en sluit direct de attractie waarna hij het bestand
                # opslaat. Ook checkt het of de locatie al gesloten is of niet
                # om te voorkomen dat een locatie 2x in de lijst komt te staan.
                locatie_id = int(value.split()[-1].strip("(").strip(")"))
                if not self.gesloten_locaties.is_location_closed(locatie_id):
                    locatie_list.close_location(locatie_id)
                    locatie_list.save_to_file()

                    # Gebruikt de locatie id om ook de locatie te sluiten in het
                    # locaties bestand van de geselecteerde dag.
                    self.gesloten_locaties.close_location(locatie_id)
                    self.gesloten_locaties.save_to_file()

                    # Voegt de locatie toe aan de listbox
                    gesloten_locaties_listbox.insert(0, value)

                    # Past het aantal locaties die geopend zijn aan naar het
                    # nieuwe aantal geopende locaties.
                    opened_text = f"Open Locaties: {len(
                        self.gesloten_locaties.open_locaties)}"
                    open_label.config(text=opened_text)

                    # Past het aantal locaties die gesloten zijn aan naar het
                    # nieuwe aantal gesloten locaties.
                    close_text = f"Gesloten Locaties: {len(
                        self.gesloten_locaties.gesloten_locaties)}"
                    closed_label.config(text=close_text)

        # Creeert knop om locaties toe te voegen aan de lijst.
        button = Button(self.frame, text="Toevoegen", command=get)
        button.grid(row=1, column=1)

        # Creeert knop om locaties te verwijderen van de lijst.
        verwijderen_button = Button(self.frame, text="Verwijderen",
                                    command=remove)
        verwijderen_button.grid(row=1, column=2)

        # Creeert de frame voor de gesloten locaties listbox met een kleine
        # outline.
        gesloten_locaties_list = Frame(self.frame, highlightbackground="grey",
                                        highlightthickness=1)
        gesloten_locaties_list.grid(row=2, column=0, columnspan=3, pady=(20,0))

        # Voegt de listbox met gesloten locaties toe aan de bovenstaande frame
        # en maakt deze listbox scrollbaar met een scrollbar.
        gesloten_locaties_listbox = Listbox(gesloten_locaties_list, width=50,
                                            height=20)
        gesloten_locaties_listbox.pack(side=LEFT, fill=BOTH)
        gesloten_locaties_scrollbar = Scrollbar(gesloten_locaties_list)
        gesloten_locaties_scrollbar.pack(side=RIGHT, fill=BOTH)
        gesloten_locaties_listbox.config(
            yscrollcommand=gesloten_locaties_scrollbar.set)
        gesloten_locaties_scrollbar.config(
            command=gesloten_locaties_listbox.yview)
        
        # Hier worden alle gesloten locaties toegevoegd aan de listbox.
        for locatie in self.gesloten_locaties.gesloten_locaties:
            gesloten_locaties_listbox.insert(0,f"{locatie.naam} ({locatie.id})")

        # Hier staat de tekst waar de open locaties worden getelt.
        open_locations = len(self.gesloten_locaties.open_locaties)
        open_text = f"Open Locaties: {open_locations}"
        open_label = Label(self.frame, text=open_text)
        open_label.grid(row=3, column=0, pady=(10, 0))

        # Hier staat de tekst waar de gesloten locaties worden getelt.
        closed_locations = len(self.gesloten_locaties.gesloten_locaties)
        closed_text = f"Gesloten Locaties: {closed_locations}"
        closed_label = Label(self.frame, text=closed_text)
        closed_label.grid(row=3, column=1, pady=(10, 0))

    def initialise_file(self):
        """Een functie om alle locaties toe te voegen aan de nieuwe
        geselecteerde dag."""
        
        locatie_list = Locaties('data/locaties.json')
        if not self.gesloten_locaties.locaties:
            self.gesloten_locaties.to_class(locatie_list.to_list())
            self.gesloten_locaties.save_to_file()

class Aanwezigen_Frame:
    """Class voor de aanwezigen frame om aanwezigen te selecteren en weer te
    geven."""

    def __init__(self, frame, master):
        """Initialisatie van de class waarbij aanwezigen van de geselecteerde
        datum worden gelezen."""

        self.frame = frame
        self.master = master
        self.aanwezigen = Ingeplanden(f"{get_date.get()[0]}_ingeplanden.json")

        # De text wat leest aanwezigen. Heeft een eigen font.
        categories_font = Font(self.master, size=24, weight=BOLD)
        label_aanwezigen = Label(self.frame, text="Aanwezigen:",
                                 font=categories_font, padx=20)
        label_aanwezigen.grid(row=0, column=0, sticky="nsew", columnspan=3,
                                pady=10)

        # Zet de opties in een lijst die in de searchable combobox worden
        # weergegeven. Het is een lijst van alle werknemers met
        # personeelsnummer in haakjes ernaast.
        werknemers = Werknemers()
        options = []
        for werknemer in werknemers.medewerkers:
            options.append(f"{werknemer.naam} ({werknemer.personeelsnummer})")

        # Searchable combobox wordt gecreeert met als standaard waarde van de
        # eerste medewerker in de medewerkers lijst.
        search_aanwezigen = SearchableComboBox(self.frame, options)
        search_aanwezigen.set(options[0])
        search_aanwezigen.grid(1, 0)

        def get():
            """Een functie die de geselecteerde werknemer in de searchable
            combobox toevoegd aan de aanwezigen lijst en ze in de bestanden
            aanpast."""

            value = search_aanwezigen.get()
            if value:

                # Gebruikt wat string manipulatie om het personeelsnummer van
                # de werknemer te krijgen en voegt deze toe aan de aanwezigen
                # werknemers. Ook checkt het of de werknemer al in de lijst
                # staat op niet om 2x dezelfde werknemer te voorkomen.
                personeelsnummer = int(value.split()[-1].strip("(").strip(")"))
                if not self.aanwezigen.is_employee_in_list(personeelsnummer):
                    employee = werknemers.get_employee_by_id(personeelsnummer)
                    self.aanwezigen.to_class([employee])
                    self.aanwezigen.save_to_file()

                    # Voegt de werknemer toe aan de aanwezigen listbox.
                    aanwezigen_listbox.insert(0, value)

                    # Past het totaal aantal werknemers aan zodat het klopt met
                    # alle werknemers die geselecteerd zijn in de listbox.
                    total_text = f"Totaal: {len(self.aanwezigen.medewerkers)}"
                    total_employees_label.config(text=total_text)

                    # Past het totaal aantal inwerkers aan zodat het klopt met
                    # alle inwerkers die geselecteerd zijn in de listbox.
                    inwork_text = f"Inwerkers: {len(self.aanwezigen.inwerkers)}"
                    total_inwerkers_label.config(text=inwork_text)

        def remove():
            """Een functie die de geselecteerde werknemer verwijderd uit de
            listbox en direct de werknemer uit de opgeslagen lijst die erna
            opnieuw de lijst opslaat."""

            value = aanwezigen_listbox.curselection()
            if value:
                val = aanwezigen_listbox.get(value[0])

                # Gebruikt wat string manipulatie om het personeelsnummer van
                # de werknemer te krijgen en verwijdert deze van de aanwezigen
                # werknemers van de geselecteerde dag die staat opgeslagen.
                personeelsnummer = int(val.split()[-1].strip("(").strip(")"))
                self.aanwezigen.delete_werknemer(personeelsnummer)
                self.aanwezigen.save_to_file()
                
                # Verwijdert de werknemer van de listbox.
                aanwezigen_listbox.delete(value)

                # Checkt eerst of er een csv voor de dagindeling is opgeslagen.
                # Verwijderd daarna de medewerker van de lijst als hij bestaat
                # en als hij in de lijst staat.
                path = f"dagindelingen/{get_date.get()[0]}.csv"
                if csv.path_exists(path):
                    dagindeling = Dagindeling()
                    dagindeling.delete_medewerker(personeelsnummer)


                # Past het totaal aantal werknemers aan zodat het klopt met
                    # alle werknemers die geselecteerd zijn in de listbox.
                total_text = f"Totaal: {len(self.aanwezigen.medewerkers)}"
                total_employees_label.config(text=total_text)

                # Past het totaal aantal inwerkers aan zodat het klopt met
                # alle inwerkers die geselecteerd zijn in de listbox.
                inwork_text = f"Inwerkers: {len(self.aanwezigen.inwerkers)}"
                total_inwerkers_label.config(text=inwork_text)

        # Creeert de knop waarmee werknemers toegevoegd kunnen worden die zijn
        # geselecteerd uit de searchable combobox.
        toevoegen_button = Button(self.frame, text="Toevoegen", command=get)
        toevoegen_button.grid(row=1, column=1)

        # Creeert de knop waarmee werknemers verwijderd kunnen worden die zijn
        # geselecteerd in de listbox.
        verwijderen_button = Button(self.frame, text="Verwijderen",
                                    command=remove)
        verwijderen_button.grid(row=1, column=2)

        # Creeert een frame voor de listbox waar alle aanwezige werknemers
        # staan met een kleine border.
        aanwezigen_list = Frame(self.frame, highlightbackground="grey",
                                highlightthickness=1)
        aanwezigen_list.grid(row=2, column=0, columnspan=3, pady=(20,0))

        # Voegt de listbox met aanwezige medewerkers toe aan de frame
        # en maakt deze listbox scrollbaar met een scrollbar.
        aanwezigen_listbox = Listbox(aanwezigen_list, width=50, height=20)
        aanwezigen_scrollbar = Scrollbar(aanwezigen_list)
        aanwezigen_listbox.pack(side=LEFT, fill=BOTH)
        aanwezigen_scrollbar.pack(side=RIGHT, fill=BOTH)
        aanwezigen_listbox.config(yscrollcommand=aanwezigen_scrollbar.set)
        aanwezigen_scrollbar.config(command=aanwezigen_listbox.yview)

        # Voegt alle aanwezige medewerkers toe die gevonden zijn in de json met
        # alle aanwezigen van de geselecteerde dag.
        if self.aanwezigen.medewerkers:
            for employee in self.aanwezigen.medewerkers:
                value = f"{employee.naam} ({employee.personeelsnummer})"
                aanwezigen_listbox.insert(0, value)

        # Hier staat de tekst waar het totaal aantal medewerkers staat.
        total_employees_text = f"Totaal: {len(self.aanwezigen.medewerkers)}"
        total_employees_label = Label(self.frame, text=total_employees_text)
        total_employees_label.grid(row=3, column=0, pady=(10, 0))
        
        # Hier staat de tekst waar het totaal aantal Inwerkers staat.
        total_inwerkers_text = f"Inwerkers: {len(self.aanwezigen.inwerkers)}"
        total_inwerkers_label = Label(self.frame, text=total_inwerkers_text)
        total_inwerkers_label.grid(row=3, column=1, pady=(10, 0))

class Date_Frame:
    """Class voor het selecteren van een datum."""

    def __init__(self, frame, master):
        """Initialisatie van de class."""
        self.frame = frame
        self.master = master

        # De datum waar het laatst een dagindeling voor is gemaakt wordt hier
        # weergegeven.
        date = get_date.get()
        self.day = int(date[0].split("/")[2])
        self.month = int(date[0].split("/")[1])
        self.year = int(date[0].split("/")[0])

        # De text wat leest datum. Heeft een eigen font.
        categories_font = Font(self.master, size=24, weight=BOLD)
        Label(self.frame, text="Datum:", font=categories_font,
                padx=20).grid(row=0, column=0, columnspan=3, pady=10)
        
        # Creert een spinbox voor het selecteren van de dag met eigen font. Met
        # wrap kan je bij de hoogste waarde terug naar de laagste waarde en
        # andersom.
        spinbox_font = Font(family='Helvetica', size=24)
        spinboxval1 = IntVar(value=self.day)
        spinbox1 = Spinbox(self.frame, from_=1, to=31, wrap=True,
                        width=2, textvariable=spinboxval1, font=spinbox_font)
        spinbox1.grid(row=1, column=0)

        # Creert een spinbox voor het selecteren van de maand met eigen font.
        spinboxval2 = IntVar(value=self.month)
        spinbox2 = Spinbox(self.frame, from_=1, to=12, wrap=True,
                        width=2, textvariable=spinboxval2, font=spinbox_font)
        spinbox2.grid(row=1, column=1)

        # Creert een spinbox voor het selecteren van jaar met eigen font.
        spinboxval3 = IntVar(value=self.year)
        spinbox3 = Spinbox(self.frame, from_=1900, to=2100, wrap=True,
                        width=4, textvariable=spinboxval3, font=spinbox_font)
        spinbox3.grid(row=1, column=2)
        
        # Update de dag van de class naar de waarde van de spinbox.
        def update_day(event):
            self.day = int(spinbox1.get())
        
        # Update de maand van de class naar de waarde van de spinbox.
        def update_month(event):
            self.month = int(spinbox2.get())
        
        # Update het jaar van de class naar de waarde van de spinbox.
        def update_year(event):
            self.year = int(spinbox3.get())

        # Verbind de bovenstaande functies met de event "Leave". Dit houd in
        # dat als je met je muis in een van de spinboxes zit en er dan uit
        # beweegt dat dan het event wordt getriggerd.
        spinbox1.bind("<Leave>", update_day)
        spinbox2.bind("<Leave>", update_month)
        spinbox3.bind("<Leave>", update_year)

    def get(self):
        """Returnt een tuple van de waardes uit de class (jaar, maand en dag)."""
        return (self.year, self.month, self.day)

class Generation_Page(Frame):
    """Class voor de generatie pagina frame waarbij je aanwezigen en gesloten
    locaties kan toevoegen en verwijderen, de datum kan selecteren en terug kan
    gaan naar het hoofdmenu of door naar de dagindeling generatie."""

    def __init__(self, parent, controller):
        """Initialiseerd de frame en stuurt zichzelf naar de parent (app class
        die alles beheert). Controller is de frame waar functies aan gebonden
        zijn die je kan terug lezen in main."""
        Frame.__init__(self, parent)

        # Creeert de bovenste frame.
        topFrame = Frame(self)
        topFrame.pack(pady=(50,0))

        # Checkt of de json voor de geselecteerde datum bestaat of niet. Maakt
        # een nieuw bestand aan met de huidige datum als het niet bestaat.
        get_date.get()

        def checkdate():
            """Pakt de datum van de date frame en checkt of de datum bestaat."""
            year, month, day = date.get()
            
            # Checkt of het geselecteerde jaar een schrikkeljaar is.
            is_leapyear = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
            
            # Returns True wanneer de datum klopt. Returns False wanneer de
            # datum niet klopt.
            if is_leapyear and month == 2 and day == 29:
                return True
            if month == 2 and day > 28:
                return False
            if not month in [1, 3, 5, 7, 8, 10, 12] and day > 30:
                return False
            return True
        
        def refresh():
            """Een functie die de geselecteerde datum checkt of het bestaat. Zo
            ja zet het de geselecteerde datum in de work_date json in de goede
            format en refresht de aanwezigen en gesloten locatie frames."""

            if checkdate():
                # Pakt de datum en zet het in de goede format om opgeslagen te
                # worden.
                year, month, day = date.get()
                get_date.set(f"{year}/{month}/{day}")

                # Verwijdert elk item in de gesloten_locaties en aanwezigen
                # frames.
                for widget in aanwezigen_frame.winfo_children() and (
                    gesloten_locaties_frame.winfo_children()):
                    widget.destroy()

                # Voegt alle widgets weer toe aan de aanwezigen frame.
                Aanwezigen_Frame(aanwezigen_frame, self.master)

                # Voegt alle widgets weer toe aan de gesloten locaties frame.
                Gesloten_Locaties_Frame(gesloten_locaties_frame, self.master)

        # Creeert de titel dat lees Dagindeling Instellingen. Heeft eigen font.
        title_font = Font(self.master, size=36, weight=BOLD)
        label_title = Label(topFrame, text="Dagindeling Instellingen",
                            font=title_font)
        label_title.grid(row=0, column=0)

        # Creeert de frame die in het midden staat.
        middleFrame = Frame(self)
        middleFrame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Creert de frame binnen middleframe die aan de linkerkant van het
        # scherm zal plaatsen en voegt de date_frame class toe.
        date_frame = Frame(middleFrame)
        date_frame.place(anchor="c", relx=.25, rely=.5)
        date = Date_Frame(date_frame, self.master)
        
        # Creert een frame binnen de date_frame frame om deze gecentreerd weer
        # te geven.
        buttonFrame = Frame(date_frame)
        buttonFrame.grid(row=2, column=1, pady=20)
        
        # Creert de bevestigen knop die de datum checkt en aanpast.
        button = Button(buttonFrame, text="Bevestigen", command=refresh)
        button.grid()

        # Creert frame voor de aanwezigen_frame en voegt de class toe.
        aanwezigen_frame = Frame(middleFrame)
        aanwezigen_frame.place(anchor="c", relx=.5, rely=.5)
        Aanwezigen_Frame(aanwezigen_frame, self.master)

        # Creert frame voor de gesloten_locaties_frame en voegt de class toe.
        gesloten_locaties_frame = Frame(middleFrame)
        gesloten_locaties_frame.place(anchor="c", relx=.75, rely=.5)
        Gesloten_Locaties_Frame(gesloten_locaties_frame, self.master)

        # Creeert de frame aan de onderkant van de pagina.
        bottomFrame = Frame(self)
        bottomFrame.pack(padx=50, pady=(0,50), side=TOP)

        # Voegt de terug knop toe die de gebruiker stuurt naar het hoofdmenu.
        command=lambda:controller.show_home()
        terug_button = Button(bottomFrame, text="Terug", command=command)
        terug_button.pack(side=LEFT, padx=(0,100))

        # Voegt genereren/bekijken knop toe die de gebruiker stuurt naar de
        # gegenereerde dagindeling.
        command=lambda:controller.show_generated_dagindeling()
        button_text = "Genereren/Bekijken"
        genereer_button = Button(bottomFrame, text=button_text, command=command)
        genereer_button.pack(side=RIGHT)