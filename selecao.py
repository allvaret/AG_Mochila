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
            return individuo