from tkinter.ttk import Combobox

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
        
        def set(event):
            self.get_value = combo_box.get()

        combo_box.bind("<<ComboboxSelected>>", set)
        combo_box.bind('<KeyRelease>', search)

    def get(self):
        return self.get_value