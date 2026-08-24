"""
eventos_carrinho.py — Entrypoint do gerador de telemetria de carrinho.
Delega para modules.eventos_carrinho.EventosCarrinhoGenerator.
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).resolve().parent))

from modules.eventos_carrinho import EventosCarrinhoGenerator, generate
from modules.clientes import ClientesGenerator
from modules.carrinhos import CarrinhosGenerator
from config.profiles import get_standard_profile

if __name__ == '__main__':
    settings = get_standard_profile()
    clientes_df = ClientesGenerator(settings).run()
    carrinhos_df = CarrinhosGenerator(settings).run(clientes_df=clientes_df)

    gen = EventosCarrinhoGenerator(settings)
    df = gen.run(carrinhos_df=carrinhos_df)

    print(f"✓ Eventos Carrinho: {len(df)} registros")
    print(f"  Média eventos/carrinho: {len(df)/len(carrinhos_df):.1f}")
    print(f"  Tipos de evento: {df['tipo_evento'].value_counts().to_dict()}")
