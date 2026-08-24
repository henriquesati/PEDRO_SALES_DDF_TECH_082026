---
doc_id: "meta_qualify_clientes_001"
version: "1.0.0"
layer: "qualify"
entity_name: "clientes_qualify"
storage_path: "pipelines/datalakes/qualify/clientes_qualify/"
snowflake_table: "CART_RECOVERY.CLIENTES"
dadosfera_asset_id: "0327fecc-f826-48fb-bb0a-1493fe18a32c"
classification: "Confidencial (PII / LGPD)"
owner: "CRM Corporativo & Governança de Dados"
upstream:
  - layer: "raw"
    table: "clientes_raw"
downstream:
  - layer: "curated"
    target: "curated.clientes_curated"
  - layer: "curated"
    target: "curated.dim_clientes"
---

# 🧹 Catálogo & Metadados: clientes_qualify

## 💼 Visão de Negócio & Papel na Camada Qualify
A tabela `clientes_qualify` é a base mestre higienizada de clientes do marketplace. Ela fornece dados cadastrais auditados, histórico de segmentação RFM e permissões de contato (opt-ins) necessárias para acionamento de réguas de recuperação multicanal. A granularidade é de uma linha por cliente único.

## ⚙️ Diretrizes de Transformação e Qualidade
O pipeline aplica validação sintática estrita sobre e-mails via expressão regular, normaliza nomes e cidades e mascara dados sensíveis para conformidade com a LGPD. As regras de unicidade de chave, preenchimento obrigatório e classificação de sensibilidade obedecem às **validações declaradas no corpo da entidade** em [`clientes.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/clientes.md).
