import random
from individuo import Individuo


def crossover(individuo1, individuo2,limitacoes, peso_limite):
    filho1_cromossomo = []
    filho2_cromossomo = []
    
    for gene1, gene2 in zip(individuo1.cromossomo, individuo2.cromossomo):
        if random.random() < 0.5:
            filho1_cromossomo.append(gene1)
            filho2_cromossomo.append(gene2)
        else:
            filho1_cromossomo.append(gene2)
            filho2_cromossomo.append(gene1)

    filho1 = Individuo(cromossomo=filho1_cromossomo, limitacoes=limitacoes, peso_limite=peso_limite)
    filho2 = Individuo(cromossomo=filho2_cromossomo, limitacoes=limitacoes, peso_limite=peso_limite)
    
        
    if filho1.valido == False:
            filho1 = filho1.reparar()

    if filho2.valido == False:
            filho2 = filho2.reparar()

    return filho1, filho2


def mutacao(individuos, taxa_mutacao, limitacoes):
    if random.random() < taxa_mutacao:
        sorteio = random.random()
        for i, individuo in enumerate(individuos):
            if sorteio < (i + 1) / len(individuos):
                gene = random.randint(0, len(individuo.cromossomo) - 1)
                individuo.cromossomo[gene] = random.randint(0, limitacoes[gene].qtd_item)
                break

