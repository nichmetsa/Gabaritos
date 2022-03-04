from kivy.uix.popup import Popup
from kivy.uix.label import Label

class PopUpManager():

    def insert_numbers_only():

        popup = Popup(title = 'Aviso!',
                        content = Label(text='Inserir somente numeros'),
                        size_hint = (None, None), size=(400, 400),
                        background_color = 'yellow')
        popup.open()