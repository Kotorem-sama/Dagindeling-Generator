from tkinter import *
from tkinter.font import *
# from tkinter.ttk import Combobox
# from classes.werknemers import Werknemers
# from classes.locaties import Locaties

class Dagindeling_Page(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        command=lambda:controller.show_generation_page()
        terug_button = Button(self, text="Terug", command=command)
        terug_button.pack()