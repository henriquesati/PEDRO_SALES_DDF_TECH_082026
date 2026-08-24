"""
Wrapper do Gráfico do Item 6 para o Pitch Executivo.
Importa e executa a função canônica de geração de pipelines/case-item-06/scripts/generate_chart.py,
salvando o artefato de imagem no diretório local da view do pitch.
"""

from typing import Final
import os
import sys
import matplotlib.pyplot as plt

# Localização e caminhos
VIEW_DIR: Final[str] = os.path.abspath(os.path.dirname(__file__))
BASE_DIR: Final[str] = os.path.abspath(os.path.join(VIEW_DIR, "..", "..", "..", ".."))
OUTPUT_IMAGE_PATH: Final[str] = os.path.join(VIEW_DIR, "chart_caseitem06_kimball_model.png")

import importlib.util

# Caminho do gerador canônico
CASE_06_SCRIPT_PATH: Final[str] = os.path.join(BASE_DIR, "pipelines", "case-item-06", "scripts", "generate_chart.py")

spec = importlib.util.spec_from_file_location("case06_generate_chart", CASE_06_SCRIPT_PATH)
if spec is None or spec.loader is None:
    raise ImportError(f"Não foi possível carregar o módulo em: {CASE_06_SCRIPT_PATH}")
case06_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(case06_module)

plot_kimball_dashboard = case06_module.plot_kimball_dashboard
generate_chart_artifacts = case06_module.generate_chart_artifacts

def main() -> None:
    print("[PITCH VIEW: CASE ITEM 06] Executando gerador canônico de pipelines/case-item-06...")
    
    # 1. Gera os artefatos canônicos no diretório original do case 06
    generated_paths = generate_chart_artifacts()
    
    # 2. Gera e salva a cópia local para a view do pitch
    fig = plot_kimball_dashboard()
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    
    print(f"[PITCH VIEW: CASE ITEM 06] Artefato sincronizado com sucesso em:\n -> {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    main()
