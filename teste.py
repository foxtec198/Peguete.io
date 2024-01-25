import requests, json

api_key = "AIzaSyB6s6PXZD_K30qfLiMwQn7q7eVWHgQK4OU"

def raiseError(rq):
    try: return rq['error']['message']
    except KeyError: return True

def singIn(email, pwd):
    link = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={api_key}"
    data = json.dumps({"email": email, "password": pwd, "returnSecureToken": True})
    resp = requests.post(link, data=data)
    a = raiseError(resp.json())
    print(a)

def createUser(email, pwd):
    link = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={api_key}"
    data = json.dumps({"email": email, "password": pwd, "returnSecureToken": True})
    request_object = requests.post(link, data=data)

singIn("foxtec198@gmail.com","84584609")