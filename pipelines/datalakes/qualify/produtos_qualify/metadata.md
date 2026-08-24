---
doc_id: "meta_qualify_produtos_001"
version: "1.0.0"
layer: "qualify"
entity_name: "produtos_qualify"
storage_path: "pipelines/datalakes/qualify/produtos_qualify/"
snowflake_table: "CART_RECOVERY.PRODUTOS"
dadosfera_asset_id: "65fcfa25-a6f3-4cb8-a444-7fd23df3fa84"
classification: "Interno"
owner: "Catálogo de Produtos & Merchandising"
upstream:
  - layer: "raw"
    table: "produtos_raw"
downstream:
  - layer: "curated"
    target: "curated.produtos_curated"
---

# 🧹 Catálogo & Metadados: produtos_qualify

## 💼 Visão de Negócio & Papel na Camada Qualify
A tabela `produtos_qualify` contém o catálogo homologado de produtos e marcas comercializados na plataforma. Ela enriquece os itens dos carrinhos com categoria, preços de referência e status de estoque para alimentar análises de elasticidade e atratividade de ofertas. A granularidade é de uma linha por SKU de produto.

## ⚙️ Diretrizes de Transformação e Qualidade
O pipeline valida que o preço atual seja estritamente positivo e não ultrapasse o preço de tabela original, eliminando distorções de promoções invertidas. As especificações de tipos e consistência de categorização seguem as **validações declaradas no corpo da entidade** em [`produtos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/produtos.md).
