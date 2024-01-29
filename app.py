try: 
    from kivymd.toast import toast
    dialog = False
except: dialog = True
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager 
from kivy.lang import Builder
from backend import BackEnd

if dialog:
    from kivymd.uix.dialog import MDDialog
    def toast(msg):
        MDDialog(title = msg).open()

class Cad(MDScreen): ...
class Login(MDScreen): ...
class Main(MDScreen): ...

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
        self.idsMain = self.root.get_screen('main').ids
        if self.verify: 
            self.back.lastLogin()
            self.root.current = 'main'
        elif not self.verify: self.root.current = 'cad'
        if self.root.current == 'main': self.atualizarStatus()

    def atualizarStatus(self, status = None):
        self.idsMain.lblStatus.text = f'Olá {self.back.nome}, seu status atual é {status}'

    def login(self, uid, pwd):
        res = self.back.login(uid, pwd)
        toast(res)
        if res == 'Sucesso':
            self.atualizarStatus()
            self.root.current = 'main'

    def cad(self, uid, pwd, name): 
        res = self.back.cadastro(uid, pwd, name)
        toast(res)
        if res == 'Cadastrado com Sucesso':
            self.atualizarStatus()
            self.root.current = 'main'

if __name__ == '__main__':
    FrontEnd().run()
