"""
Generator: produtos
Gera ~250 produtos em 7 categorias com marcas, preços e avaliações realistas.
Dirty data: preco_atual > preco_original (~5%, promoção invertida).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
import numpy as np
from datetime import timedelta
import _config as cfg

# Templates de nomes por categoria
NOMES_PRODUTO = {
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

SUFIXOS = ['Pro', 'Plus', 'Max', 'Lite', 'Ultra', 'Neo', 'Prime', 'Elite', 'Classic', 'Sport']


def generate():
    """Gera DataFrame de produtos com categorias, marcas e preços realistas."""
    np.random.seed(cfg.SEED)

    rows = []
    produto_id = 1

    categorias = list(cfg.CATEGORIAS.keys())
    pesos_cat = [cfg.CATEGORIAS[c]['peso'] for c in categorias]

    # Distribuir produtos por categoria proporcionalmente
    qtds = np.random.multinomial(cfg.N_PRODUTOS, pesos_cat)

    for cat, qtd in zip(categorias, qtds):
        info = cfg.CATEGORIAS[cat]
        preco_min, preco_max = info['faixa_preco']

        for _ in range(qtd):
            subcat = np.random.choice(info['subcategorias'])
            marca = np.random.choice(info['marcas'])

            # Nome do produto
            templates = NOMES_PRODUTO.get(cat, {}).get(subcat, ['{m} Produto'])
            template = np.random.choice(templates)
            sufixo = np.random.choice(SUFIXOS)
            nome = template.format(m=sufixo)

            # Preços
            preco_original = round(float(np.random.uniform(preco_min, preco_max)), 2)

            # Normal: preco_atual <= preco_original (promoção ativa)
            if np.random.random() < 0.30:
                # 30% com desconto ativo
                desconto = np.random.uniform(0.05, 0.35)
                preco_atual = round(preco_original * (1 - desconto), 2)
            else:
                preco_atual = preco_original

            # Dirty data: ~5% preco_atual > preco_original (promoção invertida)
            if np.random.random() < cfg.DIRTY_RATE:
                preco_atual = round(preco_original * np.random.uniform(1.05, 1.40), 2)

            # Avaliações
            tem_avaliacao = np.random.random() > 0.15
            if tem_avaliacao:
                avaliacao_media = round(float(np.random.uniform(1.0, 5.0)), 1)
                # Distribuição mais realista: maioria entre 3.0-5.0
                avaliacao_media = round(float(np.clip(np.random.normal(3.8, 0.8), 1.0, 5.0)), 1)
                total_avaliacoes = int(np.random.randint(1, 2000))
            else:
                avaliacao_media = None
                total_avaliacoes = 0

            days_offset = int(np.random.randint(0, 365))
            data_cadastro = cfg.PERIODO_INICIO - timedelta(days=days_offset)

            rows.append({
                'produto_id':       produto_id,
                'nome':             f"{marca} {nome}",
                'categoria':        cat,
                'subcategoria':     subcat,
                'marca':            marca,
                'preco_atual':      preco_atual,
                'preco_original':   preco_original,
                'em_estoque':       bool(np.random.random() > 0.08),
                'avaliacao_media':  avaliacao_media,
                'total_avaliacoes': total_avaliacoes,
                'url_imagem':       f"https://cdn.marketplace.com.br/img/{produto_id}.jpg",
                'data_cadastro':    data_cadastro,
                'ativo':            bool(np.random.random() > 0.05),
            })

            produto_id += 1

    df = pd.DataFrame(rows)
    df['data_cadastro'] = pd.to_datetime(df['data_cadastro'], utc=True)

    return df


if __name__ == '__main__':
    df = generate()
    print(f"✓ Produtos: {len(df)} registros")
    print(f"  Categorias: {df['categoria'].value_counts().to_dict()}")
    dirty = df[df['preco_atual'] > df['preco_original']]
    print(f"  Dirty (preço invertido): {len(dirty)} ({len(dirty)/len(df)*100:.1f}%)")
    print(df[['produto_id', 'nome', 'categoria', 'preco_atual', 'preco_original']].head(10))
