from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager 
from kivy.lang import Builder
from kivy.clock import Clock
from models.functions import *

# Toast
dialog = False
try: from kivymd.toast import toast
except: dialog = True

if dialog:
    from kivymd.uix.dialog import MDDialog
    def toast(msg):
        MDDialog(title = msg).open()

class Cad(MDScreen): ...
class Login(MDScreen): ...
class Main(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._on_enter_trig = trig = Clock.create_trigger(self._my_on_enter)
        self.bind(on_enter=trig)
        
    def _my_on_enter(self, *largs):
        newText = self.ids.lblStatus.text.replace('{NOME}', query("select name from config")[0])
        self.ids.lblStatus.text = newText
class FrontEnd(MDApp):
    def build(self):
        Builder.load_file('src/style.kv')
        self.title = 'Peguete.io'
        self.icon = 'src/logo.png'
        th = self.theme_cls
        th.theme_style = 'Dark'
        th.primary_palette = 'Indigo'
        self.sm = MDScreenManager()
        self.sm.add_widget(Login())
        self.sm.add_widget(Cad())
        self.sm.add_widget(Main())
        query("create table if not exists config(name varchar, email varchar)")
        return self.sm

    def change_screen(self, c: str, t = 'right'):
        self.sm.transition.direction = t
        self.sm.current = c

    def login(self, email, pwd):
        res = login(email, pwd)
        self.change_screen('main') if res[0] else toast(res[1]) 

    def singup(self, email, pwd, nome):
        res = singup(email, pwd, nome)
        if res[0]:
            self.change_screen('login') 
            toast("Realize login!")
        else: toast(res[1])

if __name__ == '__main__':
    FrontEnd().run()
