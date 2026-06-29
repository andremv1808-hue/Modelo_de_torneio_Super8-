from flask import Flask, render_template,request, url_for, redirect
from database import *
import random


app = Flask(__name__)


'''defs'''
def generate_rank():
    rank = []
    database = connect_db()
    cursor = database.cursor()
    
    temp = 3

    database.execute("UPDATE jogadores SET pontos = ?", (3,))

    database.execute("SELECT pontos FROM jogadores ")
    pontuacoes = cursor.fetchall()

    for ponto in pontuacoes:
        rank.append(ponto)

    rank.sort()

    rank_jogadores = []

    for ponto in rank:
        database.execute("SELECT nome FROM jogadores WHERE pontos (?)", (ponto,))
        jogador = cursor.fetchone()[0]
        rank_jogadores.append(jogador)

    return rank_jogadores 


'''routes'''
@app.route("/")
def reqplayers():
    return render_template("reqplayers.html")

@app.route("/sup8", methods = ["POST"])
def super8():
    init_db()
    database = connect_db()
    


    cursor = database.cursor()

    player = []
    
    for i in range(8):
        i = i+1
        x = "jogador"+str(i)
        nome = request.form[x]
        player.append(nome)

    random.shuffle(player)

    i = 0
    for players in player:
        i = i +1
        database.execute("INSERT INTO jogadores (id, nome) VALUES (?,?)", (str(i),players,))
        database.commit()

    rank = []
    
    cursor.execute("UPDATE jogadores SET pontos = ?", (3,))
    database.commit()

    database.execute("SELECT pontos FROM jogadores ")
    pontuacoes = cursor.fetchall()
    print(pontuacoes)

    for ponto in pontuacoes:
        rank.append(ponto)

    rank.sort()
    print(rank)

    rank_jogadores = []

    for ponto in rank:
        database.execute("SELECT nome FROM jogadores WHERE pontos (?)", (ponto,))
        jogador = cursor.fetchone()[0]
        rank_jogadores.append(jogador)



    return render_template("torneio.html", player=player, rank_jogadores = rank_jogadores)
 

@app.route("/encerrar", methods = ['GET'])
def func_button():
    database = connect_db()
    database.execute("DELETE FROM jogadores")
    database.commit()

    return redirect(url_for('reqplayers'))

@app.route("/refresh", methods = ['POST', 'GET'])
def button_refresh():
    rank = []
    database = connect_db()
    cursor = database.cursor()
    
    database.execute("INSERT INTO jogadores (pontos) VALUES (?)", (3,))

    database.execute("SELECT pontos FROM jogadores ")
    pontuacoes = cursor.fetchall()

    for ponto in pontuacoes:
        rank.append(ponto)

    rank.sort()

    rank_jogadores = []

    for ponto in rank:
        database.execute("SELECT nome FROM jogadores WHERE pontos (?)", (ponto,))
        jogador = cursor.fetchone()[0]
        rank_jogadores.append(jogador)

    return redirect(url_for('/sup8'), rank_jogadores = rank_jogadores)
    
'''init'''
if __name__ == ("__main__"):
    init_db()
    app.run(debug=True)
    