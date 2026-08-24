---
doc_id: "meta_raw_pedidos_001"
version: "1.0.0"
layer: "raw"
entity_name: "pedidos_raw"
storage_path: "pipelines/datalakes/raw/pedidos_raw/"
format: "parquet"
dadosfera_asset_id: "7f82a988-8e68-416a-b6fa-5007c4789d1a"
classification: "Interno"
owner: "Área Financeira & Engenharia de Dados"
upstream:
  source: "ERP Corporativo / Checkout Gateway"
  protocol: "Batch S3 Landing"
downstream:
  - layer: "qualify"
    target: "qualify.pedidos"
  - layer: "anomaly"
    target: "anomaly.pedidos_anomalies"
---

# 📥 Catálogo & Metadados: pedidos_raw

## 💼 Visão de Negócio & Papel na Camada Raw
O dataset `pedidos_raw` consolida os registros brutos de transações financeiras e ordens de compra finalizadas pelos clientes no marketplace. Ele viabiliza a apuração do faturamento bruto e o rastreamento da conversão de vendas e recuperação de receita. A granularidade do dataset é de uma linha por ordem de compra gerada.

## ⚙️ Diretrizes de Ingestão e Governança
Os registros aterrissam diariamente em arquivos Parquet com carimbo de carga, sendo mantidos inclusive registros com pedidos cancelados ou pendentes de estorno para auditoria contábil. A conformidade estrutural e os tipos de dados obedecem às **validações declaradas no corpo da entidade** em [`pedidos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/data-models/logical/entities/pedidos.md).
