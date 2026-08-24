---
doc_id: "meta_qualify_eventos_carrinho_001"
version: "1.0.0"
layer: "qualify"
entity_name: "eventos_carrinho_qualify"
storage_path: "pipelines/datalakes/qualify/eventos_carrinho_qualify/"
snowflake_table: "CART_RECOVERY.EVENTOS_CARRINHO"
dadosfera_asset_id: "397c3ebc-15cb-42d2-a717-a3b5d150c3ea"
classification: "Interno"
owner: "Produto Analytics & Telemetria Web/App"
upstream:
  - layer: "raw"
    table: "eventos_carrinho_raw"
downstream:
  - layer: "curated"
    target: "curated.eventos_carrinho_curated"
---

# 🧹 Catálogo & Metadados: eventos_carrinho_qualify

## 💼 Visão de Negócio & Papel na Camada Qualify
A tabela `eventos_carrinho_qualify` estrutura a sequência temporal de navegação e interações de checkout executadas pelo usuário em cada sessão. Ela fundamenta o mapeamento de etapas críticas onde ocorre desistência (ex: etapa de frete ou pagamento). A granularidade é de uma linha por evento de telemetria auditado.

## ⚙️ Diretrizes de Transformação e Qualidade
O pipeline valida a coerência cronológica dos eventos, elimina registros duplicados por retransmissão de rede e confirma a vinculação com sessões ativas de carrinho. As especificações de tipos e categorização de etapas respeitam as **validações declaradas no corpo da entidade** em [`eventos_carrinho.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/eventos_carrinho.md).
