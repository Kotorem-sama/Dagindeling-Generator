from tkinter.ttk import Combobox
from tkinter import *

window = Tk()
window.geometry("500x500")

class SearchableComboBox:
    def __init__(self, frame, options=[], value=StringVar()):
        self.frame = frame
        self.options = options
        self.set_value = value

    def grid(self, row=0, column=0, columnspan=1):

        combo_box = Combobox(self.frame, value=self.options)
        combo_box.set(self.set_value.get())
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
            self.set_value.set(combo_box.get())

        combo_box.bind("<<ComboboxSelected>>", set)
        combo_box.bind('<KeyRelease>', search)

outcome = []
options = ["a", "b", "c", "d", "e", "f"]
for i in range(3):
    test = StringVar()
    test.set(options[0])
    outcome.append(test)
    sc = SearchableComboBox(window, options, test)
    sc.grid(0, 0+i)

def get():
    for i in outcome:
        print(i.get())

button = Button(window, text="test", command=get).grid(column=0, row=1)

window.mainloop()