from flask import Flask, render_template,request, url_for, redirect
from database import *
import random


app = Flask(__name__)


'''routes'''
@app.route("/")
def reqplayers():
    database = connect_db()
    database.execute("DELETE FROM jogadores")
    database.execute("DELETE FROM partidas")
    database.commit()
    return render_template("reqplayers.html")

@app.route("/sup8", methods = ["POST"])
def super8():
    init_db()
    database = connect_db()
    cursor = database.cursor()
    just_to_fill = ["A definir","A definir","A definir","A definir","A definir","A definir","A definir","A definir"]
    just_to_fill2 = [0,0,0,0,0,0,0,0]
    just_to_fill3 = [0,0,0,0,0,0,0,0]
    results = [0,0,0,0,0,0,0,0]
    results_on_data = []
    status = ["False","False","False","False","False","False","False","False","False","False","False","False","False","False",]


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
    database.execute("UPDATE jogadores SET vitorias = ?", (0,))
    database.commit()
    
    cursor.execute("SELECT pontos FROM jogadores")
    rank_pontos = cursor.fetchall()

    return render_template("torneio.html", player=player, rank_pontos = just_to_fill3, rank_jogadores = just_to_fill, rank_vitorias = just_to_fill2, results_on_data = results_on_data, status = status)
 


# BOTAO ENCERRAR SUP 8

@app.route("/encerrar", methods = ['GET'])
def func_button():
    database = connect_db()
    database.execute("DELETE FROM jogadores")
    database.execute("DELETE FROM partidas")
    database.commit()

    return redirect(url_for('reqplayers'))


# BOTAO ATUALIZAR RANKING

@app.route("/refresh", methods = ['POST', 'GET'])
def button_refresh():
    database = connect_db()
    cursor = database.cursor()
# RETORNANDO OS PLAYERS DO BANCO DE DADOS PARA QUE O HTML NAO PERCA ESTES DADOS 
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

# AJUSTA A TABELA DE PARTIDAS COM NOMES APENAS UMA VEZ
    cursor.execute("SELECT EXISTS(SELECT 1 FROM partidas)")
    tem_data = cursor.fetchone()[0]
    if not tem_data:
        for i in range(0,28,2):
            cursor.execute("INSERT INTO partidas (id, j1time1, j2time1, j1time2, j2time2, result_time1, result_time2, status) VALUES (?,?,?,?,?,?,?,?)", (str(i//2 + 1),hidden_ids[i][0], hidden_ids[i][1], hidden_ids[i + 1][0], hidden_ids[i + 1][1], 0, 0, "False"))
    database.commit()


# ATUALIZA O BANCO DE DADOS COM A SOMA DA VITORIA DE CADA UM, SE FOR EMPATE NAO SOMA NADA
    
    for num in range(0,len(hidden_ids), 2):
        if results[num] == results[num+1]:
            continue
        elif results[num] > results[num+1]:
            cursor.execute("SELECT nome FROM jogadores WHERE nome IN (?,?)", (hidden_ids[num][0], hidden_ids[num][1]))
            nomes = cursor.fetchall()

            cursor.execute("SELECT vitorias FROM jogadores WHERE nome IN (?,?)", (hidden_ids[num][0], hidden_ids[num][1]))
            vitorias = cursor.fetchall()
            for i in range(2):
                database.execute("UPDATE jogadores SET vitorias = ? WHERE nome = ?", (1 + int(vitorias[i][0]), nomes[i][0]))
            database.commit()
        else:
            cursor.execute("SELECT nome FROM jogadores WHERE nome IN (?,?)", (hidden_ids[num + 1][0], hidden_ids[num + 1][1]))
            nomes = cursor.fetchall()

            cursor.execute("SELECT vitorias FROM jogadores WHERE nome IN (?,?)", (hidden_ids[num + 1][0], hidden_ids[num + 1][1]))
            vitorias = cursor.fetchall()

            for i in range(2):
                database.execute("UPDATE jogadores SET vitorias = ? WHERE nome = ?", (1 + int(vitorias[i][0]), nomes[i][0]))
            database.commit()



# RECEBE OS PONTOS NO BANCO DE DADOS EM FORMA DE LISTA []
    cursor.execute("SELECT pontos FROM jogadores")
    pontos_on_data = cursor.fetchall() #lista com os pontos em tuplas
    pontos_list = [] #lista com os pontos
    for ponto in pontos_on_data:
        pontos_list.append(int(ponto[0]))

# ATUALIZA O BANCO DE DADOS jogadores COM A SOMA DAS PONTUACOES
    for num in range(28):
        cursor.execute("SELECT nome FROM jogadores WHERE nome IN (?,?)",(hidden_ids[num][0],hidden_ids[num][1]))
        nome = cursor.fetchall()
        cursor.execute("SELECT pontos FROM jogadores WHERE nome IN (?,?)",(hidden_ids[num][0],hidden_ids[num][1]))
        ponto = cursor.fetchall()

        for i in range(2):
            database.execute("UPDATE jogadores SET pontos = ? WHERE nome = ?",(results[num] + int(ponto[i][0]), nome[i][0]))

        database.commit()

# ATUALIZA O BANDO DE DADOS partidas COM OS RESULTADOS e jogo acontecido
    for i in range (0,28,2):
        
        if results[i] or results[i+1] > 0:
            database.execute("UPDATE partidas SET status = ? WHERE id = ?", ("True", str(i//2 +1)))

        cursor.execute("SELECT result_time1, result_time2 FROM partidas WHERE id = ?", (str(i//2 + 1),))
        resultado_aux = cursor.fetchall()[0]
        if resultado_aux[0] == 0 and resultado_aux[1] == 0:
            database.execute("UPDATE partidas SET result_time1 = ? WHERE id = ?", (results[i], str(i//2 + 1)))
            database.execute("UPDATE partidas SET result_time2 = ? WHERE id = ?", (results[i+1], str(i//2 +1)))
            database.execute("UPDATE partidas SET result_time2 = ? WHERE id = ?", (results[i+1], str(i//2 +1)))
    database.commit()


# COLOCA O RANK DO MAIOR PARA O MENOR
    rank_pontos = []
    cursor.execute("SELECT pontos FROM jogadores")
    pontos_atualiazados_data = cursor.fetchall()
    for pontos in pontos_atualiazados_data:
        rank_pontos.append(int(pontos[0]))

    rank_pontos.sort() #ordena a lista do maior para o menor


# COLOCA O NOME DE CADA JOGADOR NO RANKING DE ACORDO COM O MAIOR PARA O MENOR
    rank_jogadores = []
    rank_vitorias = []
    cursor.execute("SELECT * FROM jogadores ORDER BY pontos DESC")
    dados_db  = cursor.fetchall()

    for i in range(len(dados_db)):
        rank_jogadores.append(dados_db[i][1])
        rank_vitorias.append(dados_db[i][3])
    
# RETORNA O STATUS DOS JOGOS
    cursor.execute("SELECT status FROM partidas")
    status_on_data = cursor.fetchall()
    status = []
    for texts in status_on_data:
        status.append(texts[0])

# RETORNA O RESULTADO DE CADA JOGO [[x,x]...]
    cursor.execute("SELECT result_time1, result_time2 FROM partidas")
    results_on_data = [list(linha) for linha in cursor.fetchall()]




    return render_template("torneio.html",rank_pontos = rank_pontos, player = player, rank_jogadores = rank_jogadores, rank_vitorias = rank_vitorias, status = status, results_on_data = results_on_data)
    







'''init'''
if __name__ == ("__main__"):
    init_db()
    app.run(debug=True)