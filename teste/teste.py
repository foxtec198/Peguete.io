from kivymd.app import MDApp
from kivy.lang import Builder

class Teste(MDApp):
    def builder(self):
        return Builder.load_file('teste.kv')

if __name__ == '__main__':
    Teste().run()