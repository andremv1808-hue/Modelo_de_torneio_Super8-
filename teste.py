

def generate_rank(lista_pontos):
    rank = []
    for ponto in lista_pontos:
        rank.append(ponto)
    rank.sort()
    print (rank)


lista_pontos = []
for i in range (8):
    ponto = int(input("D: "))
    lista_pontos.append(ponto)

generate_rank(lista_pontos)