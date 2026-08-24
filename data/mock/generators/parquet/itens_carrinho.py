"""
itens_carrinho.py — Entrypoint do gerador de itens do carrinho.
Delega para modules.itens_carrinho.ItensCarrinhoGenerator.
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).resolve().parent))

from modules.itens_carrinho import ItensCarrinhoGenerator, generate
from modules.clientes import ClientesGenerator
from modules.produtos import ProdutosGenerator
from modules.carrinhos import CarrinhosGenerator
from config.profiles import get_standard_profile

if __name__ == '__main__':
    settings = get_standard_profile()
    clientes_df = ClientesGenerator(settings).run()
    produtos_df = ProdutosGenerator(settings).run()
    carrinhos_df = CarrinhosGenerator(settings).run(clientes_df=clientes_df)

    gen = ItensCarrinhoGenerator(settings)
    df = gen.run(carrinhos_df=carrinhos_df, produtos_df=produtos_df)

    print(f"✓ Itens Carrinho: {len(df)} registros")
    print(f"  Média itens/carrinho: {len(df)/len(carrinhos_df):.1f}")
    print("\nAuditoria de Anomalias:")
    print(gen.audit.to_dataframe()[['anomaly', 'target_min_pct', 'affected_rows', 'actual_pct']])
