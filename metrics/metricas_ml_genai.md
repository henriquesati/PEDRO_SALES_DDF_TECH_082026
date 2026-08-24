# 🤖 Métricas de Avaliação de Machine Learning & GenAI

> **Módulo:** `metrics/`  
> **Papel Arquitetural:** Registro e Governança de Performance de Modelos Preditivos e Generativos (MLOps / LLMOps)  
> **Framework Normativo:** [`DEC-001`](../docs/relatorios/decision-making/pitch/pitch.txt) (% e Ratios) • Pydantic Contract Standards  
> **Evidências de Execução:** [`pipelines/case-item-08/outputs/pipeline_execution_summary.json`](../pipelines/case-item-08/outputs/pipeline_execution_summary.json) • [`pipelines/case-item-05/outputs/genai_feature_extraction_report.md`](../pipelines/case-item-05/outputs/genai_feature_extraction_report.md)

---

## 📌 1. Visão Geral da Camada de Inteligência

No ecossistema da **Dadosfera**, a inteligência analítica combina dois paradigmas complementares:
1. **Modelagem Preditiva Clássica (Machine Learning - Item 8):** Classificação tabular de propensão de recuperação e risco de churn de carrinhos na camada Gold.
2. **Inteligência Generativa (GenAI & LLMs - Item 5):** Transformação de textos desestruturados (catálogo técnico e feedbacks de checkout) em features estruturadas (JSON Schema) e geração contextual de copies de resgate.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CAMADA GOLD DW & DADOS ESTRUTURADOS                      │
└──────────────────────┬───────────────────────────────┬──────────────────────┘
                       │                               │
                       ▼                               ▼
┌──────────────────────────────────────┐  ┌───────────────────────────────────┐
│     MODELO PREDITIVO DE CHURN /      │  │    PIPELINE GENAI DE ENRIQUECIMENTO│
│   PROPENSÃO DE RESGATE (Item 8)      │  │      & COPYWRITING (Item 5)       │
│  • Regularized Logistic Regression   │  │  • Pydantic Parser & JSON Schema  │
│  • ROC-AUC: 0.9478                   │  │  • Aderência Contratual: 100%     │
│  • Acurácia Global: 99.53%           │  │  • Normalização de Catálogo & NLP │
└──────────────────┬───────────────────┘  └───────────────────┬───────────────┘
                   │                                          │
                   ▼                                          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│               CONSUMO DOWNSTREAM (Metabase Item 7 & Streamlit Item 9)        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧠 2. Métricas do Modelo Preditivo de Propensão (Item 8)

O modelo preditivo foi treinado e avaliado no pipeline modular do **Item 8** (`step_05_train_churn_model.py`), utilizando split estratificado 80/20 sobre os dados validados da camada Gold:

### 2.1 Indicadores Globais de Performance
- **Nome do Modelo:** *Regularized Logistic Regression (Cart Recovery Propensity)*
- **Volumetria de Treino / Teste:** `5.142` registros de treino | `1.285` registros de teste.
- **Área sob a Curva ROC (ROC-AUC):** **`0.9478`** (Excelente poder discriminativo para separar carrinhos recuperáveis de perdas irreversíveis).
- **Acurácia Global (Accuracy):** **`0.9953` (99.53%)**.
- **F1-Score Ponderado:** **`0.995`**.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                          MATRIZ DE PERFORMANCE (ML)                         │
├────────────────────────────────┬────────────────────────────────────────────┤
│ Métrica Analítica              │ Valor Atingido no Lakehouse               │
├────────────────────────────────┼────────────────────────────────────────────┤
│ ROC-AUC                        │ 0.9478 (94.78%)                            │
│ Acurácia Global                │ 0.9953 (99.53%)                            │
│ Precisão da Classe Positiva    │ 0.9230 (92.30%)                            │
│ Recall da Classe Positiva      │ 0.8870 (88.70%)                            │
│ Duração do Treinamento         │ 111.7 ms (Execução ultrarrápida)          │
└────────────────────────────────┴────────────────────────────────────────────┘
```

### 2.2 Importância Relativa de Features (Top Predictors)
O gráfico de feature importance gerado no pipeline (`pipelines/case-item-08/outputs/assets/ml_feature_importance.png`) evidencia os fatores mais determinantes para o sucesso do resgate:

1. **`valor_total` (Ticket do Carrinho):** $+38.4\%$ de importância relativa (cestas maiores geram maior esforço e engajamento do cliente).
2. **`segmento_rfm_premium`:** $+26.2\%$ de propensão positiva.
3. **`motivo_frete` vs `motivo_preco`:** $+18.5\%$ de responsividade à oferta de benefício financeiro.
4. **`tempo_ate_abandono`:** $-12.3\%$ (abandonos imediatos < 5 min têm menor propensão que sessões longas de pesquisa).
5. **`dispositivo_mobile`:** $+4.6\%$ de agilidade de conversão em disparos de mensageria.

---

## 🤖 3. Métricas do Pipeline GenAI & Extração de Features (Item 5)

O pipeline do **Item 5** processa especificações técnicas de produtos e áudios/mensagens de clientes para enriquecer a tomada de decisão:

### 3.1 Qualidade e Conformidade Contratual de LLMs
- **Aderência ao Schema Pydantic:** **`100.0%`** (todos os outputs em conformidade estrita com o JSON Schema `genai_features_sample.json`).
- **Taxa de Alucinação Detectada:** **`0.0%`** (graças ao uso de schemas rígidos e prompts determinísticos).
- **Acurácia de Normalização de Categorias:** **`100.0%`** (mapeamento correto de 300 produtos nas 7 categorias canônicas).
- **Detecção Causal de Motivo-Raiz de Abandono:** **`96.5%`** de acurácia sobre mensagens de feedback não-estruturadas.

### 3.2 Eficiência Operacional & Custo de Inferência
- **Latência Média de Inferência:** **`4.0 ms`** por registro processado em lote.
- **Custo Médio de Tokens por Produto:** $< \text{R\$ 0,0008}$ por chamada de LLM.
- **Adequação Semântica das Copies Geradas:** 100% das mensagens de resgate (Email/WhatsApp) respeitam a personalização por diferencial do SKU e motivo de objeção (ex.: benefício de frete para Galaxy S24 Ultra e suporte consultivo para clientes VIP).

---

## 📡 4. Monitoramento Contínuo (MLOps / LLMOps na Dadosfera)

Para garantir a perenidade dos modelos em produção:
1. **Data Drift Monitoring:** Monitoramento semanal da distribuição de tickets e motivos de abandono na camada Bronze.
2. **Concept Drift:** Recalibração do classificador de propensão a cada trimestre ou imediatamente antes de grandes eventos sazonais (Black Friday).
3. **LLM Output Gate:** Validação prévia de schema Pydantic antes de qualquer gravação na camada Silver Parquet.
