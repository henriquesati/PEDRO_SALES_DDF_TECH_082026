# Especificação Visual & Regra de Negócio: Série Temporal de Abandono vs Recuperação

## 📌 Contexto & Regra de Negócio
- **Regra de Ciclo de Vida do Carrinho**: Um carrinho ativo transiciona para `'abandonado'` após 30 minutos de inatividade do cliente. Caso o cliente retorne através de uma régua de resgate, o status muda para `'recuperado'` e, ao finalizar o checkout, para `'comprado'`. Carrinhos sem retorno após 90 dias tornam-se `'expirados'`.
- **Período de Análise**: Janeiro a Junho de 2026 (6 meses com sazonalidade e picos em março/maio).

## 📊 Métricas & Fórmulas (Ancoradas em %)
- **Taxa de Abandono (%)**: $\frac{\text{Carrinhos Abandonados}}{\text{Total de Carrinhos Criados}} \times 100 \approx 69.7\%$ (Alinhado ao benchmark global Baymard Institute de ~69.8%).
- **Taxa de Recuperação Geral (%)**: $\frac{\text{Carrinhos Recuperados}}{\text{Total de Carrinhos Abandonados}} \times 100 \approx 10.1\%$ (Benchmark Klaviyo/Salesforce: 5% a 15%).
- **Lift de Conversão com Resgate**: $+50\%$ de incremento sobre a taxa basal de conversão sem intervenção.

## 🎯 Objetivo no Pitch
Provar a consistência estatística do problema de abandono e demonstrar como as réguas de comunicação da Dadosfera interceptam o vale de abandono, gerando uma curva de resgate previsível e sustentável ao longo de todo o primeiro semestre.

## 📍 Mapeamento Plataforma Dadosfera
- **Módulo**: Visualizar / Metabase & Pipelines.
- **Camada**: Gold (Kimball DW - `fato_abandono`, `fato_resgate` e `dim_tempo`).
- **Visão Analítica**: `v_abandonment_summary`.

## 🖼️ Artefato Visual Gerado
- **Arquivo**: [`chart_01_serie_temporal_abandono_resgate.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/01_abandono_vs_recuperacao_timeline/chart_01_serie_temporal_abandono_resgate.png)
- **Tipo de Gráfico**: Gráfico de Linhas com Múltiplos Eixos Y (Taxas % vs Volumes Absolutos).
