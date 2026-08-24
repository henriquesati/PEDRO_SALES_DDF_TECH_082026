"""
Script de Limpeza: Clientes
Lê data/mock/output/parquet/clientes.parquet, remove inconsistências e salva os dados limpos.
"""
import os
import re
import pandas as pd
import numpy as np

def clean_clientes(input_path: str, output_parquet: str, output_csv: str) -> pd.DataFrame:
    df = pd.read_parquet(input_path)
    print(f"[CLIENTES] Registros originais: {len(df):,}")

    # 1. Tratar e-mails nulos ou malformados
    for idx, row in df.iterrows():
        email = str(row['email']) if pd.notna(row['email']) else ""
        primeiro_nome = str(row['primeiro_nome']).lower() if pd.notna(row['primeiro_nome']) else "cliente"
        cid = row['cliente_id']
        
        if not email or email == "None" or email == "nan":
            email = f"{primeiro_nome}.{cid}@exemplo.com.br"
        
        # Corrigir duplicação de @ ou extensões inválidas
        email = email.replace("@@", "@").replace("..com_invalido", ".com.br").replace("..com", ".com.br")
        if "@" not in email:
            email = f"{primeiro_nome}.{cid}@exemplo.com.br"
        
        # Padronizar lowercase
        df.at[idx, 'email'] = email.strip().lower()

    # 2. Padronizar formato de telefones
    for idx, row in df.iterrows():
        tel = str(row['telefone']) if pd.notna(row['telefone']) else ""
        if tel and tel != "None" and tel != "nan":
            digits = re.sub(r'\D', '', tel)
            if len(digits) == 11:
                df.at[idx, 'telefone'] = f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
            elif len(digits) == 10:
                df.at[idx, 'telefone'] = f"({digits[:2]}) 9{digits[2:6]}-{digits[6:]}"
            else:
                df.at[idx, 'telefone'] = f"(11) 9{str(row['cliente_id']).zfill(8)[:8]}"

    # 3. Corrigir inconsistência de LTV para clientes sem compras
    mask_zero_compras = (df['total_compras'] == 0)
    df.loc[mask_zero_compras, 'lifetime_value'] = 0.0

    # Garantir ordenação temporal de compras
    df['data_criacao'] = pd.to_datetime(df['data_criacao'], utc=True)
    df['data_primeira_compra'] = pd.to_datetime(df['data_primeira_compra'], errors='coerce')
    df['data_ultima_compra'] = pd.to_datetime(df['data_ultima_compra'], errors='coerce')

    # Salvar
    os.makedirs(os.path.dirname(os.path.abspath(output_parquet)), exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(output_csv)), exist_ok=True)
    df.to_parquet(output_parquet, index=False, engine='pyarrow')
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"[CLIENTES] Limpeza concluída: {len(df):,} registros limpos salvos em Parquet e CSV.")
    return df

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    inp = os.path.join(base_dir, "data", "mock", "output", "parquet", "clientes.parquet")
    out_pq = os.path.join(base_dir, "data", "mock", "output_cleaned", "parquet", "clientes.parquet")
    out_csv = os.path.join(base_dir, "data", "mock", "output_cleaned", "csv", "clientes.csv")
    clean_clientes(inp, out_pq, out_csv)
