# 🧠 Especificação Canônica: Modelos Preditivos de Negócio (`01_modelos_preditivos_ml`)

> **Módulo:** `insights/04_intelligence_ai/01_modelos_preditivos_ml/`  
> **Artefato Canônico:** [`chart_modelos_preditivos_ml.png`](chart_modelos_preditivos_ml.png)  
> **Item do Case:** Item 8 — Pipelines & Machine Learning na Dadosfera  
> **Framework Normativo:** [`DEC-001`](../../../docs/relatorios/decision-making/pitch/pitch.txt) • Stepsfera Standard • Scikit-Learn / Snowpark ML  
> **Fontes de Dados (Ground Truth):** `data/mock/output_cleaned/parquet/carrinhos.parquet`, `eventos_resgate.parquet`, `metrics/metricas_ml_genai.md`.

---

## 🎯 1. Visão Geral e Alavancagem Analítica

O classificador supervisionado de propensão de recuperação atua na camada Gold para ranquear a chance de conversão de cada carrinho abandonado. O modelo treinado atinge **ROC-AUC de 0.9478** e **99.53% de acurácia**, permitindo que a operação de CRM priorize os clientes mais responsivos e proteja a margem financeira.
