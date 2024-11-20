from tkinter import *

class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container = Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

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

app = App()
app.mainloop()