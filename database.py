import sqlite3


def connect_db():
    database = sqlite3.connect("jogadores.db")
    return database

def init_db():

    database = connect_db()
    cursor = database.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS jogadores (nome text, pontos integer, vitorias integer)")
    database.commit()
    database.close()


