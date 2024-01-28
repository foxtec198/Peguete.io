from sqlite3 import connect

class BackEnd():
    def __init__(self) -> None:
        self.conn = connect('src/pegueteio.db')
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS USERS(Id INTEGER PRIMARY KEY AUTOINCREMENT, NOME VARCHAR(100), EMAIL VARCHAR(100), PWD VARCHAR(100))')
        self.c.execute('CREATE TABLE IF NOT EXISTS CONFER(Id INTEGER PRIMARY KEY AUTOINCREMENT, LG BOOL)')

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
        
if __name__ == '__main__':
    b = BackEnd()