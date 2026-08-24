"""
eventos_resgate.py — Entrypoint do gerador de eventos de resgate.
Delega para modules.eventos_resgate.EventosResgateGenerator.
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).resolve().parent))

from modules.eventos_resgate import EventosResgateGenerator, generate
from modules.clientes import ClientesGenerator
from modules.carrinhos import CarrinhosGenerator
from config.profiles import get_standard_profile

if __name__ == '__main__':
    settings = get_standard_profile()
    clientes_df = ClientesGenerator(settings).run()
    carrinhos_df = CarrinhosGenerator(settings).run(clientes_df=clientes_df)

    gen = EventosResgateGenerator(settings)
    df = gen.run(carrinhos_df=carrinhos_df, clientes_df=clientes_df)

    print(f"✓ Eventos Resgate: {len(df)} registros")
    print(f"  Canais: {df['canal'].value_counts().to_dict()}")
    print(f"  Conversões: {df['sucesso'].sum()} ({df['sucesso'].mean()*100:.1f}%)")
    print("\nAuditoria de Anomalias:")
    print(gen.audit.to_dataframe()[['anomaly', 'target_min_pct', 'affected_rows', 'actual_pct']])
