import requests, json

link = 'https://pegueteio-2e0a4-default-rtdb.firebaseio.com/users/.json'

users = requests.get(link, data=json.dumps({'email':'teste','password':'8458'})).json()
email = input('Email: ')
pwd = input('Senha: ')

for id in users:
    user = users[id]
    if email == user['email']:
        if pwd == user['password']:
            print('Logado')
