# 📊 Galeria de Gráficos de Insights: Dadosfera E-commerce

Este diretório contém a infraestrutura de especificações visuais, scripts declarativos em Python e artefatos gráficos de alta definição dedicados aos **insights descritivos, diagnósticos e prescritivos** do case de Recuperação de Carrinho de Compras.

---

## 📂 Módulos de Visualização

| # | Módulo | Status | Tema & Descrição | Tipo de Visualização | Artefatos na Pasta |
|:---:|---|:---:|---|---|---|
| **01** | [`01_bi_recuperacao_carrinhos/`](01_bi_recuperacao_carrinhos/) | ✅ Concluído | **BI de Recuperação de Carrinhos**: Evolução acumulada semestral (Jan–Jun / 7.500 un) e dinâmica semanal diária (09–15 Fev / 288 un) com pareamento 1-para-1 de mini cards executivos. | Curvas Suaves (Spline Cúbica), Fundo Branco (`#FFFFFF`), Preenchimento de Zonas (`fill_between`) e Mini Cards | [`spec.md`](01_bi_recuperacao_carrinhos/spec.md) • [`generate_chart.py`](01_bi_recuperacao_carrinhos/generate_chart.py) • [`generate_mini_tables.py`](01_bi_recuperacao_carrinhos/generate_mini_tables.py) • [`chart_bi_recuperacao_carrinhos.png`](01_bi_recuperacao_carrinhos/chart_bi_recuperacao_carrinhos.png) |
| **02** | [`02_motivos_abandono/`](02_motivos_abandono/) | ✅ Concluído | **Decomposição Descritiva de Motivos de Abandono**: Preço Alto (R$ 498,8k / 25,0%) e Frete Caro (R$ 434,6k / 23,1%) decompostos por Dispositivo (Mobile, Desktop, Tablet) e impacto financeiro represado em R$. | Painel Duplo: Barras Horizontais Empilhadas por Dispositivo + Barras de Perda Financeira em R$ | [`spec.md`](02_motivos_abandono/spec.md) • [`generate_chart.py`](02_motivos_abandono/generate_chart.py) • [`chart_02_motivos_abandono.png`](02_motivos_abandono/chart_02_motivos_abandono.png) |
| **03** | [`03_segmentacao_risco/`](03_segmentacao_risco/) | ✅ Concluído | **Matriz Diagnóstica de Risco & Atrito**: Score de Risco em Tempo de Sessão (Crítico, Alto, Médio, Baixo) cruzado com Segmentos RFM (Premium, Regular, Dormant, Novo) e taxa real de abandono observada. | Painel Integrado: Heatmap 2D de Risco RFM + Barras Horizontais de Volume & Triagem de Sessão | [`spec.md`](03_segmentacao_risco/spec.md) • [`generate_chart.py`](03_segmentacao_risco/generate_chart.py) • [`chart_03_segmentacao_risco.png`](03_segmentacao_risco/chart_03_segmentacao_risco.png) |
| **04** | [`04_estrategia_resgate_segmento/`](04_estrategia_resgate_segmento/) | ✅ Concluído | **Estratégia Prescritiva de Resgate**: Simulador de Viabilidade Econômica Líquida por Resgate (WhatsApp a R$ 0,30, SMS a R$ 0,15, Email a R$ 0,05, Push a R$ 0,02) e Matriz de Políticas por Cluster RFM. | Painel Integrado: Barras Agrupadas de Ganho Líquido Unitário + Matriz Prescritiva de Ações | [`spec.md`](04_estrategia_resgate_segmento/spec.md) • [`generate_chart.py`](04_estrategia_resgate_segmento/generate_chart.py) • [`chart_04_estrategia_resgate_segmento.png`](04_estrategia_resgate_segmento/chart_04_estrategia_resgate_segmento.png) |
| **05** | [`05_otimizacao_timing_envio/`](05_otimizacao_timing_envio/) | ✅ Concluído | **Otimização Prescritiva de Timing**: Curva de Decaimento Temporal de Conversão (Decay Curve) ao longo das réguas (+1h, +24h, +48h, +72h), destacando o Ponto Ótimo de Disparo em até +1h. | Painel Integrado: Curva Suave (Spline Cúbica) com Eixo Duplo (Abertura vs Conversão) + Barras de Volumetria | [`spec.md`](05_otimizacao_timing_envio/spec.md) • [`generate_chart.py`](05_otimizacao_timing_envio/generate_chart.py) • [`chart_05_otimizacao_timing_envio.png`](05_otimizacao_timing_envio/chart_05_otimizacao_timing_envio.png) |

---

## ⚙️ Como Executar os Geradores

### 1. Execução Consolidada
Para regerar todos os artefatos de visualização de uma só vez:
```bash
python presentation/insights/run_all_insights_charts.py
```
Ou via Make:
```bash
python make.py insights-charts
```

### 2. Execução Individual por Módulo
Você pode entrar em qualquer subdiretório e executar seu script isoladamente:
```bash
python presentation/insights/01_bi_recuperacao_carrinhos/generate_chart.py
python presentation/insights/02_motivos_abandono/generate_chart.py
python presentation/insights/03_segmentacao_risco/generate_chart.py
python presentation/insights/04_estrategia_resgate_segmento/generate_chart.py
python presentation/insights/05_otimizacao_timing_envio/generate_chart.py
```
*Cada script lê diretamente os datasets limpos em Parquet (`data/mock/output_cleaned/parquet/`) e salva a imagem correspondente em 300 DPI dentro do próprio diretório.*
