"""
Script de Limpeza: Eventos de Resgate
Lê data/mock/output/parquet/eventos_resgate.parquet, corrige funil de conversão e datas.
"""
import os
import pandas as pd
import numpy as np
from datetime import timedelta

def clean_eventos_resgate(input_path: str, output_parquet: str, output_csv: str) -> pd.DataFrame:
    df = pd.read_parquet(input_path)
    print(f"[EVENTOS_RESGATE] Registros originais: {len(df):,}")

    ts_cols = ['data_schedule', 'data_envio', 'data_abertura', 'data_primeiro_clique', 'data_conversao', 'created_at']
    for col in ts_cols:
        df[col] = pd.to_datetime(df[col], utc=True)

    for idx, row in df.iterrows():
        t_envio = row['data_envio']
        t_abertura = row['data_abertura']
        t_clique = row['data_primeiro_clique']
        t_conv = row['data_conversao']
        sucesso = bool(row['sucesso'])

        # Inversão de abertura vs envio
        if pd.notna(t_abertura) and pd.notna(t_envio) and t_abertura < t_envio:
            t_abertura = t_envio + timedelta(minutes=int(np.random.randint(5, 60)))
            df.at[idx, 'data_abertura'] = t_abertura

        # Clique sem abertura
        if pd.notna(t_clique):
            if pd.isna(t_abertura):
                t_abertura = t_envio + timedelta(minutes=10)
                df.at[idx, 'data_abertura'] = t_abertura
            if t_clique < t_abertura:
                t_clique = t_abertura + timedelta(minutes=5)
                df.at[idx, 'data_primeiro_clique'] = t_clique

        # Conversão sem clique
        if sucesso:
            if pd.isna(t_clique):
                t_clique = (t_abertura or t_envio) + timedelta(minutes=10)
                df.at[idx, 'data_primeiro_clique'] = t_clique
            if pd.isna(t_conv) or t_conv < t_clique:
                df.at[idx, 'data_conversao'] = t_clique + timedelta(minutes=15)

    # Salvar
    os.makedirs(os.path.dirname(os.path.abspath(output_parquet)), exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(output_csv)), exist_ok=True)
    df.to_parquet(output_parquet, index=False, engine='pyarrow')
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"[EVENTOS_RESGATE] Limpeza concluída: {len(df):,} registros limpos salvos em Parquet e CSV.")
    return df

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    inp = os.path.join(base_dir, "data", "mock", "output", "parquet", "eventos_resgate.parquet")
    out_pq = os.path.join(base_dir, "data", "mock", "output_cleaned", "parquet", "eventos_resgate.parquet")
    out_csv = os.path.join(base_dir, "data", "mock", "output_cleaned", "csv", "eventos_resgate.csv")
    clean_eventos_resgate(inp, out_pq, out_csv)
