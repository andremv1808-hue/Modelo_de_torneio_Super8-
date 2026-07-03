from flask import Flask, render_template,request, url_for, redirect
from database import *
import random


app = Flask(__name__)


'''defs'''
# def generate_rank(results_int:list,new_idden_ids:list, database = None):
#     if database is None:
#         database = connect_db()

#     cursor = database.cursor()  
    
#     for num in range(len(new_idden_ids)):
        
#         cursor.execute("SELECT pontos FROM jogadores WHERE nome IN (?,?)", (new_idden_ids[num][0],new_idden_ids[num][1]))

#         somar_com = cursor.fetchall()
#         print(somar_com)
#         for i in range(len(somar_com)):
#             database.execute("UPDATE jogadores SET pontos = ? WHERE nome IN (?,?)", (results_int[num] + somar_com[i], new_idden_ids[num][i]))

#         database.commit()

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

    database.execute("UPDATE jogadores SET pontos = ?", (0,))
    database.commit()
    
    cursor.execute("SELECT pontos FROM jogadores")
    rank_jogadores = cursor.fetchall()

    return render_template("torneio.html", player=player, rank_jogadores = rank_jogadores[0])
 


# BOTAO ENCERRAR SUP 8

@app.route("/encerrar", methods = ['GET'])
def func_button():
    database = connect_db()
    database.execute("DELETE FROM jogadores")
    database.commit()

    return redirect(url_for('reqplayers'))


# BOTAO ATUALIZAR RANKING

@app.route("/refresh", methods = ['POST', 'GET'])
def button_refresh():
    database = connect_db()
    cursor = database.cursor()

# RETORNANDO OS PLAYERS DO BANCO PARA QUE O HTML NAO PERCA ESTES DADOS 
    player = []
    cursor.execute("SELECT nome FROM jogadores")
    players_on_data = cursor.fetchall()
    for players in players_on_data:
        player.append(players[0])

# RECEBE OS RESULTADOS COMO LISTA [] E TRANSFORMA OS NUMEROS (String) EM (Inteiros) E AS STRING VAZIAS EM 0
    results = request.form.getlist('result')
    for i, resultado in enumerate(results):
        if resultado == '':
            results[i] = 0
        else:
            results[i] = int(resultado)

# RECEBE OS DOIS IDS (de cada jogador) DE CADA FORM NUMERICO EM FORMA DE LISTA []
    hidden_ids = request.form.getlist('hidden_input')
    novas_sublistas = []

    for i in range(0, 56, 2):
        par = [hidden_ids[i], hidden_ids[i+1]]
        novas_sublistas.append(par)

    hidden_ids = novas_sublistas

# RECEBE OS PONTOS NO BANCO DE DADOS EM FORMA DE LISTA []
    cursor.execute("SELECT pontos FROM jogadores")
    pontos_on_data = cursor.fetchall() #lista com os pontos em tuplas
    pontos_list = [] #lista com os pontos
    for ponto in pontos_on_data:
        pontos_list.append(int(ponto[0]))

# ATUALIZA O BANCO DE DADOS COM A SOMA DAS PONTUACOES
    for num in range(28):
        for i in range(2):
            cursor.execute("SELECT nome FROM jogadores WHERE nome IN (?,?)",(hidden_ids[num][0],hidden_ids[num][1]))
            nome = cursor.fetchall()
            cursor.execute("SELECT pontos FROM jogadores WHERE nome IN (?,?)",(hidden_ids[num][0],hidden_ids[num][1]))
            ponto = cursor.fetchall()

            database.execute("UPDATE jogadores SET pontos = ? WHERE nome = ?",(results[num] + int(ponto[i][0]), nome[i][0]))

        database.commit()

# COLOCA O RANK DO MAIOR PARA O MENOR
    rank_jogadores = []
    cursor.execute("SELECT pontos FROM jogadores")
    pontos_atualiazados_data = cursor.fetchall()
    for pontos in pontos_atualiazados_data:
        rank_jogadores.append(int(pontos[0]))

    rank_jogadores.sort() #ordena a lista do maior para o menor


    return render_template("torneio.html",rank_jogadores = rank_jogadores, player = player)
    
'''init'''
if __name__ == ("__main__"):
    init_db()
    app.run(debug=True)