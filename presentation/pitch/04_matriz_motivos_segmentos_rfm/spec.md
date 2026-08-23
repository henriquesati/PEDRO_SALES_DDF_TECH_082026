# Especificação Visual & Regra de Negócio: Matriz de Motivos vs Segmentos RFM

## 📌 Contexto & Regra de Negócio
- **Regra de Classificação de Motivo de Abandono**:
  - `pagamento`: Último evento foi `erro_pagamento`.
  - `indecisao`: Visualizou checkout sem iniciar pagamento.
  - `frete`: `valor_frete > 15% do valor_subtotal`.
  - `preco`: Fricção por ausência de cupom ou valor alto.
  - `estoque`: Item indisponível durante a navegação.
- **Segmentação RFM**:
  - `premium`: LTV > R$ 2.000, 5+ compras, ativo nos últimos 30 dias.
  - `regular`: LTV R$ 500–2.000, 2–4 compras, ativo nos últimos 90 dias.
  - `dormant`: LTV < R$ 500, inativo há mais de 90 dias.
  - `novo`: Primeira visita / 0 compras.

## 📊 Métricas & Fórmulas (Ancoradas em %)
- **Taxa de Recuperação por Segmento**:
  - *Premium*: ~18% (alta responsividade).
  - *Regular*: ~10% (volume central).
  - *Novo*: ~12% (reativo a cupom de primeira compra).
  - *Dormant*: ~6% (menor taxa, mas reativação crítica).
  - **Ratio Premium / Dormant**: **3x** (comprova matematicamente que segmentar compensa).
- **Distribuição de Causa-Raiz (%)**: % de ocorrência de cada motivo dentro de cada segmento RFM.

## 🎯 Objetivo no Pitch
Evidenciar a perda de receita que ocorre quando uma empresa envia réguas genéricas de desconto. Com a Dadosfera, clientes Premium que abandonam por indecisão recebem prova social e contato VIP, enquanto novos clientes com atrito de frete recebem incentivo logístico.

## 📍 Mapeamento Plataforma Dadosfera
- **Módulo**: Visualizar / Metabase & Pipelines.
- **Camada**: Gold (Kimball DW - `dim_clientes`, `dim_motivo_abandono`, `dim_segmento_rfm`, `fato_abandono`).
- **Visão Analítica**: `v_abandonment_summary`.

## 🖼️ Artefato Visual Gerado
- **Arquivo**: [`chart_04_matriz_motivos_rfm_heatmap.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/04_matriz_motivos_segmentos_rfm/chart_04_matriz_motivos_rfm_heatmap.png)
- **Tipo de Gráfico**: Mapa de Calor (Heatmap) com Percentuais de Incidência Cruzada.
