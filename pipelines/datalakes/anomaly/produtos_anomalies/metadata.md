---
doc_id: "meta_anomaly_produtos_001"
version: "1.0.0"
layer: "anomaly"
entity_name: "produtos_anomalies"
storage_path: "pipelines/datalakes/anomaly/produtos_anomalies/"
snowflake_table: "CART_RECOVERY_ANOMALIES.PRODUTOS_ANOMALIES"
classification: "Interno / Auditoria"
owner: "Catálogo de Produtos & Merchandising"
upstream:
  - layer: "raw"
    table: "produtos_raw"
downstream:
  - consumer: "Auditoria de Preços e Catálogo"
---

# ⚠️ Catálogo & Metadados: produtos_anomalies

## 💼 Visão de Negócio & Papel na Camada Anomaly
O dataset `produtos_anomalies` quarentena SKUs com preços zerados ou negativos, além de itens com anomalia de promoção invertida (onde o preço promocional cadastrado supera o preço de tabela original). Esse isolamento previne cálculos distorcidos de tíquete médio e margem financeira. A granularidade é de uma linha por produto em inconformidade.

## ⚙️ Regras de Isolamento e Diagnóstico de Falhas
Os registros são direcionados ao time de merchandising para retificação no PIM. As condições de preço e integridade de categorização violadas seguem as **validações declaradas no corpo da entidade** em [`produtos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/produtos.md).
