# 📊 Relatório Executivo de Análise de Dados & BI (Case Item 07)

> **Case Técnico Dadosfera:** Recuperação de Carrinho Abandonado (E-commerce / Marketplace)  
> **Identificador Oficial:** `PEDRO_SALES_DDF_TECH_082026`  
> **Módulo:** `pipelines/case-item-07/` (Hub Central de BI & Serving Analítico)  
> **Status:** ✅ Concluído e Validado (Ground Truth em Parquet)  
> **Notebook Reproduzível:** [`pipelines/case-item-07/notebooks/07_bi_dashboards_visualizations.ipynb`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/notebooks/07_bi_dashboards_visualizations.ipynb)  
> **Script Batch:** [`pipelines/case-item-07/scripts/run_bi_analysis.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/scripts/run_bi_analysis.py) (`python make.py notebook-gen`)  

---

## 1. 🎯 Visão Geral da Entrega & Papel do Hub

Este documento consolida a camada analítica de **Visualização de Dados e BI (Item 7)**, atuando como o **Hub Central** que integra as visualizações analíticas de dashboards no Metabase, os modelos dimensionais Kimball da camada Gold e a camada semântica de governança de KPIs.

Foram gerados **6 tipos distintos de visualizações** a partir dos dados auditados do Lakehouse (`carrinhos`, `produtos`, `eventos_resgate`, `clientes`, `itens_carrinho`), cumprindo integralmente os requisitos de **Análise de Série Temporal**, **Performance de Categorias**, **Rentabilidade/ROI por Canal**, **Matriz de Atrito RFM**, **Dispersão Prescritiva de Viabilidade** e **Scorecard de Data Quality**:

```text
pipelines/case-item-07/outputs/assets/
├── chart_01_serie_temporal_abandono_resgate.png   # 1. Gráfico de Linha Duplo Eixo (Série Temporal)
├── chart_02_performance_categorias.png            # 2. Barras Horizontais (Análise de Categorias)
├── chart_03_roi_eficiencia_canais.png             # 3. Gráfico Combo Barras + Linha (ROI por Canal)
├── chart_04_matriz_motivos_rfm_heatmap.png        # 4. Mapa de Calor (Atrito por Segmento RFM)
├── chart_05_dispersao_viabilidade_recuperacao.png # 5. Scatter Plot com Bolhas (Matriz Prescritiva)
└── chart_06_data_quality_anomalies_summary.png    # 6. Donut + Barras (Data Quality & Quarentena)
```

---

## 2. 📈 Análise Detalhada dos 6 Artefatos Visuais

### 2.1 Visualização 1: Série Temporal (Evolução Semanal de Abandono vs Resgate)
- **Artefato Gerado:** [`chart_01_serie_temporal_abandono_resgate.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_01_serie_temporal_abandono_resgate.png)
- **Tipo de Gráfico:** Time Series com Duplo Eixo Y e preenchimento de área (`fill_between`).
- **Atendimento ao Case:** Cumpre o requisito obrigatório de **análise de série temporal**.
- **Diagnóstico:** A taxa de abandono permanece em um patamar consistente de ~70,9% ao longo de 2026, com a taxa de recuperação atingindo ~10,1% e gerando um fluxo semanal contínuo de GMV recuperado.

![Série Temporal](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_01_serie_temporal_abandono_resgate.png)

---

### 2.2 Visualização 2: Performance de Catálogo por Categoria de Produto
- **Artefato Gerado:** [`chart_02_performance_categorias.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_02_performance_categorias.png)
- **Tipo de Gráfico:** Barras Horizontais Empilhadas/Agrupadas.
- **Atendimento ao Case:** Cumpre o requisito obrigatório de **análise por categoria**.
- **Diagnóstico:** *Eletrônicos* concentra o maior volume absoluto de carrinhos abandonados e maior ticket médio (R$ 850+), sendo o departamento com maior sensibilidade a custos de frete; *Moda* e *Beleza* apresentam o maior índice de resposta rápida a réguas de cupom de primeira compra.

![Performance Categorias](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_02_performance_categorias.png)

---

### 2.3 Visualização 3: Eficiência Financeira e ROI por Canal de Resgate
- **Artefato Gerado:** [`chart_03_roi_eficiencia_canais.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_03_roi_eficiencia_canais.png)
- **Tipo de Gráfico:** Combo Chart (Barras de Receita vs Linha de Multiplicador de ROI).
- **Diagnóstico:** O canal *Email* entrega o maior retorno multiplicador unitário (~113x) pelo custo marginal de envio (R$ 0,02); o *WhatsApp* é responsável pelo maior faturamento absoluto recuperado, justificando seu custo unitário superior (R$ 0,45) em clientes de alto ticket e VIP.

![ROI Canais](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_03_roi_eficiencia_canais.png)

---

### 2.4 Visualização 4: Matriz de Atrito RFM (Heatmap de Causas-Raiz)
- **Artefato Gerado:** [`chart_04_matriz_motivos_rfm_heatmap.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_04_matriz_motivos_rfm_heatmap.png)
- **Tipo de Gráfico:** Mapa de Calor com anotações de densidade percentual.
- **Diagnóstico:** Clientes *Novos* sofrem atrito predominantemente por *Frete Alto* (42%) e *Preço*; clientes *Premium* abandonam por *Indecisão / Navegação* (38%), apontando que estratégias de resgate devem ser personalizadas por segmento.

![Heatmap RFM](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_04_matriz_motivos_rfm_heatmap.png)

---

### 2.5 Visualização 5: Matriz Prescritiva de Viabilidade (Valor vs Probabilidade)
- **Artefato Gerado:** [`chart_05_dispersao_viabilidade_recuperacao.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_05_dispersao_viabilidade_recuperacao.png)
- **Tipo de Gráfico:** Scatter Plot com Bolhas e delimitação do Quadrante de Ouro.
- **Diagnóstico:** Segmenta os carrinhos em tempo real para automação de CRM: carrinhos de alta viabilidade e alto ticket são despachados para atendimento VIP/WhatsApp, enquanto tickets baixos recebem réguas automatizadas de Email/Push.

![Scatter Viabilidade](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_05_dispersao_viabilidade_recuperacao.png)

---

### 2.6 Visualização 6: Scorecard Executivo de Data Quality & Quarentena
- **Artefato Gerado:** [`chart_06_data_quality_anomalies_summary.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_06_data_quality_anomalies_summary.png)
- **Tipo de Gráfico:** Donut de Conformidade + Barras de Anomalias Isoladas.
- **Diagnóstico:** Evidencia a integridade dos dados que alimentam os relatórios: 94,2% de conformidade aprovada na camada Silver Qualify e 5,8% de anomalias isoladas na Quarentena (DEC-006) sem poluir os dashboards executivos.

![Data Quality Summary](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_06_data_quality_anomalies_summary.png)

---

## 3. 🌐 Hub de Referências Cruzadas

O módulo `pipelines/case-item-07/` conecta-se diretamente aos seguintes artefatos do repositório:
- **Dashboards Metabase:** [`dashboards/dashboard_recuperacao_carrinho.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/dashboards/dashboard_recuperacao_carrinho.md)
- **Camada Semântica de Métricas:** [`metrics/catalogo_kpis.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/metrics/catalogo_kpis.md) & [`metrics/matriz_metricas_dimensoes.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/metrics/matriz_metricas_dimensoes.md)
- **Modelagem Dimensional Gold (Item 6):** [`pipelines/case-item-06/specs.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-06/specs.md)
- **Galeria de Gráficos de Insights:** [`insights/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/insights/)
- **Guidelines do Pitch (Item 10):** [`presentation/pitch/pitch_spec.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/pitch_spec.md)
- **Regras Canônicas de Negócio:** [`data/data-models/logical/business-rules.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/data-models/logical/business-rules.md)
