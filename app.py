from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager 
from kivy.lang import Builder
from kivymd.toast import toast
from sqlite3 import connect
from random import randint
import email.message
import smtplib
import pyrebase as fb

class Cad(MDScreen): ...
class Main(MDScreen): ...
class Login(MDScreen): ...
class vEmail(MDScreen): ...

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
        sm.add_widget(vEmail())
        return sm

    def changeScreen(self, c: str, t = 'right'):
        self.root.transition.direction = t
        self.root.current = c

    def on_start(self):
        self.verify = self.back.conferLogin()

        if self.verify: self.root.current = 'main'
        elif not self.verify: self.root.current = 'cad'
        else: toast('Erro desconhecido!')

    def login(self, uid, pwd):
        try:
            b.login(uid, pwd)
            b.sendMail(uid)
            self.root.current = 'vEmail'
        except: toast('Verifique as credenciais!')

    def cad(self, uid, pwd, name): 
        try:
            b.cadastro(uid, pwd, name)
            b.sendMail(uid)
            self.root.current = 'vEmail'
        except: toast('Verifique as credenciais!')

    def verifyCodigo(self, cdg):
        if int(cdg) == int(b.codigoMail):
            self.root.current = 'main'
        else: toast('Código Incorreto')

class BackEnd:
    def __init__(self):
        self.conn = connect('src/pegueteio.db')
        self.c = self.conn.cursor()
        self.config = {"apiKey": "AIzaSyB6s6PXZD_K30qfLiMwQn7q7eVWHgQK4OU",
            "authDomain": "pegueteio-2e0a4.firebaseapp.com",
            "databaseURL": "https://databaseName.firebaseio.com",
            "storageBucket": "pegueteio-2e0a4.appspot.com",}
        self.firebase = fb.initialize_app(self.config)
        self.auth = self.firebase.auth()
    
    def conferLogin(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS Confer(Verify BOOLEAN)')
        self.conferVerify = self.c.execute('SELECT Verify from Confer').fetchone()
        if self.conferVerify is None: self.conferVerify = False
        return self.conferVerify
    
    def login(self, mail: str, pwd:str):
        self.user = self.auth.sign_in_with_email_and_password(mail, pwd)

    def cadastro(self, mail: str, pwd:str, name = ''):
        self.user = self.auth.create_user_with_email_and_password(mail, pwd)
        self.auth.update_profile(self.user['idToken'], name)

    def sendMail(self, mailTo):
        self.codigoMail = randint(100000, 999999)
        corpo = f'''
            <h1>Verificação de Email!</h1>
            <p><i> Não responda este email </i></p>
            <p>Segue seu código para verificar seu email </p>
            <p><b>{self.codigoMail} <b></p>
            <p>Se você não solicitou a verificação deste endereço, ignore este emai.</p>
            <p>Att pegueteio - tecnobreve.pegueteio@gmail.com</p>
        '''
        mail = 'tecnobreve.pegueteio@gmail.com'
        pwd = 'qpyb hdxx hiou wifp'
        msg = email.message.Message() 
        msg['Subject'] = 'Verificação de Email - Peguete.io'
        # msg['From'] = mail
        msg['To'] = mailTo
        msg.add_header('Content-type','text/html')
        msg.set_payload(corpo)
        
        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        s.login(mail, pwd)
        s.sendmail(mail, [msg['To']], msg.as_string().encode('utf-8'))
        
if __name__ == '__main__':
    b = BackEnd()
    FrontEnd().run()
