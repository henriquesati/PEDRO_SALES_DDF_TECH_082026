"""
clientes.py — Entrypoint do gerador de clientes.
Delega para modules.clientes.ClientesGenerator.
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).resolve().parent))

from modules.clientes import ClientesGenerator, generate
from config.profiles import get_standard_profile

if __name__ == '__main__':
    settings = get_standard_profile()
    gen = ClientesGenerator(settings)
    df = gen.run()
    print(f"✓ Clientes: {len(df)} registros")
    print(f"  Distribuição RFM: {df['segmento_rfm'].value_counts().to_dict()}")
    print(f"  Emails nulos: {df['email'].isna().sum()} ({df['email'].isna().mean()*100:.1f}%)")
    print(f"  Telefones nulos: {df['telefone'].isna().sum()} ({df['telefone'].isna().mean()*100:.1f}%)")
    print("\nAuditoria de Anomalias:")
    print(gen.audit.to_dataframe()[['anomaly', 'target_min_pct', 'affected_rows', 'actual_pct']])
