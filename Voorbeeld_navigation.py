from tkinter import *
from tkinter.font import *
from pages.generation_page import Generation_Page
from pages.home_screen import HomeScreen
from pages.dagindeling_page import Dagindeling_Page

class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.container = Frame(self)
        self.container.place(x=0, y=0, relwidth=1, relheight=1)

        self.frames = {}

        for F in (HomeScreen, Generation_Page, Dagindeling_Page, PageOne, PageTwo, StartPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_frame(Generation_Page)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

    def show_home(self):
        frame = self.frames[HomeScreen]
        frame.tkraise()

    def show_generation_page(self):
        frame = self.frames[Generation_Page]
        frame.tkraise()

    def show_generated_dagindeling(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        self.frames = {}

        for F in (HomeScreen, Generation_Page, Dagindeling_Page, PageOne, PageTwo, StartPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.show_frame(Dagindeling_Page)

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

app = App()
app.geometry("1440x750")
app.mainloop()