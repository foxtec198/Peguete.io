from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder

class Cad(MDScreen): ...

class HotReload(MDApp):
    KV_FILES = ['src/style.kv']
    DEBUG = True
    def build_app(self):
        Builder.load_file('src/style.kv')
        self.theme_cls.theme_style = 'Dark'
        sm = MDScreenManager()
        sm.add_widget(Cad())
        return sm

if __name__=='__main__':
    HotReload().run()