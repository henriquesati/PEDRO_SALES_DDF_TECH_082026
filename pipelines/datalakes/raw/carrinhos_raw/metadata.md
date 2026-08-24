---
doc_id: "meta_raw_carrinhos_001"
version: "1.0.0"
layer: "raw"
entity_name: "carrinhos_raw"
storage_path: "pipelines/datalakes/raw/carrinhos_raw/"
format: "parquet"
dadosfera_asset_id: "e2d3b1bb-bf22-456e-bc66-4ac843deec82"
classification: "Interno"
owner: "Engenharia de Dados & Webstore"
upstream:
  source: "Webstore / E-commerce Session Collector"
  protocol: "Batch S3 Landing"
downstream:
  - layer: "qualify"
    target: "qualify.carrinhos"
  - layer: "anomaly"
    target: "anomaly.carrinhos_anomalies"
---

# 📥 Catálogo & Metadados: carrinhos_raw

## 💼 Visão de Negócio & Papel na Camada Raw
O dataset `carrinhos_raw` representa a captura bruta e imutável das sessões de compra abertas pelos usuários na plataforma de e-commerce e aplicativo móvel. Seu propósito é registrar o estado das intenções de compra no instante exato da captura, servindo como histórico operacional fidedigno para auditoria e conciliação contábil. A granularidade é de uma linha por sessão de carrinho criada.

## ⚙️ Diretrizes de Ingestão e Governança
Os dados são ingeridos em lotes diários e persistidos no formato Parquet sob compressão Snappy, preservando integralmente a estrutura da fonte sem descarte de linhas. As regras de tipagem, estrutura de campos, unicidade e domínios aceitos correspondem às **validações declaradas no corpo da entidade** em [`carrinhos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/data-models/logical/entities/carrinhos.md).
