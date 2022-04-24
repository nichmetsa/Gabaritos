from kivy.uix.popup import Popup
from kivy.uix.label import Label

class PopUpManager():

    def insert_numbers_only():

        popup = Popup(title = 'Warning!',
                        content = Label(text='Insert only numbers!'),
                        size_hint = (None, None), size=(400, 400),
                        background_color = 'yellow')
        popup.open()