---
doc_id: "meta_raw_produtos_001"
version: "1.0.0"
layer: "raw"
entity_name: "produtos_raw"
storage_path: "pipelines/datalakes/raw/produtos_raw/"
format: "parquet"
dadosfera_asset_id: "65fcfa25-a6f3-4cb8-a444-7fd23df3fa84"
classification: "Interno"
owner: "Catálogo de Produtos & Merchandising"
upstream:
  source: "PIM / Catálogo de Marketplace"
  protocol: "Batch S3 Landing"
downstream:
  - layer: "qualify"
    target: "qualify.produtos"
  - layer: "anomaly"
    target: "anomaly.produtos_anomalies"
---

# 📥 Catálogo & Metadados: produtos_raw

## 💼 Visão de Negócio & Papel na Camada Raw
O dataset `produtos_raw` registra o catálogo completo de SKUs comercializados no marketplace, incluindo marcas, categorias e tabelas de preços originais e promocionais. Sua finalidade é prover o contexto mercadológico dos itens presentes nos carrinhos abandonados. A granularidade é de uma linha por produto único.

## ⚙️ Diretrizes de Ingestão e Governança
A carga ocorre via snapshots periódicos em Parquet com codificação UTF-8 estrita para preservação de acentuações. Os critérios de tipo, chave primária e consistência de valores monetários correspondem às **validações declaradas no corpo da entidade** em [`produtos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/data-models/logical/entities/produtos.md).
