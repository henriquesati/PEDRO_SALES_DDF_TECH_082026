---
doc_id: "meta_qualify_pedidos_001"
version: "1.0.0"
layer: "qualify"
entity_name: "pedidos_qualify"
storage_path: "pipelines/datalakes/qualify/pedidos_qualify/"
snowflake_table: "CART_RECOVERY.PEDIDOS"
dadosfera_asset_id: "7f82a988-8e68-416a-b6fa-5007c4789d1a"
classification: "Interno"
owner: "Área Financeira & Engenharia de Dados"
upstream:
  - layer: "raw"
    table: "pedidos_raw"
downstream:
  - layer: "curated"
    target: "curated.pedidos_curated"
  - layer: "curated"
    target: "curated.fato_resgate"
---

# 🧹 Catálogo & Metadados: pedidos_qualify

## 💼 Visão de Negócio & Papel na Camada Qualify
A tabela `pedidos_qualify` consolida todas as compras aprovadas e faturadas no marketplace. Ela estabelece a conexão exata entre a ordem de compra finalizada, o carrinho original de origem e o identificador do disparo de marketing que motivou a conversão, viabilizando o cálculo de receita recuperada líquida. A granularidade é de uma linha por ordem de pedido.

## ⚙️ Diretrizes de Transformação e Qualidade
O pipeline valida a não-nulidade e unicidade da chave primária, a integridade referencial com clientes e carrinhos, a coerência financeira de valores totais positivos e a correlação entre a flag de origem de resgate e o ID da campanha. As regras detalhadas de qualidade e integridade dimensional seguem as **validações declaradas no corpo da entidade** em [`pedidos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/pedidos.md).
