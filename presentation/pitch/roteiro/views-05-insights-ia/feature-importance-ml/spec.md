# 🧠 Especificação Visual & Técnica: Feature Importance & Pesos do Modelo ML (`feature-importance-ml`)

> **Momento do Roteiro**: **Ato 4 / Seção [5.1.1] — Pesos Técnicos e Transparência do Modelo Supervisionado (Explainable AI / XAI)**  
> **Artefato Gerado**: [`chart_feature_importance_ml.png`](chart_feature_importance_ml.png) (e referência técnica [`ml_feature_importance.png`](../../../../pipelines/case-item-08/outputs/assets/ml_feature_importance.png))  
> **Framework Normativo**: [`DEC-001`](../../../docs/relatorios/decision-making/pitch/pitch.txt) (% e Ratios) • Stepsfera Standard • Scikit-Learn / Snowpark ML  
> **Fontes de Dados (Ground Truth)**: `pipelines/case-item-08/stepsfera/step_05_train_churn_model.py`, `pipelines/case-item-08/outputs/pipeline_execution_summary.json`, `metrics/metricas_ml_genai.md`.

---

## 🎯 1. Papel no Roteiro e Mensagem Estratégica

No **Módulo de Inteligência** da Dadosfera, os modelos preditivos não são caixas-pretas inalcançáveis para o time de negócio. A plataforma democratiza a interpretabilidade de Machine Learning (**Explainable AI**), permitindo que analistas e gestores de CRM compreendam com exatidão matemática quais fatores impulsionam a recuperação de cada carrinho.

### 🥊 Contraste de Valor no Pitch:
* **Antes (AWS DIY):** Modelos treinados em scripts isolados com pouca visibilidade para o Marketing. O time de negócios não sabe por que o algoritmo priorizou determinado cliente, gerando desconfiança e intervenções manuais contraproducentes.
* **Agora (Dadosfera):** Decomposição transparente dos coeficientes e pesos de features calculados in-database via **Stepsfera (Item 8)** em apenas **111.7 ms**, gerando regras operacionais automatizadas para cada canal de mensageria.

---

## 📊 2. Decomposição do Painel Visual

O painel executivo 16:9 é estruturado em 4 blocos analíticos de alta densidade:

1. **Header com 4 KPI Cards de Destaque**:
   * **Mecanismo Stepsfera**: *Snowpark ML / In-Database* — Eliminação de cold-start de clusters Spark/Glue.
   * **Driver Preditor #1**: *Ticket do Carrinho (+38.4%)* — Maior alavanca de esforço e retorno.
   * **Poder Discriminativo**: *ROC-AUC: 0.9478* — Discriminação de alto rigor estatístico.
   * **Acurácia no Teste**: *99.53% (F1: 0.995)* — Avaliação sobre 1.285 carrinhos do conjunto de teste.

2. **Ranking Horizontal de Pesos das Features (Feature Importance)**:
   * **`valor_carrinho_atribuido` (Ticket do Carrinho)**: **`+38.4%`** — Cestas de alto valor (R$ > 500) têm maior engajamento e justificam atendimento VIP.
   * **`segmento_rfm_premium` (Segmentação RFM VIP)**: **`+26.2%`** — Clientes com histórico de compras respondem prontamente a comunicações.
   * **`motivo_atrito_frete` (Sensibilidade a Frete)**: **`+18.5%`** — Elevada elasticidade a incentivos de frete grátis ou cupons imediatos.
   * **`flag_clicado_mobile` (Engajamento Mobile)**: **`+9.8%`** — Maior conversão em mensagens instantâneas (WhatsApp).
   * **`historico_frequencia_compras`**: **`+7.1%`** — Recompra natural facilitada.
   * **`tempo_sessao_abandono` (Abandono < 5 min)**: **`-12.3%`** — Sessões superficiais têm menor propensão e não justificam canais caros.

3. **Decomposição Dimensional dos Fatores de Resgate**:
   * Visualização sintética agrupada por macro-dimensões:
     * *Valor Monetário (Ticket)*: 38.4%
     * *Perfil & Histórico do Cliente*: 33.3%
     * *Causa-Raiz do Atrito*: 18.5%
     * *Canal & Telemetria Mobile*: 9.8%

4. **Matriz de Regras Operacionais Prescritivas (CRM Actionable)**:
   * Ações prescritivas acionadas em tempo real pelas réguas da Dadosfera com base no vetor de propensão do carrinho.

---

## 🛠️ 3. Governança e Reprodutibilidade

* **Script Python**: [`generate_chart.py`](generate_chart.py)
* **Padrão Gráfico**: Fundo Branco Puro (`#FFFFFF`), alta legibilidade, tipografia `Segoe UI` e resolução de 300 DPI (`charts-maker` standard).
* **Integridade**: Zero hardcoding — todas as medidas reconciliam com `metrics/metricas_ml_genai.md` e `pipelines/case-item-08/outputs/pipeline_execution_summary.json`.
