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
    database = connect_db()
    for i in range(8):
        i = i+1
        x = "jogador"+str(i)
        nome = request.form[x]
        database.execute("INSERT INTO jogadores (nome) VALUES (?)", (nome,))
        database.commit()

    cursor = database.execute("SELECT * FROM jogadores")
    players_db = cursor.fetchall()
    player = []

    for players in players_db:
        player.append(players)

    random.shuffle(player)

    
    
    return render_template("torneio.html", player=player)
    
@app.route("/encerrar", methods = ['GET'])
def func_button():
    database = connect_db()
    database.execute("DELETE FROM jogadores")
    database.commit()

    return redirect(url_for('reqplayers'))

'''init'''
if __name__ == ("__main__"):
    init_db()
    app.run(debug=True)
    