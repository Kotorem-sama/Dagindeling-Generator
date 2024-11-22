from tkinter import *
from tkinter.font import *
# from tkinter.ttk import Combobox
# from classes.werknemers import Werknemers
# from classes.locaties import Locaties

class HomeScreen(Frame):
    """De class voor de homescreen. Dit kan nuttig worden wanneer de app meer
    functies heeft naast alleen het generen van de dagindeling."""

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Hier staat een knop die een functie van de controller (de frame van
        # de app class die wordt meegestuurd) uitvoert waarmee je naar de
        # generatie pagina wordt gebracht.
        command=lambda:controller.show_generation_page()
        terug_button = Button(self, text="Genereer Dagindeling", command=command)
        terug_button.pack()