"""
clean_all.py — Orquestrador de Limpeza de Datasets (Cart Recovery).

Lê os datasets existentes em data/mock/output/parquet/, executa todas as limpezas de dados
e salva os resultados tratados em data/mock/output_cleaned/ (parquet e csv).
"""

import os
import sys
from pathlib import Path

# Adiciona diretório local ao sys.path
CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

from clean_clientes import clean_clientes
from clean_produtos import clean_produtos
from clean_carrinhos import clean_carrinhos
from clean_itens_carrinho import clean_itens_carrinho
from clean_eventos_carrinho import clean_eventos_carrinho
from clean_eventos_resgate import clean_eventos_resgate
from clean_pedidos import clean_pedidos

BASE_DIR = CURRENT_DIR.parent.parent.parent # wheels root
INPUT_PARQUET_DIR = BASE_DIR / "data" / "mock" / "output" / "parquet"

def run_cleaning_pipeline():
    print("=" * 75)
    print(" INICIANDO PIPELINE DE LIMPEZA DE DADOS (OUTPUT_CLEANED)")
    print("=" * 75)
    print(f" Origem: {INPUT_PARQUET_DIR}\n")

    primary_pq_dir = CURRENT_DIR / "parquet"
    primary_csv_dir = CURRENT_DIR / "csv"
    primary_pq_dir.mkdir(parents=True, exist_ok=True)
    primary_csv_dir.mkdir(parents=True, exist_ok=True)

    # 1. Clientes
    print("-> 1/7 Limpando Clientes...")
    clean_clientes(
        str(INPUT_PARQUET_DIR / "clientes.parquet"),
        str(primary_pq_dir / "clientes.parquet"),
        str(primary_csv_dir / "clientes.csv")
    )

    # 2. Produtos
    print("\n-> 2/7 Limpando Produtos...")
    clean_produtos(
        str(INPUT_PARQUET_DIR / "produtos.parquet"),
        str(primary_pq_dir / "produtos.parquet"),
        str(primary_csv_dir / "produtos.csv")
    )

    # 3. Carrinhos
    print("\n-> 3/7 Limpando Carrinhos...")
    clean_carrinhos(
        str(INPUT_PARQUET_DIR / "carrinhos.parquet"),
        str(primary_pq_dir / "carrinhos.parquet"),
        str(primary_csv_dir / "carrinhos.csv")
    )

    # 4. Itens do Carrinho
    print("\n-> 4/7 Limpando Itens do Carrinho...")
    clean_itens_carrinho(
        str(INPUT_PARQUET_DIR / "itens_carrinho.parquet"),
        str(primary_pq_dir / "itens_carrinho.parquet"),
        str(primary_csv_dir / "itens_carrinho.csv")
    )

    # 5. Eventos do Carrinho
    print("\n-> 5/7 Limpando Eventos do Carrinho...")
    clean_eventos_carrinho(
        str(INPUT_PARQUET_DIR / "eventos_carrinho.parquet"),
        str(primary_pq_dir / "eventos_carrinho.parquet"),
        str(primary_csv_dir / "eventos_carrinho.csv")
    )

    # 6. Eventos de Resgate
    print("\n-> 6/7 Limpando Eventos de Resgate...")
    clean_eventos_resgate(
        str(INPUT_PARQUET_DIR / "eventos_resgate.parquet"),
        str(primary_pq_dir / "eventos_resgate.parquet"),
        str(primary_csv_dir / "eventos_resgate.csv")
    )

    # 7. Pedidos
    print("\n-> 7/7 Limpando Pedidos...")
    clean_pedidos(
        str(INPUT_PARQUET_DIR / "pedidos.parquet"),
        str(primary_pq_dir / "pedidos.parquet"),
        str(primary_csv_dir / "pedidos.csv")
    )

    print("\n" + "=" * 75)
    print(" [SUCESSO] Todas as 7 entidades foram limpas e salvas com sucesso em output_cleaned!")
    print("=" * 75)

if __name__ == "__main__":
    run_cleaning_pipeline()
