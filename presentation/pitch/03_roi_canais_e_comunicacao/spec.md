# Especificação Visual & Regra de Negócio: Eficiência de Canais & ROI de Resgate

## 📌 Contexto & Regra de Negócio
- **Topologia de Canais & Custos Unitários**:
  - `push_app`: R$ 0,02 por envio (menor custo unitário, alta velocidade).
  - `email`: R$ 0,05 por envio (espinha dorsal de volume e maior ROI agregado).
  - `sms`: R$ 0,15 por envio (canal de reforço com alta taxa de entrega).
  - `whatsapp`: R$ 0,30 por envio (maior engajamento e conversão unitária para clientes Premium).
- **Fórmula do ROI**:
  $$\text{ROI} = \frac{\text{Receita Recuperada} - \text{Descontos} - \text{Custo de Disparos}}{\text{Custo de Disparos}}$$

## 📊 Métricas & Fórmulas (Ancoradas em Ratios e %)
- **Funil de Conversão por Canal**:
  - *Email*: Abertura ~42% | Clique ~28% | Conversão ~15% (Conversão End-to-End: ~4.5%).
  - *WhatsApp*: Abertura ~68% | Clique ~35% | Conversão ~18% (Conversão End-to-End: ~2.5%).
  - *SMS*: Abertura ~55% | Clique ~22% | Conversão ~14% (Conversão End-to-End: ~1.8%).
  - *Push*: Abertura ~30% | Clique ~18% | Conversão ~12% (Conversão End-to-End: ~1.2%).
- **ROI Consolidado Multiplicador**: **~45x** (para cada R$ 1,00 investido em disparos, retornam R$ 45,00 líquidos).
- **Custo por Conversão**: **< 1%** do valor do pedido resgatado.

## 🎯 Objetivo no Pitch
Eliminar o receio do cliente sobre o custo de campanhas multicanal, provando que a orquestração inteligente da Dadosfera equilibra volume de baixo custo (Email/Push) com canais de alto impacto (WhatsApp para VIPs), mantendo o ROI acima de 40x.

## 📍 Mapeamento Plataforma Dadosfera
- **Módulo**: Visualizar / Metabase & Pipelines.
- **Camada**: Gold (Kimball DW - `dim_canal_resgate`, `fato_resgate`).
- **Visão Analítica**: `v_recovery_roi_by_segment`.

## 🖼️ Artefato Visual Gerado
- **Arquivo**: [`chart_03_roi_eficiencia_canais.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/03_roi_canais_e_comunicacao/chart_03_roi_eficiencia_canais.png)
- **Tipo de Gráfico**: Gráfico Combinado (Combo Chart - Barras de Conversão e Custo vs Linha de Múltiplo de ROI).
