---
doc_id: "meta_raw_eventos_resgate_001"
version: "1.0.0"
layer: "raw"
entity_name: "eventos_resgate_raw"
storage_path: "pipelines/datalakes/raw/eventos_resgate_raw/"
format: "parquet"
dadosfera_asset_id: "04739f6d-e8c3-4d6f-80b7-0f98c12a5798"
classification: "Interno"
owner: "CRM de Resgate & Growth Marketing"
upstream:
  source: "Hub de Disparo de Mensagens (E-mail, SMS, Push, WhatsApp)"
  protocol: "Batch S3 Landing"
downstream:
  - layer: "qualify"
    target: "qualify.eventos_resgate"
  - layer: "anomaly"
    target: "anomaly.eventos_resgate_anomalies"
---

# 📥 Catálogo & Metadados: eventos_resgate_raw

## 💼 Visão de Negócio & Papel na Camada Raw
O dataset `eventos_resgate_raw` registra o histórico operacional de todos os disparos de réguas de recuperação de carrinho acionadas pela equipe de CRM (via E-mail, SMS, Push Notification e WhatsApp). Ele é o insumo fundamental para avaliar a eficácia das mensagens, taxas de abertura e custo de envio. A granularidade é de uma linha por disparo de régua de comunicação.

## ⚙️ Diretrizes de Ingestão e Governança
Os lotes são recebidos com metadados de envio e telemetria de engajamento do destinatário. A consistência de schema e os domínios de canais e gatilhos de resgate seguem as **validações declaradas no corpo da entidade** em [`eventos_resgate.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/data-models/logical/entities/eventos_resgate.md).
