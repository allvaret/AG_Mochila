import random
from individuo import Individuo


def crossover(individuo1, individuo2):
    filho1_cromossomo = []
    filho2_cromossomo = []
    trocados = []

    for i, (gene1, gene2) in enumerate(zip(individuo1.cromossomo, individuo2.cromossomo)):
        if random.random() < 0.5:
            filho1_cromossomo.append(gene1)
            filho2_cromossomo.append(gene2)
        else:
            filho1_cromossomo.append(gene2)
            filho2_cromossomo.append(gene1)
            trocados.append(i)

    return filho1_cromossomo, filho2_cromossomo, trocados


def mutacao(individuos, taxa_mutacao, limitacoes):
    sorteio_mutacao = random.random()
    if sorteio_mutacao < taxa_mutacao:
        sorteio_individuo = random.random()
        for i, individuo in enumerate(individuos):
            if sorteio_individuo < (i + 1) / len(individuos):
                gene = random.randint(0, len(individuo.cromossomo) - 1)
                valor_antigo = individuo.cromossomo[gene]
                individuo.cromossomo[gene] = random.randint(0, limitacoes[gene].qtd_item)
                return True, sorteio_mutacao, sorteio_individuo, i, gene, valor_antigo, individuo.cromossomo[gene]
    return False, sorteio_mutacao, None, None, None, None, None