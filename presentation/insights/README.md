# 📊 Galeria de Gráficos de Insights: Dadosfera E-commerce

Este diretório contém a infraestrutura de especificações, scripts geradores em Python e artefatos visuais de alta definição dedicados aos **insights analíticos, diagnósticos e prescritivos** do case de Recuperação de Carrinho.

---

## 📂 Módulos de Visualização

| # | Módulo | Status | Tema do Gráfico | Tipo Visual | Artefatos na Pasta |
|:---:|---|:---:|---|---|---|
| **01** | [`01_bi_recuperacao_carrinhos/`](01_bi_recuperacao_carrinhos/) | ✅ Concluído | **BI de Recuperação de Carrinhos**: Evolução acumulada partindo de 0 até o topo (7.500 un), linha basal de comprados (2.229 un) e linha intermediária de resgate & reengajamento (~4.100 un) com span balanceado. | Curvas Suaves (Spline Cúbica), Fundo Branco (`#FFFFFF`) e Zonas Coloridas (`fill_between`) | [`spec.md`](01_bi_recuperacao_carrinhos/spec.md) • [`generate_chart.py`](01_bi_recuperacao_carrinhos/generate_chart.py) • [`chart_bi_recuperacao_carrinhos.png`](01_bi_recuperacao_carrinhos/chart_bi_recuperacao_carrinhos.png) |
| **02** | `02_motivos_abandono/` | ⏳ Em processo | **Decomposição Descritiva de Motivos de Abandono**: Atrito por categoria e dispositivo | Barras Horizontais com Quebra por Canal / Dispositivo | *A ser gerado no próximo agente* |
| **03** | `03_segmentacao_risco/` | ⏳ Em processo | **Matriz Diagnóstica de Risco & Atrito**: Segmentação de checkout e propensão ao abandono | Heatmap de Risco / Dispersão de Segmentos | *A ser gerado no próximo agente* |
| **04** | `04_estrategia_resgate_segmento/` | ⏳ Em processo | **Estratégia Prescritiva de Resgate**: Alocação de canais de CRM por cluster RFM | Matriz de Viabilidade & Alocação de Budget | *A ser gerado no próximo agente* |
| **05** | `05_otimizacao_timing_envio/` | ⏳ Em processo | **Otimização Prescritiva de Timing**: Decaimento temporal de conversão de disparos | Curva de Decaimento com Ponto Ótimo de Disparo | *A ser gerado no próximo agente* |

---

## ⚙️ Como Executar os Geradores

### 1. Execução Consolidada
```bash
python presentation/insights/run_all_insights_charts.py
```
Ou via Make:
```bash
python make.py insights-charts
```

### 2. Execução Individual
```bash
python presentation/insights/01_bi_recuperacao_carrinhos/generate_chart.py
```
*Cada script lê diretamente os datasets em Parquet (`data/mock/output/parquet/`) e salva a imagem correspondente em 300 DPI no próprio diretório.*
