---
doc_id: "meta_raw_eventos_carrinho_001"
version: "1.0.0"
layer: "raw"
entity_name: "eventos_carrinho_raw"
storage_path: "pipelines/datalakes/raw/eventos_carrinho_raw/"
format: "parquet"
dadosfera_asset_id: "397c3ebc-15cb-42d2-a717-a3b5d150c3ea"
classification: "Interno"
owner: "Produto Analytics & Telemetria Web/App"
upstream:
  source: "Clickstream Telemetry Collector"
  protocol: "Semi-Continuous Batch Landing"
downstream:
  - layer: "qualify"
    target: "qualify.eventos_carrinho"
  - layer: "anomaly"
    target: "anomaly.eventos_carrinho_anomalies"
---

# 📥 Catálogo & Metadados: eventos_carrinho_raw

## 💼 Visão de Negócio & Papel na Camada Raw
O dataset `eventos_carrinho_raw` captura a telemetria comportamental e de navegação dos usuários ao longo do funil de checkout (visualização de carrinho, preenchimento de endereço, seleção de frete, escolha de pagamento). Ele permite diagnosticar fricções de UX que provocam o abandono de carrinhos. A granularidade é de uma linha por evento de telemetria emitido na sessão.

## ⚙️ Diretrizes de Ingestão e Governança
Os eventos chegam em alto volume e são particionados temporalmente, assegurando a persistência imutável dos timestamps ISO-8601. A estrutura de atributos e as categorias permitidas de eventos seguem as **validações declaradas no corpo da entidade** em [`eventos_carrinho.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/data-models/logical/entities/eventos_carrinho.md).
