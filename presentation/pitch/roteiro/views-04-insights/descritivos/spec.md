# 📈 Módulo de Views: Insights Descritivos (`views-04-insights/descritivos`)

> **Momento do Roteiro**: **Ato 3 / Seção [4.1] — Diagnóstico da Operação: O que aconteceu nos 7.500 carrinhos de compras**  
> **Caminho da View**: `presentation/pitch/roteiro/views-04-insights/descritivos/`  
> **Arquitetura Master**: [`presentation/pitch/roteiro/README.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/README.md)  
> **Fontes Estratégicas**: [`presentation/pitch/roteiro.txt`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro.txt), [`presentation/pitch/pitch_spec.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/pitch_spec.md#32-regras-de-negócio-e-evidências-analíticas) e [`data/mock/output_cleaned/parquet/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/mock/output_cleaned/parquet/).

---

## 🎯 1. Visão Geral dos Submódulos Descritivos

Este diretório agrupa as visões analíticas descritivas que comprovam o gargalo estrutural de abandono de carrinhos no e-commerce e a capacidade de resgate da Dadosfera, estruturado nos 3 submódulos abaixo:

---

## 📊 2. Tabela de Módulos & Artefatos

| Submódulo | Foco de Apresentação | Principais Métricas | Artefato Gráfico |
| :--- | :--- | :--- | :---: |
| [`funilrecuperacao/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-04-insights/descritivos/funilrecuperacao/) | **Diagnóstico da Operação** | 7.500 carrinhos, 69,7% abandono, +10,1% recuperação (+R$ 167,9k), ROI 45x | [`chart_insights_descritivos.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-04-insights/descritivos/funilrecuperacao/chart_insights_descritivos.png) |
| [`motivosabandono/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-04-insights/descritivos/motivosabandono/) | **Causas-Raiz de Abandono** | Frete Caro (38,2%), Indecisão (24,1%), Erro Checkout (18,3%) | [`chart_02_motivos_abandono.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-04-insights/descritivos/motivosabandono/chart_02_motivos_abandono.png) |
| [`custorecuperacao/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-04-insights/descritivos/custorecuperacao/) | **CAC de Resgate & ROI** | CAC E-mail R$ 1,02, Push R$ 1,67, SMS R$ 3,00, WhatsApp R$ 12,00 | [`chart_03_custo_recuperacao_roi.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-04-insights/descritivos/custorecuperacao/chart_03_custo_recuperacao_roi.png) |
