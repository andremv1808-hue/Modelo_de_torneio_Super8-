from flask import Flask, render_template,request, url_for, redirect
from database import *
import random


app = Flask(__name__)




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

    
    cursor.execute("UPDATE jogadores SET pontos = ?", (3,))
    database.commit()




    return render_template("torneio.html", player=player, rank_jogadores = None)
 

@app.route("/encerrar", methods = ['GET'])
def func_button():
    database = connect_db()
    database.execute("DELETE FROM jogadores")
    database.commit()

    return redirect(url_for('reqplayers'))

@app.route("/refresh", methods = ['POST', 'GET'])
def button_refresh():
    database = connect_db()
    cursor = database.cursor()

    rank_jogadores = []

    player = []

    cursor.execute("SELECT nome FROM jogadores")
    players_on_data = cursor.fetchall()

    for players in players_on_data:
        player.append(players[0])

    cursor.execute("SELECT pontos FROM jogadores ")
    pontuacoes = cursor.fetchall()

    

    for ponto in pontuacoes:
        rank_jogadores.append(ponto[0])

    rank_jogadores.sort() # ordenate the list from the smallest to the largest

    return render_template("torneio.html",rank_jogadores = rank_jogadores, player = player)
    
'''init'''
if __name__ == ("__main__"):
    init_db()
    app.run(debug=True)
    