# 🧠 Especificação Canônica: Feature Importance & Pesos do Modelo ML (`05_feature_importance_ml`)

> **Módulo:** `insights/04_intelligence_ai/05_feature_importance_ml/`  
> **Artefato Canônico:** [`chart_feature_importance_ml.png`](chart_feature_importance_ml.png) (e [`ml_feature_importance.png`](../../../pipelines/case-item-08/outputs/assets/ml_feature_importance.png))  
> **Item do Case:** Item 8 — Pipelines & Machine Learning na Dadosfera  
> **Framework Normativo:** [`DEC-001`](../../../docs/relatorios/decision-making/pitch/pitch.txt) • Stepsfera Standard • Scikit-Learn / Snowpark ML  
> **Fontes de Dados (Ground Truth):** `pipelines/case-item-08/stepsfera/step_05_train_churn_model.py`, `pipelines/case-item-08/outputs/pipeline_execution_summary.json`, `metrics/metricas_ml_genai.md`.

---

## 🎯 1. Visão Geral e Mensagem Estratégica

Enquanto abordagens legadas (AWS DIY) sofrem com modelos "caixa-preta" e clusters Spark desconectados da operação, a Dadosfera viabiliza a extração e visualização imediata dos pesos das variáveis (*Explainable AI / XAI*) treinadas in-database via **Stepsfera / Snowpark ML**.

O classificador supervisionado de propensão de recuperação identifica os drivers matemáticos de maior elasticidade para priorização na régua de CRM:
* **Ticket do Carrinho (`valor_carrinho_atribuido`):** **`+38.4%`** — Principal alavanca marginal de engajamento do consumidor.
* **Segmentação RFM VIP (`segmento_rfm_premium`):** **`+26.2%`** — Clientes fiéis com alta probabilidade de conversão após lembrete.
* **Atrito de Frete (`motivo_atrito_frete`):** **`+18.5%`** — Alta elasticidade a incentivo pontual de frete grátis ou cupom.
* **Engajamento Mobile:** **`+9.8%`** — Maior resposta em canais instantâneos (WhatsApp/Push).
* **Abandono Ultrarrápido (< 5 min):** **`-12.3%`** — Menor propensão que requer canal de baixo custo (Push automatizado) em vez de disparo caro.

---

## 📊 2. Decomposição do Painel Visual (16:9 Widescreen)

1. **Header com 4 KPI Cards**:
   * **Mecanismo Stepsfera**: Snowpark ML in-database (Zero cold-start).
   * **Driver Preditor #1**: Ticket do Carrinho (+38.4%).
   * **Poder Discriminativo**: ROC-AUC: 0.9478.
   * **Acurácia no Teste**: 99.53% (F1: 0.995) em 1.285 amostras.

2. **Ranking Horizontal de Pesos (Feature Importance)**:
   * Barras verdes (impacto propulsor positivo) e barras coral (fricção/impacto redutor), com anotações de percentual exato.

3. **Decomposição Dimensional dos Fatores de Resgate**:
   * Agregação por macro-pilares (Monetário, Perfil/Cliente, Causa do Atrito, Canal/Telemetria).

4. **Matriz de Regras Operacionais Prescritivas**:
   * Ações táticas de CRM acionadas automaticamente com base no score de cada variável.

---

## 🛠️ 3. Governança e Reprodutibilidade

* **Script Python**: `generate_chart.py`
* **Padrão Gráfico**: Fundo Branco Puro (`#FFFFFF`), 300 DPI, `charts-maker` standard.
* **Integridade de Dados**: 100% alinhado com `pipelines/case-item-08/outputs/pipeline_execution_summary.json` e `metrics/metricas_ml_genai.md`.
