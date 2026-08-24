"""
Script de Limpeza: Produtos
Lê data/mock/output/parquet/produtos.parquet, remove promoções invertidas e inconsistências de catálogo.
"""
import os
import pandas as pd
import numpy as np

def clean_produtos(input_path: str, output_parquet: str, output_csv: str) -> pd.DataFrame:
    df = pd.read_parquet(input_path)
    print(f"[PRODUTOS] Registros originais: {len(df):,}")

    # 1. Corrigir promoções invertidas (preco_atual > preco_original)
    for idx, row in df.iterrows():
        orig = float(row['preco_original'])
        atual = float(row['preco_atual'])
        if atual > orig:
            # Reajustar preço atual para ter desconto normal entre 5% e 25%
            df.at[idx, 'preco_atual'] = round(orig * 0.85, 2)
        elif atual <= 0:
            df.at[idx, 'preco_atual'] = orig

    # 2. Consistência de avaliações
    for idx, row in df.iterrows():
        total_av = int(row['total_avaliacoes']) if pd.notna(row['total_avaliacoes']) else 0
        if total_av == 0:
            df.at[idx, 'avaliacao_media'] = None
        elif pd.isna(row['avaliacao_media']):
            df.at[idx, 'avaliacao_media'] = 4.2

    df['data_cadastro'] = pd.to_datetime(df['data_cadastro'], utc=True)
    df['ativo'] = df['ativo'].astype(bool)
    df['em_estoque'] = df['em_estoque'].astype(bool)

    # Salvar
    os.makedirs(os.path.dirname(os.path.abspath(output_parquet)), exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(output_csv)), exist_ok=True)
    df.to_parquet(output_parquet, index=False, engine='pyarrow')
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"[PRODUTOS] Limpeza concluída: {len(df):,} registros limpos salvos em Parquet e CSV.")
    return df

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    inp = os.path.join(base_dir, "data", "mock", "output", "parquet", "produtos.parquet")
    out_pq = os.path.join(base_dir, "data", "mock", "output_cleaned", "parquet", "produtos.parquet")
    out_csv = os.path.join(base_dir, "data", "mock", "output_cleaned", "csv", "produtos.csv")
    clean_produtos(inp, out_pq, out_csv)
