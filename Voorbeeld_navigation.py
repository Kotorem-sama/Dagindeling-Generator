from tkinter import *
from tkinter.font import *
from tkinter.ttk import Combobox
from classes.werknemers import Werknemers

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
        

class Generation_Page(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Genereer dagindeling text
        title_font = Font(self.master, size=36, weight=BOLD)
        label_title = Label(self, text="Genereer Dagindeling",
                            font=title_font)
        label_title.grid(row=0, column=0)
        # #Add duinrell logo

        # Aanwezigen text
        categories_font = Font(self.master, size=24, weight=BOLD)
        label_aanwezigen = Label(self, text="Aanwezigen:",
                                 font=categories_font, padx=20)
        label_aanwezigen.grid(row=1, column=0, sticky="nsew")

        # Set options for adding aanwezigen
        werknemers = Werknemers()
        options = []
        for werknemer in werknemers.medewerkers:
            options.append(f"{werknemer.naam} ({werknemer.personeelsnummer})")

        # Searchable combobox
        search_aanwezigen = SearchableComboBox(self, options)
        search_aanwezigen.grid(2, 0)

        # Command for button to add to listbox
        def get():
            value = search_aanwezigen.get()
            aanwezigen.insert(0, value)
            aanwezigen_listbox.insert(0, value)

        # Button that adds to listbox
        button = Button(self, text="Toevoegen", command=get)
        button.grid(row=2, column=1)


        aanwezigen = []
        aanwezigen_list = Frame(self)
        aanwezigen_list.grid(row=3, column=0)

        aanwezigen_listbox = Listbox(aanwezigen_list)
        aanwezigen_listbox.pack(side = LEFT, fill = BOTH)

        aanwezigen_scrollbar = Scrollbar(aanwezigen_list)
        aanwezigen_scrollbar.pack(side = RIGHT, fill = BOTH)

        aanwezigen_listbox.config(yscrollcommand=aanwezigen_scrollbar.set)
        aanwezigen_scrollbar.config(command=aanwezigen_listbox.yview)


        # label_gesloten_locaties = Label(MiddlePart, text="Gesloten Locaties:",
        #                          font=categories_font, padx=20)
        # label_gesloten_locaties.pack(side=LEFT)

        # label_afwezigen = Label(MiddlePart, text="Afwezigen:",
        #                          font=categories_font, padx=20)
        # label_afwezigen.pack(side=LEFT)

app = App()
app.geometry("1440x750")
app.mainloop()