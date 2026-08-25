#!/usr/bin/env python3
"""
powerpoint-medallion.py
Módulo: view-lake-architecture (Ato 2 / Seção [3] - Arquitetura Lakehouse Medallion)
Wrapper sincronizado com generate_chart.py para manter conformidade e padrão visual único.
"""

from typing import Final
from pathlib import Path
from generate_chart import plot_lake_architecture, COLORS, OUTPUT_POWERPOINT_PATH
import matplotlib.pyplot as plt

def main() -> None:
    print(f"[RUNNING] Gerando visualização Medallion com representação cilíndrica 3D...")
    fig = plot_lake_architecture()
    fig.savefig(str(OUTPUT_POWERPOINT_PATH), dpi=300, bbox_inches="tight", facecolor=COLORS["bg"])
    plt.close(fig)
    print(f"[SUCCESS] Artefato gerado com sucesso em: {OUTPUT_POWERPOINT_PATH}")

if __name__ == "__main__":
    main()
