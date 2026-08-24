---
doc_id: "meta_qualify_produtos_enriquecidos_001"
version: "1.0.0"
layer: "qualify"
entity_name: "produtos_enriquecidos_qualify"
storage_path: "pipelines/datalakes/qualify/produtos_enriquecidos_qualify/"
snowflake_table: "CART_RECOVERY.PRODUTOS_ENRIQUECIDOS"
dadosfera_asset_id: "78aeef12-9c41-4da2-b118-8ee12cf4da99"
classification: "Interno"
owner: "Inteligência de IA, CRM & Merchandising"
upstream:
  - layer: "qualify"
    table: "produtos_qualify"
  - layer: "raw"
    table: "checkout_feedback_raw"
downstream:
  - layer: "curated"
    target: "curated.v_recovery_roi_by_segment"
  - layer: "serving"
    target: "metabase.dashboards"
  - layer: "apps"
    target: "streamlit.data_app"
---

# 🤖 Catálogo & Metadados: produtos_enriquecidos_qualify

## 💼 Visão de Negócio & Papel na Camada Qualify
A tabela `produtos_enriquecidos_qualify` armazena o catálogo de produtos enriquecido com **features semânticas estruturadas extraídas por Inteligência Artificial Generativa (LLMs)** a partir de textos livres de anúncios e feedbacks de abandono de checkout. Ela fornece a base de inteligência para identificar atrito técnico em SKUs, segmentar clientes por sensibilidade a preço e acionar disparos de resgate altamente personalizados no CRM.

## ⚙️ Diretrizes de Transformação e Qualidade
O pipeline de GenAI (`pipelines/case-item-05/scripts/run_genai_pipeline.py`) processa os campos textuais desestruturados e valida a estrutura de saída através de contratos estritos **Pydantic** e **JSON Schema**. Todas as colunas, tipagens e descrições seguem as **validações declaradas no corpo da entidade** em [`produtos_enriquecidos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/produtos_enriquecidos.md).
