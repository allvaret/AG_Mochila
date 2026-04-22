from cromossomo_tabela import Cromossomo_Tabela
from individuo import Individuo


def ler_inteiro(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")


def limitacoes_individuos():
    limitacoes = []
    nomes = ['Blusa', 'Calça', 'Sapato', 'Bolsa', 'Relógio', 'Cinto', 'Chapéu', 'Óculos', 'Jaqueta', 'Meia']

    n_ind = int(input(f"Quantos itens deseja definir? (máximo {len(nomes)}): "))
    while n_ind < 1 or n_ind > len(nomes):
        n_ind = int(input(f"Quantos itens deseja definir? (máximo {len(nomes)}): "))
        

    for ind in range(n_ind):
        print(f"Insira as limitações do Cromossomo {nomes[ind]}:")
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

    print("Defina o critério de parada (gerações sem melhora): ")
    limite_s_melhora = ler_inteiro("Limite sem melhora: ")

    return limitacoes, peso_limite, tamanho_populacao, taxa_mutacao, limite_s_melhora


def gera_individuos(tamanho_populacao, limitacoes, peso_limite):
    individuos = []

    for _ in range(tamanho_populacao):
        individuo = Individuo.criar_valido(limitacoes, peso_limite)
        individuos.append(individuo)
    return individuos


# if __name__ == "__main__":
#     limitacao = limitacoes_individuos()
#     print(gera_individuos(limitacao[2], limitacao[0]))