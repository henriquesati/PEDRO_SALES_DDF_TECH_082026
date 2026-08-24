---
doc_id: "meta_curated_eventos_carrinho_001"
version: "1.0.0"
layer: "curated"
entity_name: "eventos_carrinho_curated"
storage_path: "pipelines/datalakes/curated/eventos_carrinho_curated/"
snowflake_table: "CART_RECOVERY_GOLD.EVENTOS_CARRINHO_CURATED"
classification: "Interno / Analítico"
owner: "UX Research & Telemetria"
upstream:
  - layer: "qualify"
    table: "qualify.eventos_carrinho"
downstream:
  - consumer: "Metabase: Funil de Checkout & Análise de Fricção de UX"
---

# 📊 Catálogo & Metadados: eventos_carrinho_curated

## 💼 Visão de Negócio & Papel na Camada Curated
O dataset `eventos_carrinho_curated` estrutura a telemetria comportamental em uma visão de funil de conversão consolidado, permitindo mensurar a taxa de transição e o tempo médio despendido em cada etapa (visualização do carrinho, frete, endereço, pagamento) para detectar pontos de atrito na experiência do usuário. A granularidade é de uma linha por evento de telemetria consolidado.

## ⚙️ Diretrizes de Modelagem e Agregações
O modelo preserva a sequência de navegação e flags de transição entre etapas. Todas as definições conceituais e restrições de consistência baseiam-se nas **validações declaradas no corpo da entidade** em [`eventos_carrinho.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/eventos_carrinho.md).
