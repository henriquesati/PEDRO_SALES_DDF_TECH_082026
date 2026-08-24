"""
carrinhos.py — Entrypoint do gerador de carrinhos.
Delega para modules.carrinhos.CarrinhosGenerator.
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).resolve().parent))

from modules.carrinhos import CarrinhosGenerator, generate, save_df
from modules.clientes import ClientesGenerator
from config.profiles import get_standard_profile

if __name__ == '__main__':
    settings = get_standard_profile()
    clientes_df = ClientesGenerator(settings).run()
    gen = CarrinhosGenerator(settings)
    df = gen.run(clientes_df=clientes_df)

    print(f"✓ Carrinhos: {len(df)} registros")
    print(f"  Status: {df['status'].value_counts().to_dict()}")
    abandonados = df[df['_lifecycle'].isin(['abandonado', 'recuperado_comprado', 'recuperado_pendente', 'expirado'])]
    recuperados = df[df['_lifecycle'] == 'recuperado_comprado']
    print(f"  Taxa abandono: {len(abandonados)/len(df)*100:.1f}%")
    print(f"  Taxa recuperação: {len(recuperados)/len(abandonados)*100:.1f}%")
    print("\nAuditoria de Anomalias:")
    print(gen.audit.to_dataframe()[['anomaly', 'target_min_pct', 'affected_rows', 'actual_pct']])
