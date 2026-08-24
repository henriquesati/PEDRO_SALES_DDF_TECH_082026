---
name: charts-maker
description: >-
  Especialista em geração de gráficos, visualizações executivas e mini cards analíticos
  com rigor absoluto de integridade de dados (Ground Truth) e padronização visual
  baseada no padrão canônico de presentation/insights. Garante que 100% dos dados
  plotados venham diretamente dos datasets persistidos (Parquet, DW, Data Views), aplicando
  como default o tema de fundo branco, tipografia moderna e paleta semântica executiva.
---

# Charts Maker — Visualizações Executivas com Rigor Analítico & Estilo Padrão Canônico

> [!IMPORTANT]
> **DIRETRIZ DE ESTILIZAÇÃO PADRÃO (DEFAULT STYLE)**  
> Toda geração de gráficos por agentes e skills deve, por padrão, buscar manter a harmonia e a identidade visual consolidada em [`presentation/insights/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/) (fundo branco puro, tipografia limpa sem serifa, spines limpas e paleta semântica executiva), a menos que o usuário ou o contexto especifiquem um formato alternativo.
>
> A criação de gráficos é flexível e declarativa — cada script deve ser autocontido, aplicando as propriedades visuais diretamente sem engessamento ou dependências rígidas.
> Consulte o catálogo de atributos e boas práticas em [presentation_insights_style_guide.md](./references/presentation_insights_style_guide.md).

---

## 🎯 1. Princípios Fundamentais & Ground Truth (Zero Fabrication)

Todo gráfico, dashboard, mini card ou visualização gerada no projeto deve seguir o **princípio fundamental da verdade dos dados**:

1. **PROIBIÇÃO ABSOLUTA DE DADOS FALSIFICADOS OU ESCALAS ARTIFICIAIS**:
   - É estritamente proibido aplicar multiplicadores arbitrários (ex: `abandono * 0.45`), somas artificiais ou fatores de expansão visual apenas para "abrir espaço" ou "gerar faixas bonitas" no gráfico.
   - Cada linha, barra, dispersão, área (`fill_between`) e marcador deve refletir **exatamente** as contagens, somas e proporções reais calculadas dos datasets.

2. **DADOS AUDITÁVEIS E REPRODUZÍVEIS**:
   - Toda visualização deve ser gerada por script Python declarativo que lê diretamente os arquivos de dados persistidos (`data/mock/output_cleaned/parquet/*.parquet` ou `data/mock/output/parquet/*.parquet`).
   - Os valores exibidos em títulos, cards, anotações de vértices e tabelas devem ser derivados diretamente das variáveis computadas, nunca "hardcoded" com números hipotéticos não fundamentados.

3. **DISTINÇÃO ENTRE DADO OBSERVADO E BENCHMARK TEÓRICO**:
   - **Dado Observado (Realidade do Dataset)**: Plotado nas séries temporais, barras e áreas reais.
   - **Benchmark de Mercado (Baymard, Klaviyo, Salesforce)**: Plotado exclusivamente como linha de referência pontilhada/tracejada (`ax.axhline(69.8, linestyle=':', label='Benchmark Global')`), **nunca** alterando a série de dados subjacente.

4. **REFERÊNCIA CANÔNICA DE BASELINE & ENTIDADE DE NEGÓCIO (PITCH SPEC)**:
   - Todo gráfico, métrica, faixa de ticket de exemplo ou custo de canal deve reconciliar com a especificação canônica master em [`presentation/pitch/pitch_spec.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/pitch_spec.md) (Seções 4 e 5).

---

## 🎨 2. Atributos Visuais Recomendados (Presentation Insights Standard)

### 2.1 Estrutura & Canvas
- **Fundo da Figura (`facecolor`)**: `#FFFFFF` (Branco Puro).
- **Fundo dos Eixos (`ax.set_facecolor`)**: `#FFFFFF`.
- **Containers e Cards de KPI**: Fundo `#F8FAFC` (Slate 50) com borda `#94A3B8` / `#CBD5E1` (Slate 400/300).
- **Spines dos Eixos**: Linhas em `#CBD5E1`. Recomendado ocultar as bordas superior e direita (`ax.spines["top"].set_visible(False)`, `ax.spines["right"].set_visible(False)`).
- **Grade (Grid)**: Tracejada suave (`linestyle="--"`, `alpha=0.40 - 0.50`, cor `#CBD5E1`, `zorder=1`).

### 2.2 Tipografia & Textos
- **Font Family**: `["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]`.
- **Título da Figura / Supertitle**: Negrito, `#0F172A` (Slate 900), `fontsize=13.5 - 15.0 pt`, `pad=14 - 16`.
- **Subtítulo / Eixos (`xlabel`, `ylabel`)**: Negrito, `#1E293B` ou `#334155` (Slate 800/700), `fontsize=10.5 - 11.5 pt`.
- **Rótulos dos Ticks**: Negrito, `#334155` ou `#1E293B`, `fontsize=9.5 - 10.5 pt`.
- **Anotações Diretas de Dados**: Rótulos informativos de 2 linhas (`f"{val} ({pct}%)\n{detalhe}"`), texto primário `#0F172A` em negrito, subtítulo de contexto em `#64748B` / `#334155`.

### 2.3 Paleta Semântica de Negócio
- 🔵 **Conversão Direta Orgânica / Base Total**: `#2563EB` (Blue 600) / `#1E3A8A` (Blue 900) | Fill suave: `alpha=0.14`.
- 🟢 **Recuperação Ativa & Resgate Dadosfera**: `#059669` (Emerald 600) / `#10B981` (Emerald 500) | Fill suave: `alpha=0.28`.
- 🔴 **Zona de Atrito / Abandono / Perda**: `#E11D48` (Rose 600) / `#9F1239` (Rose 800) | Fill suave: `alpha=0.14`.
- 🟡 **Atenção / Risco Médio / SMS**: `#F59E0B` (Amber 500) / `#D97706` (Amber 600).
- 🟣 **Canais Especiais / Push / Segmentação VIP / IA**: `#8B5CF6` (Violet 500) / `#7C3AED` (Violet 600).
- ⚪ **Marcadores de Vértices Reais**: Ponto com preenchimento `#FFFFFF` e borda colorida (`linewidth=2.0`, `s=40 - 50`, `zorder=5`).

### 2.4 Resolução de Exportação
- `dpi=300` padrão.
- `bbox_inches="tight"`.
- `facecolor="#FFFFFF"`.

---

## 🏗️ 3. Estrutura Autocontida de Script Python (Exemplo Prático)

Cada script pode ser construído de forma autocontida e direta:

```python
from typing import Final, Tuple
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Caminhos
BASE_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
PARQUET_PATH: Final[str] = os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "carrinhos.parquet")
OUTPUT_PATH: Final[str] = os.path.join(os.path.dirname(__file__), "chart_output.png")

# 2. Carga dos Dados Persistidos (Ground Truth)
def load_data() -> pd.DataFrame:
    df = pd.read_parquet(PARQUET_PATH)
    df["data_criacao"] = pd.to_datetime(df["data_criacao"])
    return df

# 3. Transformação & Agregação Funcional
def prepare_metrics(df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
    ...
    return df_agg, kpis

# 4. Plotagem Estilizada Executiva (Fundo Branco, Tipografia Moderna)
def plot_chart(df_agg: pd.DataFrame, kpis: dict) -> plt.Figure:
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    plt.rcParams["axes.edgecolor"] = "#CBD5E1"
    plt.rcParams["axes.linewidth"] = 1.1

    fig, ax = plt.subplots(figsize=(14.0, 7.5), facecolor="#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    # Plotagem de séries, barras ou áreas
    ...

    # Limpeza de eixos e grid suave
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.45, color="#CBD5E1", zorder=1)

    ax.set_title("TÍTULO DO GRÁFICO\nSubtítulo explicativo com período e escopo",
                 fontsize=13.5, fontweight="bold", color="#0F172A", pad=15)
                 
    plt.tight_layout()
    return fig

# 5. Execução Principal
def main() -> None:
    df = load_data()
    df_agg, kpis = prepare_metrics(df)
    fig = plot_chart(df_agg, kpis)
    
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[SUCCESS] Gráfico salvo em: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
```

---

## 📐 4. Layouts Canônicos de Referência

| Tipo de Gráfico | Formato Recomendado | Exemplo de Referência no Repositório |
|---|---|---|
| **Evolução Temporal & Funil (Splines)** | `figsize=(14.0, 7.5)`, interpolação `k=3`, `fill_between` em zonas | [`presentation/insights/01_descriptive/01_bi_recuperacao_carrinhos/generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/01_descriptive/01_bi_recuperacao_carrinhos/generate_chart.py) |
| **Painel Duplo Lado a Lado (Comparativo)** | `figsize=(15.0, 6.8)`, `gridspec_kw={"width_ratios": [1.0, 1.18]}`, barras `barh` | [`presentation/insights/01_descriptive/02_motivos_abandono/generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/01_descriptive/02_motivos_abandono/generate_chart.py) |
| **Dashboard Executivo com KPI Cards** | `figsize=(15.0, 7.8)`, `GridSpec(2, 2, height_ratios=[0.28, 0.72])`, 4 KPI cards | [`presentation/insights/02_risk/01_segmentacao_risco/generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/02_risk/01_segmentacao_risco/generate_chart.py) |
| **Eficiência Unitária & CAC vs ROI** | `figsize=(15.0, 7.0)`, barras ordenadas com anotações diretas | [`presentation/insights/01_descriptive/03_custo_recuperacao_roi/generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/01_descriptive/03_custo_recuperacao_roi/generate_chart.py) |
| **Estratégia Prescritiva por Canal & RFM** | `figsize=(16.5, 7.2)`, barras agrupadas + Matriz prescritiva | [`presentation/insights/03_prescriptive/01_estrategia_resgate_segmento/generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/03_prescriptive/01_estrategia_resgate_segmento/generate_chart.py) |

---

## 📋 5. Checklist de Validação

- [ ] O visual segue o padrão harmônico de **fundo branco (`#FFFFFF`)**, **tipografia moderna** e **paleta corporativa** de `presentation/insights`?
- [ ] Todos os dados foram carregados diretamente de arquivos Parquet persistidos do repositório?
- [ ] Não existe nenhum multiplicador ou ajuste artificial manual nos dados?
- [ ] As spines superior e direita foram ocultadas (`set_visible(False)`) e o grid está sutil (`#CBD5E1`)?
- [ ] A imagem foi exportada em 300 DPI com `bbox_inches="tight"` e fundo branco?
