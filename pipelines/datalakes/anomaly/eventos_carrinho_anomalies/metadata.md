---
doc_id: "meta_anomaly_eventos_carrinho_001"
version: "1.0.0"
layer: "anomaly"
entity_name: "eventos_carrinho_anomalies"
storage_path: "pipelines/datalakes/anomaly/eventos_carrinho_anomalies/"
snowflake_table: "CART_RECOVERY_ANOMALIES.EVENTOS_CARRINHO_ANOMALIES"
classification: "Interno / Auditoria"
owner: "Produto Analytics & Telemetria Web/App"
upstream:
  - layer: "raw"
    table: "eventos_carrinho_raw"
downstream:
  - consumer: "Monitoramento de Telemetria de Checkout"
---

# ⚠️ Catálogo & Metadados: eventos_carrinho_anomalies

## 💼 Visão de Negócio & Papel na Camada Anomaly
O dataset `eventos_carrinho_anomalies` isola telemetrias com payloads de evento corrompidos, ausência de identificador de sessão de carrinho ou quebras severas na hierarquia de navegação de checkout que indiquem falhas de instrumentação no frontend web ou aplicativo. A granularidade é de uma linha por evento anômalo.

## ⚙️ Regras de Isolamento e Diagnóstico de Falhas
Os registros são armazenados para suporte ao time de engenharia de frontend e telemetria. Os critérios de conformidade violados baseiam-se nas **validações declaradas no corpo da entidade** em [`eventos_carrinho.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/eventos_carrinho.md).
