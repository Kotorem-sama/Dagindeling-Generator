from tkinter import *
from tkinter.font import *
from tkinter.ttk import Combobox
from classes.werknemers import Werknemers, Ingeplanden
from classes.locaties import Locaties
from classes.read_files import date as get_date
from pathlib import *

class SearchableComboBox:
    def __init__(self, frame, options=[]):
        self.frame = frame
        self.options = options
        self.set_value = ""
        self.get_value = ""

    def set(self, value):
        self.set_value = value

    def grid(self, row=0, column=0, columnspan=1):

        combo_box = Combobox(self.frame, value=self.options)
        combo_box.set(self.set_value)
        combo_box.grid(row=row, column=column, columnspan=columnspan)

        def search(event):
            value = event.widget.get()
            if value == '':
                combo_box['values'] = self.options
            else:
                data = []
                for item in self.options:
                    if value.lower() in item.lower():
                        data.append(item)
                combo_box['values'] = data
        
        def set(event):
            self.get_value = combo_box.get()

        combo_box.bind("<<ComboboxSelected>>", set)
        combo_box.bind('<KeyRelease>', search)

    def get(self):
        return self.get_value

class Gesloten_Locaties_Frame:
    def __init__(self, frame, master):
        self.frame = frame
        self.master = master
        self.path = f"data/ingeplanden/{get_date.get()[0]}_locaties.json"
        self.gesloten_locaties = Locaties(self.path)

        # Aanwezigen text
        categories_font = Font(self.master, size=24, weight=BOLD)
        label_gesloten_locaties = Label(self.frame, text="Gesloten Locaties:",
                                    font=categories_font, padx=20)
        label_gesloten_locaties.grid(row=0, column=0, sticky="nsew",
                                    columnspan=3, pady=10)

        # Set options for adding locaties
        locatie_list = Locaties('data/locaties.json')
        options = []
        for locatie in locatie_list.locaties:
            options.append(f"{locatie.naam} ({locatie.id})")
        
        if not self.gesloten_locaties.locaties:
            self.gesloten_locaties.to_class(locatie_list.to_list())
            self.gesloten_locaties.save_to_file()

        # Searchable combobox
        search_gesloten_locaties = SearchableComboBox(self.frame, options)
        search_gesloten_locaties.grid(1, 0)

        def remove():
            value = gesloten_locaties_listbox.curselection()
            if value:
                val = gesloten_locaties_listbox.get(value[0])
                
                # Gets the id from the string and closes the attraction.
                locatie_id = int(val.split()[-1].strip("(").strip(")"))
                locatie_list.open_location(locatie_id)
                locatie_list.save_to_file()

                self.gesloten_locaties.open_location(locatie_id)
                self.gesloten_locaties.save_to_file()

                gesloten_locaties_listbox.delete(value)

                opened_text = f"Open Locaties: {len(
                    self.gesloten_locaties.open_locaties)}"
                open_label.config(text=opened_text)

                close_text = f"Gesloten Locaties: {len(
                    self.gesloten_locaties.gesloten_locaties)}"
                closed_label.config(text=close_text)

        # Command for button to add items to listbox.
        def get():
            value = search_gesloten_locaties.get()
            if value:
                
                # Gets the id from the string and closes the attraction.
                locatie_id = int(value.split()[-1].strip("(").strip(")"))
                if not self.gesloten_locaties.is_location_closed(locatie_id):
                    locatie_list.close_location(locatie_id)
                    locatie_list.save_to_file()

                    self.gesloten_locaties.close_location(locatie_id)
                    self.gesloten_locaties.save_to_file()

                    gesloten_locaties_listbox.insert(0, value)

                    opened_text = f"Open Locaties: {len(
                        self.gesloten_locaties.open_locaties)}"
                    open_label.config(text=opened_text)

                    close_text = f"Gesloten Locaties: {len(
                        self.gesloten_locaties.gesloten_locaties)}"
                    closed_label.config(text=close_text)

        # Button that adds to listbox
        button = Button(self.frame, text="Toevoegen", command=get)
        button.grid(row=1, column=1)

        # Button that removes from listbox
        verwijderen_button = Button(self.frame, text="Verwijderen",
                                    command=remove)
        verwijderen_button.grid(row=1, column=2)

        # Creates frame for scrollable listbox
        gesloten_locaties_list = Frame(self.frame, highlightbackground="grey",
                                        highlightthickness=1)
        gesloten_locaties_list.grid(row=2, column=0, columnspan=3, pady=(20,0))

        # Adds listbox and makes it scrollable
        gesloten_locaties_listbox = Listbox(gesloten_locaties_list, width=50,
                                            height=20)
        gesloten_locaties_listbox.pack(side=LEFT, fill=BOTH)
        gesloten_locaties_scrollbar = Scrollbar(gesloten_locaties_list)
        gesloten_locaties_scrollbar.pack(side=RIGHT, fill=BOTH)
        gesloten_locaties_listbox.config(
            yscrollcommand=gesloten_locaties_scrollbar.set)
        gesloten_locaties_scrollbar.config(
            command=gesloten_locaties_listbox.yview)
        
        # Adds the already closed locations to the list
        for locatie in self.gesloten_locaties.gesloten_locaties:
            gesloten_locaties_listbox.insert(0,f"{locatie.naam} ({locatie.id})")

        open_text = f"Open Locaties: {len(self.gesloten_locaties.open_locaties)}"
        open_label = Label(self.frame, text=open_text)
        open_label.grid(row=3, column=0, pady=(10, 0))

        closed_text = f"Gesloten Locaties: {len(self.gesloten_locaties.gesloten_locaties)}"
        closed_label = Label(self.frame, text=closed_text)
        closed_label.grid(row=3, column=1, pady=(10, 0))

    def get(self):
        return self.gesloten_locaties

class Aanwezigen_Frame:
    def __init__(self, frame, master):
        self.frame = frame
        self.master = master
        self.aanwezigen = Ingeplanden(f"{get_date.get()[0]}_ingeplanden.json")

        # Aanwezigen text
        categories_font = Font(self.master, size=24, weight=BOLD)
        label_aanwezigen = Label(self.frame, text="Aanwezigen:",
                                 font=categories_font, padx=20)
        label_aanwezigen.grid(row=0, column=0, sticky="nsew", columnspan=3,
                                pady=10)

        # Set options for adding aanwezigen
        werknemers = Werknemers()
        options = []
        for werknemer in werknemers.medewerkers:
            options.append(f"{werknemer.naam} ({werknemer.personeelsnummer})")

        # Searchable combobox with all aanwezigen
        search_aanwezigen = SearchableComboBox(self.frame, options)
        search_aanwezigen.grid(1, 0)

        # Command for button to add to listbox
        def get():
            value = search_aanwezigen.get()
            if value:
                personeelsnummer = int(value.split()[-1].strip("(").strip(")"))
                if not self.aanwezigen.is_employee_in_list(personeelsnummer):
                    employee = werknemers.get_employee_by_id(personeelsnummer)
                    self.aanwezigen.to_class([employee])
                    self.aanwezigen.save_to_file()

                    aanwezigen_listbox.insert(0, value)

                    total_text = f"Totaal: {len(self.aanwezigen.medewerkers)}"
                    total_employees_label.config(text=total_text)
                    inwork_text = f"Inwerkers: {len(self.aanwezigen.inwerkers)}"
                    total_inwerkers_label.config(text=inwork_text)

        def remove():
            value = aanwezigen_listbox.curselection()
            if value:
                val = aanwezigen_listbox.get(value[0])
                personeelsnummer = int(val.split()[-1].strip("(").strip(")"))
                self.aanwezigen.delete_werknemer(personeelsnummer)
                aanwezigen_listbox.delete(value)
                self.aanwezigen.save_to_file()

                total_text = f"Totaal: {len(self.aanwezigen.medewerkers)}"
                total_employees_label.config(text=total_text)
                inwork_text = f"Inwerkers: {len(self.aanwezigen.inwerkers)}"
                total_inwerkers_label.config(text=inwork_text)

        # Button that adds to listbox
        toevoegen_button = Button(self.frame, text="Toevoegen", command=get)
        toevoegen_button.grid(row=1, column=1)

        # Button that removes from listbox
        verwijderen_button = Button(self.frame, text="Verwijderen",
                                    command=remove)
        verwijderen_button.grid(row=1, column=2)

        # Creates frame for scrollable listbox.
        aanwezigen_list = Frame(self.frame, highlightbackground="grey",
                                highlightthickness=1)
        aanwezigen_list.grid(row=2, column=0, columnspan=3, pady=(20,0))

        # Adds listbox and makes it scrollable
        aanwezigen_listbox = Listbox(aanwezigen_list, width=50, height=20)
        aanwezigen_listbox.pack(side=LEFT, fill=BOTH)
        aanwezigen_scrollbar = Scrollbar(aanwezigen_list)
        aanwezigen_scrollbar.pack(side=RIGHT, fill=BOTH)
        aanwezigen_listbox.config(yscrollcommand=aanwezigen_scrollbar.set)
        aanwezigen_scrollbar.config(command=aanwezigen_listbox.yview)

        if self.aanwezigen.medewerkers:
            for employee in self.aanwezigen.medewerkers:
                value = f"{employee.naam} ({employee.personeelsnummer})"
                aanwezigen_listbox.insert(0, value)

        total_employees_text = f"Totaal: {len(self.aanwezigen.medewerkers)}"
        total_employees_label = Label(self.frame, text=total_employees_text)
        total_employees_label.grid(row=3, column=0, pady=(10, 0))

        total_inwerkers_text = f"Inwerkers: {len(self.aanwezigen.inwerkers)}"
        total_inwerkers_label = Label(self.frame, text=total_inwerkers_text)
        total_inwerkers_label.grid(row=3, column=1, pady=(10, 0))

    def get(self):
        return self.aanwezigen

class Date_Frame:
    def __init__(self, frame, master):
        self.frame = frame
        self.master = master

        date = get_date.get()
        self.day = int(date[0].split("/")[2])
        self.month = int(date[0].split("/")[1])
        self.year = int(date[0].split("/")[0])

        categories_font = Font(self.master, size=24, weight=BOLD)
        Label(self.frame, text="Dag:", font=categories_font,
                padx=20).grid(row=0, column=0, columnspan=3, pady=10)
        
        spinbox_font = Font(family='Helvetica', size=24)
        spinboxval1 = IntVar(value=self.day)
        spinbox1 = Spinbox(self.frame, from_=1, to=31, wrap=True,
                        width=2, textvariable=spinboxval1, font=spinbox_font)
        spinbox1.grid(row=1, column=0)

        spinboxval2 = IntVar(value=self.month)
        spinbox2 = Spinbox(self.frame, from_=1, to=12, wrap=True,
                        width=2, textvariable=spinboxval2, font=spinbox_font)
        spinbox2.grid(row=1, column=1)

        spinboxval3 = IntVar(value=self.year)
        spinbox3 = Spinbox(self.frame, from_=1900, to=2024, wrap=True,
                        width=4, textvariable=spinboxval3, font=spinbox_font)
        spinbox3.grid(row=1, column=2)

        def pressed_1(event):
            self.day = int(spinbox1.get())

        def pressed_2(event):
            self.month = int(spinbox2.get())

        def pressed_3(event):
            self.year = int(spinbox3.get())

        spinbox1.bind("<Leave>", pressed_1)
        spinbox2.bind("<Leave>", pressed_2)
        spinbox3.bind("<Leave>", pressed_3)

    def get(self):
        return (self.year, self.month, self.day)

class Generation_Page(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Create top frame.
        topFrame = Frame(self)
        topFrame.pack(pady=(50,0))

        # Sets date if it doesnt exist
        get_date.get()

        # Checks whether a date exists or not
        def checkdate():
            year, month, day = date.get()
            
            leapyear = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
            
            if leapyear and month == 2 and day == 29:
                return True
            if month == 2 and day > 28:
                return False
            if not month in [1, 3, 5, 7, 8, 10, 12] and day > 30:
                return False
            return True
        
        # Refreshes the aanwezigen and gesloten locaties frame if date exists.
        def refresh():
            if checkdate():
                year, month, day = date.get()
                get_date.set(f"{year}/{month}/{day}")

                for widget in aanwezigen_frame.winfo_children() and (
                    gesloten_locaties_frame.winfo_children()):
                    widget.destroy()

                # Create aanwezigen frame and add context.
                Aanwezigen_Frame(aanwezigen_frame, self.master)

                # # Create gesloten locaties frame and add context.
                Gesloten_Locaties_Frame(gesloten_locaties_frame, self.master)

        # Genereer dagindeling text.
        title_font = Font(self.master, size=36, weight=BOLD)
        label_title = Label(topFrame, text="Genereer Dagindeling",
                            font=title_font)
        label_title.grid(row=0, column=0)
        
        # path = Path(__file__).parent.parent / "data/images/duinrell.jpg"
        # path = PhotoImage(file = path.absolute())
        # label1 = Label(topFrame, image=path, highlightbackground="blue", highlightthickness=2)
        # label1.grid(row=0, column=1)

        # Create middle frame for the following frames.
        middleFrame = Frame(self)
        middleFrame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Creates date frame and adds content.
        date_frame = Frame(middleFrame)
        date_frame.place(anchor="c", relx=.25, rely=.5)
        date = Date_Frame(date_frame, self.master)
        
        buttonFrame = Frame(date_frame)
        buttonFrame.grid(row=2, column=1, pady=20)

        button = Button(buttonFrame, text="Bevestigen", command=refresh)
        button.grid()
        # Create aanwezigen frame and adds content.
        aanwezigen_frame = Frame(middleFrame)
        aanwezigen_frame.place(anchor="c", relx=.5, rely=.5)
        Aanwezigen_Frame(aanwezigen_frame, self.master)

        # Create gesloten locaties frame and adds content.
        gesloten_locaties_frame = Frame(middleFrame)
        gesloten_locaties_frame.place(anchor="c", relx=.75, rely=.5)
        Gesloten_Locaties_Frame(gesloten_locaties_frame, self.master)

        # Create bottom frame for the buttons
        bottomFrame = Frame(self)
        bottomFrame.pack(padx=50, pady=(0,50), side=TOP)

        # Add back button
        terug_button = Button(bottomFrame, text="Terug")
        terug_button.pack(side=LEFT, padx=(0,100))

        # Add generate button
        genereer_button = Button(bottomFrame, text="Genereren")
        genereer_button.pack(side=RIGHT)