import random


def fitness(individuos):
    maior_valor = 0
    for individuo in individuos:
        if individuo.valor_total > maior_valor:
            maior_valor = individuo.valor_total
            melhor_individuo = individuo

    return maior_valor, melhor_individuo


def fitness_total(individuos):
    valor_total = sum(individuo.valor_total for individuo in individuos)
    return valor_total



def selecao_roleta(individuos):
    total_fitness = fitness_total(individuos)
    sorteio = random.random()

    probabilidade_roleta = 0
    for individuo in individuos:
        probabilidade_roleta += individuo.valor_total / total_fitness
        if sorteio <= probabilidade_roleta:
            return individuo, sorteio
    return individuos[-1], sorteio  # fallback


def roleta_viciada(individuos):
    populacao_ordenada = sorted(individuos, key=lambda ind: ind.valor_total, reverse=True)

    metade = len(populacao_ordenada) // 2
    melhores = populacao_ordenada[:metade]
    piores = populacao_ordenada[metade:]

    if random.random() < 0.5:
        pai, sorteio_pai = selecao_roleta(melhores)
        mae, sorteio_mae = selecao_roleta(piores)
        origem_pai, origem_mae = "melhores", "piores"

    else:
        pai, sorteio_pai = selecao_roleta(piores)
        mae, sorteio_mae = selecao_roleta(melhores)
        origem_pai, origem_mae = "piores", "melhores"

    return (pai, sorteio_pai, origem_pai), (mae, sorteio_mae, origem_mae)