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
        with open('data_input.json', mode='r') as json_file:
            self.db_json = json.load(json_file)
        
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
        
        self.material_label = Label(text='Material = ')
        self.calc_temp_label = Label(text='Calculated temperature = ')
        self.strenght_at_calc_temp_label = Label(text='Strenght at calculated temp = ')
        self.set_solution_lavel_display_values(self.material_label)
        self.set_solution_lavel_display_values(self.calc_temp_label)
        self.set_solution_lavel_display_values(self.strenght_at_calc_temp_label)
        
        self.btn_calculate.bind(on_press=self.calculate_solution)
        
        
        self.add_widget(self.btn_calculate)
        self.add_widget(self.value_label)
        
        self.print_solution()
        
        
    def print_solution(self):
        self.add_widget(self.od_label)
        self.add_widget(self.wall_label)
        self.add_widget(self.id_label)
        self.add_widget(self.wall_area_label)
        self.add_widget(self.material_label)
        self.add_widget(self.calc_temp_label)
        self.add_widget(self.strenght_at_calc_temp_label)
                


    def calculate_solution(self, instance):
        dn = self.select_params.dn_input.text
        sch = self.select_params.sch_input.text
        material = self.select_params.material_input.text
        calc_temp = self.select_params.calc_temp_input.text
        
        if not self.validate_inputs(dn, sch, material, calc_temp):
            return None
        
        calc_temp = int(calc_temp)
        strenght_at_temp = self.aproximate_strenght_at_calc_temp(material, calc_temp)
        
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
        self.material_label.text = f'Material = {material}'
        self.calc_temp_label.text = f'Calculated temperature = {calc_temp}'
        self.strenght_at_calc_temp_label.text = f'Strenght at calculated temp = {self.aproximate_strenght_at_calc_temp(material, calc_temp)}'


    # Validation main function
    def validate_inputs(self, dn, sch, material, calc_temp) -> bool:
        if not self.validate_dn_input(dn):
            self.value_label.text = 'Select DN and press Calculate button again.'
            return False
        if not self.validate_material_input(material):
            self.value_label.text = 'Select Material and press Calculate button again.'
            return False
        
        if not self.validate_calc_temp_input(material, calc_temp):
            self.value_label.text = 'Type value for Calculation temperature field and press Calculate button again.'
            return False
        
        return True
        
    # Validation sub-functions
    def validate_dn_input(self, dn) -> bool:
        if dn not in self.db_json['dn'].keys():
            return False
        return True
    
    def validate_material_input(self, material) -> bool:
        if material not in self.db_json['strenght_at_temp'].keys():
            return False
        return True
    
    def validate_calc_temp_input(self, material, calc_temp) -> bool:
        # validate empty field
        if self.select_params.calc_temp_input.text == '':
            self.value_label.text = 'Type value for Calculation temperature field and press Calculate button again.'
            return False
        
        #validate calc_temp is in temp range of the DB
        material_dict = self.db_json['strenght_at_temp'][material]
        material_list_temp_strenght = [[int(temp), strenght] for temp, strenght in material_dict.items()]
        # print(f'{material_dict = }')
        # print(f'{material_list_temp_strenght = }')
        lowest_temp = 0
        highest_temp = 0
        for temp, strenght in material_list_temp_strenght:
            if not lowest_temp and strenght > 0:
                lowest_temp = temp
            if lowest_temp and strenght == 0:
                break
            highest_temp = temp
        print(f'{lowest_temp = }')
        print(f'{highest_temp = }')
        if lowest_temp <= int(calc_temp) <= highest_temp:
            return True
        self.value_label.text = f'Calculation temperature out of range of {lowest_temp} ~ {highest_temp}'
        return False
    ###################################
    
    def set_solution_lavel_display_values(self, widget:Widget) -> None:
        widget.size_hint_y = 0.5
    
    def aproximate_strenght_at_calc_temp(self, material, calc_temp) -> int:
        material_dict = self.db_json['strenght_at_temp'][material]
        # material_list_temp_strenght = [[int(temp), strenght] for temp, strenght in material_dict.items()]
        # lower_temp = 0
        # higher_temp = 0
        # for i, temp in enumerate(material_temps):
        #     if calc_temp < temp:
        #         # print(f'{i = }, {temp = }, {material_temps[i-1] = }')
        #         lower_temp = material_temps[i-1]
        #         higher_temp = temp
        #         break
        
        # strenght_lower_temp = material_dict[f'{lower_temp}']
        # strenght_higher_temp = material_dict[f'{higher_temp}']
        # # print(f'{strenght_lower_temp = }')
        # # print(f'{strenght_higher_temp = }')
        
        # for t in material_temps[::-1]:
        #     if not material_dict[f'{t}'] > 0:
        #         max_material_temp = t
        #         break
        # if material_temps[0] <= calc_temp <= max_material_temp:
        #     self.value_label.text = f'Calculation out of temp range, for {material} try temp between {material_temps[0]} ~ {max_material_temp}'
        
        lower_temp = int(list(material_dict.keys())[0])
        strenght_lower_temp = list(material_dict.values())[0]
        for temp, strenght in material_dict.items():
            temp = int(temp)
            if calc_temp < temp:
                higher_temp = temp
                strenght_higher_temp = strenght
                break
            lower_temp = temp
            strenght_lower_temp = strenght
        
        temp_ratio = (calc_temp-lower_temp)/(higher_temp-lower_temp)
        strenght_delta = strenght_lower_temp - strenght_higher_temp
        
        return strenght_lower_temp - strenght_delta * temp_ratio


class SelectParameters(GridLayout):
    def __init__(self, db_json, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        
        
        ### DN ###
        self.dn_label = Label(text = 'DN')
        self.add_widget(self.dn_label)
        # DN_LIST = [8, 10, 15, 20, 25, 32, 40, 50]
        DN_LIST = db_json['dn'].keys()
        self.dn_input, self.dn_input_dropdown = self.create_dropdown_button(DN_LIST, 'select DN')
        self.add_widget(self.dn_input)
        
        ### SCH ###
        self.sch_label = Label(text = 'SCH')
        self.add_widget(self.sch_label)
        # SCH_LIST = [8, 10, 16, 25, 40, 60]
        SCH_LIST = db_json['SCH']
        self.sch_input, self.sch_input_dropdown = self.create_dropdown_button(SCH_LIST, 'select SCH')
        self.add_widget(self.sch_input)
        
        ### Material ###
        self.material_label = Label(text = 'Material')
        self.add_widget(self.material_label)
        MATERIALS = db_json['strenght_at_temp'].keys()
        self.material_input, self.material_input_dropdown = self.create_dropdown_button(MATERIALS, 'select material')
        self.add_widget(self.material_input)
        
        ### Calculation Temperature ###
        self.calc_temp_label = Label(text = 'Calculation temperature')
        self.add_widget(self.calc_temp_label)
        self.calc_temp_input = TextInput(hint_text='type only INT value', input_filter='int', multiline=False, halign='center')
        self.add_widget(self.calc_temp_input)
        # CALC_TEMPS = db_json['strenght_at_temp']['P195GH'].values()
        # self.calc_temp_input, self.calc_temp_input_dropdown = self.create_dropdown_button(CALC_TEMPS, 'select calc_temp')
        # self.add_widget(self.calc_temp_input)
        
        
        ### calculater value ###
        # self.add_widget(Label(text='Calculated value is:'))
        # self.add_widget(Label(text=f'DN{self.dn_input.text} PN{self.pn_input.text}'))
    
    
    
    def create_dropdown_button(self, list_of_choise: list, btn_text:str) -> tuple[Button, DropDown]:
        main_btn = Button(text=btn_text)
        dropdown_btn = DropDown()
        for choise in list_of_choise:
            btn = Button(text=str(choise), size_hint=(None, None), size=(dp(120), dp(22)))
            btn.bind(on_release=lambda btn: dropdown_btn.select(btn.text))
            dropdown_btn.add_widget(btn)
        main_btn.bind(on_release=dropdown_btn.open)
        dropdown_btn.bind(on_select=lambda instance, x: setattr(main_btn, 'text', x))
        return (main_btn, dropdown_btn)
        
            