try: from kivymd.toast import toast
except: dialog = True

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager 
from kivy.lang import Builder
from sqlite3 import connect
from random import randint
import email.message, smtplib, requests, json

dialog = False

def raiseError(rq):
    try: return rq['error']['message']
    except KeyError: return rq

class Cad(MDScreen): ...
class Main(MDScreen): ...
class Login(MDScreen): ...
class vEmail(MDScreen): ...
class BackEnd:
    def __init__(self):
        self.conn = connect('src/pegueteio.db')
        self.c = self.conn.cursor()
        self.api = "AIzaSyB6s6PXZD_K30qfLiMwQn7q7eVWHgQK4OU"
    
    def conferLogin(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS Confer(Verify BOOLEAN)')
        self.conferVerify = self.c.execute('SELECT Verify from Confer').fetchone()
        if self.conferVerify is None: self.conferVerify = False
        return self.conferVerify
    
    def login(self, mail: str, pwd:str):
        link = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={self.api}"
        self.user = raiseError(requests.post(link, data=json.dumps({"email": mail, "password": pwd, "returnSecureToken": True})).json())
        
    def cadastro(self, mail: str, pwd:str, name = ''):
        link = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={self.api}"
        self.user = raiseError(requests.post(link, data=json.dumps({"email": mail, "password": pwd, "returnSecureToken": True})).json())
        try: self.updateUser(self.user['idToken'], name)
        except: ...

    def updateUser(self, id, display_name = None, photo_url = None, delete_attribute = None):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={self.api}"
        data = json.dumps({"idToken": id, "displayName": display_name, "photoURL": photo_url, "deleteAttribute": delete_attribute, "returnSecureToken": True})
        self.user = requests.post(link, data=data)
    
    def sendMail(self, mailTo):
        self.codigoMail = randint(100000, 999999)
        corpo = f'''
            <h1>Verificação de Email!</h1>
            <p><i> Não responda este email </i></p>
            <p>Segue seu código para verificar seu email </p>
            <p><b>{self.codigoMail} <b></p>
            <p>Se você não solicitou a verificação deste endereço, ignore este emai.</p>
            <p>Att pegueteio - tecnobreve.pegueteio@gmail.com</p> '''

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
        self.idsLogin = self.root.get_screen('login').ids
        self.idsCad = self.root.get_screen('cad').ids
        if self.verify: self.root.current = 'main'
        elif not self.verify: self.root.current = 'cad'

    def login(self, uid, pwd):
        # if uid != '' and pwd != '':
            # try:
            #     if self.back.user == 'INVALID_LOGIN_CREDENTIALS': toast('Credenciais Invalidas')
            #     elif self.back.user == 'USER_DISABLED': toast('Usuario Desabilitado!')
            #     else:
            #         try:
        self.back.login(uid, pwd)
        self.nome = self.back.user['displayName']
        self.root.current = 'vEmail'
        self.back.sendMail(uid)
        #             except: toast(f'Erro nas credencias')
        #     except: toast(f'Erro na requisição!')
        # else: toast('Preencha os dados acima!')

    def cad(self, uid, pwd, name): 
        if uid != '' and pwd != '':
            try:
                self.back.cadastro(uid, pwd, name)
                if self.back.user == 'EMAIL_EXISTS': toast('Email ja cadastrado, faça login!')
                else: 
                    try:
                        self.back.user['kind']
                        self.login(uid, pwd)
                    except: toast(f'{self.back.user}')
            except: toast(f'Credenciais Invalidas!')
        else: toast('Preencha os dados acima!')

    def verifyCodigo(self, cdg: int):
        if cdg == self.back.codigoMail:
            self.root.current = 'main'
        else: toast('Código Incorreto')
    
    
    
if __name__ == '__main__':
    FrontEnd().run()
