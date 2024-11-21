from tkinter import *
from tkinter.font import *
# from tkinter.ttk import Combobox
# from classes.werknemers import Werknemers
# from classes.locaties import Locaties

class Dagindeling_Page(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        
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

        


        # command=lambda:controller.show_generation_page()
        # terug_button = Button(self, text="Terug", command=command)
        # terug_button.pack()