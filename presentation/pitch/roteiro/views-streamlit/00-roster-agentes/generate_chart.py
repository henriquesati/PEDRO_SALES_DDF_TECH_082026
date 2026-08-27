#!/usr/bin/env python3
"""
generate_chart.py
Módulo: presentation/pitch/roteiro/views-streamlit/00-roster-agentes
Função: Renderização executiva da Central do Avaliador: Agentes e Skills (Header Toggle + Visualizador Fidedigno + Contextos Arquiteturais estilo README).
Padrão Gráfico: Fundo Branco Puro (#FFFFFF), 16:9 Widescreen, 300 DPI, charts-maker standard.
"""

from typing import Final
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_IMAGE_PATH: Final[Path] = Path(__file__).resolve().parent / "chart_streamlit_roster_agentes.png"

# Paleta Semântica Corporativa Sóbria & Elegante
COLOR_PRIMARY: Final[str] = "#0F172A"       # Slate 900
COLOR_SURFACE: Final[str] = "#090D16"       # Dark Jet Surface
COLOR_TEXT_MUTED: Final[str] = "#475569"    # Slate 600
COLOR_TEXT_LIGHT: Final[str] = "#94A3B8"    # Slate 400
COLOR_CYAN: Final[str] = "#38BDF8"          # Sky 400
COLOR_GREEN: Final[str] = "#10B981"         # Emerald 500
COLOR_BORDER: Final[str] = "#CBD5E1"        # Slate 300
COLOR_DARK_BORDER: Final[str] = "#1E293B"   # Slate 800
COLOR_SLOT_BG: Final[str] = "#161B22"       # Dark Slot Background


def plot_streamlit_roster_view() -> plt.Figure:
    """Renderiza a interface de Agentes e Skills com correlação visual de identidade e referências do README."""
    plt.rcParams["text.parse_math"] = False
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Segoe UI", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = COLOR_BORDER
    plt.rcParams["axes.linewidth"] = 1.1

    fig = plt.figure(figsize=(16.0, 9.0), facecolor="#FFFFFF")

    # =========================================================================
    # 0. HEADER SUPERIOR UNIFICADO (Título à esquerda + Toggle Agentes/Skills à direita)
    # =========================================================================
    ax_top = fig.add_axes([0.03, 0.905, 0.94, 0.075])
    ax_top.axis("off")

    ctrl_bg = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        boxstyle="round,pad=0.0,rounding_size=0.015",
        facecolor=COLOR_SURFACE, edgecolor=COLOR_DARK_BORDER, linewidth=1.2,
        transform=ax_top.transAxes
    )
    ax_top.add_patch(ctrl_bg)

    top_bar = patches.FancyBboxPatch(
        (0.0, 0.93), 1.0, 0.07,
        boxstyle="round,pad=0.0,rounding_size=0.005",
        facecolor=COLOR_CYAN, edgecolor="none",
        transform=ax_top.transAxes
    )
    ax_top.add_patch(top_bar)

    # Título puro à esquerda
    ax_top.text(0.025, 0.48, "Agentes e Skills",
                fontsize=15.0, fontfamily="monospace", fontweight="bold", color="#F0F6FC", va="center", transform=ax_top.transAxes)

    # Botões de Toggle integrados no Header à Direita
    btn_w = 0.115
    btn_h = 0.60
    btn_y = 0.20

    # Botão Agentes (Ativo)
    b_ag = patches.FancyBboxPatch(
        (0.74, btn_y), btn_w, btn_h,
        boxstyle="round,pad=0.0,rounding_size=0.01",
        facecolor="#2563EB", edgecolor=COLOR_CYAN, linewidth=1.2,
        transform=ax_top.transAxes
    )
    ax_top.add_patch(b_ag)
    ax_top.text(0.74 + btn_w/2.0, btn_y + btn_h/2.0, "Agentes",
                fontsize=8.5, fontfamily="monospace", fontweight="bold", color="#FFFFFF", ha="center", va="center", transform=ax_top.transAxes)

    # Botão Skills (Inativo)
    b_sk = patches.FancyBboxPatch(
        (0.865, btn_y), btn_w, btn_h,
        boxstyle="round,pad=0.0,rounding_size=0.01",
        facecolor="#161B22", edgecolor="#30363D", linewidth=0.9,
        transform=ax_top.transAxes
    )
    ax_top.add_patch(b_sk)
    ax_top.text(0.865 + btn_w/2.0, btn_y + btn_h/2.0, "Skills",
                fontsize=8.5, fontfamily="monospace", fontweight="bold", color="#8B949E", ha="center", va="center", transform=ax_top.transAxes)

    # =========================================================================
    # 1. COLUNA ESQUERDA: TÍTULO DO MENU + LISTA DE AGENTES
    # =========================================================================
    ax_roster = fig.add_axes([0.03, 0.035, 0.26, 0.85])
    ax_roster.axis("off")

    roster_bg = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0,
        boxstyle="round,pad=0.0,rounding_size=0.015",
        facecolor="#0D1117", edgecolor="#30363D", linewidth=1.1,
        transform=ax_roster.transAxes
    )
    ax_roster.add_patch(roster_bg)

    # Título da Categoria no Topo do Menu
    ax_roster.text(0.06, 0.950, "AGENTES DISPONIVEIS", fontsize=7.8, fontfamily="monospace",
                   fontweight="bold", color=COLOR_CYAN, transform=ax_roster.transAxes)
    line_menu = patches.Rectangle(
        (0.04, 0.930), 0.92, 0.002,
        facecolor="#1E293B", edgecolor="none", transform=ax_roster.transAxes
    )
    ax_roster.add_patch(line_menu)

    roster_items = [
        ("MASTER STRATEGIST", "Case Context Specialist", True),
        ("REPOSITORY ARCHITECT", "Project Context Specialist", False),
        ("ANALYTICS MASTERMIND", "Cart Recovery Insights", False),
        ("PLATFORM GUARDIAN", "Platform Registry Consultant", False),
        ("LINEAGE CHRONICLER", "Data Pipeline Documentation", False),
        ("PURE LOGIC SAGE", "Declarative Functional Coding", False),
        ("VISUAL VIRTUOSO", "Charts Maker", False),
        ("SENIOR CONSULTANT", "Data Strategy Analyst", False),
        ("SYNTHETIC WORLD BUILDER", "DataMaker", False),
        ("CODE EXPLORER", "Scout", False),
    ]

    card_h = 0.082
    y_slot = 0.925
    for arch, name, is_sel in roster_items:
        y_slot -= card_h
        slot_bg = patches.FancyBboxPatch(
            (0.04, y_slot), 0.92, card_h - 0.008,
            boxstyle="round,pad=0.0,rounding_size=0.008",
            facecolor="#1E293B" if is_sel else COLOR_SLOT_BG,
            edgecolor=COLOR_CYAN if is_sel else "#30363D",
            linewidth=1.2 if is_sel else 0.8,
            transform=ax_roster.transAxes
        )
        ax_roster.add_patch(slot_bg)

        if is_sel:
            active_bar = patches.FancyBboxPatch(
                (0.04, y_slot), 0.02, card_h - 0.008,
                boxstyle="round,pad=0.0,rounding_size=0.004",
                facecolor=COLOR_CYAN, edgecolor="none", transform=ax_roster.transAxes
            )
            ax_roster.add_patch(active_bar)

        ax_roster.text(0.09, y_slot + (card_h - 0.008) * 0.65, arch, fontsize=6.2,
                       fontfamily="monospace", fontweight="bold",
                       color=COLOR_CYAN if is_sel else "#94A3B8", transform=ax_roster.transAxes)
        ax_roster.text(0.09, y_slot + (card_h - 0.008) * 0.22, name, fontsize=7.8,
                       fontweight="bold",
                       color="#FFFFFF" if is_sel else "#F0F6FC", transform=ax_roster.transAxes)

        y_slot -= 0.004

    # =========================================================================
    # 2. COLUNA DIREITA: CORRELAÇÃO VISUAL, VISUALIZADOR E CONTEXTOS DO README
    # =========================================================================
    ax_dossier = fig.add_axes([0.31, 0.035, 0.66, 0.85])
    ax_dossier.axis("off")

    # 2.1 Header de Correlação Visual (Identidade + Fonte)
    id_box = patches.FancyBboxPatch(
        (0.0, 0.89), 1.0, 0.11,
        boxstyle="round,pad=0.0,rounding_size=0.012",
        facecolor="#090D16", edgecolor=COLOR_DARK_BORDER, linewidth=1.2,
        transform=ax_dossier.transAxes
    )
    ax_dossier.add_patch(id_box)

    id_accent = patches.FancyBboxPatch(
        (0.0, 0.99), 1.0, 0.01,
        boxstyle="round,pad=0.0,rounding_size=0.003",
        facecolor=COLOR_CYAN, edgecolor="none", transform=ax_dossier.transAxes
    )
    ax_dossier.add_patch(id_accent)

    # Identidade correlacionada
    ax_dossier.text(0.025, 0.965, "MASTER STRATEGIST", fontsize=7.0, fontfamily="monospace",
                    fontweight="bold", color=COLOR_CYAN, transform=ax_dossier.transAxes)
    ax_dossier.text(0.025, 0.932, "Case Context Specialist", fontsize=11.5,
                    fontweight="bold", color="#F0F6FC", transform=ax_dossier.transAxes)
    ax_dossier.text(0.025, 0.903, "[DOC] Localizacao: .agents/agents/case-context-specialist.md", fontsize=6.8,
                    fontfamily="monospace", color="#94A3B8", transform=ax_dossier.transAxes)

    ax_dossier.text(0.975, 0.945, "Modo: Read-Only", fontsize=7.2, fontfamily="monospace",
                    color="#A7F3D0", ha="right", transform=ax_dossier.transAxes)
    ax_dossier.text(0.975, 0.912, "22 linhas • Markdown", fontsize=6.6, fontfamily="monospace",
                    color="#64748B", ha="right", transform=ax_dossier.transAxes)

    # 2.2 Container do Arquivo Fidedigno
    doc_box = patches.FancyBboxPatch(
        (0.0, 0.44), 1.0, 0.43,
        boxstyle="round,pad=0.0,rounding_size=0.012",
        facecolor="#090D16", edgecolor=COLOR_DARK_BORDER, linewidth=1.1,
        transform=ax_dossier.transAxes
    )
    ax_dossier.add_patch(doc_box)

    file_lines = [
        ("---", "#64748B", 0.025),
        ("name: case-context-specialist", "#38BDF8", 0.025),
        ("description: Agente especialista em contexto estratégico, requisitos e direção geral do case técnico.", "#E2E8F0", 0.025),
        ("tools: [view_file, list_dir, grep_search]", "#FBBF24", 0.025),
        ("mode: read-only", "#34D399", 0.025),
        ("---", "#64748B", 0.025),
        ("", "#FFFFFF", 0.025),
        ("# 01 — ROLE & IDENTIDADE", "#38BDF8", 0.025),
        ("Você é o Case Context Specialist (Master Strategist), guardião absoluto do contexto estratégico.", "#F8FAFC", 0.025),
        ("", "#FFFFFF", 0.025),
        ("# 02 — MISSÃO", "#38BDF8", 0.025),
        ("Centralizar o entendimento consolidado dos 11 itens obrigatórios do case de estágio em Engenharia de Analytics & IA,", "#E2E8F0", 0.025),
        ("garantindo que todas as decisões e entregas atendam ao critério Outlier de avaliação técnica.", "#E2E8F0", 0.025),
        ("", "#FFFFFF", 0.025),
        ("# 03 — CONSTRAINTS & GOVERNANÇA", "#38BDF8", 0.025),
        ("• Modo Read-Only: Proibida qualquer mutação não autorizada no repositório.", "#F87171", 0.045),
        ("• Zero Local SQL: Nenhum arquivo .sql local deve ser gerado (DEC-004). As consultas pertencem à plataforma.", "#F87171", 0.045),
        ("• DEC-001 Ancorada: Métricas de pitch e KPIs estruturadas em ratios e percentuais para máxima transferibilidade.", "#F87171", 0.045),
    ]

    y_code = 0.840
    for code_text, code_col, indent in file_lines:
        if code_text:
            ax_dossier.text(indent, y_code, code_text, fontsize=6.8, fontfamily="monospace",
                            color=code_col, transform=ax_dossier.transAxes)
        y_code -= 0.023

    # 2.3 Contextos e Referências Arquiteturais (Estilo README)
    ref_box = patches.FancyBboxPatch(
        (0.0, 0.0), 1.0, 0.42,
        boxstyle="round,pad=0.0,rounding_size=0.012",
        facecolor="#090D16", edgecolor=COLOR_DARK_BORDER, linewidth=1.2,
        transform=ax_dossier.transAxes
    )
    ax_dossier.add_patch(ref_box)

    ax_dossier.text(0.025, 0.385, "Contextos e Referências", fontsize=8.2,
                    fontfamily="monospace", fontweight="bold", color=COLOR_CYAN, transform=ax_dossier.transAxes)

    # 1. Diretórios Arquiteturais
    ax_dossier.text(0.025, 0.355, "[DIR] DIRETORIOS ARQUITETURAIS & SKILLS VINCULADAS", fontsize=6.2, fontfamily="monospace",
                    fontweight="bold", color="#38BDF8", transform=ax_dossier.transAxes)
    ax_dossier.text(0.025, 0.332, "• .agents/skills/case-context-specialist/ — Diretório de governança e especificação de execução",
                    fontsize=5.8, fontfamily="monospace", color="#94A3B8", transform=ax_dossier.transAxes)
    ax_dossier.text(0.025, 0.312, "• .agents/skills/project-context-specialist/ — Mapeamento do repositório e decisões arquiteturais",
                    fontsize=5.8, fontfamily="monospace", color="#94A3B8", transform=ax_dossier.transAxes)

    # 2. Especificações e Artefatos Fonte
    ax_dossier.text(0.025, 0.280, "[DOC] ESPECIFICACOES & ARTEFATOS FONTE GERENCIADOS", fontsize=6.2, fontfamily="monospace",
                    fontweight="bold", color="#34D399", transform=ax_dossier.transAxes)
    ax_dossier.text(0.025, 0.258, "• specs-internship.txt  •  relatorios/decision-making/DEC-001-metricas-propostas-valor.md",
                    fontsize=5.8, fontfamily="monospace", color="#6EE7B7", transform=ax_dossier.transAxes)

    # 3. Regras e Decisões
    ax_dossier.text(0.025, 0.228, "[DEC] REGRAS DE GOVERNANCA & DECISOES ARQUITETURAIS (DECs)", fontsize=6.2, fontfamily="monospace",
                    fontweight="bold", color="#F87171", transform=ax_dossier.transAxes)
    ax_dossier.text(0.025, 0.206, "[READ-ONLY]  [DEC-001 ANCHORED]  [GROUND TRUTH REQUIRED]  [ZERO LOCAL SQL (DEC-004)]",
                    fontsize=5.6, fontfamily="monospace", color="#FCA5A5", transform=ax_dossier.transAxes)

    # 4. Mapeamento Detalhado de Tarefas por Entregável (README Spec)
    ax_dossier.text(0.025, 0.170, "[TASKS] MAPEAMENTO DETALHADO DE TAREFAS POR ENTREGAVEL (README SPEC)", fontsize=6.2, fontfamily="monospace",
                    fontweight="bold", color="#E2E8F0", transform=ax_dossier.transAxes)

    readme_tasks = [
        "[x] [case-00] Agilidade & Planejamento — Planejamento iterativo entidade a entidade e matriz de decisão",
        "[x] [case-01] Base de Dados (mín. 100k) — Gerador Python modular com 115.777+ registros em Parquet/CSV",
        "[x] [case-03] Explorar & Catalogar — Dicionários de dados, Lakehouse Medallion e Data Asset IDs oficiais",
        "[x] [case-04] Data Quality & Anomalias — Pipeline Dual-Artifact, suíte Great Expectations (18 regras) e quarentena",
        "[x] [case-10] Apresentação em Vídeo (Pitch) — Roteiro master, 8 módulos com scripts e gráficos em 300 DPI",
    ]

    ty = 0.142
    for task in readme_tasks:
        ax_dossier.text(0.025, ty, task, fontsize=5.5, fontfamily="monospace",
                        color="#CBD5E1", transform=ax_dossier.transAxes)
        ty -= 0.022

    return fig


def main() -> None:
    fig = plot_streamlit_roster_view()
    OUTPUT_IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[SUCCESS] Gráfico de Agentes e Skills atualizado com sucesso em: {OUTPUT_IMAGE_PATH}")


if __name__ == "__main__":
    main()
