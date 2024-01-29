from sqlite3 import connect
import pandas as pd
import plotly.io as pio
import plotly_express as px

class BackEnd():
    def __init__(self) -> None:
        self.conn = connect('src/pegueteio.db')
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS USERS(Id INTEGER PRIMARY KEY AUTOINCREMENT, NOME VARCHAR(100), EMAIL VARCHAR(100), PWD VARCHAR(100))')
        self.c.execute('CREATE TABLE IF NOT EXISTS CONFER(Id INTEGER PRIMARY KEY AUTOINCREMENT, LG BOOL)')
        self.c.execute('CREATE TABLE IF NOT EXISTS CASOS(Id INTEGER PRIMARY KEY AUTOINCREMENT, NOME TEXT, STATUS TEXT, DATA DATE, OBS TEXT)')

    def conferLogin(self):
        db = self.c.execute('select LG from CONFER ORDER BY Id DESC').fetchone()
        try:
            if db[0]: return True
        except:
            if db == None or db: return False

    def login(self, email, pwd):
        if email != '' and pwd != '':
            db = self.c.execute('select LG from CONFER ORDER BY Id DESC').fetchone()
            users = self.c.execute('SELECT EMAIL, PWD, NOME FROM USERS').fetchall()
            if users != None:
                for a in users:
                    self.email = a[0]
                    if self.email == email:
                        self.pwd = a[1]
                        if self.pwd == pwd:
                            self.nome = a[2]
                            if db == None: self.c.execute('INSERT INTO CONFER(LG) VALUES (True)')
                            elif db != None: self.c.execute('UPDATE CONFER SET LG = True')
                            self.conn.commit()
                            resposta = 'Sucesso'
                        else: resposta = 'Senha Incorreta'
                    else: resposta = 'Email não econtrado'
            try: return resposta
            except: return 'Nenhum cadastro no banco de dados'
        else: return 'Valores vazios'

    def cadastro(self, email, pwd, nome = ''):
        if email != '' and pwd != '':
            users = self.c.execute('SELECT EMAIL, PWD, NOME FROM USERS').fetchall()
            exist = False
            if users != None:
                for a in users:
                    self.email = a[0]
                    if self.email == email: exist = True

            if not exist:
                self.c.execute(f'INSERT INTO USERS(NOME,EMAIL,PWD) VALUES ("{nome}","{email}","{pwd}")')
                self.conn.commit()
                self.login(email, pwd)
                return 'Cadastrado com Sucesso'
            if exist: return 'Email ja cadastrados!'
        else: return 'Valores Vazios'

    def cons(self):
        return self.c.execute('select * from CONFER').fetchall()

    def lastLogin(self):
        users = self.c.execute('SELECT EMAIL, PWD, NOME FROM USERS ORDER BY Id DESC').fetchone()
        if users != None:
            self.email = users[0]
            self.pwd = users[1]
            self.nomeCompleto = users[2]
            self.nome = self.nomeCompleto.split()
            self.nome = self.nome[0]

    def addLove(self, nome: str, status, data: str, obs = None):
        self.c.execute(f'INSERT INTO CASOS(NOME, STATUS, DATA, OBS) VALUES("{nome}","{status}","{data}","{obs}")')
        self.conn.commit()
    
    def getDados(self):
        self. dados = self.c.execute('select nome, status, data, obs, id from CASOS order by Id DESC').fetchall()

    def organizarDados(self, dados):
        for i in dados:
            self.nomeLove = i[0]
            self.status = i[1]
            self.data = i[2]
            self.obs = i[3]
            break

    def criarGrafico(self): 
        self.getDados()
        if self.dados != None:
            df = []
            for i in self.dados:
                df.append([i[1].capitalize(), 1])

            pio.templates.default = 'plotly_dark'
            df= pd.DataFrame(df, columns=['Status','Quant'])
            pie = px.pie(df, values='Quant', names='Status')
            pie.update_traces(textfont_size=20)
            pie.update_legends(font_size=25)
            pie.write_image('src/plt.png')


if __name__ == '__main__':
    b = BackEnd()
    b.criarGrafico()
    # for i in range(10):
    #     b.addLove('teste','decepcionado','10/10/1010')
