from tkinter.ttk import Combobox

class SearchableComboBox:
    """Maakt het mogelijk om een combobox te creeren met zoekfunctie."""

    def __init__(self, frame, options=[]):
        """Creeert de searchable combobox. Moet de frame meegeven en mogelijke
        opties die de combobox heeft."""

        self.frame = frame
        self.options = options
        self.set_value = ""
        self.get_value = ""
    
    def set(self, value):
        """Set de waarde van de searchable combobox. Moet altijd gebeuren voor grid
        sinds in de grid hij ook in de frame wordt gezet. Aanpassen is hierna
        niet meer mogelijk."""

        self.set_value = value
        self.get_value = value

    def grid(self, row=0, column=0, columnspan=1, padx=0):
        """Zet de searchable combobox neer op de grid. Kan de row, column,
        columnspan em padx aanpassen."""

        combo_box = Combobox(self.frame, value=self.options)
        combo_box.set(self.set_value)
        combo_box.grid(row=row, column=column, columnspan=columnspan, padx=padx)

        def search(event):
            """Zoekt voor de opties die hetgeen dat de gebruiker heeft ingetypt
            bevat."""

            value = event.widget.get()

            # Als waarde '' is, worden de opties gereset. Anders wordt er een
            # nieuwe lijst aangemaakt.
            if value == '':
                combo_box['values'] = self.options
            else:
                data = []
                for item in self.options:
                    if value.lower() in item.lower():
                        data.append(item)
                combo_box['values'] = data
        
        def set(event):
            """Zet de waarde van de searchable combobox naar 'get_value'."""
            self.get_value = combo_box.get()

        # Zorgt ervoor dat de waarde van "get_value" wordt vervangen elke keer
        # Dat er op een optie wordt gedrukt van de combobox.
        combo_box.bind("<<ComboboxSelected>>", set)

        # Zorgt ervoor dat de combobox wordt geupdate met nieuwe zoekopties.
        combo_box.bind('<KeyRelease>', search)

    def get(self):
        """Returnt de waarde van 'get_value"""
        return self.get_value