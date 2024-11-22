from tkinter import *
from tkinter.font import *
from tkinter import messagebox
from .widgets import SearchableComboBox
from classes.werknemers import Ingeplanden
from classes.read_files import date as get_date
from classes.locaties import Locaties
from classes.dagindeling import Dagindeling

class Dagindeling_Page(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        get_date.get()
        
        topFrame = Frame(self)
        middleFrame = Frame(self)
        leftFrame = Frame(middleFrame)
        rightFrame = Frame(middleFrame)

        topFrame.pack(side = TOP)
        middleFrame.pack(fill=BOTH, expand=TRUE)
        leftFrame.place(x=0, y=0, relwidth=0.7, relheight=1)
        rightFrame.place(relx=0.7, y=0, relwidth=0.3, relheight=1)

        title_font = Font(self.master, size=36, weight=BOLD)
        dagindeling_label = Label(topFrame, text="Gegenereerde Dagindeling",
                                  font=title_font)
        dagindeling_label.grid(row=0, column=0)

        ingeplanden = Ingeplanden(f"{get_date.get()[0]}_ingeplanden.json")
        locations = Locaties(f"data/ingeplanden/{get_date.get()[0]}_locaties.json")
        
        werknemer_options = [""]
        for werknemer in ingeplanden.medewerkers:
            werknemer_options.append(f"{werknemer.naam} ({werknemer.personeelsnummer})")

        inwerker_options = [""]
        for inwerker in ingeplanden.inwerkers:
            inwerker_options.append(f"{inwerker.naam} ({inwerker.personeelsnummer})")

        dagindeling = Dagindeling()
        changed_dagindeling = {}
        changed_inwerkers = {}
        index = 0

        for key, values in dagindeling.dagindeling.items():
            location_frame = Frame(leftFrame)
            location_frame.grid(row=1+index, column=0)

            location = locations.get_location_by_id(int(key))

            Label(location_frame, text=location.id).grid(row=0, column=0)
            Label(location_frame, text=location.naam+":").grid(row=0, column=1)
            
            listofboxes = []
            
            for i in range(3):
                try:
                    employee = f"{values[i].naam} ({values[i].personeelsnummer})"
                except:
                    employee = ""

                werknemer_box = SearchableComboBox(location_frame, werknemer_options)
                werknemer_box.set(employee)
                werknemer_box.grid(row=0, column=2+i)
                listofboxes.append(werknemer_box)

            changed_dagindeling[key] = listofboxes

            inwerker_box = SearchableComboBox(location_frame, inwerker_options)
            if dagindeling.inwerkers[key]:
                person = dagindeling.inwerkers[key][0]
                inwerker_box.set(f"{person.naam} ({person.personeelsnummer})")
            inwerker_box.grid(row=0, column=6, padx=50)
            changed_inwerkers[key] = [inwerker_box]

            index += 1

        def opslaan():
            for key, values in changed_dagindeling.items():
                dagindeling.dagindeling[int(key)] = []
                dagindeling.inwerkers[int(key)] = []

                for value in values:
                    try:
                        person = value.get()
                        id = int(person.split()[-1].strip("(").strip(")"))
                        employee = ingeplanden.get_employee_by_id(id)
                        dagindeling.dagindeling[int(key)].append(employee)
                    except:
                        pass
                
                try:
                    person = changed_inwerkers[int(key)][0].get()
                    id = int(person.split()[-1].strip("(").strip(")"))
                    employee = ingeplanden.get_employee_by_id(id)
                    dagindeling.inwerkers[int(key)].append(employee)
                except:
                    pass

            dagindeling.save_csv()
            controller.show_generation_page()

        def opnieuw_genereren():
            message = "Weet u zeker dat u opnieuw wilt genereren?"
            message2 = message + " De csv wordt hierbij verwijderd."
            waarschuwing = messagebox.askyesno("Waarschuwing", message2)
            if waarschuwing:
                dagindeling.delete_csv()
                controller.show_generated_dagindeling()

        def verwijderen():
            message = "Weet u zeker dat u de dagindeling wil verwijderen?"
            message2 = message + " Alle bestanden van de dag worden verwijderd."
            waarschuwing = messagebox.askyesno("Waarschuwing", message2)
            if waarschuwing:
                dagindeling.delete()
                ingeplanden.delete()
                locations.delete()
                controller.show_generation_page()


        terug_button = Button(rightFrame, text="Opslaan", command=opslaan)
        terug_button.pack()

        regerenerate_button = Button(rightFrame, text="Opnieuw genereren",
                                    command=opnieuw_genereren)
        regerenerate_button.pack()

        delete_button = Button(rightFrame, text="Verwijderen",
                                    command=verwijderen)
        delete_button.pack()

        command=lambda:controller.show_generation_page()
        terug_button = Button(rightFrame, text="Terug", command=command)
        terug_button.pack()