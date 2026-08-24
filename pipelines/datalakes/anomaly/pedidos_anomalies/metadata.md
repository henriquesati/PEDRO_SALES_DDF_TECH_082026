---
doc_id: "meta_anomaly_pedidos_001"
version: "1.0.0"
layer: "anomaly"
entity_name: "pedidos_anomalies"
storage_path: "pipelines/datalakes/anomaly/pedidos_anomalies/"
snowflake_table: "CART_RECOVERY_ANOMALIES.PEDIDOS_ANOMALIES"
classification: "Interno / Auditoria"
owner: "Área Financeira & Engenharia de Dados"
upstream:
  - layer: "raw"
    table: "pedidos_raw"
downstream:
  - consumer: "Conciliação de Faturamento"
---

# ⚠️ Catálogo & Metadados: pedidos_anomalies

## 💼 Visão de Negócio & Papel na Camada Anomaly
O dataset `pedidos_anomalies` isola ordens de compra emitidas com valores monetários zerados ou negativos, status de pagamento indefinidos, parcelamentos incompatíveis com a forma de liquidação ou ausência de identificação do cliente pagador. A granularidade é de uma linha por transação de pedido com desvio.

## ⚙️ Regras de Isolamento e Diagnóstico de Falhas
Os registros são armazenados para conciliação entre o gateway de pagamentos e o ERP. As checagens de validação e as regras de obrigatoriedade de campos violadas correspondem às **validações declaradas no corpo da entidade** em [`pedidos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/pedidos.md).
