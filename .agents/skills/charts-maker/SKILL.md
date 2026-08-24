---
name: charts-maker
description: >-
  Especialista em geração de gráficos, visualizações executivas e mini cards analíticos
  com rigor absoluto de integridade de dados (Ground Truth). Garante que 100% dos dados
  plotados venham diretamente dos datasets persistidos (Parquet, DW, Data Views), proibindo
  estritamente qualquer falsificação, multiplicador arbitrário, inflação visual ou adulteração
  de números para fins estéticos.
---

# Charts Maker — Visualizações com Rigor Analítico e Integridade de Dados

## 🎯 Missão & Princípio Fundamental: Zero Fabrication (Ground Truth)

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

---

## 🏗️ Padrão Arquitetural de Geração de Gráficos

Todo script de geração de visualizações deve seguir a estrutura modular funcional:

```python
from typing import Final
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Constantes e Caminhos Centralizados
BASE_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PARQUET_PATH: Final[str] = os.path.join(BASE_DIR, "data", "mock", "output_cleaned", "parquet", "carrinhos.parquet")
OUTPUT_PATH: Final[str] = os.path.join(os.path.dirname(__file__), "chart_output.png")

# 2. Carga Pura de Dados Persistidos (Sem Mock Fake em Memória)
def load_data() -> pd.DataFrame:
    df = pd.read_parquet(PARQUET_PATH)
    df["data_criacao"] = pd.to_datetime(df["data_criacao"])
    return df

# 3. Transformação & Agregação Funcional
def compute_series(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    # Agregações reais sem multiplicadores artificiais
    ...
    return x_data, y_real_1, y_real_2

# 4. Plotagem Estilizada Executiva
def plot_chart(...) -> plt.Figure:
    ...

# 5. Execução Principal com Salvamento em 300 DPI
def main() -> None:
    ...
```

---

## 🎨 Diretrizes Visuais Executivas (Visual Standard)

1. **Tipografia & Resolução**:
   - Fontes: `Segoe UI`, `DejaVu Sans`, `Helvetica`, `Arial`, `sans-serif`.
   - Exportação: `dpi=300`, `bbox_inches="tight"`, `facecolor="#FFFFFF"`.

2. **Paleta de Cores Semântica Consistente**:
   - 🔵 **Conversão Direta Orgânica**: Azul Royal (`#2563EB`) | Fundo Suave (`#EFF6FF` / `#DBEAFE`, alpha 0.15 - 0.20).
   - 🟢 **Recuperação Ativa & Reengajamento**: Verde Esmeralda (`#059669` / `#16A34A`) | Fundo Suave (`#ECFDF5` / `#D1FAE5`, alpha 0.15 - 0.20).
   - 🔴 **Zona de Atrito / Abandono / Perda**: Vermelho Rose (`#E11D48` / `#DC2626`) | Fundo Suave (`#FEF2F2` / `#FEE2E2`, alpha 0.15 - 0.20).
   - ⚪ **Totalizadores & Fundo**: Cinza Escuro Executivo (`#0F172A`, `#1E293B`) sobre Fundo Branco Puro (`#FFFFFF`) e Cards em Slate Suave (`#F8FAFC`, borda `#94A3B8`).

3. **Curvas Suaves (Spline Cúbica) com Integridade**:
   - Ao interpolar pontos com `scipy.interpolate.make_interp_spline`, a curva deve passar pelos vértices reais e respeitar limites físicos (`np.maximum(0, ...)`).
   - Os marcadores pontuais circulares (`scatter`) devem marcar exatamente os pontos reais auditáveis nos eixos X e Y.

4. **Mini Cards e Mini Tabelas para Apresentações (PowerPoint)**:
   - Gerar mini cards compactos com proporção limpa para inclusão em slides.
   - Exibir simultaneamente o **volume absoluto (`un`)** e a **porcentagem (`%`)** correspondente calculada sobre a base correta.
   - Indicar com clareza a base do percentual (se sobre o total de carrinhos criados ou sobre o total de carrinhos abandonados).

---

## 📋 Checklist de Validação Obrigatória (Definition of Done)

Antes de aprovar e salvar qualquer gráfico ou mini card:

- [ ] Todos os dados foram carregados diretamente de arquivos Parquet / fontes limpas do repositório?
- [ ] Não existe nenhum multiplicador, offset ou inflação visual manual no código?
- [ ] Os percentuais somam 100% ou respeitam a relação matemática declarada?
- [ ] A taxa de recuperação está claramente rotulada quanto ao seu denominador (sobre abandonados vs sobre o total)?
- [ ] A imagem foi salva em 300 DPI com `bbox_inches="tight"` e fundo branco `#FFFFFF`?
- [ ] O script pode ser executado autonomamente via orquestrador (`python run_all_insights_charts.py` / `python run_all_pitch_charts.py`) sem erros?
