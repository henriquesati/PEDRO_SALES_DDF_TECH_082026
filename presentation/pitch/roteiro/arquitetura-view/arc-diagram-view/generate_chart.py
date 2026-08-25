#!/usr/bin/env python3
"""
generate_l2r_charts.py
Gera tanto a versão vazia (template oficial de animação no PowerPoint)
quanto a versão preenchida (populated) com todos os ícones mapeados e nomeados
para guiar a montagem e apresentação no PowerPoint.

Estrutura de 5 Pilares de Negócio (Alinhada ao Roteiro e Data Platform Spec):
1. INGESTÃO (#1E3A8A)
2. VALIDAÇÃO (#2563EB)
3. MODELAGEM (#7C3AED)
4. GOVERNANÇA (#D97706)
5. INTELIGÊNCIA (#059669)
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from PIL import Image
import numpy as np

# Diretórios
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
ICONS_DIR.mkdir(parents=True, exist_ok=True)

# Paleta Final Aprovada com os 5 Nomes de Negócio
PALETTE = {
    "bg": "#FFFFFF",
    "pillars": [
        {
            "num": "1",
            "name": "INGESTÃO",
            "subtitle": "Captura & Buffering Raw",
            "color": "#1E3A8A",      # Navy Blue oficial
            "arrow_label": "INGESTÃO",
            "icons": [
                {"file": "kinesis.png", "name": "Kinesis Stream"},
                {"file": "firehose.png", "name": "Firehose"},
                {"file": "s3.png", "name": "S3 Raw Lake"},
            ],
        },
        {
            "num": "2",
            "name": "VALIDAÇÃO",
            "subtitle": "Data Quality & Quarentena",
            "color": "#2563EB",      # Royal Blue oficial
            "arrow_label": "VALIDAÇÃO",
            "icons": [
                {"file": "lambda.png", "name": "AWS Lambda"},
                {"file": "sqs.png", "name": "SQS DLQ"},
                {"file": "dynamodb.png", "name": "DynamoDB Quarentena"},
                {"file": "datadog.png", "name": "CloudWatch Alarms"},
            ],
        },
        {
            "num": "3",
            "name": "MODELAGEM",
            "subtitle": "Star Schema & Sustentação DW",
            "color": "#7C3AED",      # Vibrant Purple
            "arrow_label": "MODELAGEM",
            "icons": [
                {"file": "glue.png", "name": "Glue (PySpark)"},
                {"file": "redshift.png", "name": "Redshift DW"},
                {"file": "airflow.png", "name": "MWAA Airflow"},
                {"file": "redis.png", "name": "Redis ElastiCache"},
                {"file": "docker.png", "name": "Docker / ECR"},
                {"file": "terraform.png", "name": "Terraform / IaC"},
                {"file": "github-actions.png", "name": "GitHub CI/CD"},
                {"file": "secrets-manager.png", "name": "Secrets Manager"},
            ],
        },
        {
            "num": "4",
            "name": "GOVERNANÇA",
            "subtitle": "Catálogo, Linhagem & LGPD",
            "color": "#D97706",      # Amber Orange oficial
            "arrow_label": "GOVERNANÇA",
            "icons": [
                {"file": "lake-formation.png", "name": "Lake Formation"},
                {"file": "datahub.png", "name": "DataHub Catalog"},
            ],
        },
        {
            "num": "5",
            "name": "INTELIGÊNCIA",
            "subtitle": "BI, Data Apps & Resgate",
            "color": "#059669",      # Emerald Green oficial
            "arrow_label": "INTELIGÊNCIA",
            "icons": [
                {"file": "powerbi.png", "name": "PowerBI / Tableau"},
                {"file": "streamlit.png", "name": "Streamlit App"},
                {"file": "genai.png", "name": "Copilot GenAI"},
                {"file": "eventbridge.png", "name": "Alertas de Resgate"},
            ],
        },
    ],
    # Seta Contínua Âmbar Translúcida
    "arrow_bg": "#D97706",           # Amber Orange do Quadrado 4
    "arrow_alpha": 0.72,             # Opacidade suave
    "arrow_border": "#B45309",       # Borda Âmbar Marcante
    "arrow_text": "#FFFFFF",         # Texto Branco Nítido
    "arrow_symbol": "#FEF3C7",       # Conector ➔ em Âmbar Claro
    "external_label_text": "#475569",
}


def draw_pure_empty_template(out_filename: str):
    """
    Renderiza o template vazio para animações no PowerPoint.
    """
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor(PALETTE["bg"])
    ax.set_facecolor(PALETTE["bg"])
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 900)
    ax.axis("off")

    col_w = 260
    col_gap = 35
    start_x = 80
    arrow_y = 270
    arrow_h = 52
    
    block_y = arrow_y + arrow_h + 24
    block_h = 340

    # 1. Blocos Retos com Números 1 a 5
    for i, p_cfg in enumerate(PALETTE["pillars"]):
        cx = start_x + i * (col_w + col_gap)

        block = Rectangle(
            (cx, block_y),
            col_w,
            block_h,
            facecolor=p_cfg["color"],
            edgecolor="#FFFFFF",
            linewidth=3.5,
            zorder=2,
        )
        ax.add_patch(block)

        center_x = cx + (col_w / 2)
        number_y = block_y + block_h - 22

        ax.text(
            center_x,
            number_y,
            p_cfg["num"],
            fontsize=11.5,
            fontweight="bold",
            color="#FFFFFF",
            ha="center",
            va="center",
            zorder=5,
        )

    # 2. Seta Central Contínua
    arrow_start_x = start_x - 10
    arrow_body_end_x = start_x + 5 * col_w + 4 * col_gap + 15
    arrow_tip_x = arrow_body_end_x + 35

    arrow_rect = Rectangle(
        (arrow_start_x, arrow_y),
        arrow_body_end_x - arrow_start_x,
        arrow_h,
        facecolor=PALETTE["arrow_bg"],
        edgecolor=PALETTE["arrow_border"],
        alpha=PALETTE["arrow_alpha"],
        linewidth=2.0,
        zorder=6,
    )
    ax.add_patch(arrow_rect)

    tip_points = [
        (arrow_body_end_x, arrow_y - 14),
        (arrow_tip_x, arrow_y + (arrow_h / 2)),
        (arrow_body_end_x, arrow_y + arrow_h + 14),
    ]
    arrow_tip = Polygon(
        tip_points,
        closed=True,
        facecolor=PALETTE["arrow_bg"],
        edgecolor=PALETTE["arrow_border"],
        alpha=PALETTE["arrow_alpha"],
        linewidth=2.0,
        zorder=7,
    )
    ax.add_patch(arrow_tip)

    # 3. Tópicos de Negócio dentro da seta
    for i, p_cfg in enumerate(PALETTE["pillars"]):
        cx = start_x + i * (col_w + col_gap)
        pillar_center_x = cx + (col_w / 2)

        ax.text(
            pillar_center_x,
            arrow_y + (arrow_h / 2),
            p_cfg["arrow_label"],
            fontsize=9.2,
            fontweight="bold",
            color=PALETTE["arrow_text"],
            ha="center",
            va="center",
            zorder=8,
        )

        if i < 4:
            sep_x = cx + col_w + (col_gap / 2)
            ax.text(
                sep_x,
                arrow_y + (arrow_h / 2),
                "➔",
                fontsize=11,
                fontweight="bold",
                color=PALETTE["arrow_symbol"],
                ha="center",
                va="center",
                zorder=8,
            )

    # 4. Texto Explicativo Abaixo da Seta
    label_y = arrow_y - 36
    external_explanation = "FLUXO CONTÍNUO DO CICLO DE VIDA ANALÍTICO"

    ann_box = Rectangle(
        (540, label_y - 14),
        520,
        28,
        facecolor="#F8FAFC",
        edgecolor="#CBD5E1",
        linewidth=1.0,
        zorder=6,
    )
    ax.add_patch(ann_box)

    ax.text(
        800,
        label_y,
        external_explanation,
        fontsize=9.5,
        fontweight="bold",
        color=PALETTE["external_label_text"],
        ha="center",
        va="center",
        zorder=7,
    )

    out_path_assets = ASSETS_DIR / out_filename
    out_path_base = BASE_DIR / out_filename
    plt.savefig(
        out_path_assets,
        dpi=300,
        bbox_inches="tight",
        facecolor=PALETTE["bg"],
        edgecolor="none",
    )
    plt.savefig(
        out_path_base,
        dpi=300,
        bbox_inches="tight",
        facecolor=PALETTE["bg"],
        edgecolor="none",
    )
    plt.close(fig)
    print(f"[OK] Template vazio gerado com sucesso: {out_path_base}")


def draw_populated_reference(out_filename: str):
    """
    Renderiza o gráfico de referência preenchido com todos os ícones e nomes de serviços,
    mostrando exatamente onde colar cada ícone no PowerPoint.
    """
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor(PALETTE["bg"])
    ax.set_facecolor(PALETTE["bg"])
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 900)
    ax.axis("off")

    col_w = 260
    col_gap = 35
    start_x = 80
    arrow_y = 270
    arrow_h = 52
    
    block_y = arrow_y + arrow_h + 24
    block_h = 340

    # 1. Blocos com Ícones e Nomes Mapeados
    for i, p_cfg in enumerate(PALETTE["pillars"]):
        cx = start_x + i * (col_w + col_gap)
        center_x = cx + (col_w / 2)

        # Bloco Sólido com borda branca
        block = Rectangle(
            (cx, block_y),
            col_w,
            block_h,
            facecolor=p_cfg["color"],
            edgecolor="#FFFFFF",
            linewidth=3.5,
            zorder=2,
        )
        ax.add_patch(block)

        # Número discreto no topo
        number_y = block_y + block_h - 22
        ax.text(
            center_x,
            number_y,
            p_cfg["num"],
            fontsize=11.5,
            fontweight="bold",
            color="#FFFFFF",
            ha="center",
            va="center",
            zorder=5,
        )

        # Subtítulo da etapa no topo do bloco
        ax.text(
            center_x,
            number_y - 20,
            p_cfg["subtitle"],
            fontsize=7.8,
            fontweight="bold",
            color="#FFFFFF",
            ha="center",
            va="center",
            zorder=5,
            alpha=0.88,
        )

        # Renderização dos Ícones e Nomes dentro do Bloco
        icons_list = p_cfg["icons"]
        num_icons = len(icons_list)
        
        # Grid para os ícones
        content_top = block_y + block_h - 58
        content_bottom = block_y + 12
        available_h = content_top - content_bottom

        if num_icons <= 4:
            # Layout em 1 coluna vertical
            row_h = available_h / max(num_icons, 1)
            for idx, icon_info in enumerate(icons_list):
                iy = content_top - (idx + 0.5) * row_h
                icon_path = ICONS_DIR / icon_info["file"]
                
                # Renderiza ícone se existir
                if icon_path.exists():
                    try:
                        img = Image.open(icon_path).convert("RGBA")
                        icon_size = 28
                        ax.imshow(
                            img,
                            extent=(cx + 20, cx + 20 + icon_size, iy - icon_size / 2, iy + icon_size / 2),
                            zorder=6,
                        )
                    except Exception:
                        pass

                # Nome do serviço / tecnologia
                ax.text(
                    cx + 56,
                    iy,
                    icon_info["name"],
                    fontsize=8.2,
                    fontweight="bold",
                    color="#FFFFFF",
                    ha="left",
                    va="center",
                    zorder=6,
                )
        else:
            # Layout em 2 colunas para o Bloco 3 (Modelagem com 8 itens)
            num_rows = (num_icons + 1) // 2
            row_h = available_h / num_rows
            col_w_half = (col_w - 20) / 2

            for idx, icon_info in enumerate(icons_list):
                col_idx = idx % 2
                row_idx = idx // 2
                
                ix = cx + 10 + col_idx * col_w_half
                iy = content_top - (row_idx + 0.5) * row_h
                icon_path = ICONS_DIR / icon_info["file"]
                
                if icon_path.exists():
                    try:
                        img = Image.open(icon_path).convert("RGBA")
                        icon_size = 22
                        ax.imshow(
                            img,
                            extent=(ix + 2, ix + 2 + icon_size, iy - icon_size / 2, iy + icon_size / 2),
                            zorder=6,
                        )
                    except Exception:
                        pass

                ax.text(
                    ix + 28,
                    iy,
                    icon_info["name"],
                    fontsize=6.8,
                    fontweight="bold",
                    color="#FFFFFF",
                    ha="left",
                    va="center",
                    zorder=6,
                )

    # 2. Seta Central Contínua
    arrow_start_x = start_x - 10
    arrow_body_end_x = start_x + 5 * col_w + 4 * col_gap + 15
    arrow_tip_x = arrow_body_end_x + 35

    arrow_rect = Rectangle(
        (arrow_start_x, arrow_y),
        arrow_body_end_x - arrow_start_x,
        arrow_h,
        facecolor=PALETTE["arrow_bg"],
        edgecolor=PALETTE["arrow_border"],
        alpha=PALETTE["arrow_alpha"],
        linewidth=2.0,
        zorder=6,
    )
    ax.add_patch(arrow_rect)

    tip_points = [
        (arrow_body_end_x, arrow_y - 14),
        (arrow_tip_x, arrow_y + (arrow_h / 2)),
        (arrow_body_end_x, arrow_y + arrow_h + 14),
    ]
    arrow_tip = Polygon(
        tip_points,
        closed=True,
        facecolor=PALETTE["arrow_bg"],
        edgecolor=PALETTE["arrow_border"],
        alpha=PALETTE["arrow_alpha"],
        linewidth=2.0,
        zorder=7,
    )
    ax.add_patch(arrow_tip)

    # 3. Tópicos de Negócio dentro da seta
    for i, p_cfg in enumerate(PALETTE["pillars"]):
        cx = start_x + i * (col_w + col_gap)
        pillar_center_x = cx + (col_w / 2)

        ax.text(
            pillar_center_x,
            arrow_y + (arrow_h / 2),
            p_cfg["arrow_label"],
            fontsize=9.2,
            fontweight="bold",
            color=PALETTE["arrow_text"],
            ha="center",
            va="center",
            zorder=8,
        )

        if i < 4:
            sep_x = cx + col_w + (col_gap / 2)
            ax.text(
                sep_x,
                arrow_y + (arrow_h / 2),
                "➔",
                fontsize=11,
                fontweight="bold",
                color=PALETTE["arrow_symbol"],
                ha="center",
                va="center",
                zorder=8,
            )

    # 4. Texto Explicativo Abaixo da Seta
    label_y = arrow_y - 36
    external_explanation = "FLUXO CONTÍNUO DO CICLO DE VIDA ANALÍTICO"

    ann_box = Rectangle(
        (540, label_y - 14),
        520,
        28,
        facecolor="#F8FAFC",
        edgecolor="#CBD5E1",
        linewidth=1.0,
        zorder=6,
    )
    ax.add_patch(ann_box)

    ax.text(
        800,
        label_y,
        external_explanation,
        fontsize=9.5,
        fontweight="bold",
        color=PALETTE["external_label_text"],
        ha="center",
        va="center",
        zorder=7,
    )

    out_path_assets = ASSETS_DIR / out_filename
    out_path_base = BASE_DIR / out_filename
    plt.savefig(
        out_path_assets,
        dpi=300,
        bbox_inches="tight",
        facecolor=PALETTE["bg"],
        edgecolor="none",
    )
    plt.savefig(
        out_path_base,
        dpi=300,
        bbox_inches="tight",
        facecolor=PALETTE["bg"],
        edgecolor="none",
    )
    plt.close(fig)
    print(f"[OK] Versao preenchida de referencia gerada com sucesso: {out_path_base}")


def main():
    print("[...] Gerando template vazio (para o PowerPoint) e versao preenchida (guia de montagem)...")

    # 1. Template Vazio Oficial de Animação
    draw_pure_empty_template("grafico-legado-l2r-vazio.png")

    # 2. Versão Preenchida de Referência (Guia de Montagem com Ícones Mapeados)
    draw_populated_reference("grafico-legado-l2r-populated.png")

    # 3. Versão Legada Completa
    draw_populated_reference("grafico-legado-l2r.png")

    print("[SUCCESS] Todos os artefatos L2R gerados e sincronizados com sucesso!")


if __name__ == "__main__":
    main()
