# 🎨 Guia Canônico de Estilização Visual de Gráficos (Presentation Insights Standard)

Este documento estabelece o **padrão visual obrigatório (Default Style)** para toda e qualquer visualização de dados, gráfico, dashboard executivo e mini card analítico gerado no ecossistema do projeto.

---

## 1. 🎯 Princípio Central de Design

O padrão visual do projeto segue a identidade corporativa e analítica de **`presentation/insights/`**:
- **Clareza Executiva**: Fundo branco puro (`#FFFFFF`), tipografia sem serifa moderna, hierarquia nítida entre dados observados e anotações.
- **Rigor Matemático (Ground Truth)**: 100% dos dados plotados devem vir de fontes persistidas (`.parquet`), proibindo estritamente escalas artificiais, offsets ou multiplicadores arbitrários.
- **Eliminação de Poluição Visual**: Ocultação de bordas desnecessárias (spines superior e direita), grades suaves e legendas em caixas compactas.
- **Destaque Semântico**: Cores com significado de negócio pré-definido (Azul = Conversão Orgânica, Verde = Resgate Dadosfera, Rose/Vermelho = Atrito/Abandono, Âmbar = Atenção, Violeta = IA/Canais Especiais).

---

## 2. 🎨 Tokens de Design & Paleta de Cores

### 2.1 Cores de Fundo, Eixos e Estrutura

| Token | Código Hex | Descrição & Uso |
|---|---|---|
| `CANVAS_BG` | `#FFFFFF` | Fundo principal da figura (`fig.patch.set_facecolor`) |
| `AXES_BG` | `#FFFFFF` | Fundo da área de plotagem (`ax.set_facecolor`) |
| `CARD_BG` | `#F8FAFC` | Fundo de mini cards, KPI boxes e caixas de anotação (Slate 50) |
| `CARD_BORDER` | `#94A3B8` / `#CBD5E1` | Borda de containers e cartões analíticos (Slate 400 / 300) |
| `SPINE_COLOR` | `#CBD5E1` | Borda dos eixos inferior e esquerdo (Linha 1.1 a 1.2 pt) |
| `GRID_COLOR` | `#CBD5E1` | Linhas de grade tracejadas (`linestyle="--"`, `alpha=0.4 - 0.5`) |

### 2.2 Tipografia & Cores de Texto

| Token | Código Hex | Tamanho Típico | Descrição & Uso |
|---|---|---|---|
| `TEXT_TITLE` | `#0F172A` | `13.5 - 15.0 pt` | Títulos principais e supertitles em **Negrito** (Slate 900) |
| `TEXT_SUBTITLE` | `#1E293B` | `11.0 - 12.5 pt` | Subtítulos de seções e eixos principais (Slate 800) |
| `TEXT_BODY` | `#334155` | `9.5 - 10.5 pt` | Rótulos de eixos (X/Y ticks) e descrições (Slate 700) |
| `TEXT_MUTED` | `#64748B` | `8.0 - 9.0 pt` | Rótulos secundários de KPI cards e notas de rodapé (Slate 500) |
| `FONT_FAMILY` | `sans-serif` | — | `["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]` |

### 2.3 Cores Semânticas de Negócio

| Semântica | Cor Primária | Preenchimento (`fill_between` / `alpha`) | Significado no Domínio |
|---|---|---|---|
| 🔵 **Conversão Orgânica** | `#2563EB` (Blue 600) | `alpha=0.14` (`#2563EB`) | Compras diretas no checkout, volume total base, clientes ativos |
| 🟢 **Resgate Dadosfera** | `#059669` (Emerald 600) | `alpha=0.28` (`#059669`) | Carrinhos recuperados, ganho financeiro líquido, alto ROI |
| 🔴 **Atrito / Abandono** | `#E11D48` (Rose 600) | `alpha=0.14` (`#E11D48`) | Abandono de carrinho, receita represada em risco, churn |
| 🟡 **Atenção / Médio** | `#F59E0B` (Amber 500) | `alpha=0.20` (`#F59E0B`) | Fricção de frete, risco intermediário, SMS marketing |
| 🟣 **Canais / VIP / IA** | `#8B5CF6` (Violet 500) | `alpha=0.20` (`#8B5CF6`) | Push notifications, segmentações RFM VIP, automações GenAI |

---

## 3. 📐 Especificações de Layout & Grid

### 3.1 Resolução e Exportação
- **DPI**: `300` obrigatório (`dpi=300`).
- **Bounding Box**: `bbox_inches="tight"`.
- **Fundo**: `facecolor="#FFFFFF"`.

### 3.2 Dimensões Recomendadas (Proporção Slide 16:9 / Executiva)
- **Painel Único (Evolução Temporal / Spline / Curvas)**: `figsize=(14.0, 7.5)` ou `(13.5, 7.2)`
- **Painel Duplo Lado a Lado (Comparativo)**: `figsize=(15.0, 6.8)` ou `(15.0, 7.2)` com `gridspec_kw={"width_ratios": [1.0, 1.18]}`
- **Dashboard Integrado com KPI Cards Superiores**: `figsize=(15.0, 7.8)` com `GridSpec(2, 2, height_ratios=[0.28, 0.72])`

---

## 4. 🧩 Anatomia dos Componentes Canônicos

### 4.1 Curvas Suaves com Spline Cúbica e Marcadores
```python
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt

x_indices = np.arange(len(datas))
x_smooth = np.linspace(x_indices.min(), x_indices.max(), 350)
spl_curve = np.maximum(0, make_interp_spline(x_indices, y_values, k=3)(x_smooth))

# Linha suave
ax.plot(x_smooth, spl_curve, color="#2563EB", linewidth=3.0, label="[1] Série Real", zorder=4)

# Marcadores nos vértices reais auditáveis
ax.scatter(x_indices, y_values, color="#FFFFFF", edgecolor="#2563EB", s=45, linewidth=2.0, zorder=5)
```

### 4.2 Preenchimento de Zonas (`fill_between`)
```python
ax.fill_between(
    x_smooth, y_bottom_smooth, y_top_smooth,
    color="#059669", alpha=0.28,
    label="Zona de Recuperação Dadosfera"
)
```

### 4.3 KPI Cards Executivos Superiores
```python
import matplotlib.patches as patches

# Container
bbox = patches.FancyBboxPatch(
    (x, y), width, height,
    boxstyle="round,pad=0.04,rounding_size=0.03",
    facecolor="#F8FAFC", edgecolor="#94A3B8", linewidth=1.2,
    transform=ax_kpi.transAxes
)
ax_kpi.add_patch(bbox)

# Textos com hierarquia
ax_kpi.text(x + 0.02, y + 0.65, "TÍTULO DO KPI", fontsize=8.5, fontweight="bold", color="#64748B", transform=ax_kpi.transAxes)
ax_kpi.text(x + 0.02, y + 0.35, "R$ 173.7k", fontsize=14.5, fontweight="bold", color="#059669", transform=ax_kpi.transAxes)
ax_kpi.text(x + 0.02, y + 0.12, "+10.6% de recuperação", fontsize=8.0, color="#334155", transform=ax_kpi.transAxes)
```

### 4.4 Barras Horizontais com Rótulos Diretos de 2 Níveis
```python
bars = ax.barh(y_pos, values, height=0.52, color="#E11D48", alpha=0.88, edgecolor="#9F1239", linewidth=1.2)
for i, (val, pct, vol) in enumerate(zip(values, pcts, volumes)):
    ax.text(
        val + offset, i,
        f"R$ {val:,.1f}k ({pct:.1f}%)\n{vol:,.0f} carrinhos",
        va="center", ha="left", fontsize=9.5, fontweight="bold", color="#0F172A"
    )
```

### 4.5 Limpeza de Spines e Grade
```python
ax.grid(axis="x", linestyle="--", alpha=0.4, color="#CBD5E1", zorder=1)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#CBD5E1")
ax.spines["bottom"].set_color("#CBD5E1")
```

---

## 5. 📂 Links de Referência no Repositório

Para consultar as implementações de referência em produção:
- **Descritivos**: [`presentation/insights/01_descriptive/01_bi_recuperacao_carrinhos/generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/01_descriptive/01_bi_recuperacao_carrinhos/generate_chart.py)
- **Motivos & Perda Financeira**: [`presentation/insights/01_descriptive/02_motivos_abandono/generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/01_descriptive/02_motivos_abandono/generate_chart.py)
- **CAC & ROI**: [`presentation/insights/01_descriptive/03_custo_recuperacao_roi/generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/01_descriptive/03_custo_recuperacao_roi/generate_chart.py)
- **Risco & Dashboards Executivos**: [`presentation/insights/02_risk/01_segmentacao_risco/generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/02_risk/01_segmentacao_risco/generate_chart.py)
- **Estratégia Prescritiva**: [`presentation/insights/03_prescriptive/01_estrategia_resgate_segmento/generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/03_prescriptive/01_estrategia_resgate_segmento/generate_chart.py)
- **Orquestrador Master de Gráficos**: [`presentation/insights/run_all_insights_charts.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/run_all_insights_charts.py)
