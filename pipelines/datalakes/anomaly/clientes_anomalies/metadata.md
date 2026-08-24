---
doc_id: "meta_anomaly_clientes_001"
version: "1.0.0"
layer: "anomaly"
entity_name: "clientes_anomalies"
storage_path: "pipelines/datalakes/anomaly/clientes_anomalies/"
snowflake_table: "CART_RECOVERY_ANOMALIES.CLIENTES_ANOMALIES"
classification: "Confidencial (PII / Auditoria)"
owner: "CRM Corporativo & Governança de Dados"
upstream:
  - layer: "raw"
    table: "clientes_raw"
downstream:
  - consumer: "Rotina de Higienização Cadastral"
---

# ⚠️ Catálogo & Metadados: clientes_anomalies

## 💼 Visão de Negócio & Papel na Camada Anomaly
O dataset `clientes_anomalies` quarentena registros de clientes com endereços de e-mail sintaticamente inválidos, telefones mal formatados ou ausência de chaves cadastrais primárias. Isso impede disparos frustrados de réguas de comunicação e preserva a reputação do domínio de envio de e-mails da empresa. A granularidade é de uma linha por cadastro com inconsistência.

## ⚙️ Regras de Isolamento e Diagnóstico de Falhas
Os registros são preservados sob proteção de privacidade e encaminhados para workflows de saneamento cadastral. A validação sintática e as restrições violadas baseiam-se nas **validações declaradas no corpo da entidade** em [`clientes.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/clientes.md).
