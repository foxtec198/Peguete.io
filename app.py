from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager 
from kivy.lang import Builder

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
class Main(MDScreen): ...
class FrontEnd(MDApp):
    def build(self):
        Builder.load_file('src/style.kv')
        self.title = 'Peguete.io'
        self.icon = 'src/logo.png'
        th = self.theme_cls
        th.theme_style = 'Dark'
        th.primary_palette = 'Indigo'
        sm = MDScreenManager()
        sm.add_widget(Login())
        sm.add_widget(Cad())
        sm.add_widget(Main())
        return sm

    def change_screen(self, c: str, t = 'right'):
        self.root.transition.direction = t
        self.root.current = c

    def login(self, email, pwd):
        toast("Logado")
        self.change_screen('main')

if __name__ == '__main__':
    FrontEnd().run()
