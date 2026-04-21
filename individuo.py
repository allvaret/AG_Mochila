
from random import randint


class Individuo:
    def __init__(self, cromossomo, limitacoes, peso_limite):
        self.cromossomo = cromossomo
        self.limitacoes = limitacoes
        self.peso_limite = peso_limite
        self.peso_total = sum(qtd * peso.peso_item for qtd, peso in zip(cromossomo, limitacoes))
        self.valor_total = sum(qtd * valor.valor_item for qtd, valor in zip(cromossomo, limitacoes))
        self.valido = self._validar()

    def _validar(self):
        """Verifica se o indivíduo é válido baseado no peso total"""
        return self.peso_total <= self.peso_limite
    
    def reparar(self, max_tentativas=1000):
        """Repara um indivíduo inválido gerando um novo válido"""
        tentativas = 0
        while not self.valido and tentativas < max_tentativas:
            i = randint(0, len(self.cromossomo) - 1)
            if self.cromossomo[i] > 0:
                self.cromossomo[i] -= 1
            self.peso_total  = sum(qtd * item.peso_item  for qtd, item in zip(self.cromossomo, self.limitacoes))
            self.valor_total = sum(qtd * item.valor_item for qtd, item in zip(self.cromossomo, self.limitacoes))
            self.valido = self._validar()
            tentativas += 1
            
        if not self.valido:
            print(f"[DEBUG] Último cromossomo tentado: {self.cromossomo} | Peso: {self.peso_total} | Valor: {self.valor_total}")
            raise ValueError(f"Não foi possível gerar indivíduo válido após {max_tentativas} tentativas"
                             f"Verifique se o peso limite ({self.peso_limite}) é compatível com os itens.")
        return self
    
    @classmethod
    def criar_valido(cls, limitacoes, peso_limite, max_tentativas=1000):
        """Factory method: cria um indivíduo já válido"""
        for _ in range(max_tentativas):
            cromossomo = [randint(0, item.qtd_item) for item in limitacoes]
            individuo = cls(cromossomo, limitacoes, peso_limite)
            
            if individuo.valido:
                return individuo
        
        raise ValueError(f"Não foi possível criar indivíduo válido após {max_tentativas} tentativas")
    
    def __repr__(self):
        """Representação amigável para debug"""
        return f"Individuo(cromossomo={self.cromossomo}, válido={self.valido}, peso={self.peso_total}, valor={self.valor_total})"