# test_simples.py
from random import randint
from cromossomo_tabela import Cromossomo_Tabela
from individuo import Individuo

def testar_tudo():
    limitacoes = [
        Cromossomo_Tabela("Blusa", 3, 100, 7),
        Cromossomo_Tabela("Calça", 6, 200, 2),
        Cromossomo_Tabela("Sapato", 4, 50, 5)
    ]
    
    # Teste 1: Gerar população
    tamanho = 5
    individuos = []
    for _ in range(tamanho):
        cromossomo = [randint(0, limitacoes[i].qtd_item) for i in range(len(limitacoes))]
        individuo = Individuo(cromossomo=cromossomo, limitacoes=limitacoes, peso_limite=100)
        individuos.append(individuo)
    
    # Asserts
    assert len(individuos) == tamanho, f"Deveria ter {tamanho} indivíduos"
    
    for individuo in individuos:
        assert isinstance(individuo, Individuo)
        if individuo.valido:
            print(f"✓ Indivíduo válido: {individuo.cromossomo}")
    
        else:
            print(f"✗ Indivíduo inválido: {individuo.cromossomo} (Peso: {individuo.peso_total}, Valor: {individuo.valor_total})")

            
if __name__ == "__main__":
    testar_tudo()