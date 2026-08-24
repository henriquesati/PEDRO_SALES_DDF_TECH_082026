---
doc_id: "meta_qualify_eventos_resgate_001"
version: "1.0.0"
layer: "qualify"
entity_name: "eventos_resgate_qualify"
storage_path: "pipelines/datalakes/qualify/eventos_resgate_qualify/"
snowflake_table: "CART_RECOVERY.EVENTOS_RESGATE"
dadosfera_asset_id: "04739f6d-e8c3-4d6f-80b7-0f98c12a5798"
classification: "Interno"
owner: "CRM de Resgate & Growth Marketing"
upstream:
  - layer: "raw"
    table: "eventos_resgate_raw"
downstream:
  - layer: "curated"
    target: "curated.eventos_resgate_curated"
  - layer: "curated"
    target: "curated.fato_resgate"
---

# 🧹 Catálogo & Metadados: eventos_resgate_qualify

## 💼 Visão de Negócio & Papel na Camada Qualify
A tabela `eventos_resgate_qualify` contém os disparos de réguas de recuperação de CRM que atenderam a todos os critérios de conformidade técnica e integridade lógica de funil de marketing. Ela viabiliza a mensuração precisa do ROI por canal e da eficiência dos gatilhos de engajamento. A granularidade é de uma linha por disparo de campanha.

## ⚙️ Diretrizes de Transformação e Qualidade
O pipeline aplica testes estritos de monotonicidade do funil (`entregue >= aberto >= clicado >= convertido`), validando que a data de abertura nunca anteceda a data de envio e que os custos de disparo sejam não-negativos. As regras detalhadas de qualidade de dados baseiam-se nas **validações declaradas no corpo da entidade** em [`eventos_resgate.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/eventos_resgate.md).
