"""
Script de Limpeza: Carrinhos
Lê data/mock/output/parquet/carrinhos.parquet, remove anomalias contábeis e temporais e salva os dados limpos.
"""
import os
import pandas as pd
import numpy as np
from datetime import timedelta

def clean_carrinhos(input_path: str, output_parquet: str, output_csv: str) -> pd.DataFrame:
    df = pd.read_parquet(input_path)
    print(f"[CARRINHOS] Registros originais: {len(df):,}")

    for idx, row in df.iterrows():
        subtotal = float(row['valor_subtotal']) if pd.notna(row['valor_subtotal']) else 0.0
        frete = float(row['valor_frete']) if pd.notna(row['valor_frete']) else 0.0
        desconto = float(row['valor_desconto']) if pd.notna(row['valor_desconto']) else 0.0

        # 1. Corrigir frete negativo (ANOM-01)
        if frete < 0:
            frete = abs(frete)
            if frete == 0:
                frete = 15.00
            df.at[idx, 'valor_frete'] = frete

        # 2. Corrigir subtotal zerado ou negativo (ANOM-02)
        if subtotal <= 0:
            subtotal = 120.00
            df.at[idx, 'valor_subtotal'] = subtotal

        # 3. Corrigir desconto excessivo (ANOM-03)
        if desconto > subtotal:
            desconto = round(subtotal * 0.10, 2)
            df.at[idx, 'valor_desconto'] = desconto
        elif desconto < 0:
            desconto = 0.0
            df.at[idx, 'valor_desconto'] = desconto

        # 4. Corrigir equação contábil do total (ANOM-04)
        total_correto = round(subtotal + frete - desconto, 2)
        df.at[idx, 'valor_total'] = total_correto

    # 5. Validação e ordenação temporal
    df['data_criacao'] = pd.to_datetime(df['data_criacao'], utc=True)
    df['data_ultima_atividade'] = pd.to_datetime(df['data_ultima_atividade'], utc=True)
    df['data_abandono'] = pd.to_datetime(df['data_abandono'], utc=True)

    for idx, row in df.iterrows():
        t_cria = row['data_criacao']
        t_ult = row['data_ultima_atividade']
        t_aban = row['data_abandono']

        if pd.notna(t_ult) and t_ult < t_cria:
            df.at[idx, 'data_ultima_atividade'] = t_cria + timedelta(minutes=15)
        if pd.notna(t_aban) and t_aban < t_cria:
            df.at[idx, 'data_abandono'] = t_cria + timedelta(minutes=10)

    # 6. Consistência de Status
    valid_statuses = {"comprado", "abandonado", "expirado", "ativo", "recuperado"}
    for idx, row in df.iterrows():
        st = str(row['status']).lower()
        if st not in valid_statuses:
            df.at[idx, 'status'] = "abandonado" if pd.notna(row['data_abandono']) else "ativo"

    # Salvar
    os.makedirs(os.path.dirname(os.path.abspath(output_parquet)), exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(output_csv)), exist_ok=True)
    df.to_parquet(output_parquet, index=False, engine='pyarrow')
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"[CARRINHOS] Limpeza concluída: {len(df):,} registros limpos salvos em Parquet e CSV.")
    return df

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    inp = os.path.join(base_dir, "data", "mock", "output", "parquet", "carrinhos.parquet")
    out_pq = os.path.join(base_dir, "data", "mock", "output_cleaned", "parquet", "carrinhos.parquet")
    out_csv = os.path.join(base_dir, "data", "mock", "output_cleaned", "csv", "carrinhos.csv")
    clean_carrinhos(inp, out_pq, out_csv)
