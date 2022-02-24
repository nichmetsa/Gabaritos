﻿from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup

from Gabaritos import MohrsCircle, UnitCell

import numpy as np
import re

class TensorScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.sigma_x = TextInput(text='Sigma X')
        self.sigma_y = TextInput(text='Sigma Y')
        self.sigma_z = TextInput(text='Sigma Z')
        self.tau_yx = TextInput(text='Tau YX')
        self.tau_zx = TextInput(text='Tau ZX')
        self.tau_zy = TextInput(text='Tau ZY')

        checkboxlayout = BoxLayout(orientation = 'horizontal')
        self.mohrs = CheckBox()
        self.unitcell = CheckBox()
        mohrs_label = Label(text = "Show Mohrs Circle:")
        unitcell_label = Label(text = "Show Unit Cell:")
        checkboxlayout.add_widget(mohrs_label)
        checkboxlayout.add_widget(self.mohrs)
        checkboxlayout.add_widget(unitcell_label)
        checkboxlayout.add_widget(self.unitcell)

        run = Button(text='Run', background_color = "green", on_press = self.run_program)
        self.add_widget(self.sigma_x)
        self.add_widget(self.sigma_y)
        self.add_widget(self.sigma_z)
        self.add_widget(self.tau_yx)
        self.add_widget(self.tau_zx)
        self.add_widget(self.tau_zy)
        self.add_widget(checkboxlayout)
        self.add_widget(run)

    def run_program(self,obj):

        tensor_list = [self.sigma_x.text, 
                       self.sigma_y.text, 
                       self.sigma_z.text, 
                       self.tau_yx.text, 
                       self.tau_zx.text,
                       self.tau_zy.text]

        r = re.compile('\D+')

        value = False

        for element in tensor_list:
            if r.match(element):
                value = True
                
        
        if value:
            popup = Popup(title='Aviso!',
                        content=Label(text='Inserir somente numeros'),
                        size_hint=(None, None), size=(400, 400),
                        background_color = 'yellow')
            popup.open()

        else:
            tensor = [[float(self.sigma_x.text), float(self.tau_yx.text), float(self.tau_zx.text)],
                    [float(self.tau_yx.text), float(self.sigma_y.text), float(self.tau_zy.text)],
                    [float(self.tau_zx.text), float(self.tau_zy.text), float(self.sigma_z.text)]]

            if self.mohrs.active:

                circle = MohrsCircle(tensor)
                circle.plot_data()

            if self.unitcell.active:

                cell = UnitCell(tensor)
                cell.show()


class GabaritosApp(App):
    pass


GabaritosApp().run()