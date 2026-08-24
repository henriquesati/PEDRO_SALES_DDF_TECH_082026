---
doc_id: "meta_anomaly_carrinhos_001"
version: "1.0.0"
layer: "anomaly"
entity_name: "carrinhos_anomalies"
storage_path: "pipelines/datalakes/anomaly/carrinhos_anomalies/"
snowflake_table: "CART_RECOVERY_ANOMALIES.CARRINHOS_ANOMALIES"
classification: "Interno / Auditoria"
owner: "Engenharia de Dados & Sustentação"
upstream:
  - layer: "raw"
    table: "carrinhos_raw"
downstream:
  - consumer: "Painel de Auditoria de Anomalias"
  - consumer: "Rotina de Reconciliação Contábil"
---

# ⚠️ Catálogo & Metadados: carrinhos_anomalies

## 💼 Visão de Negócio & Papel na Camada Anomaly
O dataset `carrinhos_anomalies` armazena as sessões de carrinho que apresentaram desvios contábeis, quebra de contratos de schema ou inconsistências temporais durante o Quality Gate da camada Silver. Em conformidade com o DEC-006, o isolamento em quarentena de anomalias protege os relatórios analíticos contra dados corrompidos, mantendo histórico integral para saneamento operacional e auditoria. A granularidade é de uma linha por registro anômalo diagnosticado.

## ⚙️ Regras de Isolamento e Diagnóstico de Falhas
Os registros são bifurcados para esta camada com a preservação do payload original e a injeção de metadados de diagnóstico (`anomalia_id`, `codigo_erro`, `severidade`, `detected_at`). Os desvios capturados incluem violação da equação contábil de fechamento financeiro, frete negativo, desconto superior a 100% do subtotal e data de abandono anterior à data de criação, conforme as **validações declaradas no corpo da entidade** em [`carrinhos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/carrinhos.md).
