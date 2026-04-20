from dataclasses import dataclass


@dataclass
class Cromossomo_Tabela:
    nome_item: str
    peso_item: int
    valor_item: int
    qtd_item: int

    def __init__(self, nome_item, peso_item, valor_item, qtd_item):
        self.nome_item = nome_item
        self.peso_item = peso_item
        self.valor_item = valor_item
        self.qtd_item = qtd_item
