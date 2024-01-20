from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder

class Cad(MDScreen): ...
class Login(MDScreen): ...
class Main(MDScreen): ...
class vEmail(MDScreen): ...

class HotReload(MDApp):
    KV_FILES = ['src/style.kv']
    DEBUG = True
    def build_app(self):
        Builder.load_file('src/style.kv')
        self.theme_cls.theme_style = 'Dark'
        sm = MDScreenManager()
        sm.add_widget(Cad())
        sm.add_widget(vEmail())
        sm.add_widget(Login())
        sm.add_widget(Main())
        return sm

if __name__=='__main__':
    HotReload().run()