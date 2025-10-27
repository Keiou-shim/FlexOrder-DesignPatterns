# FlexOrder-DesignPatterns

Este repositório apresenta a refatoração do Sistema de Processamento de Pedidos Legado (LMPT), originalmente monolítico e com baixa coesão, para uma arquitetura orientada a objetos modular, aplicando os Padrões de Projeto Estruturais e Comportamentais: **Strategy**, **Decorator** e **Facade**.

O código legado, simulado em `checkout_monolitico.py`, violava os princípios SOLID, especificamente o SRP (Single Responsibility Principle) e o OCP (Open/Closed Principle).

## 1. Nova Arquitetura Orientada a Objetos

A arquitetura foi modularizada em classes e módulos com responsabilidades únicas (Adesão ao **SRP**):

1.  **`estrategias.py` (Strategy e Decorator):** Contém a lógica de variação de comportamento e cálculo de valor. O `Pedido` é o objeto central que coordena as estratégias e é envolvido pelos decoradores.
2.  **`fachada.py` (Facade):** Contém a classe `CheckoutFacade` e os subsistemas auxiliares. Sua responsabilidade é puramente orquestrar o processo de checkout.
3.  **`main.py` (Cliente):** Demonstra como configurar e usar a nova arquitetura de forma simplificada.

## 2. Aplicação dos Padrões de Projeto e Correção de Princípios SOLID

### Padrão Comportamental: Strategy (Estratégia)

| Problema Resolvido | Correção (SOLID) | Classes Envolvidas |
| :--- | :--- | :--- |
| **Violação do OCP** e **SRP**: Lógica de `if/elif` embutida em `calcular_frete()` e `processar_pagamento()`. | Isola a lógica que muda (o algoritmo de pagamento/frete) em classes separadas (`EstrategiaPagamento`/`EstrategiaFrete`). Adicionar um novo método de pagamento exige apenas a criação de uma nova classe, **sem modificar o código da classe `Pedido` (OCP)**. | `EstrategiaPagamento`, `EstrategiaFrete`, `PagamentoPix`, `FreteExpresso`, `Pedido` (Contexto). |

### Padrão Estrutural: Decorator (Decorador)

| Problema Resolvido | Correção (SOLID) | Classes Envolvidas |
| :--- | :--- | :--- |
| **Violação do OCP**: Lógica de Desconto/Taxa embutida no método de cálculo. | Permite a adição dinâmica e em camadas de responsabilidades (descontos, taxas) ao objeto `Pedido`. O código do cálculo base não precisa ser alterado para incluir ou remover regras de valor, garantindo o **OCP**. | `Calculavel`, `Pedido`, `DescontoPix`, `TaxaEmbalagemPresente`. |

### Padrão Estrutural: Facade (Fachada)

| Problema Resolvido | Correção (SOLID) | Classes Envolvidas |
| :--- | :--- | :--- |
| **Violação do SRP**: O método `finalizar_compra()` do legado orquestrava a transação e as chamadas a subsistemas, tornando-o uma classe com múltiplas responsabilidades. | A classe `CheckoutFacade` assume a **única responsabilidade** de orquestrar a sequência de chamadas (`verificar_estoque`, `processar_pagamento`, `gerar_nf`). Isso isola a complexidade e adere ao **SRP**. | `CheckoutFacade`, `SistemaEstoque`, `GeradorNotaFiscal`. |