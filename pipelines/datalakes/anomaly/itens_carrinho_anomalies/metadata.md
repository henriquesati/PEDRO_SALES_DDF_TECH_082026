---
doc_id: "meta_anomaly_itens_carrinho_001"
version: "1.0.0"
layer: "anomaly"
entity_name: "itens_carrinho_anomalies"
storage_path: "pipelines/datalakes/anomaly/itens_carrinho_anomalies/"
snowflake_table: "CART_RECOVERY_ANOMALIES.ITENS_CARRINHO_ANOMALIES"
classification: "Interno / Auditoria"
owner: "Engenharia de Dados & Microserviço de Carrinho"
upstream:
  - layer: "raw"
    table: "itens_carrinho_raw"
downstream:
  - consumer: "Diagnóstico de Microserviços de Checkout"
---

# ⚠️ Catálogo & Metadados: itens_carrinho_anomalies

## 💼 Visão de Negócio & Papel na Camada Anomaly
O dataset `itens_carrinho_anomalies` isola linhas de composição de carrinho com quantidades não-positivas (menores ou iguais a zero), preços unitários negativos ou violações cronológicas onde o timestamp de remoção do item antecede a data de sua adição. A granularidade é de uma linha por item anômalo.

## ⚙️ Regras de Isolamento e Diagnóstico de Falhas
Os registros são retidos com o payload recebido para auditoria de bugs na camada de mensageria da aplicação de checkout. As validações violadas correspondem às **validações declaradas no corpo da entidade** em [`itens_carrinho.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/itens_carrinho.md).
