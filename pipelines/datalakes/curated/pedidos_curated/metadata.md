---
doc_id: "meta_curated_pedidos_001"
version: "1.0.0"
layer: "curated"
entity_name: "pedidos_curated"
storage_path: "pipelines/datalakes/curated/pedidos_curated/"
snowflake_table: "CART_RECOVERY_GOLD.PEDIDOS_CURATED"
classification: "Interno / Analítico"
owner: "Controladoria & Finanças de E-commerce"
upstream:
  - layer: "qualify"
    table: "qualify.pedidos"
downstream:
  - consumer: "Metabase: Relatório Financeiro e Faturamento"
  - consumer: "Data App de Atribuição de Receita"
---

# 📊 Catálogo & Metadados: pedidos_curated

## 💼 Visão de Negócio & Papel na Camada Curated
O dataset `pedidos_curated` estrutura a visão consolidada de faturamento e conversões financeiras originadas tanto do checkout orgânico quanto das campanhas de recuperação de carrinho. Ele possibilita a conciliação exata da receita líquida resgatada, deduzindo custos de frete e concessão de cupons de incentivo. A granularidade é de uma linha por ordem de compra liquidada.

## ⚙️ Diretrizes de Modelagem e Agregações
O modelo integra chaves dimensionais de tempo, cliente e canal de resgate. As medidas armazenadas refletem numeradores financeiros aditivos (`valor_total`, `desconto_total`, `valor_frete`), assegurando total consistência em agregações multidimensionais sem distorções de cálculo. Os contratos de campos seguem as **validações declaradas no corpo da entidade** em [`pedidos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/pedidos.md).
