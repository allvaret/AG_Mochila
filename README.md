# Algoritmo Genético — Problema da Mochila

Implementação de um Algoritmo Genético (AG) para resolver o problema da mochila, onde o objetivo é maximizar o valor total dos itens carregados sem ultrapassar um peso limite.

---

## Estrutura de arquivos

```
├── cromossomo_tabela.py   # Definição dos itens (dataclass)
├── individuo.py           # Classe que representa um indivíduo da população
├── populacao_inicial.py   # Geração da população e leitura de inputs
├── selecao.py             # Fitness e seleção por roleta
├── troca.py               # Crossover e mutação
└── main.py                # Orquestração do AG
```

---

## Como executar

### Modo interativo

No `main.py`, defina:

```python
MODO_TESTE = False
```

Execute:

```bash
python main.py
```

O programa solicitará os dados de cada item (peso, valor, quantidade limite), além das configurações do AG (peso limite da mochila, tamanho da população, taxa de mutação e critério de parada).

### Modo teste

Para rodar sem inputs manuais, defina:

```python
MODO_TESTE = True
```

Os valores pré-configurados em `limitacoes_teste()` serão usados automaticamente.

### Debug

Para visualizar todo o fluxo do AG geração a geração:

```python
main(debug=True)
```

Com debug ativo, cada geração exibe a população atual, o melhor indivíduo encontrado, os pais selecionados pela roleta, os genes trocados no crossover (marcados com `[ ]`) e se houve mutação.

---

## Configurações

### Itens disponíveis

O sistema suporta até 10 itens com nomes pré-definidos:

```
Blusa, Calça, Sapato, Bolsa, Relógio, Cinto, Chapéu, Óculos, Jaqueta, Meia
```

Para adicionar mais itens ou alterar os nomes, edite a lista `nomes` em `limitacoes_individuos()` dentro de `populacao_inicial.py`.

### Parâmetros do AG

| Parâmetro | Descrição |
|---|---|
| Peso limite | Capacidade máxima da mochila |
| Tamanho da população | Número de indivíduos por geração |
| Taxa de mutação | Probabilidade de mutação (0.0 a 1.0) |
| Critério de parada | Número de gerações consecutivas sem melhora |

---

## Funcionamento do algoritmo

### 1. Representação

Cada **indivíduo** é representado por um cromossomo — uma lista de inteiros onde cada posição corresponde à quantidade de um item na mochila:

```
cromossomo = [3, 1, 2, 0, 4, ...]
              ↑   ↑   ↑   ↑   ↑
            Blusa Calça Sapato Bolsa Relógio ...
```

### 2. População inicial

Indivíduos são gerados aleatoriamente respeitando a quantidade limite de cada item. Caso um indivíduo ultrapasse o peso limite, o método `reparar()` reduz genes aleatoriamente (um de cada vez) até que o peso seja válido.

### 3. Fitness

A função de fitness avalia cada indivíduo pelo seu **valor total**:

```
valor_total = Σ (quantidade[i] × valor_item[i])
```

Indivíduos com maior valor total têm maior aptidão.

### 4. Seleção — roleta viciada

A seleção usa uma **roleta proporcional ao fitness** dividida em dois grupos (melhores e piores, metades da população). Com 50% de chance, o pai vem dos melhores e a mãe dos piores, ou vice-versa. Isso equilibra **explotação** (aproveitar bons genes) e **exploração** (manter diversidade).

### 5. Crossover uniforme

Cada gene é decidido **independentemente** com 50% de chance de troca entre pai e mãe. Isso permite qualquer combinação dos genes dos pais, inclusive trocar um único gene isolado.

Filhos inválidos (que ultrapassam o peso limite) são **descartados** — a população não é alterada para aquele slot. Essa abordagem respeita a pressão seletiva natural do AG sem interferência manual.

### 6. Mutação

A mutação ocorre com probabilidade igual à taxa de mutação definida. Quando ocorre, um indivíduo é sorteado (com probabilidade uniforme entre os filhos) e um gene aleatório recebe um novo valor dentro do limite permitido para aquele item.

### 7. Substituição

Os dois piores indivíduos da população são substituídos pelos filhos gerados, **somente se estes forem válidos**.

### 8. Critério de parada

O AG para quando a população fica um número definido de gerações consecutivas sem encontrar um valor total melhor do que o atual.

---

## Módulos

### `cromossomo_tabela.py`

Define a estrutura de dados de cada item:

```python
@dataclass
class Cromossomo_Tabela:
    nome_item: str    # Nome do item
    peso_item: int    # Peso unitário
    valor_item: int   # Valor unitário
    qtd_item: int     # Quantidade máxima permitida
```

### `individuo.py`

Representa um indivíduo da população. Calcula automaticamente peso total, valor total e validade ao ser instanciado.

Métodos:
- `_validar()` — verifica se o peso total não ultrapassa o limite
- `reparar()` — reduz genes aleatórios até o indivíduo se tornar válido (usado apenas na geração inicial)
- `criar_valido()` — factory method que gera cromossomos aleatórios até encontrar um válido

### `populacao_inicial.py`

- `ler_inteiro(mensagem)` — leitura segura de inteiros com tratamento de erro
- `limitacoes_individuos()` — coleta todos os parâmetros do usuário via input
- `gera_individuos(tamanho, limitacoes, peso_limite)` — cria a população inicial

### `selecao.py`

- `fitness(individuos)` — retorna o maior valor encontrado e o melhor indivíduo
- `fitness_total(individuos)` — soma os valores de toda a população (base da roleta)
- `selecao_roleta(individuos)` — sorteia um indivíduo proporcional ao fitness; retorna o indivíduo e o número sorteado
- `roleta_viciada(individuos)` — divide a população em melhores e piores e sorteia um pai e uma mãe; retorna indivíduo, sorteio e origem de cada um

### `troca.py`

- `crossover(individuo1, individuo2)` — crossover uniforme; retorna dois cromossomos filhos e a lista de posições trocadas
- `mutacao(individuos, taxa_mutacao, limitacoes)` — aplica mutação com base na taxa; retorna informações detalhadas para debug

### `main.py`

- `imprimir_tabela_itens(...)` — imprime os dados de entrada formatados antes do AG iniciar
- `limitacoes_teste()` — retorna configuração fixa para testes sem input manual
- `main(debug)` — orquestra todo o AG; alterne `debug=True/False` e `MODO_TESTE=True/False` conforme necessário

---

## Exemplo de saída com debug

```
Geração 3 | Sem melhora: 1/10
========================================
  Ind 1: [3, 1, 2, 2, 4, 5, 3, 2, 1, 3] | Peso: 58 | Valor: 3720
  Ind 2: [2, 0, 1, 3, 2, 4, 2, 3, 1, 5] | Peso: 55 | Valor: 3490
  ...

  [FITNESS] Melhor: [3, 1, 2, 2, 4, 5, 3, 2, 1, 3] | Valor: 3720
  [ROLETA] Pai (melhores) — sorteio: 0.412 → [3, 1, 2, 2, 4, 5, 3, 2, 1, 3] | Valor: 3720
  [ROLETA] Mãe (piores)   — sorteio: 0.731 → [2, 0, 1, 3, 2, 4, 2, 3, 1, 5] | Valor: 3490

  [CROSSOVER] genes trocados: posições [1, 4, 7]
  Pai:      3 [1] 2  2 [4] 5  3 [2] 1  3
  Mãe:      2 [0] 1  3 [2] 4  2 [3] 1  5
  Filho 1:  3 [0] 2  2 [2] 5  3 [3] 1  3  | Peso: 55 | Valor: 3380 | ✓ válido
  Filho 2:  2 [1] 1  3 [4] 4  2 [2] 1  5  | Peso: 57 | Valor: 3490 | ✓ válido

  [MUTAÇÃO] Sorteio: 0.087 (taxa: 0.1) — OCORREU | Ind 1 | Gene 5: 5 → 3
```

---

## Adaptando para outros problemas

O código suporta qualquer quantidade de itens (até o limite da lista `nomes`). Para adaptar a outros cenários:

- Altere os itens em `limitacoes_teste()` para testes rápidos
- Ajuste `peso_limite`, `tamanho_populacao` e `taxa_mutacao` conforme a complexidade do problema
- Para problemas com restrições diferentes do peso, a lógica de validação está centralizada em `Individuo._validar()` e pode ser estendida sem impactar o restante do código
