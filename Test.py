from tkinter import *
from tkinter.ttk import Combobox
   
root = Tk()
root.title("combobox")
root.geometry("500x500")

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

        def get():
            self.get_value = combo_box.get()
        
        button = Button(self.frame, text="Toevoegen", command=get)
        button.grid(row=row, column=column+1, columnspan=columnspan)
        combo_box.bind('<KeyRelease>', search)

search = SearchableComboBox(root, ["C", "C#", "C++"])
search.grid(1, 1)
root.mainloop()