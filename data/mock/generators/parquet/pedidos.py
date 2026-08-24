"""
pedidos.py — Entrypoint do gerador de pedidos.
Delega para modules.pedidos.PedidosGenerator.
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).resolve().parent))

from modules.pedidos import PedidosGenerator, generate
from modules.clientes import ClientesGenerator
from modules.carrinhos import CarrinhosGenerator
from modules.eventos_resgate import EventosResgateGenerator
from config.profiles import get_standard_profile

if __name__ == '__main__':
    settings = get_standard_profile()
    clientes_df = ClientesGenerator(settings).run()
    carrinhos_df = CarrinhosGenerator(settings).run(clientes_df=clientes_df)
    resgate_df = EventosResgateGenerator(settings).run(carrinhos_df=carrinhos_df, clientes_df=clientes_df)

    gen = PedidosGenerator(settings)
    df = gen.run(carrinhos_df=carrinhos_df, clientes_df=clientes_df, resgate_df=resgate_df)

    print(f"✓ Pedidos: {len(df)} registros")
    print(f"  Recuperados: {df['origem_recuperacao'].sum()} ({df['origem_recuperacao'].mean()*100:.1f}%)")
    print(f"  Valor médio: R${df['valor_total'].mean():.2f}")
