"""
Modulo de Processamento de Vendas e Logistica de Despacho.
"""

class GerenciadorPedidos:
    """
    Classe utilitaria para faturamento e gestao de pedidos de clientes.
    """

    # Parametros de faturamento (Constantes)
    REDUCAO_VIP = 0.85
    REDUCAO_PREMIUM = 0.90
    VALE_10 = 0.90
    VALE_20 = 0.80
    MINIMO_FRETE_GRATIS = 200
    ADICIONAL_CARTAO = 1.05

    def obter_total_itens(self, itens):
        """Calcula o somatorio bruto do valor total dos produtos."""
        return sum(i['preco'] * i['quantidade'] for i in itens)

    def _validar_custo_entrega(self, localidade, total_compra):
        """Determina o valor do frete conforme a regiao e montante."""
        if total_compra > self.MINIMO_FRETE_GRATIS:
            return 0
        tarifas = {'SP': 15, 'RJ': 20, 'MG': 18}
        return tarifas.get(localidade, 30)

    def _computar_descontos(self, base, categoria, ticket):
        """Aplica deducoes baseadas no perfil do cliente e cupons ativos."""
        final = base
        if categoria == 'vip':
            final *= self.REDUCAO_VIP
        elif categoria == 'premium':
            final *= self.REDUCAO_PREMIUM

        if ticket == 'DESC10':
            final *= self.VALE_10
        elif ticket == 'DESC20':
            final *= self.VALE_20
        return final

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def processar_pedido(self, cliente_nome, cliente_email, cliente_tipo,
                         itens, cupom, regiao, forma_pagamento):
        """
        Realiza a liquidacao completa de um pedido de venda.
        """
        bruto = self.obter_total_itens(itens)
        com_desconto = self._computar_descontos(bruto, cliente_tipo, cupom)
        frete_calculado = self._validar_custo_entrega(regiao, com_desconto)
        montante_final = com_desconto + frete_calculado

        if forma_pagamento == 'cartao':
            montante_final *= self.ADICIONAL_CARTAO

        montante_final = round(montante_final, 2)
        documento = (f"Pedido para {cliente_nome} ({cliente_email})\n"
                     f"Total: R$ {montante_final}")

        return {
            'cliente': cliente_nome,
            'subtotal': com_desconto,
            'frete': frete_calculado,
            'total': montante_final,
            'comprovante': documento
        }

    def calcular_total_relatorio(self, pedidos):
        """Soma o valor bruto de uma lista de pedidos para fins estatisticos."""
        return sum(self.obter_total_itens(p['itens']) for p in pedidos)