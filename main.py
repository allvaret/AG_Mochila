from populacao_inicial import limitacoes_individuos, gera_individuos
from troca import mutacao, crossover
from selecao import roleta_viciada, fitness, fitness_total


def main(debug=False):
    limitacoes, peso_limite, tamanho_populacao, taxa_mutacao = limitacoes_individuos()

    try:
        individuos = gera_individuos(tamanho_populacao, limitacoes, peso_limite)
    except ValueError as e:
        print(f"Erro na geração da população: {e}")
        return

    melhor_valor_antigo = 0
    contagem_s_melhora = 0
    limite_s_melhora = 3
    iteracao = 0

    while contagem_s_melhora < limite_s_melhora:
        if debug:
            print(f"\n{'='*40}")
            print(f"Geração {iteracao} | Sem melhora: {contagem_s_melhora}/{limite_s_melhora}")
            print(f"{'='*40}")
            for j, ind in enumerate(individuos):
                print(f"  Ind {j+1}: {ind.cromossomo} | Peso: {ind.peso_total} | Valor: {ind.valor_total} | Válido: {ind.valido}")

        melhor_valor, melhor_individuo = fitness(individuos)

        if melhor_valor > melhor_valor_antigo:
            melhor_valor_antigo = melhor_valor
            contagem_s_melhora = 0
            if debug:
                print(f"\n  [FITNESS] Nova melhora encontrada!")
        else:
            contagem_s_melhora += 1

        if debug:
            print(f"  [FITNESS] Melhor: {melhor_individuo.cromossomo} | Valor: {melhor_valor}")

        (pai, sorteio_pai, origem_pai), (mae, sorteio_mae, origem_mae) = roleta_viciada(individuos)

        if debug:
            print(f"\n  [ROLETA] Pai ({origem_pai}) — sorteio: {sorteio_pai:.3f} → {pai.cromossomo} | Valor: {pai.valor_total}")
            print(f"  [ROLETA] Mãe ({origem_mae})   — sorteio: {sorteio_mae:.3f} → {mae.cromossomo} | Valor: {mae.valor_total}")

        filho1, filho2 = crossover(pai, mae, limitacoes, peso_limite)

        if debug:
            print(f"\n  [CROSSOVER] {pai.cromossomo} x {mae.cromossomo}")
            print(f"  [CROSSOVER] Filho 1: {filho1.cromossomo} | Peso: {filho1.peso_total} | Valor: {filho1.valor_total}")
            print(f"  [CROSSOVER] Filho 2: {filho2.cromossomo} | Peso: {filho2.peso_total} | Valor: {filho2.valor_total}")

        houve, sorteio_mut, sorteio_ind, idx, gene, v_antigo, v_novo = mutacao([filho1, filho2], taxa_mutacao, limitacoes)

        if debug:
            print(f"\n  [MUTAÇÃO] Sorteio: {sorteio_mut:.3f} (taxa: {taxa_mutacao}) — ", end="")
            if houve:
                print(f"OCORREU | Ind selecionado: {idx+1} | Gene {gene}: {v_antigo} → {v_novo} (sorteio ind: {sorteio_ind:.3f})")
            else:
                print("não ocorreu")

        individuos = sorted(individuos, key=lambda ind: ind.valor_total, reverse=True)
        individuos[-1] = filho1
        individuos[-2] = filho2

        iteracao += 1

    print(f"\nConvergiu após {iteracao} gerações.")
    print(f"Melhor solução: {melhor_individuo.cromossomo} | Valor: {melhor_valor_antigo}")


if __name__ == '__main__':
    main(debug=True)
