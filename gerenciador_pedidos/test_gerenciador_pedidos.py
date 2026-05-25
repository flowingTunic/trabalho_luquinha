"""
Testes do GerenciadorPedidos.

Estes testes definem o COMPORTAMENTO ESPERADO da classe.
Durante a refatoracao, eles devem permanecer todos em verde.
Se algum quebrar, a refatoracao mudou o comportamento --- desfaca e tente outro caminho.
"""

from gerenciador_pedidos import GerenciadorPedidos


def test_pedido_basico_cliente_comum():
    gp = GerenciadorPedidos()
    itens = [{'preco': 50, 'quantidade': 2}]
    r = gp.processar_pedido('Joao', 'joao@email.com', 'comum',
                            itens, None, 'SP', 'pix')
    # subtotal = 50 * 2 = 100; frete SP = 15; total = 115
    assert r['subtotal'] == 100
    assert r['frete'] == 15
    assert r['total'] == 115


def test_cliente_vip_recebe_15_por_cento_desconto():
    gp = GerenciadorPedidos()
    itens = [{'preco': 100, 'quantidade': 1}]
    r = gp.processar_pedido('Maria', 'maria@email.com', 'vip',
                            itens, None, 'SP', 'pix')
    # 100 * 0.85 = 85; frete = 15; total = 100
    assert r['subtotal'] == 85.0
    assert r['total'] == 100.0


def test_cliente_premium_recebe_10_por_cento_desconto():
    gp = GerenciadorPedidos()
    itens = [{'preco': 100, 'quantidade': 1}]
    r = gp.processar_pedido('Carla', 'carla@email.com', 'premium',
                            itens, None, 'SP', 'pix')
    # 100 * 0.90 = 90; frete = 15; total = 105
    assert r['subtotal'] == 90.0
    assert r['total'] == 105.0


def test_cupom_desc10_aplica_10_por_cento():
    gp = GerenciadorPedidos()
    itens = [{'preco': 100, 'quantidade': 1}]
    r = gp.processar_pedido('Ana', 'ana@email.com', 'comum',
                            itens, 'DESC10', 'SP', 'pix')
    # 100 * 0.90 = 90; frete = 15; total = 105
    assert r['subtotal'] == 90.0
    assert r['total'] == 105.0


def test_cupom_desc20_aplica_20_por_cento():
    gp = GerenciadorPedidos()
    itens = [{'preco': 100, 'quantidade': 1}]
    r = gp.processar_pedido('Bruno', 'bruno@email.com', 'comum',
                            itens, 'DESC20', 'SP', 'pix')
    # 100 * 0.80 = 80; frete = 15; total = 95
    assert r['subtotal'] == 80.0
    assert r['total'] == 95.0


def test_frete_gratis_acima_de_200():
    gp = GerenciadorPedidos()
    itens = [{'preco': 250, 'quantidade': 1}]
    r = gp.processar_pedido('Pedro', 'pedro@email.com', 'comum',
                            itens, None, 'SP', 'pix')
    # subtotal 250 > 200; frete = 0; total = 250
    assert r['frete'] == 0
    assert r['total'] == 250


def test_frete_por_regiao_rj():
    gp = GerenciadorPedidos()
    itens = [{'preco': 50, 'quantidade': 1}]
    r = gp.processar_pedido('Lu', 'lu@email.com', 'comum',
                            itens, None, 'RJ', 'pix')
    assert r['frete'] == 20
    assert r['total'] == 70


def test_frete_por_regiao_mg():
    gp = GerenciadorPedidos()
    itens = [{'preco': 50, 'quantidade': 1}]
    r = gp.processar_pedido('Lu', 'lu@email.com', 'comum',
                            itens, None, 'MG', 'pix')
    assert r['frete'] == 18
    assert r['total'] == 68


def test_frete_regiao_desconhecida_usa_padrao():
    gp = GerenciadorPedidos()
    itens = [{'preco': 50, 'quantidade': 1}]
    r = gp.processar_pedido('Lu', 'lu@email.com', 'comum',
                            itens, None, 'XX', 'pix')
    assert r['frete'] == 30
    assert r['total'] == 80


def test_cartao_aplica_5_por_cento_de_juros():
    gp = GerenciadorPedidos()
    itens = [{'preco': 100, 'quantidade': 1}]
    r = gp.processar_pedido('Luis', 'luis@email.com', 'comum',
                            itens, None, 'SP', 'cartao')
    # subtotal 100 + frete 15 = 115; * 1.05 = 120.75
    assert r['total'] == 120.75


def test_combinacao_premium_cupom_cartao():
    """Caso composto: desconto VIP/premium + cupom + juros do cartao."""
    gp = GerenciadorPedidos()
    itens = [{'preco': 100, 'quantidade': 1}]
    r = gp.processar_pedido('Bia', 'bia@email.com', 'premium',
                            itens, 'DESC20', 'RJ', 'cartao')
    # 100 * 0.90 (premium) = 90; * 0.80 (DESC20) = 72
    # + frete RJ 20 = 92; * 1.05 (cartao) = 96.6
    assert r['subtotal'] == 72.0
    assert r['frete'] == 20
    assert r['total'] == 96.6


def test_comprovante_contem_nome_e_email():
    gp = GerenciadorPedidos()
    itens = [{'preco': 50, 'quantidade': 1}]
    r = gp.processar_pedido('Joao', 'joao@email.com', 'comum',
                            itens, None, 'SP', 'pix')
    assert 'Joao' in r['comprovante']
    assert 'joao@email.com' in r['comprovante']


def test_calcular_total_relatorio():
    gp = GerenciadorPedidos()
    pedidos = [
        {'itens': [{'preco': 10, 'quantidade': 2}]},                       # 20
        {'itens': [{'preco': 30, 'quantidade': 1},
                   {'preco': 5, 'quantidade': 4}]},                        # 30 + 20 = 50
    ]
    # total agregado = 20 + 50 = 70
    assert gp.calcular_total_relatorio(pedidos) == 70
