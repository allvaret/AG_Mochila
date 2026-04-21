from cromossomo_tabela import Cromossomo_Tabela
from individuo import Individuo
from populacao_inicial import limitacoes_individuos, gera_individuos
from troca import mutacao, crossover
from selecao import roleta_viciada, fitness, fitness_total

 
def imprimir_tabela_itens(limitacoes, peso_limite, tamanho_populacao, taxa_mutacao):
    print("\n" + "="*55)
    print(f"  {'ITEM':<10} {'PESO':>8} {'VALOR':>8} {'QTD LIMITE':>12}")
    print("-"*55)
    for item in limitacoes:
        print(f"  {item.nome_item:<10} {item.peso_item:>8} {item.valor_item:>8} {item.qtd_item:>12}")
    print("="*55)
    print(f"  Peso limite:       {peso_limite}")
    print(f"  Tamanho população: {tamanho_populacao}")
    print(f"  Taxa de mutação:   {taxa_mutacao}")
    print("="*55 + "\n")


def limitacoes_teste():
    limitacoes = [
        Cromossomo_Tabela('Blusa',  3, 100, 7),
        Cromossomo_Tabela('Calça',  6, 200, 2),
        Cromossomo_Tabela('Sapato', 4,  50, 5),
        Cromossomo_Tabela('Bolsa',  5, 150, 3),
        Cromossomo_Tabela('Relógio', 2, 300, 4),
        Cromossomo_Tabela('Cinto',  1,  80, 6),
        Cromossomo_Tabela('Chapéu', 2, 120, 4),
        Cromossomo_Tabela('Óculos', 1, 250, 3),
        Cromossomo_Tabela('Jaqueta', 7, 400, 2),
        Cromossomo_Tabela('Meia',   1,  20, 10)
    ]
    peso_limite       = 100
    tamanho_populacao = 4
    taxa_mutacao      = 0.1
    limite_s_melhora  = 5

    return limitacoes, peso_limite, tamanho_populacao, taxa_mutacao, limite_s_melhora

MODO_TESTE = True


def main(debug=True):
    if MODO_TESTE:
        limitacoes, peso_limite, tamanho_populacao, taxa_mutacao, limite_s_melhora = limitacoes_teste()
    else:
        limitacoes, peso_limite, tamanho_populacao, taxa_mutacao, limite_s_melhora = limitacoes_individuos()
    
    imprimir_tabela_itens(limitacoes, peso_limite, tamanho_populacao, taxa_mutacao)

    try:
        individuos = gera_individuos(tamanho_populacao, limitacoes, peso_limite)
    except ValueError as e:
        print(f"Erro na geração da população: {e}")
        return

    melhor_valor_antigo = 0
    contagem_s_melhora = 0
    iteracao = 0

    while contagem_s_melhora < limite_s_melhora:
        if debug:
            print(f"\n{'='*40}")
            print(f"Geração {iteracao} | Sem melhora: {contagem_s_melhora}/{limite_s_melhora}")
            print(f"{'='*40}")
            for j, ind in enumerate(individuos):
                print(f"  Ind {j+1}: {ind.cromossomo} | Peso: {ind.peso_total} | Valor: {ind.valor_total}")

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

        f1_cromo, f2_cromo, trocados = crossover(pai, mae)
        filho1 = Individuo(f1_cromo, limitacoes, peso_limite)
        filho2 = Individuo(f2_cromo, limitacoes, peso_limite)

        if debug:
            pai_fmt = [f"[{g}]" if i in trocados else f" {g} " for i, g in enumerate(pai.cromossomo)]
            mae_fmt = [f"[{g}]" if i in trocados else f" {g} " for i, g in enumerate(mae.cromossomo)]
            f1_fmt  = [f"[{g}]" if i in trocados else f" {g} " for i, g in enumerate(filho1.cromossomo)]
            f2_fmt  = [f"[{g}]" if i in trocados else f" {g} " for i, g in enumerate(filho2.cromossomo)]

            print(f"\n  [CROSSOVER] genes trocados: posições {trocados}")
            print(f"  Pai:     {''.join(pai_fmt)}")
            print(f"  Mãe:     {''.join(mae_fmt)}\n")

            status1 = "✓ válido" if filho1.valido else "✗ descartado"
            status2 = "✓ válido" if filho2.valido else "✗ descartado"
            print(f"  Filho 1: {''.join(f1_fmt)} | Peso: {filho1.peso_total} | Valor: {filho1.valor_total} | {status1}")
            print(f"  Filho 2: {''.join(f2_fmt)} | Peso: {filho2.peso_total} | Valor: {filho2.valor_total} | {status2}")

        individuos = sorted(individuos, key=lambda ind: ind.valor_total, reverse=True)

        if filho1.valido:
            individuos[-1] = filho1
        if filho2.valido:
            individuos[-2] = filho2

            
        houve, sorteio_mut, sorteio_ind, idx, gene, v_antigo, v_novo = mutacao([filho1, filho2], taxa_mutacao, limitacoes)

        if debug:
            print(f"\n  [MUTAÇÃO] Sorteio: {sorteio_mut:.3f} (taxa: {taxa_mutacao}) — ", end="")
            if houve:
                print(f"OCORREU | Ind selecionado: {idx+1} | Gene {gene}: {v_antigo} → {v_novo} (sorteio ind: {sorteio_ind:.3f})") # type: ignore
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
