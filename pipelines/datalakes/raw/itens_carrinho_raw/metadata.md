---
doc_id: "meta_raw_itens_carrinho_001"
version: "1.0.0"
layer: "raw"
entity_name: "itens_carrinho_raw"
storage_path: "pipelines/datalakes/raw/itens_carrinho_raw/"
format: "parquet"
dadosfera_asset_id: "7649755a-c6e8-4b56-a092-be9eefde1dab"
classification: "Interno"
owner: "Engenharia de Dados & Microserviço de Carrinho"
upstream:
  source: "Microserviço de Carrinho / Checkout"
  protocol: "Batch S3 Landing"
downstream:
  - layer: "qualify"
    target: "qualify.itens_carrinho"
  - layer: "anomaly"
    target: "anomaly.itens_carrinho_anomalies"
---

# 📥 Catálogo & Metadados: itens_carrinho_raw

## 💼 Visão de Negócio & Papel na Camada Raw
O dataset `itens_carrinho_raw` documenta a composição granular de cada sessão de compra, rastreando produtos específicos, quantidades selecionadas, preços praticados e histórico de adições e remoções. A granularidade é de uma linha por item adicionado em um carrinho.

## ⚙️ Diretrizes de Ingestão e Governança
Os registros brutos são armazenados sem agregações para manter o grão atômico intacto. As especificações de tipos, chaves estrangeiras vinculadas a carrinhos e produtos, e regras de integridade cronológica de adição/remoção baseiam-se nas **validações declaradas no corpo da entidade** em [`itens_carrinho.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/data-models/logical/entities/itens_carrinho.md).
