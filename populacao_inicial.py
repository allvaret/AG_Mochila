from random import randint
from cromossomo_tabela import Cromossomo_Tabela
from individuo import Individuo


def ler_inteiro(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")


def limitacoes_individuos(n_ind=3):
    limitacoes = []
    nomes = ['Blusa', 'Calça', 'Sapato']


    for ind in range(n_ind):
        print(f"Insira as limitações do individuo {ind}")
        limitacoes_peso = ler_inteiro("Definição de peso por item: ")
        limitacoes_valor = ler_inteiro("Definição de Valor: ")
        limitacoes_quantidade = ler_inteiro("Quantidade Limite: ")

        limitacoes.append(Cromossomo_Tabela(nome_item=nomes[ind], peso_item=(limitacoes_peso), valor_item=(limitacoes_valor), qtd_item=(limitacoes_quantidade)))

    print(f"Defina o peso limite que a mochila pode carregar: ")
    peso_limite = ler_inteiro("Peso limite: ")

    print("Defina o tamanho da população: ")
    tamanho_populacao = ler_inteiro("Tamanho da população: ")

    print("Defina a taxa de mutação: ")
    taxa_mutacao = float(input("Taxa de mutação (decimal, entre 0 e 1): "))

    return limitacoes, peso_limite, tamanho_populacao, taxa_mutacao


def gera_individuos(tamanho_populacao, limitacoes, peso_limite):
    individuos = []

    for ind in range(tamanho_populacao):
        cromossomo = [randint(0, limitacoes[i].qtd_item) for i in range(len(limitacoes))]
        individuo = Individuo(cromossomo=cromossomo, limitacoes=limitacoes, peso_limite=peso_limite)
        
        if individuo.valido == False:
            while individuo.valido == False:
                individuo = individuo.reparar()
        
        individuos.append(individuo)

    return individuos


# if __name__ == "__main__":
#     limitacao = limitacoes_individuos()
#     print(gera_individuos(limitacao[2], limitacao[0]))