from flask import Flask
import openpyxl
from flask import render_template

app = Flask(__name__)

from routes import *


wb = openpyxl.open('Pasta1.xlsx')
workbook = wb['Planilha1']



if __name__ == ("__main__"):
    app.run()




# while True:
#     p1 = workbook['B3'] = input("Primeiro Atleta:")
#     p2 = workbook['B4'] = input("Segundo Atleta:")
#     p3 = workbook['B5'] = input("Terceiro Atleta:")
#     p4 = workbook['B7'] = input("Quarto Atleta:")
#     p5 = workbook['B8'] = input("Quinto Atleta:")
#     p6 = workbook['B6'] = input("Sexto Atleta:")
#     p7 = workbook['B9'] = input("Sétimo Atleta:")
#     p8 = workbook['B10'] = input("Oitavo Atleta:")

#     acao = input ("\n \n \n \n [1] - Iniciar super 8 \n [2] - Nomear jogadores novamente \n\n\n\n")

#     if int(acao) == 2:
#         print("Digite os nomes novamente \n \n")

#     if int(acao) == 1:
#         print("Super 8 iniciado, gerando games...")
#         break
#         # printando os games
# print (f" jogo 1: {p6} e {p8} X {p7} e {p5}" )
# print (f" jogo 2: {p6} e {p2} X {p3} e {p5}" )
# print (f" jogo 3: {p1} e {p7} X {p2} e {p3}" )
# print (f" jogo 4: {p8} e {p4} X {p6} e {p5}" )
# print (f" jogo 5: {p1} e {p3} X {p8} e {p5}" )
# print (f" jogo 6: {p7} e {p2} X {p4} e {p6}" )
# print (f" jogo 7: {p1} e {p4} X {p6} e {p3}" )
# print (f" jogo 8: {p8} e {p7} X {p2} e {p5}" )
# print (f" jogo 9: {p1} e {p2} X {p8} e {p6}" ) 
# print (f" jogo 10: {p7} e {p3} X {p4} e {p5}" )
# print (f" jogo 11: {p1} e {p6} X {p7} e {p5}" )
# print (f" jogo 12: {p8} e {p2} X {p4} e {p3}" )
# print (f" jogo 13: {p8} e {p3} X {p7} e {p6}" )
# print (f" jogo 14: {p1} e {p5} X {p4} e {p2}" )
# wb.save(filename='Pasta1.xlsx')
