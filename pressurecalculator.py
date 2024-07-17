import json

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput




class PressureCalculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        
        ### Load data from json file ###
        with open('data_input.json', mode='r') as jj:
            self.db_json = json.load(jj)
        
        self.select_params = SelectParameters(self.db_json)
        self.select_params.size_hint_y = 3
        self.add_widget(self.select_params)
        
        
        self.btn_calculate = Button(text='Calculate')
        self.value_label = Label(text='Press Calculate button to get solution')
        
        
        self.btn_calculate.bind(on_press=self.calculate_solution)
        
        
        self.add_widget(self.btn_calculate)
        self.add_widget(self.value_label)
        
                


    def calculate_solution(self, instance):
        dn = self.select_params.dn_input.text
        pn = self.select_params.pn_input.text
        od = self.db_json['dn'][f'{dn}']['od']
        index = 0
        
        # print(self.db_json['pn'])
        for i, db_pn in enumerate(self.db_json['pn']):
            
            if pn == str(db_pn):
                index = i
        wall = self.db_json['dn'][f'{dn}']['walls'][index]
        self.value_label.text = f'DN{dn} OD={od} and PN{pn}, wall={wall}'



class SelectParameters(GridLayout):
    def __init__(self, db_json, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        
            
        ### DN ###
        self.dn_label = Label(text = 'DN')
        self.add_widget(self.dn_label)
        DN_LIST = [8, 10, 15, 20, 25, 32, 40, 50]
        DN_LIST = db_json['dn'].keys()
        self.dn_input, self.dn_input_dropdown = self.create_dropdown_button(DN_LIST, 'select DN')
        self.add_widget(self.dn_input)
        
        ### PN ###
        self.pn_label = Label(text = 'PN')
        self.add_widget(self.pn_label)
        PN_LIST = [8, 10, 16, 25, 40, 60]
        PN_LIST = db_json['pn']
        self.pn_input, self.pn_input_dropdown = self.create_dropdown_button(PN_LIST, 'select PN')
        self.add_widget(self.pn_input)
        
        
        ### calculater value ###
        # self.add_widget(Label(text='Calculated value is:'))
        # self.add_widget(Label(text=f'DN{self.dn_input.text} PN{self.pn_input.text}'))
    
    
    
    def create_dropdown_button(self, list_of_choise: list, btn_text:str) -> tuple[Button]:
        main_btn = Button(text=btn_text)
        dropdown_btn = DropDown()
        for choise in list_of_choise:
            btn = Button(text=str(choise), size_hint=(None, None), size=(dp(120), dp(25)))
            btn.bind(on_release=lambda btn: dropdown_btn.select(btn.text))
            dropdown_btn.add_widget(btn)
        main_btn.bind(on_release=dropdown_btn.open)
        dropdown_btn.bind(on_select=lambda instance, x: setattr(main_btn, 'text', x))
        return (main_btn, dropdown_btn)
        
            