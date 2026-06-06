import sqlite3


def connect_db():
    database = sqlite3.connect("jogadores.db")
    return database

def init_db():

    database = connect_db()
    cursor = database.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS jogares (nome text)")
    database.commit()
    database.close()


