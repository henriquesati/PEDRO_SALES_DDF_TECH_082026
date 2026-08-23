# 📊 Relatório de Views Analíticas & Artefatos de BI (Item 7)

> **Case Técnico:** Recuperação de Carrinho Abandonado (Dadosfera)  
> **Camada:** Gold (Curated Views / Metabase Dashboards)  
> **Status:** ✅ Executado e Artefatos Gerados  
> **Script Gerador:** [`notebooks/pipelines/serving/generate_bi_charts.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/notebooks/pipelines/serving/generate_bi_charts.py)  
> **Notebook Reproduzível:** [`notebooks/07_bi_dashboards_visualizations.ipynb`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/notebooks/07_bi_dashboards_visualizations.ipynb)  

---

## 1. 🎯 Visão Geral dos Artefatos de BI

Este documento consolida a geração de artefatos visuais das views analíticas projetadas para a plataforma Dadosfera (Metabase) e Data Apps (Streamlit).

Foram gerados **6 tipos distintos de visualizações** a partir dos dados do lakehouse (`carrinhos`, `produtos`, `eventos_resgate`, `clientes`), cobrindo requisitos explícitos de **Série Temporal**, **Performance de Categorias**, **Rentabilidade/ROI por Canal**, **Matriz de Atrito RFM** e **Matriz de Priorização**:

```text
dashboards/assets/
├── chart_01_serie_temporal_abandono_resgate.png   # 1. Gráfico de Linha Duplo Eixo (Série Temporal)
├── chart_02_performance_categorias.png            # 2. Barras Horizontais (Análise de Categorias)
├── chart_03_roi_eficiencia_canais.png             # 3. Gráfico Combo Barras + Linha (ROI por Canal)
├── chart_04_matriz_motivos_rfm_heatmap.png        # 4. Mapa de Calor (Atrito por Segmento RFM)
├── chart_05_dispersao_viabilidade_recuperacao.png # 5. Scatter Plot com Bolhas (Matriz de Decisão)
├── chart_06_data_quality_anomalies_summary.png    # 6. Donut + Barras (Data Quality & Quarentena)
└── golden_metrics_summary.json                    # Resumo JSON com KPIs consolidados
```

---

## 2. 📈 Visualizações & BI Retratado

### 2.1 Visualização 1: Série Temporal (Evolução Semanal de Abandono vs Resgate)
- **Artefato:** [`chart_01_serie_temporal_abandono_resgate.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/dashboards/assets/chart_01_serie_temporal_abandono_resgate.png)
- **Conceito de BI:** Permite monitorar a sazonalidade do e-commerce, picos de tráfego e a eficácia das réguas de automação ao longo das semanas de 2026.
- **KPIs Relacionados:** Taxa de Abandono (~70.9%), Taxa de Recuperação (~10.1%), GMV Abandonado (R$).

---

### 2.2 Visualização 2: Performance de Catálogo por Categoria
- **Artefato:** [`chart_02_performance_categorias.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/dashboards/assets/chart_02_performance_categorias.png)
- **Conceito de BI:** Identifica quais categorias do marketplace sofrem maior atrito no checkout (ex: Eletrônicos com ticket elevado vs Moda com maior volume de conversão).
- **Atendimento ao Case:** Cumpre o requisito explícito de análise de categorias de produto.

---

### 2.3 Visualização 3: Rentabilidade Financeira e ROI por Canal (Combo Chart)
- **Artefato:** [`chart_03_roi_eficiencia_canais.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/dashboards/assets/chart_03_roi_eficiencia_canais.png)
- **Conceito de BI:** Cruza o custo operacional unitário de mensageria com o faturamento recuperado, demonstrando por que o E-mail tem ROI explosivo (~113x) e o WhatsApp entrega maior volume financeiro absoluto (R$ 215.000).

---

### 2.4 Visualização 4: Matriz de Atrito — Motivos de Abandono por Segmento RFM
- **Artefato:** [`chart_04_matriz_motivos_rfm_heatmap.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/dashboards/assets/chart_04_matriz_motivos_rfm_heatmap.png)
- **Conceito de BI:** Mostra a causa-raiz comportamental: clientes *Novos* abandonam por frete e preço; clientes *Premium* abandonam por indecisão e navegação.

---

### 2.5 Visualização 5: Dispersão de Viabilidade & Priorização Prescritiva
- **Artefato:** [`chart_05_dispersao_viabilidade_recuperacao.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/dashboards/assets/chart_05_dispersao_viabilidade_recuperacao.png)
- **Conceito de BI:** Matriz de decisão para acionamento comercial e Data Apps: segmenta carrinhos no quadrante de ouro (alto ticket + alta probabilidade de conversão).

---

### 2.6 Visualização 6: Resumo de Data Quality & Quarentena
- **Artefato:** [`chart_06_data_quality_anomalies_summary.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/dashboards/assets/chart_06_data_quality_anomalies_summary.png)
- **Conceito de BI:** Evidência executiva do Item 4, ilustrando a taxa de 94,2% de registros qualificados e a distribuição de 5,8% de anomalias isoladas.
