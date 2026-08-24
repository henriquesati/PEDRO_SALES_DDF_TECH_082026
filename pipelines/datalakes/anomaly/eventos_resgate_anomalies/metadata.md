---
doc_id: "meta_anomaly_eventos_resgate_001"
version: "1.0.0"
layer: "anomaly"
entity_name: "eventos_resgate_anomalies"
storage_path: "pipelines/datalakes/anomaly/eventos_resgate_anomalies/"
snowflake_table: "CART_RECOVERY_ANOMALIES.EVENTOS_RESGATE_ANOMALIES"
classification: "Interno / Auditoria"
owner: "CRM de Resgate & Growth Marketing"
upstream:
  - layer: "raw"
    table: "eventos_resgate_raw"
downstream:
  - consumer: "Auditoria de Campanhas de CRM"
---

# ⚠️ Catálogo & Metadados: eventos_resgate_anomalies

## 💼 Visão de Negócio & Papel na Camada Anomaly
O dataset `eventos_resgate_anomalies` isola disparos de marketing que apresentaram quebra da lógica de funil de conversão (como registros que acusam conversão ou clique sem registro prévio de abertura ou entrega) ou inconsistências de tempo onde a abertura ocorreu antes do envio do disparo. A granularidade é de uma linha por disparo anômalo.

## ⚙️ Regras de Isolamento e Diagnóstico de Falhas
Os registros são retidos para conciliação junto aos fornecedores de disparos de mensageria (provedores de e-mail, gateway SMS, WhatsApp Business API). Os testes lógicos e restrições temporais violadas seguem as **validações declaradas no corpo da entidade** em [`eventos_resgate.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/eventos_resgate.md).
