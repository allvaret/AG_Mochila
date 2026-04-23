import random
from individuo import Individuo


def crossover(individuo1, individuo2):
    tamanho = len(individuo1.cromossomo)
    max_trocas = max(1, tamanho // 2)

    indices = list(range(tamanho))
    random.shuffle(indices)
    indices_trocados = set(indices[:random.randint(1, max_trocas)])

    filho1_cromossomo = []
    filho2_cromossomo = []
    trocados = []

    for i, (gene1, gene2) in enumerate(zip(individuo1.cromossomo, individuo2.cromossomo)):
        if i in indices_trocados:
            filho1_cromossomo.append(gene2)
            filho2_cromossomo.append(gene1)
            trocados.append(i)
        else:
            filho1_cromossomo.append(gene1)
            filho2_cromossomo.append(gene2)

    return filho1_cromossomo, filho2_cromossomo, trocados


def mutacao(individuos, taxa_mutacao, limitacoes):
    sorteio_mutacao = random.random()
    if sorteio_mutacao < taxa_mutacao:
        sorteio_individuo = random.random()
        for i, individuo in enumerate(individuos):
            if sorteio_individuo < (i + 1) / len(individuos):
                gene = random.randint(0, len(individuo.cromossomo) - 1)
                valor_antigo = individuo.cromossomo[gene]
                opcoes = [v for v in range(0, limitacoes[gene].qtd_item + 1) if v != valor_antigo]

                if opcoes:
                    individuo.cromossomo[gene] = random.choice(opcoes)

                return True, sorteio_mutacao, sorteio_individuo, i, gene, valor_antigo, individuo.cromossomo[gene]
    return False, sorteio_mutacao, None, None, None, None, None


def taxa_mutacao_dinamica(individuos, taxa_base):
    valores = [ind.valor_total for ind in individuos]
    if max(valores) == min(valores):
        return min(taxa_base * 5, 0.9)  # população homogênea — força mutação

    diversidade = (max(valores) - min(valores)) / max(valores)
    if diversidade < 0.05:  # menos de 5% de variação
        return min(taxa_base * 3, 0.7)

    return taxa_base

