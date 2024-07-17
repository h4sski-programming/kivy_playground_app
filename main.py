from kivy.app import App
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, OptionProperty
)
from kivy.clock import Clock
from kivy.vector import Vector
from hashlib import sha256

from pressurecalculator import PressureCalculator


class MenuScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        # self.size_hint = (1, None)
        # self.height = dp(60)
        
        btn_home = Button(text='Start', size_hint_x=4)
        btn_profile = Button(text='Restart')
        btn_exit = Button(text='Exit')
        self.add_widget(btn_home)
        self.add_widget(btn_profile)
        self.add_widget(btn_exit)


# class PlayerScreen(RelativeLayout):
#     def __init__(self, name:str, **kwargs):
#         super().__init__(**kwargs)
#         self.name = name
#         self.value = 0
        
        
#         class PlayerScore(BoxLayout):
#             def __init__(self, **kwargs):
#                 super().__init__(**kwargs)
#                 self.size_hint_y = None
#                 self.height = dp(80)
#                 self.b = Button(text='ttt')
#                 self.add_widget(Button(text='ttt'))
                
        
#         # self.value_layout = PlayerScore()
#         # self.value_layout.add_widget(Label(text=str(self.value), pos_hint={'x': 0.5, 'y': 0.9}))
#         # self.value_layout.add_widget(Button(text=str(self.value)))
#         self.add_widget(PlayerScore())
        
#         self.score = Label(text=str(name))
#         self.add_widget(self.score)
#         # self.add_widget(Button(text='Start')

        

class PongGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.orientation = 'horizontal'
        # player_left = PlayerScreen(name='left')
        # player_right = PlayerScreen(name='right')
        # self.add_widget(player_left)
        # self.add_widget(player_right)
        # self.add_widget(Button(text='left'))
        # self.add_widget(Button(text='right'))
        
        # testing part
        self.orientation = 'vertical'
        
        self.text_label = Label(
            text='Password codder',
            )
        self.add_widget(self.text_label)
        
        self.pass_input = TextInput(
            hint_text = 'Type here your password',
            halign = 'center',
            padding_y = (20,20),
            size_hint_y = None,
            size = (1, dp(60)),
            multiline = False,
            )
        self.add_widget(self.pass_input)
        
        self.codde_button = Button(
            text = 'Code your pass',
            size_hint_y = None,
            size = (1, dp(90)),
            on_press = self.hash_text,
            )
        self.add_widget(self.codde_button)
    
    
    def hash_text(self, widget):
        self.text_label.text = str(sha256(self.pass_input.text.encode('utf-8')).hexdigest())


class BallLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Button(text='left'))

class MainWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.orientation = 'vertical'
        
        menu = MenuScreen()
        menu.pos_hint = {'x': 0, 'top':1}
        menu.size_hint = (1, None)
        menu.height = dp(60)
        self.add_widget(menu)
        
        # ball = BallLayout()
        # self.assign_settings_main_screen(ball)
        # self.add_widget(ball)
        
        # game = PongGame()
        # self.assign_settings_main_screen(game)
        # self.add_widget(game)
        
        calculator = PressureCalculator()
        # self.assign_settings_main_screen(calculator)
        self.add_widget(calculator)
        
    
    def assign_settings_main_screen(self, widget:Widget):
        widget.size_hint = (0.7, 0.6)
        widget.pos_hint = {'center_x': 0.5, 'center_y': 0.45}


class FirstKivyApp(App):
    def build(self):
        return MainWidget()


if __name__ == '__main__':
    FirstKivyApp().run()
