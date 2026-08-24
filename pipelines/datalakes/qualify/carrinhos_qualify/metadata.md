---
doc_id: "meta_qualify_carrinhos_001"
version: "1.0.0"
layer: "qualify"
entity_name: "carrinhos_qualify"
storage_path: "pipelines/datalakes/qualify/carrinhos_qualify/"
snowflake_table: "CART_RECOVERY.CARRINHOS"
dadosfera_asset_id: "e2d3b1bb-bf22-456e-bc66-4ac843deec82"
classification: "Interno"
owner: "Engenharia de Dados & Produto Analytics"
upstream:
  - layer: "raw"
    table: "carrinhos_raw"
downstream:
  - layer: "curated"
    target: "curated.carrinhos_curated"
  - layer: "curated"
    target: "curated.fato_abandono"
---

# 🧹 Catálogo & Metadados: carrinhos_qualify

## 💼 Visão de Negócio & Papel na Camada Qualify
A tabela `carrinhos_qualify` consolida as sessões de carrinho que foram validadas tecnicamente e cumprem integralmente as regras de integridade contábil e de negócio. Ela é o ativo central do pipeline de recuperação, separando com precisão os carrinhos convertidos organicamente, expirados e abandonados elegíveis para réguas de resgate. A granularidade é estritamente atômica: uma linha por sessão de carrinho.

## ⚙️ Diretrizes de Transformação e Qualidade
Os dados brutos passam por padronização de tipos (conversão de valores para float/decimal e timestamps ISO canônicos) e deduplicação. A aprovação para esta camada exige a verificação da equação contábil de fechamento financeiro, validade temporal entre criação e abandono, e existência da chave de cliente. Todos os critérios de validação estrutural e de integridade correspondem às **validações declaradas no corpo da entidade** em [`carrinhos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/carrinhos.md).
