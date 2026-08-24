---
doc_id: "meta_curated_eventos_resgate_001"
version: "1.0.0"
layer: "curated"
entity_name: "eventos_resgate_curated"
storage_path: "pipelines/datalakes/curated/eventos_resgate_curated/"
snowflake_table: "CART_RECOVERY_GOLD.EVENTOS_RESGATE_CURATED"
classification: "Interno / Analítico"
owner: "CRM de Resgate & Growth Marketing"
upstream:
  - layer: "qualify"
    table: "qualify.eventos_resgate"
downstream:
  - consumer: "Metabase: Dashboard de ROI por Canal de CRM"
  - consumer: "Data App Streamlit: Simulador de Gatilhos de Resgate"
---

# 📊 Catálogo & Metadados: eventos_resgate_curated

## 💼 Visão de Negócio & Papel na Camada Curated
O dataset `eventos_resgate_curated` estrutura a visão analítica de desempenho das réguas de comunicação de marketing de recuperação. Ele correlaciona o canal de envio (E-mail, SMS, Push, WhatsApp), o tipo de gatilho acionado, o custo operacional do disparo e o valor do pedido convertido, viabilizando o cômputo preciso do ROI líquido de recuperação por canal e segmento de cliente. A granularidade é de uma linha por disparo de campanha.

## ⚙️ Diretrizes de Modelagem e Agregações
O modelo preserva as flags individuais do funil (`flag_entregue`, `flag_aberto`, `flag_clicado`, `flag_convertido`) e as métricas financeiras aditivas (`custo_envio`, `valor_pedido_recuperado`). A integridade lógica do funil e os contratos de atributos seguem as **validações declaradas no corpo da entidade** em [`eventos_resgate.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/eventos_resgate.md).
