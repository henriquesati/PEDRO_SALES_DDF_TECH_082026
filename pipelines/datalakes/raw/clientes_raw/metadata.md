---
doc_id: "meta_raw_clientes_001"
version: "1.0.0"
layer: "raw"
entity_name: "clientes_raw"
storage_path: "pipelines/datalakes/raw/clientes_raw/"
format: "parquet"
dadosfera_asset_id: "0327fecc-f826-48fb-bb0a-1493fe18a32c"
classification: "Confidencial (PII / LGPD)"
owner: "CRM Corporativo & Governança de Dados"
upstream:
  source: "CRM de Contas de Usuários"
  protocol: "Batch S3 Landing Criptografado"
downstream:
  - layer: "qualify"
    target: "qualify.clientes"
  - layer: "anomaly"
    target: "anomaly.clientes_anomalies"
---

# 📥 Catálogo & Metadados: clientes_raw

## 💼 Visão de Negócio & Papel na Camada Raw
O dataset `clientes_raw` contém a base cadastral bruta de clientes, histórico de contas e preferências de contato (opt-ins para e-mail, SMS, push e WhatsApp). Ele é a entidade mestra para identificação do consumidor e atribuição de ações de recuperação de carrinho. A granularidade é de uma linha por cliente cadastrado.

## ⚙️ Diretrizes de Ingestão e Governança
Por conter dados pessoais identificáveis (PII), os dados brutos são armazenados sob criptografia at-rest AES-256 e políticas restritas de acesso. Todas as definições de campos, expressões regulares de contato e regras de sensibilidade seguem as **validações declaradas no corpo da entidade** em [`clientes.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/data-models/logical/entities/clientes.md).
