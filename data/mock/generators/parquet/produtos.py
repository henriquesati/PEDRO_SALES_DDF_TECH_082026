"""
produtos.py — Entrypoint do gerador de produtos.
Delega para modules.produtos.ProdutosGenerator.
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).resolve().parent))

from modules.produtos import ProdutosGenerator, generate
from config.profiles import get_standard_profile

if __name__ == '__main__':
    settings = get_standard_profile()
    gen = ProdutosGenerator(settings)
    df = gen.run()
    print(f"✓ Produtos: {len(df)} registros")
    print(f"  Categorias: {df['categoria'].value_counts().to_dict()}")
    dirty = df[df['preco_atual'] > df['preco_original']]
    print(f"  Promoções invertidas: {len(dirty)} ({len(dirty)/len(df)*100:.1f}%)")
    print("\nAuditoria de Anomalias:")
    print(gen.audit.to_dataframe()[['anomaly', 'target_min_pct', 'affected_rows', 'actual_pct']])
