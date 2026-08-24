# 📊 Galeria de Gráficos de Insights: Dadosfera E-commerce

Este diretório contém a infraestrutura de especificações visuais, scripts declarativos em Python e artefatos gráficos de alta definição (300 DPI) organizados pela taxonomia analítica do case (**Descritivos**, **Risco/Diagnóstico** e **Prescritivos**).

---

## 📂 Taxonomia & Módulos de Visualização

### 1. 📈 Insights Descritivos (`01_descriptive/`)

| # | Módulo | Status | Tema & Descrição | Tipo de Visualização | Artefatos na Pasta |
|:---:|---|:---:|---|---|---|
| **01** | [`01_bi_recuperacao_carrinhos/`](01_descriptive/01_bi_recuperacao_carrinhos/) | ✅ Concluído | **BI de Recuperação de Carrinhos**: Evolução acumulada semestral (Jan–Jun / 7.500 un) e dinâmica semanal diária (09–15 Fev / 288 un) com pareamento 1-para-1 de mini cards executivos. | Curvas Suaves (Spline Cúbica), Fundo Branco (`#FFFFFF`), Preenchimento de Zonas (`fill_between`) e Mini Cards | [`spec.md`](01_descriptive/01_bi_recuperacao_carrinhos/spec.md) • [`chart_bi_recuperacao_carrinhos.png`](01_descriptive/01_bi_recuperacao_carrinhos/chart_bi_recuperacao_carrinhos.png) • [`mini_card_zonas_dupla.png`](01_descriptive/01_bi_recuperacao_carrinhos/mini_card_zonas_dupla.png) |
| **02** | [`02_motivos_abandono/`](01_descriptive/02_motivos_abandono/) | ✅ Concluído | **Decomposição Descritiva de Motivos de Abandono**: Treemap hierárquico proporcional ao volume (5.231 un) e gráfico lado a lado de perda financeira bruta por faixa de ticket e resgate Dadosfera (+R$ 173,7k). | [1] Treemap Hierárquico de Blocos Proporcionais<br>[2] Painel Duplo Lado a Lado de Perda por Ticket vs Resgate | [`spec.md`](01_descriptive/02_motivos_abandono/spec.md) • [`chart_02_treemap_motivos_abandono.png`](01_descriptive/02_motivos_abandono/chart_02_treemap_motivos_abandono.png) • [`chart_02_perda_financeira_motivos.png`](01_descriptive/02_motivos_abandono/chart_02_perda_financeira_motivos.png) |
| **03** | [`03_custo_recuperacao_roi/`](01_descriptive/03_custo_recuperacao_roi/) | ✅ Concluído | **Custo por Carrinho Recuperado (CAC de Resgate) & ROI**: Eficiência unitária de custos por conversão (Email R$ 1,02, Push R$ 1,67, SMS R$ 3,00, WhatsApp R$ 12,00) e retorno sobre investimento consolidado (~45x). | Painel Duplo: CAC de Resgate por Canal vs Receita Líquida & Multiplicador de ROI | [`spec.md`](01_descriptive/03_custo_recuperacao_roi/spec.md) • [`generate_chart.py`](01_descriptive/03_custo_recuperacao_roi/generate_chart.py) • [`chart_03_custo_recuperacao_roi.png`](01_descriptive/03_custo_recuperacao_roi/chart_03_custo_recuperacao_roi.png) |

---

### 2. ⚠️ Insights de Risco & Diagnóstico (`02_risk/`)

| # | Módulo | Status | Tema & Descrição | Tipo de Visualização | Artefatos na Pasta |
|:---:|---|:---:|---|---|---|
| **01** | [`01_segmentacao_risco/`](02_risk/01_segmentacao_risco/) | ✅ Concluído | **Matriz Diagnóstica de Risco & Atrito**: Score de Risco em Tempo de Sessão (Crítico, Alto, Médio, Baixo) cruzado com Segmentos RFM (Premium, Regular, Dormant, Novo) e taxa real de abandono observada. | Painel Integrado: Heatmap 2D de Risco RFM + Barras Horizontais de Volume & Triagem de Sessão | [`spec.md`](02_risk/01_segmentacao_risco/spec.md) • [`generate_chart.py`](02_risk/01_segmentacao_risco/generate_chart.py) • [`chart_03_segmentacao_risco.png`](02_risk/01_segmentacao_risco/chart_03_segmentacao_risco.png) |

---

### 3. 🎯 Insights Prescritivos (`03_prescriptive/`)

| # | Módulo | Status | Tema & Descrição | Tipo de Visualização | Artefatos na Pasta |
|:---:|---|:---:|---|---|---|
| **01** | [`01_estrategia_resgate_segmento/`](03_prescriptive/01_estrategia_resgate_segmento/) | ✅ Concluído | **Estratégia Prescritiva de Resgate**: Simulador de Viabilidade Econômica Líquida por Resgate (WhatsApp a R$ 0,30, SMS a R$ 0,15, Email a R$ 0,05, Push a R$ 0,02) e Matriz de Políticas por Cluster RFM. | Painel Integrado: Barras Agrupadas de Ganho Líquido Unitário + Matriz Prescritiva de Ações | [`spec.md`](03_prescriptive/01_estrategia_resgate_segmento/spec.md) • [`generate_chart.py`](03_prescriptive/01_estrategia_resgate_segmento/generate_chart.py) • [`chart_04_estrategia_resgate_segmento.png`](03_prescriptive/01_estrategia_resgate_segmento/chart_04_estrategia_resgate_segmento.png) |
| **02** | [`02_otimizacao_timing_envio/`](03_prescriptive/02_otimizacao_timing_envio/) | ✅ Concluído | **Otimização Prescritiva de Timing**: Curva de Decaimento Temporal de Conversão (Decay Curve) ao longo das réguas (+1h, +24h, +48h, +72h), destacando o Ponto Ótimo de Disparo em até +1h. | Painel Integrado: Curva Suave (Spline Cúbica) com Eixo Duplo (Abertura vs Conversão) + Barras de Volumetria | [`spec.md`](03_prescriptive/02_otimizacao_timing_envio/spec.md) • [`generate_chart.py`](03_prescriptive/02_otimizacao_timing_envio/generate_chart.py) • [`chart_05_otimizacao_timing_envio.png`](03_prescriptive/02_otimizacao_timing_envio/chart_05_otimizacao_timing_envio.png) |

---

## 📐 Diretriz Metodológica: Foco em Proporções (%) & Entidade Exemplo

1. **Princípio de Universalidade**: As especificações visuais e geradores priorizam **proporções (%) e taxas relativas**, garantindo que o cliente possa conectar sua operação e **adequar seu próprio Ticket Médio**.
2. **Entidade Exemplo de Baseline**: Para contextualização dos volumes absolutos em R$, adota-se o baseline padrão:
   - **Ticket Médio Geral**: `R$ 375,00`
   - **Ticket Médio Premium**: `R$ 800,00`
   - **Ticket Médio Regular**: `R$ 360,00`
   - **Ticket Médio Novo**: `R$ 250,00`
   - **Ticket Médio Dormant**: `R$ 200,00`

---

## 🚀 Como Executar Todos os Gráficos

Para gerar novamente todas as imagens em alta definição (300 DPI) com estrita fidelidade aos dados persistidos:

```bash
# Execução direta via Python:
python presentation/insights/run_all_insights_charts.py

# Ou via Makefile Python do repositório:
python make.py insights-charts
```
