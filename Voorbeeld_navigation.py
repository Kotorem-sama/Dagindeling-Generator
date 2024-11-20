from tkinter import *
from tkinter.font import *
from tkinter.ttk import Combobox
from classes.werknemers import Werknemers
from classes.locaties import Locaties

class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container = Frame(self)
        container.place(x=0, y=0, relwidth=1, relheight=1)

        self.frames = {}

        for F in (Generation_Page, PageOne, PageTwo, StartPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_frame(Generation_Page)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = Label(self, text="Start Page")
        label.pack(padx=10, pady=10)

        command=lambda:controller.show_frame(PageOne)
        page_one = Button(self, text="Page One", command=command)
        page_one.pack()

        command=lambda:controller.show_frame(PageTwo)
        page_two = Button(self, text="Page Two", command=command)
        page_two.pack()

class PageOne(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = Label(self, text="Page One")
        label.pack(padx=10, pady=10)

        command=lambda:controller.show_frame(StartPage)
        start_page = Button(self, text="Start Page", command=command)
        start_page.pack()

        command=lambda:controller.show_frame(PageTwo)
        page_two = Button(self, text="Page Two", command=command)
        page_two.pack()

class PageTwo(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = Label(self, text="Page Two")
        label.pack(padx=10, pady=10)

        command=lambda:controller.show_frame(StartPage)
        start_page = Button(self, text="Start Page", command=command)
        start_page.pack()

        command=lambda:controller.show_frame(PageOne)
        page_one = Button(self, text="Page One", command=command)
        page_one.pack()

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
        self.gesloten_locaties = []

        # Aanwezigen text
        categories_font = Font(self.master, size=24, weight=BOLD)
        label_gesloten_locaties = Label(self.frame, text="Gesloten Locaties:",
                                 font=categories_font, padx=20)
        label_gesloten_locaties.grid(row=0, column=0, sticky="nsew", columnspan=2)

        # Set options for adding locaties
        locatie_list = Locaties('data/locaties.json')
        options = []
        for locatie in locatie_list.locaties:
            options.append(f"{locatie.naam} ({locatie.id})")

        # Searchable combobox
        search_gesloten_locaties = SearchableComboBox(self.frame, options)
        search_gesloten_locaties.grid(1, 0)

        # Command for button to add to listbox
        def get():
            value = search_gesloten_locaties.get()
            self.gesloten_locaties.insert(0, value)
            gesloten_locaties_listbox.insert(0, value)

        # Button that adds to listbox
        button = Button(self.frame, text="Toevoegen", command=get)
        button.grid(row=1, column=1)


        
        gesloten_locaties_list = Frame(self.frame)
        gesloten_locaties_list.grid(row=2, column=0, columnspan=2)

        gesloten_locaties_listbox = Listbox(gesloten_locaties_list, width=50, height=20)
        gesloten_locaties_listbox.pack(side=LEFT, fill=BOTH)
        gesloten_locaties_scrollbar = Scrollbar(gesloten_locaties_list)
        gesloten_locaties_scrollbar.pack(side=RIGHT, fill=BOTH)
        gesloten_locaties_listbox.config(yscrollcommand=gesloten_locaties_scrollbar.set)
        gesloten_locaties_scrollbar.config(command=gesloten_locaties_listbox.yview)

    def get(self):
        return self.gesloten_locaties

class Aanwezigen_Frame:
    def __init__(self, frame, master):
        self.frame = frame
        self.master = master
        self.aanwezigen = []

        # Aanwezigen text
        categories_font = Font(self.master, size=24, weight=BOLD)
        label_aanwezigen = Label(self.frame, text="Aanwezigen:",
                                 font=categories_font, padx=20)
        label_aanwezigen.grid(row=0, column=0, sticky="nsew", columnspan=2)

        # Set options for adding aanwezigen
        werknemers = Werknemers()
        options = []
        for werknemer in werknemers.medewerkers:
            options.append(f"{werknemer.naam} ({werknemer.personeelsnummer})")

        # Searchable combobox
        search_aanwezigen = SearchableComboBox(self.frame, options)
        search_aanwezigen.grid(1, 0)

        # Command for button to add to listbox
        def get():
            value = search_aanwezigen.get()
            self.aanwezigen.insert(0, value)
            aanwezigen_listbox.insert(0, value)

        # Button that adds to listbox
        button = Button(self.frame, text="Toevoegen", command=get)
        button.grid(row=1, column=1)


        
        aanwezigen_list = Frame(self.frame)
        aanwezigen_list.grid(row=2, column=0, columnspan=2)

        aanwezigen_listbox = Listbox(aanwezigen_list, width=50, height=20)
        aanwezigen_listbox.pack(side=LEFT, fill=BOTH)
        aanwezigen_scrollbar = Scrollbar(aanwezigen_list)
        aanwezigen_scrollbar.pack(side=RIGHT, fill=BOTH)
        aanwezigen_listbox.config(yscrollcommand=aanwezigen_scrollbar.set)
        aanwezigen_scrollbar.config(command=aanwezigen_listbox.yview)

    def get(self):
        return self.aanwezigen

class Generation_Page(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Create top frame.
        topFrame = Frame(self)
        topFrame.pack()
        
        # Genereer dagindeling text.
        title_font = Font(self.master, size=36, weight=BOLD)
        label_title = Label(topFrame, text="Genereer Dagindeling",
                            font=title_font)
        label_title.grid(row=0, column=0)
        # #Add duinrell logo

        # Create middle frame for the following frames.
        middleFrame = Frame(self, highlightbackground="blue", highlightthickness=2)
        middleFrame.pack(fill=X)

        # Create aanwezigen frame and add context.
        aanwezigen_frame = Frame(middleFrame, highlightbackground="blue", highlightthickness=2)
        aanwezigen_frame.grid(row=0,column=0)
        Aanwezigen_Frame(aanwezigen_frame, self.master)

        # Create gesloten locaties frame and add context.
        gesloten_locaties_frame = Frame(middleFrame, highlightbackground="blue", highlightthickness=2)
        gesloten_locaties_frame.grid(row=0,column=1)
        Gesloten_Locaties_Frame(gesloten_locaties_frame, self.master)

        # label_afwezigen = Label(middleFrame, text="Afwezigen:",
        #                          font=categories_font, padx=20)
        # label_afwezigen.grid(row=0, column=4, sticky="nsew", columnspan=2)

app = App()
app.geometry("1440x750")
app.mainloop()