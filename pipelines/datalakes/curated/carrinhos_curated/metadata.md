---
doc_id: "meta_curated_carrinhos_001"
version: "1.0.0"
layer: "curated"
entity_name: "carrinhos_curated"
storage_path: "pipelines/datalakes/curated/carrinhos_curated/"
snowflake_table: "CART_RECOVERY_GOLD.CARRINHOS_CURATED"
classification: "Interno / Analítico"
owner: "BI & Growth Analytics"
upstream:
  - layer: "qualify"
    table: "qualify.carrinhos"
downstream:
  - consumer: "Metabase: Dashboard Executivo de Abandono"
  - consumer: "Data App Streamlit de Inteligência de Resgate"
---

# 📊 Catálogo & Metadados: carrinhos_curated

## 💼 Visão de Negócio & Papel na Camada Curated
O dataset `carrinhos_curated` consolida as sessões de carrinho enriquecidas com métricas de tempo até abandono, classificação de risco e status final de recuperação. Ele atua como o ativo primário para a avaliação de desempenho global do marketplace, permitindo aos tomadores de decisão analisar as taxas de conversão direta versus recuperação via CRM. A granularidade é de uma linha por sessão de carrinho enriquecida.

## ⚙️ Diretrizes de Modelagem e Agregações
Nesta camada, os dados são vinculados às chaves surrogate de tempo, dispositivo e canal. As medidas quantitativas armazenadas são puramente aditivas (como valor total em risco e contagem de sessões), delegando o cômputo de percentuais e taxas de conversão para o tempo de consulta (DEC-001). A integridade dimensional e os domínios categóricos de status obedecem às **validações declaradas no corpo da entidade** em [`carrinhos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/carrinhos.md).
