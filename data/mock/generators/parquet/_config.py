"""
Configuração compartilhada para todos os generators de dados mock.
Constantes, distribuições e paths derivados do data_model_specs.md e business-rules.md.
Seed fixa para reprodutibilidade total.
"""
from pathlib import Path
from datetime import datetime
import pytz

# ─── Reprodutibilidade ─────────────────────────────────────────────────────
SEED = 42

# ─── Paths ──────────────────────────────────────────────────────────────────
MOCK_DIR = Path(__file__).resolve().parent.parent.parent      # data/mock/
OUTPUT_DIR = MOCK_DIR / "output"

# ─── Período temporal ───────────────────────────────────────────────────────
TZ = pytz.timezone("America/Sao_Paulo")
PERIODO_INICIO = datetime(2026, 1, 1, tzinfo=TZ)
PERIODO_FIM = datetime(2026, 6, 30, 23, 59, 59, tzinfo=TZ)

# ─── Volumes ────────────────────────────────────────────────────────────────
N_CLIENTES = 1_200
N_PRODUTOS = 250
N_CARRINHOS = 6_000

# ─── Dirty data rate ────────────────────────────────────────────────────────
DIRTY_RATE = 0.05  # 5% base para anomalias

# ─── Distribuição RFM de clientes ───────────────────────────────────────────
RFM_DIST = {
    'premium': 0.15,
    'regular': 0.40,
    'dormant': 0.30,
    'novo':    0.15,
}

# ─── Lifecycle dos carrinhos ────────────────────────────────────────────────
# Define o caminho completo de cada carrinho no funil
# Total: 6.000 carrinhos
#   - 70% abandonam em algum momento (4.200)
#   - Taxa de recuperação: 10% dos abandonados (420)
#   - Pedidos totais: 1.800 (direto + recuperado)
LIFECYCLE_DIST = {
    'direto_comprado':      0.23,   # ativo → comprado  (1.380)
    'abandonado':           0.56,   # ativo → abandonado (3.360, permaneceu)
    'recuperado_comprado':  0.07,   # abandonado → recuperado → comprado (420)
    'recuperado_pendente':  0.02,   # abandonado → recuperado (120, em andamento)
    'expirado':             0.05,   # abandonado → expirado (300)
    'ativo':                0.07,   # ativo recente (420)
}

LIFECYCLE_TO_STATUS = {
    'direto_comprado':     'comprado',
    'abandonado':          'abandonado',
    'recuperado_comprado': 'comprado',
    'recuperado_pendente': 'recuperado',
    'expirado':            'expirado',
    'ativo':               'ativo',
}

# ─── Motivos de abandono ────────────────────────────────────────────────────
MOTIVOS_ABANDONO = {
    'preco':          0.25,
    'frete':          0.22,
    'pagamento':      0.18,
    'indecisao':      0.20,
    'estoque':        0.05,
    'nao_informado':  0.10,
}

# ─── Canais e custos ────────────────────────────────────────────────────────
CUSTO_CANAL = {
    'email':    0.05,
    'sms':      0.15,
    'push_app': 0.02,
    'whatsapp': 0.30,
}

# Conversão end-to-end por canal (% do total de abandonados)
CONVERSAO_CANAL = {
    'email':    0.045,
    'whatsapp': 0.025,
    'sms':      0.018,
    'push_app': 0.012,
}

# Funil por canal: envio → abertura → clique → conversão
FUNIL_CANAL = {
    'email':    {'abertura': 0.42, 'clique': 0.28, 'conversao': 0.15},
    'whatsapp': {'abertura': 0.68, 'clique': 0.35, 'conversao': 0.18},
    'sms':      {'abertura': 0.55, 'clique': 0.22, 'conversao': 0.14},
    'push_app': {'abertura': 0.30, 'clique': 0.18, 'conversao': 0.12},
}

# ─── Taxas de recuperação por segmento RFM ──────────────────────────────────
TAXA_RECUPERACAO_RFM = {
    'premium': 0.18,
    'regular': 0.10,
    'dormant': 0.06,
    'novo':    0.12,
}

# ─── Sequência de comunicação (max 4 por carrinho) ─────────────────────────
SEQUENCIA_RESGATE = [
    {'tipo': 'lembrete_1h',   'horas': 1,  'canais': ['email'],               'desconto': (0, 0)},
    {'tipo': 'lembrete_24h',  'horas': 24, 'canais': ['email', 'push_app'],   'desconto': (0, 0)},
    {'tipo': 'desconto_48h',  'horas': 48, 'canais': ['email', 'sms'],        'desconto': (5, 10)},
    {'tipo': 'urgencia_72h',  'horas': 72, 'canais': ['email', 'whatsapp'],   'desconto': (10, 15)},
]

# Distribuição de conversões por toque
CONVERSAO_POR_TOQUE = {
    'lembrete_1h':  0.35,
    'lembrete_24h': 0.30,
    'desconto_48h': 0.25,
    'urgencia_72h': 0.10,
}

# ─── Dispositivos / browsers / origens ──────────────────────────────────────
DISPOSITIVOS = {'mobile': 0.55, 'desktop': 0.35, 'tablet': 0.10}

BROWSERS = {
    'mobile':  ['Chrome Mobile', 'Safari Mobile', 'Samsung Internet'],
    'desktop': ['Chrome', 'Firefox', 'Edge', 'Safari'],
    'tablet':  ['Safari', 'Chrome'],
}

CANAIS_ORIGEM = {
    'google':    0.30,
    'direct':    0.25,
    'facebook':  0.15,
    'instagram': 0.15,
    'email':     0.10,
    'outros':    0.05,
}

# ─── Categorias de produtos ─────────────────────────────────────────────────
CATEGORIAS = {
    'Eletrônicos': {
        'subcategorias': ['Smartphones', 'Notebooks', 'Tablets', 'Acessórios', 'Áudio'],
        'marcas': ['Samsung', 'Apple', 'Xiaomi', 'Motorola', 'JBL', 'Sony', 'LG'],
        'faixa_preco': (49.90, 4999.90),
        'peso': 0.25,
    },
    'Moda': {
        'subcategorias': ['Camisetas', 'Calças', 'Vestidos', 'Calçados', 'Acessórios'],
        'marcas': ['Nike', 'Adidas', 'Zara', 'Hering', 'Renner', 'C&A'],
        'faixa_preco': (29.90, 599.90),
        'peso': 0.20,
    },
    'Casa & Decoração': {
        'subcategorias': ['Móveis', 'Iluminação', 'Decoração', 'Cama & Banho', 'Cozinha'],
        'marcas': ['Tok&Stok', 'Etna', 'Tramontina', 'Camicado'],
        'faixa_preco': (19.90, 2999.90),
        'peso': 0.15,
    },
    'Esportes': {
        'subcategorias': ['Fitness', 'Corrida', 'Natação', 'Camping', 'Suplementos'],
        'marcas': ['Nike', 'Adidas', 'Under Armour', 'Puma', 'Decathlon'],
        'faixa_preco': (24.90, 799.90),
        'peso': 0.15,
    },
    'Beleza': {
        'subcategorias': ['Skincare', 'Maquiagem', 'Cabelos', 'Perfumaria', 'Corpo'],
        'marcas': ['Natura', 'O Boticário', 'MAC', 'Avon', 'Dove'],
        'faixa_preco': (14.90, 399.90),
        'peso': 0.10,
    },
    'Livros': {
        'subcategorias': ['Ficção', 'Não-Ficção', 'Técnicos', 'Infantil', 'HQs'],
        'marcas': ['Companhia das Letras', 'Intrínseca', 'Rocco', 'Darkside'],
        'faixa_preco': (9.90, 149.90),
        'peso': 0.08,
    },
    'Brinquedos': {
        'subcategorias': ['Educativos', 'Bonecas', 'Jogos', 'LEGO', 'Eletrônicos'],
        'marcas': ['LEGO', 'Mattel', 'Hasbro', 'Estrela', 'Fisher-Price'],
        'faixa_preco': (19.90, 499.90),
        'peso': 0.07,
    },
}

# ─── Tipos de evento (time series) ─────────────────────────────────────────
TIPOS_EVENTO = [
    'view_produto', 'add_carrinho', 'remove_carrinho',
    'update_quantidade', 'view_checkout', 'inicio_pagamento',
    'erro_pagamento', 'abandono', 'retorno',
]

# ─── Métodos de pagamento ───────────────────────────────────────────────────
METODOS_PAGAMENTO = {
    'pix':             0.35,
    'cartao_credito':  0.40,
    'cartao_debito':   0.10,
    'boleto':          0.15,
}

# ─── Status de pedido ───────────────────────────────────────────────────────
STATUS_PEDIDO = {
    'confirmado': 0.15,
    'enviado':    0.20,
    'entregue':   0.60,
    'cancelado':  0.05,
}
