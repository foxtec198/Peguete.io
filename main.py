from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager 
from kivy.lang import Builder

class Cad(MDScreen): ...
class Main(MDScreen): ...
class Login(MDScreen): ...

class BackEnd(MDApp):
    def build(self):
        Builder.load_file('src/style.kv')
        sm = MDScreenManager()
        sm.add_widget(Cad())
        sm.add_widget(Login())
        sm.add_widget(Main())
        return sm
    
    def on_start(self):
        self.root.current = 'cad'

if __name__ == '__main__':
    BackEnd().run()