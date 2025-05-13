from sqlite3 import connect
from requests import get, post

conn = connect('pegueteio.bd')
cursor = conn.cursor()

def cons(): ...
def query(): ...

def login(mat, pwd):
    ...