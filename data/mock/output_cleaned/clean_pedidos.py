"""
Script de Limpeza: Pedidos
Lê data/mock/output/parquet/pedidos.parquet, valida integridade contábil e datas.
"""
import os
import pandas as pd

def clean_pedidos(input_path: str, output_parquet: str, output_csv: str) -> pd.DataFrame:
    df = pd.read_parquet(input_path)
    print(f"[PEDIDOS] Registros originais: {len(df):,}")

    df['data_pedido'] = pd.to_datetime(df['data_pedido'], utc=True)
    df['created_at'] = pd.to_datetime(df['created_at'], utc=True)

    for idx, row in df.iterrows():
        sub = float(row['valor_subtotal']) if pd.notna(row['valor_subtotal']) else 0.0
        frete = float(row['valor_frete']) if pd.notna(row['valor_frete']) else 0.0
        desc = float(row['valor_desconto']) if pd.notna(row['valor_desconto']) else 0.0
        df.at[idx, 'valor_total'] = round(sub + frete - desc, 2)

    # Salvar
    os.makedirs(os.path.dirname(os.path.abspath(output_parquet)), exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(output_csv)), exist_ok=True)
    df.to_parquet(output_parquet, index=False, engine='pyarrow')
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"[PEDIDOS] Limpeza concluída: {len(df):,} registros limpos salvos em Parquet e CSV.")
    return df

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    inp = os.path.join(base_dir, "data", "mock", "output", "parquet", "pedidos.parquet")
    out_pq = os.path.join(base_dir, "data", "mock", "output_cleaned", "parquet", "pedidos.parquet")
    out_csv = os.path.join(base_dir, "data", "mock", "output_cleaned", "csv", "pedidos.csv")
    clean_pedidos(inp, out_pq, out_csv)
