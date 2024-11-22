from tkinter import *
from tkinter.font import *
from pages.generation_page import Generation_Page
from pages.home_screen import HomeScreen
from pages.dagindeling_page import Dagindeling_Page

class App(Tk):
    """Class voor de applicatie zodat het wisselen van schermen mogelijk is."""
    def __init__(self):
        Tk.__init__(self)

        # Zet zichzelf als frame bovenop onder de naam container
        self.container = Frame(self)
        self.container.place(x=0, y=0, relwidth=1, relheight=1)

        self.frames = {}

        # Laad alle schermen in op container.
        for F in (HomeScreen, Generation_Page, Dagindeling_Page):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        # Laat de generatie pagina zien.
        self.show_frame(Generation_Page)

    # Laat geselecteerde frame (context) zien.
    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

    # Zet homescherm bovenaan
    def show_home(self):
        frame = self.frames[HomeScreen]
        frame.tkraise()

    # Zet generatiepagina bovenaan.
    def show_generation_page(self):
        frame = self.frames[Generation_Page]
        frame.tkraise()

    # Laat de gegenereerde dagindeling zien en herlaad alles door alles te
    # verwijderen en opnieuw in te laten.
    def show_generated_dagindeling(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        self.frames = {}

        for F in (HomeScreen, Generation_Page, Dagindeling_Page):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.show_frame(Dagindeling_Page)

app = App()
app.geometry("1440x750")
app.title("Duinrell Dagindeling Generator")
app.mainloop()