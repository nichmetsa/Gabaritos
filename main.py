from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox

from Gabaritos import MohrsCircle, UnitCell
from InputManager import InputManager

class TensorScreen(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 2
        self.sigma_x_text = Label(text='Sigma X')
        self.sigma_x = TextInput(text='0')
        self.sigma_y_text = Label(text='Sigma Y')
        self.sigma_y = TextInput(text='0')
        self.sigma_z_text = Label(text='Sigma Z')
        self.sigma_z = TextInput(text='0')
        self.tau_yx_text = Label(text='Tau YX')
        self.tau_yx = TextInput(text='0')
        self.tau_zx_text = Label(text='Tau ZX')
        self.tau_zx = TextInput(text='0')
        self.tau_zy_text = Label(text='Tau ZY')
        self.tau_zy = TextInput(text='0')

        self.mohrs = CheckBox()
        self.unitcell = CheckBox()
        mohrs_label = Label(text = "Show Mohrs Circle:")
        unitcell_label = Label(text = "Show Unit Cell:")

        run = Button(text='Run', background_color = "green", on_press = self.run_program)
        self.add_widget(self.sigma_x_text)
        self.add_widget(self.sigma_x)

        self.add_widget(self.sigma_y_text)
        self.add_widget(self.sigma_y)

        self.add_widget(self.sigma_z_text)
        self.add_widget(self.sigma_z)

        self.add_widget(self.tau_yx_text)
        self.add_widget(self.tau_yx)

        self.add_widget(self.tau_zx_text)
        self.add_widget(self.tau_zx)
        
        self.add_widget(self.tau_zy_text)
        self.add_widget(self.tau_zy)

        self.add_widget(mohrs_label)
        self.add_widget(self.mohrs)
        self.add_widget(unitcell_label)
        self.add_widget(self.unitcell)
        self.add_widget(run)
    

    def run_program(self,obj):

        tensor_list = [self.sigma_x.text, 
                       self.sigma_y.text, 
                       self.sigma_z.text, 
                       self.tau_yx.text, 
                       self.tau_zx.text,
                       self.tau_zy.text]

        value = InputManager.input_filter(tensor_list)

        if value:
          
            tensor = [[float(self.sigma_x.text), float(self.tau_yx.text), float(self.tau_zx.text)],
                    [float(self.tau_yx.text), float(self.sigma_y.text), float(self.tau_zy.text)],
                    [float(self.tau_zx.text), float(self.tau_zy.text), float(self.sigma_z.text)]]

            if self.unitcell.active:

                cell = UnitCell(tensor)
                cell.show()

            if self.mohrs.active:

                circle = MohrsCircle(tensor)
                circle.plot_data()

            

class GabaritosApp(App):
    pass


GabaritosApp().run()