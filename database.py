import sqlite3




def connect_db():
    database = sqlite3.connect("database.db")
    return database

def init_db():

    database = connect_db()
    cursor = database.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS jogadores (id text,nome text, pontos integer, vitorias integer)")
    cursor.execute("CREATE TABLE IF NOT EXISTS partidas (id text, j1time1 text,j2time1 text, j1time2 text,j2time2 text, result_time1 integer, result_time2 interger, status text)")
    database.commit()


