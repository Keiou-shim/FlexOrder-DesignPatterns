from typing import TYPE_CHECKING
# Para evitar importação circular no type-hinting
if TYPE_CHECKING:
    from .estrategias import Pedido 

# --- Subsistemas (Comportamentos que eram da classe monolítica) ---
class SistemaEstoque:
    def verificar_disponibilidade(self, pedido: 'Pedido') -> bool:
        print("[Estoque] Verificando itens...")
        # Lógica complexa de estoque aqui...
        return True # Assumindo que estão disponíveis

    def reservar_itens(self, pedido: 'Pedido'):
        print("[Estoque] Itens reservados e prontos para envio.")

class GeradorNotaFiscal:
    def gerar(self, pedido: 'Pedido'):
        print(f"[Nota Fiscal] NF gerada para o pedido. Valor total final: R${pedido.get_valor_total():.2f}")

class NotificadorCliente:
    def enviar_confirmacao(self, pedido: 'Pedido'):
        print(f"[Notificação] E-mail de confirmação enviado ao cliente.")

# --- Padrão Facade: CheckoutFacade ---
class CheckoutFacade:
    """
    Fornece uma interface de alto nível e simplificada para o processo de checkout,
    orquestrando as chamadas para os subsistemas e a classe Pedido (Contexto/Componente).
    """
    def __init__(self):
        self._estoque = SistemaEstoque()
        self._nf = GeradorNotaFiscal()
        self._notificador = NotificadorCliente()

    def concluir_transacao(self, pedido: 'Pedido') -> bool:
        """Simplifica a orquestração do checkout (substitui finalizar_compra() monolítico)."""
        print("\n--- INÍCIO DO CHECKOUT FACADE ---")

        # 1. Verificação (Subsistema)
        if not self._estoque.verificar_disponibilidade(pedido):
            print("ERRO: Itens fora de estoque.")
            return False

        # 2. Processamento do Valor/Comportamento (Estratégias e Decorators no objeto Pedido)
        if not pedido.processar_pagamento():
            print("ERRO: Pagamento falhou.")
            return False

        # 3. Finalização (Subsistemas)
        self._estoque.reservar_itens(pedido)
        self._nf.gerar(pedido)
        self._notificador.enviar_confirmacao(pedido)
        
        print("--- CHECKOUT CONCLUÍDO COM SUCESSO ---\n")
        return True