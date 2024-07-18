import json
import math

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget




class PressureCalculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        
        ### Load data from json file
        with open('data_input.json', mode='r') as jj:
            self.db_json = json.load(jj)
        
        self.select_params = SelectParameters(self.db_json)
        ### for now size_hint is not needed
        # self.select_params.size_hint_y = 1
        self.add_widget(self.select_params)
        
        
        self.btn_calculate = Button(text='Calculate')
        self.btn_calculate.size_hint = (0.8, 0.6)
        self.btn_calculate.background_color = (0.3, 0.8, 0.3, 1)
        self.btn_calculate.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.value_label = Label(text='Press Calculate button to get solution')
        self.set_solution_lavel_display_values(self.value_label)
        
        ### solution labels, will be updated after calculation
        self.od_label = Label(text='OD = ')
        self.wall_label = Label(text='Wall = ')
        self.id_label = Label(text='ID = ')
        self.wall_area_label = Label(text='Wall Area = ')
        self.set_solution_lavel_display_values(self.od_label)
        self.set_solution_lavel_display_values(self.wall_label)
        self.set_solution_lavel_display_values(self.id_label)
        self.set_solution_lavel_display_values(self.wall_area_label)
        
        self.btn_calculate.bind(on_press=self.calculate_solution)
        
        
        self.add_widget(self.btn_calculate)
        self.add_widget(self.value_label)
        
        self.add_widget(self.od_label)
        self.add_widget(self.wall_label)
        self.add_widget(self.id_label)
        self.add_widget(self.wall_area_label)
                


    def calculate_solution(self, instance):
        dn = self.select_params.dn_input.text
        sch = self.select_params.sch_input.text
        
        if dn not in self.db_json['dn'].keys():
            self.value_label.text = 'Select DN and press Calculate button again.'
            return None
        self.value_label.text = 'Press Calculate button to get solution'
        od = self.db_json['dn'][f'{dn}']['od']
        
        ## using index only as temp solution. this is not propper way
        ## to bind PN and wall thickness
        index = 0
        for i, db_sch in enumerate(self.db_json['SCH']):
            if sch == str(db_sch):
                index = i
        wall = self.db_json['dn'][f'{dn}']['walls'][index]
        id = od - 2*wall
        ### wall_area = PI (R + r) (R - r)
        R = od/2
        r = id/2
        wall_area = math.pi*(R+r)*(R-r)
        
        # solution = f'{od=}, {wall=}, id={id:.2f}, wall_area={wall_area:.2f}'
        
        self.od_label.text = f'OD => {od}'
        self.wall_label.text = f'Wall => {wall:.2f}'
        self.id_label.text = f'ID => {id:.2f}'
        self.wall_area_label.text = f'Wall Area => {wall_area:.2f}'

    def set_solution_lavel_display_values(self, widget:Widget) -> None:
        widget.size_hint_y = 0.5


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
        
        ### SCH ###
        self.sch_label = Label(text = 'PN')
        self.add_widget(self.sch_label)
        SCH_LIST = [8, 10, 16, 25, 40, 60]
        SCH_LIST = db_json['SCH']
        self.sch_input, self.pn_input_dropdown = self.create_dropdown_button(SCH_LIST, 'select SCH')
        self.add_widget(self.sch_input)
        
        
        ### calculater value ###
        # self.add_widget(Label(text='Calculated value is:'))
        # self.add_widget(Label(text=f'DN{self.dn_input.text} PN{self.pn_input.text}'))
    
    
    
    def create_dropdown_button(self, list_of_choise: list, btn_text:str) -> tuple[Button]:
        main_btn = Button(text=btn_text)
        dropdown_btn = DropDown()
        for choise in list_of_choise:
            btn = Button(text=str(choise), size_hint=(None, None), size=(dp(120), dp(22)))
            btn.bind(on_release=lambda btn: dropdown_btn.select(btn.text))
            dropdown_btn.add_widget(btn)
        main_btn.bind(on_release=dropdown_btn.open)
        dropdown_btn.bind(on_select=lambda instance, x: setattr(main_btn, 'text', x))
        return (main_btn, dropdown_btn)
        
            