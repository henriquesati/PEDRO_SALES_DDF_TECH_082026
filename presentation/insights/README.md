# 📊 Galeria de Gráficos de Insights: Dadosfera E-commerce

> [!IMPORTANT]
> **REFERÊNCIA CANÔNICA DE NEGÓCIO E BASELINE (SOURCE OF TRUTH)**:  
> Toda a taxonomia analítica, entidades, fórmulas, métricas e parâmetros de simulação monetária (R$) desta galeria seguem **rigorosamente a especificação canônica master em [`presentation/pitch/pitch_spec.md`](../pitch/pitch_spec.md)**.  
> Qualquer ajuste em tickets de referência, custos unitários de canais ou segmentações RFM deve reconciliar diretamente com as Seções 4 e 5 da `pitch_spec.md`.

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
| **01** | [`01_segmentacao_risco/`](02_risk/01_segmentacao_risco/) | ✅ Concluído | **Segmentação de Risco de Abandono (Suíte de 3 Dashboards)**: Dashboard 1 Executivo (KPIs + Distribuição + Pareto), Dashboard 2 Causal (Heatmap Motivos x Dispositivo) e Dashboard 3 Prescritivo (Fila de Acionamento + Matriz Estratégica Risk x Expected ROI com imagens dedicadas anti-overlap). | [1] Dashboard 1: Risk Overview<br>[2] Dashboard 2: Risk Drivers<br>[3A] Fila de Acionamento Prescritiva<br>[3B] Matriz Estratégica Risk x ROI<br>[4] Painel Integrado Consolidado | [`spec.md`](02_risk/01_segmentacao_risco/spec.md) • [`chart_03_dashboard_01_risk_overview.png`](02_risk/01_segmentacao_risco/chart_03_dashboard_01_risk_overview.png) • [`chart_03_dashboard_02_risk_drivers.png`](02_risk/01_segmentacao_risco/chart_03_dashboard_02_risk_drivers.png) • [`chart_03_dashboard_03a_fila_acionamento.png`](02_risk/01_segmentacao_risco/chart_03_dashboard_03a_fila_acionamento.png) • [`chart_03_dashboard_03b_matriz_risk_roi.png`](02_risk/01_segmentacao_risco/chart_03_dashboard_03b_matriz_risk_roi.png) • [`chart_03_segmentacao_risco.png`](02_risk/01_segmentacao_risco/chart_03_segmentacao_risco.png) |
| **02** | [`02_ltv_vs_abandono/`](02_risk/02_ltv_vs_abandono/) | ✅ Concluído | **Análise de LTV vs Abandono & Sensibilidade Financeira**: Relação entre o valor histórico do cliente (LTV) e o ticket da cesta, provando o retorno desproporcional do WhatsApp VIP para Premium e Email para Novos. | Painel Duplo: Gráfico de Bolhas (Abandono vs Ticket vs R$ em Risco) + Matriz de Decisão Econômica | [`spec.md`](02_risk/02_ltv_vs_abandono/spec.md) • [`generate_chart.py`](02_risk/02_ltv_vs_abandono/generate_chart.py) • [`chart_02_ltv_vs_abandono.png`](02_risk/02_ltv_vs_abandono/chart_02_ltv_vs_abandono.png) |
| **03** | [`03_viabilidade_recuperacao_carrinho/`](02_risk/03_viabilidade_recuperacao_carrinho/) | ✅ Concluído | **Score de Viabilidade de Recuperação (Recovery Viability)**: Modelo de triagem combinando Probabilidade Empírica de Recuperação, Custo de Canal e Expected ROI em 3 níveis (Alta, Média, Baixa). | Painel Duplo: Scatter Plot de Viabilidade (Probabilidade vs Valor da Cesta) + Decomposição Operacional | [`spec.md`](02_risk/03_viabilidade_recuperacao_carrinho/spec.md) • [`generate_chart.py`](02_risk/03_viabilidade_recuperacao_carrinho/generate_chart.py) • [`chart_03_viabilidade_recuperacao_carrinho.png`](02_risk/03_viabilidade_recuperacao_carrinho/chart_03_viabilidade_recuperacao_carrinho.png) |

---

### 3. 🎯 Insights Prescritivos (`03_prescriptive/`)

| # | Módulo | Status | Tema & Descrição | Tipo de Visualização | Artefatos na Pasta |
|:---:|---|:---:|---|---|---|
| **01** | [`01_estrategia_resgate_segmento/`](03_prescriptive/01_estrategia_resgate_segmento/) | ✅ Concluído | **Estratégia Prescritiva de Resgate**: Simulador de Viabilidade Econômica Líquida por Resgate (WhatsApp a R$ 0,30, SMS a R$ 0,15, Email a R$ 0,05, Push a R$ 0,02) e Matriz de Políticas por Cluster RFM. | Painel Integrado: Barras Agrupadas de Ganho Líquido Unitário + Matriz Prescritiva de Ações | [`spec.md`](03_prescriptive/01_estrategia_resgate_segmento/spec.md) • [`generate_chart.py`](03_prescriptive/01_estrategia_resgate_segmento/generate_chart.py) • [`chart_04_estrategia_resgate_segmento.png`](03_prescriptive/01_estrategia_resgate_segmento/chart_04_estrategia_resgate_segmento.png) |
| **02** | [`02_otimizacao_timing_envio/`](03_prescriptive/02_otimizacao_timing_envio/) | ✅ Concluído | **Otimização Prescritiva de Timing**: Curva de Decaimento Temporal de Conversão (Decay Curve) ao longo das réguas (+1h, +24h, +48h, +72h), destacando o Ponto Ótimo de Disparo em até +1h. | Painel Integrado: Curva Suave (Spline Cúbica) com Eixo Duplo (Abertura vs Conversão) + Barras de Volumetria | [`spec.md`](03_prescriptive/02_otimizacao_timing_envio/spec.md) • [`generate_chart.py`](03_prescriptive/02_otimizacao_timing_envio/generate_chart.py) • [`chart_05_otimizacao_timing_envio.png`](03_prescriptive/02_otimizacao_timing_envio/chart_05_otimizacao_timing_envio.png) |
| **03** | [`03_produtos_mais_abandonados/`](03_prescriptive/03_produtos_mais_abandonados/) | ✅ Concluído | **Análise de Produtos e Categorias Mais Abandonados**: Ranking de receita represada por categoria de produto (Eletrônicos, Decoração, Moda) e matriz prescritiva de intervenções de resgate e UX. | Painel Duplo: Barras de Receita Represada em R$ k + Matriz Prescritiva de Intervenções | [`spec.md`](03_prescriptive/03_produtos_mais_abandonados/spec.md) • [`generate_chart.py`](03_prescriptive/03_produtos_mais_abandonados/generate_chart.py) • [`chart_03_produtos_mais_abandonados.png`](03_prescriptive/03_produtos_mais_abandonados/chart_03_produtos_mais_abandonados.png) |
| **04** | [`04_roi_campanhas_resgate/`](03_prescriptive/04_roi_campanhas_resgate/) | ✅ Concluído | **ROI & Eficiência de Campanhas de Resgate por Canal**: Funil de engajamento (Abertura, Clique, Conversão) e matriz de rebalanceamento orçamentário (85% em Email, WhatsApp VIP, corte de SMS/Push frios). | Painel Duplo: Funil de Eficiência em Barras Agrupadas + Matriz de Rebalanceamento Orçamentário | [`spec.md`](03_prescriptive/04_roi_campanhas_resgate/spec.md) • [`generate_chart.py`](03_prescriptive/04_roi_campanhas_resgate/generate_chart.py) • [`chart_04_roi_campanhas_resgate.png`](03_prescriptive/04_roi_campanhas_resgate/chart_04_roi_campanhas_resgate.png) |

---

## 📐 Diretriz Metodológica: Foco em Proporções (%) & Entidade Exemplo (Vinculação Pitch Spec)

1. **Princípio de Universalidade (DEC-001)**: Todas as especificações visuais e geradores priorizam **proporções (%) e taxas relativas**, garantindo que o cliente possa conectar sua operação e **adequar seu próprio Ticket Médio**.
2. **Entidade Exemplo de Baseline**: Para contextualização dos volumes absolutos em R$, adota-se o baseline padrão declarado em [`presentation/pitch/pitch_spec.md`](../pitch/pitch_spec.md#42-entidade-exemplo-de-negócio-baseline-mock-para-simulações-monetárias):
   - **Ticket Médio Geral**: `R$ 375,00`
   - **Ticket Médio Premium**: `R$ 800,00`
   - **Ticket Médio Regular**: `R$ 360,00`
   - **Ticket Médio Novo**: `R$ 250,00`
   - **Ticket Médio Dormant**: `R$ 200,00`
   - **Custos Unitários de Comunicação**: WhatsApp `R$ 0,30`, SMS `R$ 0,15`, Email `R$ 0,05`, Push `R$ 0,02`
3. **Base de Dados Unificada**: 100% dos gráficos consom as entidades persistidas em `data/mock/output_cleaned/parquet/*.parquet` (`carrinhos`, `pedidos`, `clientes`, `produtos`, `itens_carrinho`, `eventos_resgate`).

---

## 🚀 Como Executar Todos os Gráficos

Para gerar novamente todas as imagens em alta definição (300 DPI) com estrita fidelidade aos dados persistidos:

```bash
# Execução direta via Python:
python presentation/insights/run_all_insights_charts.py

# Ou via Makefile Python do repositório:
python make.py insights-charts
```

