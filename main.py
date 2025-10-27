# Arquivo: main.py
# Propósito: Código cliente para demonstrar a utilização e a flexibilidade dos padrões.

from estrategias import Pedido, PagamentoPix, PagamentoCredito, FreteNormal, FreteExpresso
from estrategias import DescontoPix, TaxaEmbalagemPresente
from fachada import CheckoutFacade

# 1. Definição dos Itens
ITENS_COMPRA = [
    {'nome': 'Notebook X', 'valor': 3500.00, 'quantidade': 1, 'peso': 2.5},
    {'nome': 'Mousepad', 'valor': 50.00, 'quantidade': 2, 'peso': 0.1}
]
# Valor Base Itens: R$3600.00

facade = CheckoutFacade()

# ====================================================================
# CENÁRIO 1: PIX + FRETE NORMAL + DECORATOR DESCONTO
# Objetivo: Demonstrar Strategy (Pix, Normal) e Decorator (Desconto)
# ====================================================================
print("="*60)
print("CENÁRIO 1: PIX + FRETE NORMAL + DESCONTO PIX (DECORATOR)")

# Configuração Strategy
frete1 = FreteNormal()
pagamento1 = PagamentoPix()

# Pedido (Contexto/Componente Base)
pedido_base_1 = Pedido(ITENS_COMPRA, frete1, pagamento1)
# Valor Base (3600.00) + Frete Normal (15 + 2.6*0.5 = 16.30) = 3616.30

# Aplicação Decorator: Envolvendo o pedido base
pedido_final_1 = DescontoPix(pedido_base_1)
# Valor Final: 3616.30 * 0.95 = 3435.485

# Execução através do Facade
facade.concluir_transacao(pedido_final_1)


# ====================================================================
# CENÁRIO 2: CRÉDITO + FRETE EXPRESSO + DECORATOR EMBALAGEM PRESENTE
# Objetivo: Demonstrar Strategy (Crédito, Expresso) e Decorator (Taxa)
# ====================================================================
print("="*60)
print("CENÁRIO 2: CRÉDITO + FRETE EXPRESSO + EMBALAGEM PRESENTE (DECORATOR)")

# Configuração Strategy
frete2 = FreteExpresso()
pagamento2 = PagamentoCredito()

# Pedido (Contexto/Componente Base)
pedido_base_2 = Pedido(ITENS_COMPRA, frete2, pagamento2)
# Valor Base (3600.00) + Frete Expresso (45 + 2.6*2.0 = 50.20) = 3650.20

# Aplicação Decorator: Envolvendo o pedido base
pedido_final_2 = TaxaEmbalagemPresente(pedido_base_2)
# Valor Final: 3650.20 + 10.00 = 3660.20

# Execução através do Facade
facade.concluir_transacao(pedido_final_2)

print("="*60)