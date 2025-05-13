from kivymd.tools.hotreload.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.core.window import Window


# Toast
dialog = False
try: from kivymd.toast import toast
except: dialog = True

# if dialog:
#     from kivymd.uix.dialog import MDDialog
#     def toast(msg):
#         MDDialog(title = msg).open()

class Main(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._on_enter_trig = trig = Clock.create_trigger(self._my_on_enter)
        self.bind(on_enter=trig)
        
    def _my_on_enter(self, *largs):
        print(self.ids)
        self.ids.lblStatus.text = "TESTE"

class HotReload(MDApp):
    KV_FILES = ['src/style.kv']
    DEBUG = True


    def on_start(self):
        Window.size = 400, 600
        return super().on_start()
        
    def build_app(self):
        Builder.load_file('src/style.kv')

        self.title = 'Peguete.io'
        self.icon = 'src/logo.png'

        th = self.theme_cls
        th.theme_style = 'Dark'
        th.primary_palette = 'Indigo'

        self.sm = MDScreenManager()
        self.sm.adaptive_size = True
        self.sm.add_widget(Main(name='main'))
        
        return self.sm

HotReload().run()