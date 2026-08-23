# Especificação Visual & Aspecto Técnico: Data Quality & Quarentena de Anomalias

## 📌 Contexto & Aspecto Técnico (Item 4)
- **Desafio de Governança**: Em e-commerces com alto volume transacional, dados corrompidos (frete negativo, emails malformados, totais divergentes) poluem o CRM e geram disparos errôneos ou prejuízo financeiro.
- **Arquitetura Dual-Artifact (DEC-006)**:
  - `_qualify` (Silver Aprovada): 94.2% dos registros em conformidade rigorosa.
  - `_anomalies` (Silver Quarentena): 5.8% dos registros isolados com captura de `payload_raw` e motivo da anomalia para auditoria.

## 📊 Métricas & Fórmulas (Ancoradas em %)
- **Taxa Global de Conformidade**: **94.2%** dos registros passam de primeira na suíte Great Expectations (18 regras implementadas).
- **Taxa de Isolamento em Quarentena**: **5.8%** de anomalias operacionais interceptadas antes do envio de campanhas (ANOM-01 a ANOM-04).
- **Cotas de Dirty Data Determinísticas**: Emails inválidos (3.0%), Frete negativo (4.0%), Total divergente (5.0%), Promoções invertidas (5.0%).

## 🎯 Objetivo no Pitch
Provar a superioridade técnica da Dadosfera contra pipelines manuais: a governança não é um "processo burocrático posterior", mas uma camada ativa de validação automatizada que protege a reputação do cliente e o ROI do marketing.

## 📍 Mapeamento Plataforma Dadosfera
- **Módulo**: Processar / Pipelines & Qualify.
- **Camada**: Silver (`[entidade]_qualify` vs `[entidade]_anomalies`).
- **Suíte de Testes**: Great Expectations (`carrinhos_suite.json`).

## 🖼️ Artefato Visual Gerado
- **Arquivo**: [`chart_06_scorecard_data_quality.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/06_data_quality_e_quarentena/chart_06_scorecard_data_quality.png)
- **Tipo de Gráfico**: Scorecard & Gráfico de Rosca / Barras de Conformidade e Quarentena.
