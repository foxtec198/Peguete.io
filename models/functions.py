from sqlite3 import connect
from requests import get, post

# conn = connect('pegueteio.bd')
conn = connect(':memory:')
cursor = conn.cursor()

api_key = "AIzaSyBKRHgFh-S579TuwGpXNIuo5moZcp_p-Q0"
url = f"https://identitytoolkit.googleapis.com/v1/accounts:[action]?key={api_key}"
opt_login = 'signInWithPassword'
opt_singup = 'signUp'
opt_update = 'update'

def cons(sql, *args, all:bool=None):
    if len(args) == 1: args = args[0]
    txt = sql % args
    res = cursor.execute(txt)
    res = res.fetchall()
    if len(res) == 1 and not all: return list(res[0]) # Verifica se há somente um valor e o retorna apenas !
    else:
        # A resposta dos valores internos é uma tupla, e nao pode ser convertida para JSON
        # Por isso convertemos internamente para uma lista
        ls = []
        for item in res: ls.append(list(item))
        return ls

def query(sql, *args, commit=True):
    if len(args) == 1: args = args[0]
    txt = sql % args
    res = cursor.execute(txt)
    if commit: conn.commit()
    try:
        res = res.fetchall()
        if len(res) == 1: return list(res[0]) # Verifica se há somente um valor e o retorna apenas !
        else:
            # A resposta dos valores internos é uma tupla, e nao pode ser convertida para JSON
            # Por isso convertemos internamente para uma lista
            ls = []
            for item in res: ls.append(list(item))
            return ls
    except: return 'Sem retorno da Query!'

def change_opt(opt):
    return url.replace('[action]', opt)

def login(email, password):
    if email:
        if password:
            payload = {"email": email, "password": password, "returnSecureToken": True}
            response = post(change_opt(opt_login), json=payload)

            if response.status_code == 200:
                data = response.json()
                query("insert into config(name, email) values('%s', '%s')", (data['displayName'], data['email']))
                return [True, data]
            else: return [None, 'Confira as credenciais']
        else: return [None, 'Senha não preenchida!']
    else: return [None, 'Email não preenchido!']

def singup(email, pwd, name):
    if email:
        if pwd:
            if name:
                payload = {"email": email, "password": pwd, "displayName": name}
                response = post(change_opt(opt_singup), json=payload)
                if response.status_code == 200:
                    return [True, response.json()]
            return [False, 'Nome obrigatório!']
        return [False, 'Senha obrigatória!']
    return [False, 'Email obrigatório!']

if __name__ == '__main__':
    res = login('foxtec198@gmail.com','84584608')