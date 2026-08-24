---
doc_id: "meta_curated_clientes_001"
version: "1.0.0"
layer: "curated"
entity_name: "clientes_curated"
storage_path: "pipelines/datalakes/curated/clientes_curated/"
snowflake_table: "CART_RECOVERY_GOLD.CLIENTES_CURATED"
classification: "Confidencial (PII / Analítico)"
owner: "CRM Analytics & Ciência de Dados"
upstream:
  - layer: "qualify"
    table: "qualify.clientes"
downstream:
  - consumer: "Metabase: Segmentação RFM & Risco de Churn"
  - consumer: "Data App Streamlit: Recomendador de Resgate"
---

# 📊 Catálogo & Metadados: clientes_curated

## 💼 Visão de Negócio & Papel na Camada Curated
O dataset `clientes_curated` consolida o perfil analítico completo do cliente, incorporando métricas de recência, frequência, valor monetário (LTV), segmentação RFM canônica e scores preditivos de propensão ao resgate e risco de churn. Ele orienta a priorização de investimentos de marketing nos clientes de maior retorno potencial. A granularidade é de uma linha por cliente único.

## ⚙️ Diretrizes de Modelagem e Agregações
Os scores e indicadores são validados no intervalo contínuo normalizado de 0.0 a 1.0, e a categorização RFM respeita os clusters normatizados (`premium`, `regular`, `dormant`, `novo`). As regras de atributos e mascaramento dinâmico de dados pessoais seguem as **validações declaradas no corpo da entidade** em [`clientes.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/clientes.md).
