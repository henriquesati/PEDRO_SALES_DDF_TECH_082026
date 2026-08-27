#!/usr/bin/env python3
"""
generate_chart.py
Gera o gráfico executivo de finalização de apresentação para a view 'view-final'.
Apresenta a Dadosfera de forma abstrata e corporativa como o Hub Central que consolida
as 4 grandes frentes do ecossistema empresarial:
- Execução de Pedidos (Satisfação e Feedback)
- Gestão (Retenção e Aquisição)
- Análises (Vendas, Dados de Clientes e Insights)
- Design e Desenvolvimento (Ativos, UI/UX e Layouts)

Padrão Visual: Fundo Branco Puro (#FFFFFF), 16:9 Widescreen, 300 DPI, Tipografia Sem Serifa Moderna.
"""

from typing import Final, Tuple, List
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Polygon
from scipy.interpolate import splprep, splev

OUTPUT_DIR: Final[Path] = Path(__file__).resolve().parent
OUTPUT_IMAGE_PATH: Final[Path] = OUTPUT_DIR / "chart_view_final_consolidacao_dadosfera.png"

# Paleta Semântica Executiva (Padrão White Background Corporativo)
COLORS = {
    "bg": "#FFFFFF",
    "text_dark": "#0F172A",
    "text_muted": "#475569",
    "text_light": "#94A3B8",
    
    # Hub Central Dadosfera
    "dadosfera_blue": "#0284C7",
    "dadosfera_dark": "#0369A1",
    "hub_fill": "#E0F2FE",          # Azul celeste suave premium
    "hub_border": "#0284C7",        # Borda azul vibrante
    "orbital_ring": "#0284C7",      # Anéis orbitais concêntricos
    
    # 4 Pilares / Cores de Acento
    "north": "#0284C7",     # Execução de Pedidos (Sky Blue)
    "east": "#2563EB",      # Gestão (Royal Blue)
    "south": "#0369A1",     # Análises (Deep Blue)
    "west": "#0284C7",      # Design e Desenvolvimento (Cyan/Blue)
    
    # Satélites (Estilo Dark Pill Executivo de Alto Contraste)
    "sat_bg": "#0B132B",
    "sat_text": "#FFFFFF",
    "sat_sub": "#94A3B8",
}

def create_true_cloverleaf_polygon(cx: float, cy: float, n_points: int = 600) -> np.ndarray:
    """
    Constrói os nós de contorno do formato de trevo de 4 folhas (cloverleaf) com
    bulbos perfeitamente esféricos nos 4 polos e cintura estreita nas diagonais.
    """
    d_x = 0.250  # Distância do centro até os polos leste/oeste
    d_y = 0.190  # Distância do centro até os polos norte/sul
    r_bulb_x = 0.090 # Raio do bulbo Leste/Oeste
    r_bulb_y = 0.082 # Raio do bulbo Norte/Sul
    r_neck = 0.068   # Raio de cintura nas diagonais
    
    ctrl_pts = []
    
    # 1. Bulbo Norte (Topo): Arco de 145 deg até 35 deg passando pelo topo (90 deg)
    for ang_deg in np.linspace(145, 35, 11):
        rad = np.radians(ang_deg)
        px = cx + r_bulb_y * np.cos(rad)
        py = (cy + d_y) + r_bulb_y * np.sin(rad)
        ctrl_pts.append((px, py))
        
    # Cintura Nordeste (45 deg)
    ctrl_pts.append((cx + r_neck * np.cos(np.radians(45)), cy + r_neck * np.sin(np.radians(45))))
    
    # 2. Bulbo Leste (Direita): Arco de 55 deg até -55 deg passando pela direita (0 deg)
    for ang_deg in np.linspace(55, -55, 11):
        rad = np.radians(ang_deg)
        px = (cx + d_x) + r_bulb_x * np.cos(rad)
        py = cy + r_bulb_x * np.sin(rad)
        ctrl_pts.append((px, py))
        
    # Cintura Sudeste (-45 deg)
    ctrl_pts.append((cx + r_neck * np.cos(np.radians(-45)), cy + r_neck * np.sin(np.radians(-45))))
    
    # 3. Bulbo Sul (Baixo): Arco de -35 deg até -145 deg passando pelo fundo (-90 deg)
    for ang_deg in np.linspace(-35, -145, 11):
        rad = np.radians(ang_deg)
        px = cx + r_bulb_y * np.cos(rad)
        py = (cy - d_y) + r_bulb_y * np.sin(rad)
        ctrl_pts.append((px, py))
        
    # Cintura Sudoeste (-135 deg)
    ctrl_pts.append((cx + r_neck * np.cos(np.radians(-135)), cy + r_neck * np.sin(np.radians(-135))))
    
    # 4. Bulbo Oeste (Esquerda): Arco de 235 deg até 125 deg passando pela esquerda (180 deg)
    for ang_deg in np.linspace(235, 125, 11):
        rad = np.radians(ang_deg)
        px = (cx - d_x) + r_bulb_x * np.cos(rad)
        py = cy + r_bulb_x * np.sin(rad)
        ctrl_pts.append((px, py))
        
    # Cintura Noroeste (135 deg)
    ctrl_pts.append((cx + r_neck * np.cos(np.radians(135)), cy + r_neck * np.sin(np.radians(135))))
    
    # Fechar spline
    ctrl_x = [p[0] for p in ctrl_pts]
    ctrl_y = [p[1] for p in ctrl_pts]
    ctrl_x.append(ctrl_x[0])
    ctrl_y.append(ctrl_y[0])
    
    tck, u = splprep([ctrl_x, ctrl_y], s=0.00005, per=True, k=3)
    u_new = np.linspace(0, 1, n_points)
    smooth_x, smooth_y = splev(u_new, tck)
    
    return np.column_stack([smooth_x, smooth_y])

def draw_satellite(ax, x: float, y: float, w: float, h: float, 
                   title: str, sub: str, stem_start: Tuple[float, float], 
                   accent_color: str) -> None:
    """Desenha um satélite executivo com linha de conexão (stem) e badge estilizado."""
    # Linha conectora (stem)
    ax.plot([stem_start[0], x], [stem_start[1], y], color=accent_color,
            linewidth=1.8, linestyle="-", zorder=3, alpha=0.95)
    # Ponto de articulação na borda do bulbo
    ax.scatter([stem_start[0]], [stem_start[1]], color=accent_color, s=36, zorder=6, edgecolor="#FFFFFF", linewidth=1.4)
    # Ponto de articulação no satélite
    ax.scatter([x], [y], color=accent_color, s=22, zorder=6)
    
    # Satélite Box (Estilo dark pill premium para legibilidade máxima)
    box = FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.0,rounding_size=0.024",
        facecolor=COLORS["sat_bg"], edgecolor=accent_color,
        linewidth=1.6, zorder=7
    )
    ax.add_patch(box)
    
    # Textos do Satélite
    if sub:
        ax.text(x, y + 0.013, title, ha="center", va="center",
                fontsize=9.2, fontweight="bold", color=COLORS["sat_text"], zorder=8)
        ax.text(x, y - 0.013, sub, ha="center", va="center",
                fontsize=7.4, color=COLORS["sat_sub"], zorder=8)
    else:
        ax.text(x, y, title, ha="center", va="center",
                fontsize=9.8, fontweight="bold", color=COLORS["sat_text"], zorder=8)

def plot_final_consolidation() -> plt.Figure:
    """Monta a visualização corporativa completa do Hub Dadosfera."""
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial"]
    
    fig = plt.figure(figsize=(16, 9), facecolor=COLORS["bg"], dpi=300)
    ax = fig.add_axes([0, 0, 1, 1], facecolor=COLORS["bg"])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    
    # ----------------------------------------------------
    # 1. HEADER EXECUTIVO
    # ----------------------------------------------------
    tag_bg = FancyBboxPatch(
        (0.04, 0.94), 0.25, 0.032,
        boxstyle="round,pad=0.0,rounding_size=0.01",
        facecolor="#EFF6FF", edgecolor="#BFDBFE",
        linewidth=1.2, zorder=3
    )
    ax.add_patch(tag_bg)
    ax.text(0.165, 0.956, "ATO 4 • VISÃO DE FUTURO & FECHAMENTO", ha="center", va="center",
            fontsize=8.2, fontweight="bold", color="#1D4ED8", zorder=4)
    
    # Título Principal
    ax.text(0.04, 0.905, "Consolidação de Ferramentas na Plataforma Dadosfera", 
            ha="left", va="center", fontsize=18.5, fontweight="bold", color=COLORS["text_dark"], zorder=4)
    # Subtítulo Abstrato de Negócio
    ax.text(0.04, 0.875, "Hub central unificado conectando Operações, Gestão, Analytics e Inteligência em uma única solução SaaS",
            ha="left", va="center", fontsize=9.8, color=COLORS["text_muted"], zorder=4)
    
    # Divisor suave
    ax.plot([0.04, 0.96], [0.855, 0.855], color="#E2E8F0", linewidth=1.2, zorder=2)
    
    # ----------------------------------------------------
    # 2. HUB CENTRAL ORGÂNICO (TRUE CLOVERLEAF) & ANÉIS ORBITAIS
    # ----------------------------------------------------
    cx, cy = 0.50, 0.46
    
    # Gerar e desenhar o trevo com os 4 bulbos
    poly_points = create_true_cloverleaf_polygon(cx=cx, cy=cy)
    hub_patch = Polygon(poly_points, closed=True, facecolor=COLORS["hub_fill"], 
                        edgecolor=COLORS["hub_border"], linewidth=2.6, zorder=2, alpha=0.95)
    ax.add_patch(hub_patch)
    
    # Desenhar anéis orbitais concêntricos
    for r in [0.105, 0.140, 0.175]:
        circle = Circle((cx, cy), r, facecolor="none", edgecolor=COLORS["orbital_ring"], 
                        linewidth=1.4, linestyle="-", alpha=0.55, zorder=4)
        ax.add_patch(circle)
        
    # Núcleo Central Dadosfera
    core = Circle((cx, cy), 0.088, facecolor="#FFFFFF", edgecolor=COLORS["dadosfera_blue"],
                  linewidth=3.0, zorder=5)
    ax.add_patch(core)
    
    # Textos Centrais da Dadosfera
    ax.text(cx, cy + 0.016, "Dadosfera", ha="center", va="center",
            fontsize=24, fontweight="bold", color=COLORS["dadosfera_dark"], zorder=6)
    ax.text(cx, cy - 0.020, "PLATAFORMA UNIFICADA", ha="center", va="center",
            fontsize=7.8, fontweight="bold", color=COLORS["dadosfera_blue"], zorder=6)
    ax.text(cx, cy - 0.038, "SaaS • Dados & IA", ha="center", va="center",
            fontsize=7.0, color=COLORS["text_muted"], zorder=6)
    
    # ----------------------------------------------------
    # 3. TEXTOS NOS 4 BULBOS PRINCIPAIS (ABSTRATO)
    # ----------------------------------------------------
    d_x = 0.250
    d_y = 0.190
    
    # Bulbo Norte (Execução de Pedidos)
    ny = cy + d_y
    ax.text(cx, ny + 0.012, "Execução\nde Pedidos", ha="center", va="center",
            fontsize=13.0, fontweight="bold", color=COLORS["text_dark"], zorder=5)
    ax.text(cx, ny - 0.028, "Operações & Fluxo de Dados", ha="center", va="center",
            fontsize=7.8, fontweight="bold", color=COLORS["north"], zorder=5)
    
    # Bulbo Leste (Gestão)
    ex = cx + d_x
    ax.text(ex, cy + 0.012, "Gestão", ha="center", va="center",
            fontsize=14.0, fontweight="bold", color=COLORS["text_dark"], zorder=5)
    ax.text(ex, cy - 0.018, "Governança & Controle", ha="center", va="center",
            fontsize=7.8, fontweight="bold", color=COLORS["east"], zorder=5)
    
    # Bulbo Sul (Análises)
    sy = cy - d_y
    ax.text(cx, sy + 0.018, "Analytics & BI", ha="center", va="center",
            fontsize=7.8, fontweight="bold", color=COLORS["south"], zorder=5)
    ax.text(cx, sy - 0.012, "Análises", ha="center", va="center",
            fontsize=14.0, fontweight="bold", color=COLORS["text_dark"], zorder=5)
    
    # Bulbo Oeste (Design e Desenvolvimento)
    wx = cx - d_x
    ax.text(wx, cy + 0.012, "Design e\nDesenvolvimento", ha="center", va="center",
            fontsize=12.5, fontweight="bold", color=COLORS["text_dark"], zorder=5)
    ax.text(wx, cy - 0.028, "Data Apps & Inteligência", ha="center", va="center",
            fontsize=7.8, fontweight="bold", color=COLORS["west"], zorder=5)
    
    # ----------------------------------------------------
    # 4. SATÉLITES CONECTADOS (MODELO ABSTRATO DA PLATAFORMA)
    # ----------------------------------------------------
    # Satélites Norte (2 satélites no topo alinhados à referência)
    draw_satellite(ax, cx - 0.11, ny + 0.125, 0.165, 0.058,
                   "Satisfação do Cliente", "NPS & Qualidade",
                   (cx - 0.04, ny + 0.075), COLORS["north"])
    
    draw_satellite(ax, cx + 0.11, ny + 0.125, 0.165, 0.058,
                   "Feedback do Cliente", "Voz do Cliente & Reviews",
                   (cx + 0.04, ny + 0.075), COLORS["north"])
    
    # Satélites Leste (2 satélites à direita alinhados à referência)
    draw_satellite(ax, ex + 0.145, cy + 0.100, 0.160, 0.058,
                   "Retenção de Usuários", "LTV & Fidelização",
                   (ex + 0.070, cy + 0.045), COLORS["east"])
    
    draw_satellite(ax, ex + 0.145, cy - 0.100, 0.160, 0.058,
                   "Aquisição de Usuários", "Growth & Conversão",
                   (ex + 0.070, cy - 0.045), COLORS["east"])
    
    # Satélites Sul (3 satélites na base alinhados à referência)
    draw_satellite(ax, cx - 0.17, sy - 0.115, 0.160, 0.058,
                   "Vendas e Receita", "Performance Financeira",
                   (cx - 0.055, sy - 0.075), COLORS["south"])
    
    draw_satellite(ax, cx, sy - 0.135, 0.165, 0.058,
                   "Dados dos Clientes", "Visão 360° & Segmentação",
                   (cx, sy - 0.082), COLORS["south"])
    
    draw_satellite(ax, cx + 0.17, sy - 0.115, 0.160, 0.058,
                   "Insights de Negócio", "Tomada de Decisão",
                   (cx + 0.055, sy - 0.075), COLORS["south"])
    
    # Satélites Oeste (3 satélites à esquerda alinhados à referência)
    draw_satellite(ax, wx - 0.150, cy + 0.105, 0.170, 0.058,
                   "Ativos Estáticos e Imagens", "Catálogo, Mídia & Conteúdo",
                   (wx - 0.070, cy + 0.045), COLORS["west"])
    
    # UI/UX central azul vibrante
    draw_satellite(ax, wx - 0.165, cy, 0.135, 0.058,
                   "UI / UX", "Data Apps & Interfaces",
                   (wx - 0.090, cy), "#0284C7")
    
    draw_satellite(ax, wx - 0.150, cy - 0.105, 0.175, 0.058,
                   "Layouts e Elementos de Interface", "Componentes & Visualização",
                   (wx - 0.070, cy - 0.045), COLORS["west"])
        
    return fig

def main() -> None:
    """Executa a geração do gráfico executivo."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig = plot_final_consolidation()
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=300, facecolor=COLORS["bg"], bbox_inches="tight")
    plt.close(fig)
    print("Sucesso: Grafico executivo abstrato gerado em:", str(OUTPUT_IMAGE_PATH))

if __name__ == "__main__":
    main()
