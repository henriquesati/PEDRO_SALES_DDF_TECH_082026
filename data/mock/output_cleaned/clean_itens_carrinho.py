"""
Script de Limpeza: Itens do Carrinho
Lê data/mock/output/parquet/itens_carrinho.parquet, remove inversões temporais e erros de cálculo.
"""
import os
import pandas as pd
import numpy as np
from datetime import timedelta

def clean_itens_carrinho(input_path: str, output_parquet: str, output_csv: str) -> pd.DataFrame:
    df = pd.read_parquet(input_path)
    print(f"[ITENS_CARRINHO] Registros originais: {len(df):,}")

    df['data_adicao'] = pd.to_datetime(df['data_adicao'], utc=True)
    df['data_remocao'] = pd.to_datetime(df['data_remocao'], utc=True)

    for idx, row in df.iterrows():
        qtd = int(row['quantidade']) if pd.notna(row['quantidade']) and row['quantidade'] > 0 else 1
        preco_u = float(row['preco_unitario']) if pd.notna(row['preco_unitario']) and row['preco_unitario'] > 0 else 49.90
        
        df.at[idx, 'quantidade'] = qtd
        df.at[idx, 'preco_unitario'] = preco_u
        df.at[idx, 'preco_total'] = round(qtd * preco_u, 2)

        t_adc = row['data_adicao']
        t_rem = row['data_remocao']
        if pd.notna(t_rem) and pd.notna(t_adc) and t_rem < t_adc:
            df.at[idx, 'data_remocao'] = t_adc + timedelta(minutes=int(np.random.randint(2, 30)))

    # Salvar
    os.makedirs(os.path.dirname(os.path.abspath(output_parquet)), exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(output_csv)), exist_ok=True)
    df.to_parquet(output_parquet, index=False, engine='pyarrow')
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"[ITENS_CARRINHO] Limpeza concluída: {len(df):,} registros limpos salvos em Parquet e CSV.")
    return df

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    inp = os.path.join(base_dir, "data", "mock", "output", "parquet", "itens_carrinho.parquet")
    out_pq = os.path.join(base_dir, "data", "mock", "output_cleaned", "parquet", "itens_carrinho.parquet")
    out_csv = os.path.join(base_dir, "data", "mock", "output_cleaned", "csv", "itens_carrinho.csv")
    clean_itens_carrinho(inp, out_pq, out_csv)
