import re
from PopUpManager import PopUpManager

class InputManager():

    def input_filter(tensor_list):

        value = True

        for i, n in enumerate(tensor_list):
            tensor_list[i].strip("0")
            if n == '':
                tensor_list[i] = 0

        for element in tensor_list:
            try:
                float(element)
            except:
                PopUpManager.insert_numbers_only()
                value = False
                break

        return value