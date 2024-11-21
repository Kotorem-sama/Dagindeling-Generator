from tkinter import *
from tkinter.font import *
from .widgets import SearchableComboBox
from classes.werknemers import Ingeplanden
from classes.read_files import date as get_date
from classes.locaties import Locaties
from modules.dagindeling_generator import generator

class Dagindeling_Page(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        get_date.get()
        
        topFrame = Frame(self, highlightbackground="blue", highlightthickness=2)
        topFrame.pack(side = TOP)

        title_font = Font(self.master, size=36, weight=BOLD)
        dagindeling_label = Label(topFrame, text="Gegenereerde Dagindeling",
                                  font=title_font)
        dagindeling_label.grid(row=0, column=0)

        middleFrame = Frame(self, highlightbackground="blue", highlightthickness=2)
        middleFrame.pack(fill=BOTH, expand=TRUE)

        leftFrame = Frame(middleFrame, highlightbackground="black", highlightthickness=2)
        leftFrame.place(x=0, y=0, relwidth=0.7, relheight=1)

        rightFrame = Frame(middleFrame, highlightbackground="red", highlightthickness=2)
        rightFrame.place(relx=0.7, y=0, relwidth=0.3, relheight=1)


        locations_font = Font(self.master, size=24)
        attractions_label = Label(leftFrame, text="Attracties:",
                            font=locations_font)
        attractions_label.grid(row=0, column=0, pady=10, padx=10)

        list_sample = [{1: ["B", "B", "B"]}, {2: ["B", "B", "B"]}]
        outcomes_list = []
        ingeplanden = Ingeplanden(f"{get_date.get()[0]}_ingeplanden.json")
        locations = Locaties(f"data/ingeplanden/{get_date.get()[0]}_locaties.json")

        dagindeling = generator(ingeplanden, locations)
        print(dagindeling)
        index = 0

        for key, values in dagindeling.items():
            location_frame = Frame(leftFrame)
            location_frame.grid(row=1+index, column=0)

            location = locations.get_location_by_id(int(key))

            Label(location_frame, text=location.id).grid(row=0, column=0)
            Label(location_frame, text=location.naam+":").grid(row=0, column=1)

            index += 1

            employees = values


        # command=lambda:controller.show_generation_page()
        # terug_button = Button(self, text="Terug", command=command)
        # terug_button.pack()