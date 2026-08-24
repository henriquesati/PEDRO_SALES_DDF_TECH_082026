"""
Constantes de Domínio e Regras de Negócio — Cart Recovery Mock Data.

Define valores fixos, enums de status, distribuições comportamentais,
regras de canal, precificação e categorias do marketplace.
"""

# ─── Distribuição RFM de Clientes ──────────────────────────────────────────
RFM_DIST = {
    'premium': 0.15,
    'regular': 0.40,
    'dormant': 0.30,
    'novo':    0.15,
}

# ─── Lifecycle dos Carrinhos ───────────────────────────────────────────────
# Total de carrinhos distribuídos nas etapas do funil de navegação
LIFECYCLE_DIST = {
    'direto_comprado':      0.23,   # ativo → comprado (sem intervenção de resgate)
    'abandonado':           0.56,   # ativo → abandonado (permaneceu inativo)
    'recuperado_comprado':  0.07,   # abandonado → resgate → comprado
    'recuperado_pendente':  0.02,   # abandonado → resgate (em andamento)
    'expirado':             0.05,   # abandonado → expirado após janela limite
    'ativo':                0.07,   # sessão ativa recente
}

LIFECYCLE_TO_STATUS = {
    'direto_comprado':     'comprado',
    'abandonado':          'abandonado',
    'recuperado_comprado': 'comprado',
    'recuperado_pendente': 'recuperado',
    'expirado':            'expirado',
    'ativo':               'ativo',
}

# ─── Motivos de Abandono de Carrinho ───────────────────────────────────────
MOTIVOS_ABANDONO = {
    'preco':          0.25,
    'frete':          0.22,
    'pagamento':      0.18,
    'indecisao':      0.20,
    'estoque':        0.05,
    'nao_informado':  0.10,
}

# ─── Canais e Custos Operacionais ──────────────────────────────────────────
CUSTO_CANAL = {
    'email':    0.05,
    'sms':      0.15,
    'push_app': 0.02,
    'whatsapp': 0.30,
}

# Taxas estimadas de conversão end-to-end por canal
CONVERSAO_CANAL = {
    'email':    0.045,
    'whatsapp': 0.025,
    'sms':      0.018,
    'push_app': 0.012,
}

# Funil de engajamento por canal (envio → abertura → clique → conversão)
FUNIL_CANAL = {
    'email':    {'abertura': 0.42, 'clique': 0.28, 'conversao': 0.15},
    'whatsapp': {'abertura': 0.68, 'clique': 0.35, 'conversao': 0.18},
    'sms':      {'abertura': 0.55, 'clique': 0.22, 'conversao': 0.14},
    'push_app': {'abertura': 0.30, 'clique': 0.18, 'conversao': 0.12},
}

# ─── Taxas de Recuperação por Segmento RFM ─────────────────────────────────
TAXA_RECUPERACAO_RFM = {
    'premium': 0.18,
    'regular': 0.10,
    'dormant': 0.06,
    'novo':    0.12,
}

# ─── Sequência de Resgate (Máximo 4 toques por carrinho) ───────────────────
SEQUENCIA_RESGATE = [
    {'tipo': 'lembrete_1h',   'horas': 1,  'canais': ['email'],               'desconto': (0, 0)},
    {'tipo': 'lembrete_24h',  'horas': 24, 'canais': ['email', 'push_app'],   'desconto': (0, 0)},
    {'tipo': 'desconto_48h',  'horas': 48, 'canais': ['email', 'sms'],        'desconto': (5, 10)},
    {'tipo': 'urgencia_72h',  'horas': 72, 'canais': ['email', 'whatsapp'],   'desconto': (10, 15)},
]

CONVERSAO_POR_TOQUE = {
    'lembrete_1h':  0.35,
    'lembrete_24h': 0.30,
    'desconto_48h': 0.25,
    'urgencia_72h': 0.10,
}

# Assuntos / Copies de comunicação de resgate
ASSUNTOS_RESGATE = {
    'lembrete_1h': [
        'Você esqueceu algo no carrinho 🛒',
        'Seus produtos estão esperando por você!',
        'Finalize sua compra antes que acabe!',
    ],
    'lembrete_24h': [
        'Ainda pensando? Seus itens estão reservados ⏰',
        'Não perca! Seus produtos podem acabar',
        'Última chance de garantir seus itens',
    ],
    'desconto_48h': [
        '🎁 Desconto especial para finalizar sua compra!',
        'Presente para você: desconto exclusivo no seu carrinho',
        'Economize agora! Oferta limitada no seu carrinho',
    ],
    'urgencia_72h': [
        '🔥 ÚLTIMA CHANCE: desconto + frete grátis!',
        'Só hoje! Oferta exclusiva para você finalizar',
        'Não deixe escapar: melhor oferta no seu carrinho',
    ],
}

# ─── Dispositivos, Navegadores e Origem de Tráfego ─────────────────────────
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

# ─── Sazonalidade Mensal (Jan-Jun) ─────────────────────────────────────────
SAZONALIDADE_MESES = [0.14, 0.15, 0.19, 0.16, 0.20, 0.16]

# ─── Categorias e Catálogo de Produtos ─────────────────────────────────────
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

NOMES_PRODUTO_TEMPLATES = {
    'Eletrônicos': {
        'Smartphones': ['Galaxy {m}', 'iPhone {m}', 'Redmi Note {m}', 'Moto G{m}', 'Pixel {m}'],
        'Notebooks': ['Notebook {m} i5', 'MacBook {m}', 'IdeaPad {m}', 'Aspire {m}'],
        'Tablets': ['Tab S{m}', 'iPad {m}', 'MatePad {m}'],
        'Acessórios': ['Cabo USB-C {m}', 'Carregador Turbo {m}', 'Capinha {m}', 'Película {m}'],
        'Áudio': ['Fone Bluetooth {m}', 'Caixa de Som {m}', 'Headset {m}', 'Soundbar {m}'],
    },
    'Moda': {
        'Camisetas': ['Camiseta {m} Básica', 'T-Shirt {m} Premium', 'Polo {m}'],
        'Calças': ['Jeans {m} Slim', 'Calça {m} Cargo', 'Legging {m}'],
        'Vestidos': ['Vestido {m} Midi', 'Vestido {m} Casual', 'Vestido {m} Longo'],
        'Calçados': ['Tênis {m} Run', 'Sandália {m}', 'Bota {m}', 'Sapatênis {m}'],
        'Acessórios': ['Bolsa {m}', 'Carteira {m}', 'Cinto {m}', 'Óculos {m}'],
    },
    'Casa & Decoração': {
        'Móveis': ['Mesa {m}', 'Cadeira {m}', 'Estante {m}', 'Sofá {m}'],
        'Iluminação': ['Luminária {m}', 'Abajur {m}', 'Spot LED {m}'],
        'Decoração': ['Quadro {m}', 'Vaso {m}', 'Almofada {m}', 'Espelho {m}'],
        'Cama & Banho': ['Jogo de Cama {m}', 'Toalha {m}', 'Edredom {m}'],
        'Cozinha': ['Panela {m}', 'Frigideira {m}', 'Jogo de Talheres {m}'],
    },
    'Esportes': {
        'Fitness': ['Haltere {m}kg', 'Tapete Yoga {m}', 'Elástico {m}'],
        'Corrida': ['Tênis {m} Running', 'Relógio GPS {m}', 'Bermuda {m}'],
        'Natação': ['Óculos {m} Natação', 'Sunga {m}', 'Touca {m}'],
        'Camping': ['Barraca {m}', 'Lanterna {m}', 'Saco de Dormir {m}'],
        'Suplementos': ['Whey {m} 900g', 'Creatina {m}', 'BCAA {m}'],
    },
    'Beleza': {
        'Skincare': ['Sérum {m}', 'Hidratante {m}', 'Protetor Solar {m}'],
        'Maquiagem': ['Base {m}', 'Batom {m}', 'Paleta {m}', 'Rímel {m}'],
        'Cabelos': ['Shampoo {m}', 'Condicionador {m}', 'Máscara {m}'],
        'Perfumaria': ['Perfume {m} 100ml', 'Colônia {m}', 'Body Splash {m}'],
        'Corpo': ['Creme Corporal {m}', 'Desodorante {m}', 'Sabonete {m}'],
    },
    'Livros': {
        'Ficção': ['O {m} Perdido', 'A Jornada de {m}', 'Crônicas de {m}'],
        'Não-Ficção': ['Hábitos {m}', 'O Poder de {m}', 'Mindset {m}'],
        'Técnicos': ['Python {m}', 'Data Science {m}', 'Cloud {m}'],
        'Infantil': ['A Aventura de {m}', 'O Pequeno {m}', 'Turma do {m}'],
        'HQs': ['{m} Vol. 1', 'Saga {m}', 'Graphic Novel {m}'],
    },
    'Brinquedos': {
        'Educativos': ['Quebra-Cabeça {m}', 'Kit Ciência {m}', 'Blocos {m}'],
        'Bonecas': ['Boneca {m}', 'LOL {m}', 'Barbie {m}'],
        'Jogos': ['Jogo {m}', 'Tabuleiro {m}', 'Cartas {m}'],
        'LEGO': ['LEGO {m}', 'LEGO City {m}', 'LEGO Technic {m}'],
        'Eletrônicos': ['Robô {m}', 'Drone {m} Mini', 'Console {m}'],
    },
}

SUFIXOS_PRODUTO = ['Pro', 'Plus', 'Max', 'Lite', 'Ultra', 'Neo', 'Prime', 'Elite', 'Classic', 'Sport']

# ─── Tipos de Eventos de Telemetria ────────────────────────────────────────
TIPOS_EVENTO = [
    'view_produto', 'add_carrinho', 'remove_carrinho',
    'update_quantidade', 'view_checkout', 'inicio_pagamento',
    'erro_pagamento', 'abandono', 'retorno',
]

# ─── Pagamentos e Pedidos ──────────────────────────────────────────────────
METODOS_PAGAMENTO = {
    'pix':             0.35,
    'cartao_credito':  0.40,
    'cartao_debito':   0.10,
    'boleto':          0.15,
}

STATUS_PEDIDO = {
    'confirmado': 0.15,
    'enviado':    0.20,
    'entregue':   0.60,
    'cancelado':  0.05,
}
