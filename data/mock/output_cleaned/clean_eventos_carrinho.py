"""
Script de Limpeza: Eventos do Carrinho
Lê data/mock/output/parquet/eventos_carrinho.parquet, padroniza telemetria e datas.
"""
import os
import pandas as pd

def clean_eventos_carrinho(input_path: str, output_parquet: str, output_csv: str) -> pd.DataFrame:
    df = pd.read_parquet(input_path)
    print(f"[EVENTOS_CARRINHO] Registros originais: {len(df):,}")

    df['timestamp_evento'] = pd.to_datetime(df['timestamp_evento'], utc=True)
    df = df.dropna(subset=['evento_id', 'carrinho_id'])
    df['evento_id'] = df['evento_id'].astype(int)
    df['carrinho_id'] = df['carrinho_id'].astype(int)

    # Salvar
    os.makedirs(os.path.dirname(os.path.abspath(output_parquet)), exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(output_csv)), exist_ok=True)
    df.to_parquet(output_parquet, index=False, engine='pyarrow')
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"[EVENTOS_CARRINHO] Limpeza concluída: {len(df):,} registros limpos salvos em Parquet e CSV.")
    return df

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    inp = os.path.join(base_dir, "data", "mock", "output", "parquet", "eventos_carrinho.parquet")
    out_pq = os.path.join(base_dir, "data", "mock", "output_cleaned", "parquet", "eventos_carrinho.parquet")
    out_csv = os.path.join(base_dir, "data", "mock", "output_cleaned", "csv", "eventos_carrinho.csv")
    clean_eventos_carrinho(inp, out_pq, out_csv)
