# Arquivo: checkout_monolitico.py
# Propósito: Código legado, demonstrando a "classe deus" antes da refatoração.

class SistemaPedidoAntigo:
    """CLASSE DEUS: Viola SRP e OCP, centralizando múltiplas responsabilidades."""
    def __init__(self, itens):
        self.itens = itens
        self.valor_base = sum(item['valor'] * item['quantidade'] for item in itens)
        self.peso_total = sum(item['peso'] for item in itens)

    def calcular_desconto(self, metodo_pagamento):
        """Lógica de desconto embutida (Violação do OCP)"""
        if metodo_pagamento == 'pix':
            return self.valor_base * 0.05
        # else if para outros descontos exigiria modificação direta
        return 0

    def calcular_frete(self, tipo_frete):
        """Lógica de frete embutida (Violação do OCP)"""
        if tipo_frete == 'normal':
            return 15.00 + (self.peso_total * 0.5)
        elif tipo_frete == 'expresso':
            return 45.00 + (self.peso_total * 2.0)
        # else if para novos tipos exigiria modificação direta
        return 0

    def processar_pagamento(self, metodo_pagamento, valor):
        """Lógica de pagamento embutida (Violação do SRP)"""
        print(f"Processando {metodo_pagamento} para R${valor:.2f}")
        # Lógica de integração com gateway
        return True

    def finalizar_compra(self, metodo_pagamento, tipo_frete, tem_embalagem=False):
        """Orquestração complexa de checkout (Violação do SRP e Facade não aplicado)"""
        desconto = self.calcular_desconto(metodo_pagamento)
        frete = self.calcular_frete(tipo_frete)
        embalagem = 10.00 if tem_embalagem else 0

        valor_total = self.valor_base - desconto + frete + embalagem
        if self.processar_pagamento(metodo_pagamento, valor_total):
            print("Transação concluída. NF gerada, estoque reservado.")
            # Lógicas de estoque, NF, notificação embutidas ou chamadas internas complexas
            return True
        return False