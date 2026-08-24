---
doc_id: "meta_curated_itens_carrinho_001"
version: "1.0.0"
layer: "curated"
entity_name: "itens_carrinho_curated"
storage_path: "pipelines/datalakes/curated/itens_carrinho_curated/"
snowflake_table: "CART_RECOVERY_GOLD.ITENS_CARRINHO_CURATED"
classification: "Interno / Analítico"
owner: "Produto & Category Management"
upstream:
  - layer: "qualify"
    table: "qualify.itens_carrinho"
downstream:
  - consumer: "Metabase: Diagnóstico de Cesta de Compras e Abandono"
---

# 📊 Catálogo & Metadados: itens_carrinho_curated

## 💼 Visão de Negócio & Papel na Camada Curated
O dataset `itens_carrinho_curated` fornece a visão analítica atômica da composição das cestas de compras, correlacionando unidades de produtos, valor monetário representativo na sessão e tempo de permanência de cada item no carrinho antes de uma eventual desistência. A granularidade é de uma linha por item adicionado no carrinho.

## ⚙️ Diretrizes de Modelagem e Agregações
O modelo preserva a granularidade atômica para permitir consultas de cross-sell e afinidade de produtos em carrinhos abandonados. Os tipos de dados e relacionamentos obedecem às **validações declaradas no corpo da entidade** em [`itens_carrinho.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/itens_carrinho.md).
