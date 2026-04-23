# Algoritmo Genético — Problema da Mochila

Implementação de um Algoritmo Genético (AG) para resolver o problema da mochila, onde o objetivo é maximizar o valor total dos itens carregados sem ultrapassar um peso limite.

O projeto possui duas versões do orquestrador principal:

| Arquivo | Propósito |
|---|---|
| `main.py` | Versão acadêmica, taxa de mutação fixa definida em `limitacoes_teste()` |
| `main_teste.py` | Versão experimental — mutação adaptativa, importa `taxa_mutacao_dinamica` de `troca.py` |

---

## Estrutura de arquivos

```
├── cromossomo_tabela.py   # Definição dos itens (dataclass)
├── individuo.py           # Classe que representa um indivíduo da população
├── populacao_inicial.py   # Geração da população e leitura de inputs
├── selecao.py             # Fitness e seleção por roleta
├── troca.py               # Crossover, mutação e taxa dinâmica
├── main.py                # Orquestrador acadêmico
└── main_teste.py          # Orquestrador experimental
```

---

## Como executar

### Versão acadêmica (`main.py`)

No arquivo, defina:

```python
MODO_TESTE = False  # True para usar limitacoes_teste() sem input manual
```

Execute:

```bash
python main.py
```

O programa solicitará os dados de cada item (peso, valor, quantidade limite), além do peso limite da mochila, tamanho da população, taxa de mutação e critério de parada.

### Versão experimental (`main_teste.py`)

No arquivo, defina:

```python
MODO_TESTE = False  # True para usar limitacoes_teste() sem input manual
```

Execute:

```bash
python main_teste.py
```

Nesta versão a taxa de mutação **não é solicitada ao usuário** — ela é calculada automaticamente como `1 / tamanho do cromossomo` e ajustada dinamicamente a cada geração conforme o estado da população.

### Debug

Ambas as versões aceitam:

```python
main(debug=True)   # exibe fluxo completo geração a geração
main(debug=False)  # exibe apenas o resultado final
```

---

## Configurações

### Itens disponíveis

O sistema suporta até 10 itens com nomes pré-definidos:

```
Blusa, Calça, Sapato, Bolsa, Relógio, Cinto, Chapéu, Óculos, Jaqueta, Meia
```

Para adicionar mais itens ou alterar os nomes, edite a lista `nomes` em `limitacoes_individuos()` dentro de `populacao_inicial.py`.

### Parâmetros do AG

| Parâmetro | `main.py` | `main_teste.py` |
|---|---|---|
| Peso limite | Input do usuário | Input do usuário |
| Tamanho da população | Input do usuário | Input do usuário |
| Taxa de mutação | Input do usuário | Calculada automaticamente |
| Critério de parada | Input do usuário | Input do usuário |

---

## Funcionamento do algoritmo

### 1. Representação

Cada indivíduo é representado por um cromossomo — uma lista de inteiros onde cada posição corresponde à quantidade de um item na mochila:

```
cromossomo = [3, 1, 2, 0, 4, ...]
              ↑   ↑   ↑   ↑   ↑
            Blusa Calça Sapato Bolsa Relógio ...
```

### 2. População inicial

Indivíduos são gerados aleatoriamente respeitando a quantidade limite de cada item. Caso um indivíduo ultrapasse o peso limite, o método `criar_valido()` tenta criar novamente de maneira aleatoria até que o peso seja válido (Limite de 1000 tentativas, por segurança). Esse método é aplicado apenas na geração inicial — durante o AG, filhos inválidos são simplesmente descartados.

### 3. Fitness

A função de fitness avalia cada indivíduo pelo seu valor total:

```
valor_total = Σ (quantidade[i] × valor_item[i])
```

Indivíduos com maior valor total têm maior aptidão.

### 4. Seleção — roleta viciada

A seleção usa uma roleta proporcional ao fitness dividida em dois grupos (melhores e piores metades da população). O pai é sempre sorteado entre os melhores e a mãe entre os piores. Isso equilibra explotação (aproveitar bons genes) e exploração (manter diversidade).

### 5. Crossover com limite de trocas

O crossover embaralha os índices dos genes e sorteia quantos vão trocar, respeitando um limite proporcional ao tamanho do cromossomo:

| Tamanho do cromossomo | Máximo de trocas |
|---|---|
| 3 | 1 |
| 5 | 2 |
| 7 | 3 |
| 9 | 4 |
| 10 | 5 |

Regra geral: `max_trocas = tamanho // 2`, mínimo 1. Isso evita que os filhos sejam cópias integrais dos pais e mantém a herança genética gradual.

Filhos inválidos (que ultrapassam o peso limite) são descartados — a população não é alterada para aquele slot.

### 6. Mutação

Quando a mutação ocorre, o gene sorteado recebe obrigatoriamente um valor **diferente** do atual, garantindo que a mutação sempre introduza diversidade real.

**Versão acadêmica (`main.py`):** taxa fixa, definida pelo usuário ou em `limitacoes_teste()`.

**Versão experimental (`main_teste.py`):** taxa adaptativa calculada a cada geração com base no estado da população:

- **População homogênea** (todos com o mesmo valor): taxa aumenta até `taxa_base × 5`, limitada a 0.9
- **Baixa diversidade** (variação menor que 5%): taxa aumenta até `taxa_base × 3`, limitada a 0.7
- **População diversa**: taxa base é mantida (`1 / tamanho do cromossomo`)

### 7. Substituição

Os dois piores indivíduos da população são substituídos pelos filhos gerados, somente se estes forem válidos.

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
- `reparar()` — reduz genes aleatórios até o indivíduo se tornar válido 
- `criar_valido()` — factory method que gera cromossomos aleatórios até encontrar um válido (usado apenas na geração inicial)

### `populacao_inicial.py`

- `ler_inteiro(mensagem)` — leitura segura de inteiros com tratamento de erro
- `limitacoes_individuos()` — coleta os parâmetros do usuário via input
- `gera_individuos(tamanho, limitacoes, peso_limite)` — cria a população inicial

### `selecao.py`

- `fitness(individuos)` — retorna o maior valor encontrado e o melhor indivíduo
- `fitness_total(individuos)` — soma os valores de toda a população (base da roleta)
- `selecao_roleta(individuos)` — sorteia um indivíduo proporcional ao fitness; retorna o indivíduo e o número sorteado
- `roleta_viciada(individuos)` — pai sempre dos melhores, mãe sempre dos piores; retorna indivíduo, sorteio e origem de cada um

### `troca.py`

- `crossover(individuo1, individuo2)` — crossover com limite de trocas proporcional ao tamanho do cromossomo; retorna dois cromossomos filhos e a lista de posições trocadas
- `mutacao(individuos, taxa_mutacao, limitacoes)` — aplica mutação garantindo valor diferente do atual; retorna informações detalhadas para debug
- `taxa_mutacao_dinamica(individuos, taxa_base)` — usada apenas em `main_teste.py`; calcula a taxa efetiva com base na diversidade atual da população

### `main.py`

- `imprimir_tabela_itens(...)` — imprime os dados de entrada formatados antes do AG iniciar
- `limitacoes_teste()` — configuração fixa para testes, inclui taxa de mutação
- `main(debug)` — orquestrador acadêmico com taxa de mutação fixa

### `main_teste.py`

- `limitacoes_teste()` — configuração fixa para testes, sem taxa de mutação
- `main(debug)` — orquestrador experimental; calcula `taxa_base` uma vez no início e `taxa_atual` a cada geração via `taxa_mutacao_dinamica`

---

## Exemplo de saída com debug

```
Geração 3 | Sem melhora: 1/10
========================================
  Ind 1: [3, 1, 2] | Peso: 25 | Valor: 650
  Ind 2: [2, 2, 1] | Peso: 22 | Valor: 650
  ...

  [FITNESS] Melhor: [3, 1, 2] | Valor: 650
  [ROLETA] Pai (melhores) — sorteio: 0.412 → [3, 1, 2] | Valor: 650
  [ROLETA] Mãe (piores)   — sorteio: 0.731 → [2, 2, 1] | Valor: 650

  [CROSSOVER] genes trocados: posições [1]
  Pai:      3 [1] 2
  Mãe:      2 [2] 1
  Filho 1:  3 [2] 2  | Peso: 28 | Valor: 800 | ✓ válido
  Filho 2:  2 [1] 1  | Peso: 16 | Valor: 350 | ✓ válido

  [MUTAÇÃO] Sorteio: 0.087 (taxa: 0.333) — OCORREU | Ind 1 | Gene 1: 2 → 0 (sorteio ind: 0.341)
```

Na versão experimental o log de mutação exibe também a taxa efetiva aplicada:

```
  [MUTAÇÃO] Sorteio: 0.087 (base: 0.333 | atual: 0.900) — OCORREU | Ind 1 | Gene 1: 2 → 0
```

---

## Adaptando para outros problemas

O código suporta qualquer quantidade de itens (até o limite da lista `nomes`). Para adaptar a outros cenários:

- Altere os itens em `limitacoes_teste()` para testes rápidos
- Ajuste `peso_limite`, `tamanho_populacao` e `limite_s_melhora` conforme a complexidade do problema
- Para problemas com restrições diferentes do peso, a lógica de validação está centralizada em `Individuo._validar()` e pode ser estendida sem impactar o restante do código
