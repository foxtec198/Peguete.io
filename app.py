from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager 
from kivy.lang import Builder
from kivymd.toast import toast
from sqlite3 import connect

class Cad(MDScreen): ...
class Main(MDScreen): ...
class Login(MDScreen): ...

class FrontEnd(MDApp):
    def build(self):
        self.back = BackEnd()
        Builder.load_file('src/style.kv')
        self.title = 'Peguete.io'
        self.icon = 'src/anim2.png'
        th = self.theme_cls
        th.theme_style = 'Dark'
        th.primary_palette = 'Indigo'
        sm = MDScreenManager()
        sm.add_widget(Cad())
        sm.add_widget(Login())
        sm.add_widget(Main())
        return sm

    def changeScreen(self, c: str, t = 'right'):
        self.root.transition.direction = t
        self.root.current = c

    def on_start(self):
        self.verify = self.back.conferLogin()
        if self.verify: self.root.current = 'main'
        elif not self.verify: self.root.current = 'cad'
        else: toast('Erro desconhecido!')

class BackEnd:
    def __init__(self):
        self.conn = connect('src/pegueteio.db')
        self.c = self.conn.cursor()
        self.configApk = {
            "apiKey" : "AIzaSyDkQygvt39s_XCg8sGJxgqm8-RKUUFtSSE",
            "authDomain" : "pegueteio.firebaseapp.com",
            "projectId" : "pegueteio",
            "storageBucket" : "pegueteio.appspot.com",
            "messagingSenderId" : "526589240672",
            "appId" : "1:526589240672:web:e5e001b78d90e940f6ea05",
            "measurementId" : "G-SE70RPGEJQ"
        }
    def conferLogin(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS Confer(Verify BOOLEAN)')
        self.conferVerify = self.c.execute('SELECT Verify from Confer').fetchone()
        if self.conferVerify is None: self.conferVerify = False
        return self.conferVerify
    
    def login(self, mail: str, pwd:str):
        ...

    def cadastro(self, mail: str, pwd:str):
        ...

if __name__ == '__main__':
    FrontEnd().run()
