---
doc_id: "meta_curated_produtos_001"
version: "1.0.0"
layer: "curated"
entity_name: "produtos_curated"
storage_path: "pipelines/datalakes/curated/produtos_curated/"
snowflake_table: "CART_RECOVERY_GOLD.PRODUTOS_CURATED"
classification: "Interno / Analítico"
owner: "Pricing & Merchandising Analytics"
upstream:
  - layer: "qualify"
    table: "qualify.produtos"
downstream:
  - consumer: "Metabase: Análise de Elasticidade e Abandono por SKU"
---

# 📊 Catálogo & Metadados: produtos_curated

## 💼 Visão de Negócio & Papel na Camada Curated
O dataset `produtos_curated` estrutura a visão analítica de desempenho de catálogo e categorias, correlacionando elasticidade de preços, descontos médios aplicados e taxa de abandono de carrinhos por linha de produto. Ele apoia decisões de precificação dinâmica e montagem de kits promocionais para recuperação. A granularidade é de uma linha por SKU de produto.

## ⚙️ Diretrizes de Modelagem e Agregações
O modelo preserva medidas de preços de referência e status de estoque para cruzamento com o detalhe de itens abandonados. As restrições de consistência e domínios aceitos baseiam-se nas **validações declaradas no corpo da entidade** em [`produtos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/produtos.md).
