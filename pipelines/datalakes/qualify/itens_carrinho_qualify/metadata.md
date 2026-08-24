---
doc_id: "meta_qualify_itens_carrinho_001"
version: "1.0.0"
layer: "qualify"
entity_name: "itens_carrinho_qualify"
storage_path: "pipelines/datalakes/qualify/itens_carrinho_qualify/"
snowflake_table: "CART_RECOVERY.ITENS_CARRINHO"
dadosfera_asset_id: "7649755a-c6e8-4b56-a092-be9eefde1dab"
classification: "Interno"
owner: "Engenharia de Dados & Microserviço de Carrinho"
upstream:
  - layer: "raw"
    table: "itens_carrinho_raw"
downstream:
  - layer: "curated"
    target: "curated.itens_carrinho_curated"
---

# 🧹 Catálogo & Metadados: itens_carrinho_qualify

## 💼 Visão de Negócio & Papel na Camada Qualify
A tabela `itens_carrinho_qualify` detalha os produtos pertencentes a cada sessão de carrinho qualificada. Ela permite analisar tíquete médio por item, volume físico de mercadorias selecionadas e a influência de categorias específicas na taxa de conversão ou abandono. A granularidade é de uma linha por item adicionado no carrinho.

## ⚙️ Diretrizes de Transformação e Qualidade
O pipeline audita que as quantidades sejam números inteiros estritamente positivos, os preços unitários sejam válidos e a data de remoção (quando existente) seja posterior à adição. Todas as restrições relacionais com carrinhos e produtos seguem as **validações declaradas no corpo da entidade** em [`itens_carrinho.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/itens_carrinho.md).
