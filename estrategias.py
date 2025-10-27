from abc import ABC, abstractmethod

# --- Padrão Strategy: Interfaces Abstratas ---
class EstrategiaPagamento(ABC):
    """Interface para estratégias de pagamento."""
    @abstractmethod
    def processar_pagamento(self, valor: float) -> bool:
        pass

class EstrategiaFrete(ABC):
    """Interface para estratégias de cálculo de frete."""
    @abstractmethod
    def calcular_custo(self, peso: float) -> float:
        pass

# --- Padrão Strategy: Implementações Concretas de Pagamento ---
class PagamentoPix(EstrategiaPagamento):
    def processar_pagamento(self, valor: float) -> bool:
        print(f"[Pagamento Pix] Processando R${valor:.2f}. Transação instantânea.")
        # Lógica de integração com gateway Pix...
        return True

class PagamentoCredito(EstrategiaPagamento):
    def processar_pagamento(self, valor: float) -> bool:
        print(f"[Pagamento Cartão] Processando R${valor:.2f}. Autorização necessária.")
        # Lógica de integração com adquirente...
        return True

# --- Padrão Strategy: Implementações Concretas de Frete ---
class FreteNormal(EstrategiaFrete):
    def calcular_custo(self, peso: float) -> float:
        print(f"[Frete Normal] Peso {peso}kg. Custo base + taxa fixa.")
        return 15.00 + (peso * 0.5)

class FreteExpresso(EstrategiaFrete):
    def calcular_custo(self, peso: float) -> float:
        print(f"[Frete Expresso] Peso {peso}kg. Custo premium + taxa por peso.")
        return 45.00 + (peso * 2.0)

# --- Padrão Decorator: Interface Base (Component) ---
class Calculavel(ABC):
    """Interface Component para que o valor seja calculável."""
    @abstractmethod
    def get_valor_total(self) -> float:
        pass

# --- Padrão Decorator: Componente Concreto (Objeto Base) ---
class Pedido(Calculavel):
    """
    Contexto para Strategy e Componente Base para Decorator.
    Mantém apenas a responsabilidade de gerenciar dados e estratégias.
    """
    def __init__(self, itens: list[dict], frete_strategy: EstrategiaFrete, pagamento_strategy: EstrategiaPagamento):
        self.itens = itens
        self.peso_total = sum(item['peso'] for item in itens)
        self.valor_itens = sum(item['valor'] * item['quantidade'] for item in itens)
        self.frete_strategy = frete_strategy
        self.pagamento_strategy = pagamento_strategy
        print(f"Pedido criado. Valor dos itens: R${self.valor_itens:.2f}")

    def get_valor_itens(self) -> float:
        """Retorna o valor base dos itens."""
        return self.valor_itens

    def get_custo_frete(self) -> float:
        """Utiliza a estratégia de frete para calcular o custo."""
        return self.frete_strategy.calcular_custo(self.peso_total)

    def get_valor_total(self) -> float:
        """O valor total base é o valor dos itens mais o frete."""
        return self.get_valor_itens() + self.get_custo_frete()
    
    def processar_pagamento(self) -> bool:
        """Delega a execução da estratégia de pagamento."""
        return self.pagamento_strategy.processar_pagamento(self.get_valor_total())

# --- Padrão Decorator: Abstract Decorator ---
class DecoratorValor(Calculavel):
    """Mantém a referência ao objeto Pedido e implementa a interface Calculavel."""
    def __init__(self, pedido: Calculavel):
        self._pedido = pedido

    def get_valor_total(self) -> float:
        """Delegando a responsabilidade."""
        return self._pedido.get_valor_total()

# --- Padrão Decorator: Implementações Concretas ---
class DescontoPix(DecoratorValor):
    """Aplica 5% de desconto no total (itens + frete) se o pagamento for Pix."""
    def get_valor_total(self) -> float:
        valor_base = self._pedido.get_valor_total()
        desconto = valor_base * 0.05
        valor_final = valor_base - desconto
        print(f"[Decorator Desconto Pix] Aplicado -5% ({desconto:.2f}). Novo total: R${valor_final:.2f}")
        return valor_final

class TaxaEmbalagemPresente(DecoratorValor):
    """Adiciona uma taxa fixa de embalagem de presente."""
    TAXA = 10.00
    def get_valor_total(self) -> float:
        valor_base = self._pedido.get_valor_total()
        valor_final = valor_base + self.TAXA
        print(f"[Decorator Embalagem Presente] Adicionado R${self.TAXA:.2f}. Novo total: R${valor_final:.2f}")
        return valor_final