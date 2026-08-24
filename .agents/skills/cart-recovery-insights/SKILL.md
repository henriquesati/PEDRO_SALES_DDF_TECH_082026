---
name: cart-recovery-insights
description: >-
  Defines and organizes business insights for the Cart Recovery case using
  Markdown specifications instead of manual SQL. Creates and maintains
  insight definitions, KPIs, business rules, dashboard specifications,
  analytics pipeline specifications, and data-app specifications grouped by
  descriptive, risk, prescriptive, and opportunity insights. Use this skill
  when the user wants to define what should be analyzed, measured,
  visualized, validated, or acted upon in the Cart Recovery case, leaving
  SQL, views, and dashboard implementation to the data platform.
  Prioritizes insights that add value to the business and are actionable to be used on a pitch sale and business data driven actions.
---

# Cart Recovery Insights

## Role

Act as a specialized business-analytics specification agent for the Cart Recovery case.

Translate business questions and case requirements into structured Markdown specifications that can later be implemented in Dadosfera or another data platform.

Define **what should be analyzed and how it should be evaluated**. Do not write manual SQL unless explicitly requested.

## Core Principle

Organize the project by **type of business insight**, not by database entity.

Use four categories:

1. **Descriptive** — *What happened?*
2. **Risk** — *What is at risk?*
3. **Prescriptive** — *What should we do?*
4. **Opportunity** — *What can we gain?*

Entities such as customers, carts, products, and events belong in the data model and in the data requirements of each insight, not as the primary folder structure.

## Workflow for a New Insight

When requested to create or analyze an insight:
1. Identify the business question.
2. Classify it as *descriptive*, *risk*, *prescriptive*, or *opportunity*.
3. Identify required datasets and fields.
4. Check whether the current data model supports it.
5. Create the Markdown file in the correct directory (`cart-recovery-case/insights/...`).
6. Add or update KPI definitions in `metrics/`.
7. Add validation rules.
8. Identify dashboard implications when relevant.
9. **Do not write SQL.**
10. **Do not invent unavailable data.** (If required data is missing, explicitly document the gap).
11. **Align with Pitch Canonical Specification:** All insights, KPIs, example ticket values, channel costs, and baseline metrics must strictly reconcile with [`presentation/pitch/pitch_spec.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/pitch_spec.md) (Sections 4 & 5).
12. **Master SSOT for Business Rules & BI:** Consult [`data/data-models/logical/business-rules.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/data-models/logical/business-rules.md) as the official single source of truth for cross-entity business rules, state machines, and canonical KPI formulas.

## Arbitraty contraint for Insight Generation

  This is an intern test case, so it should not opt in for analyze ultra granular things or really edge cases, so it limits the complexity of the project to be finalized under 1 or 2 days. The approach is for a study technical case to be used on a mock pitch interview, not real business data insights, so dont create unnecessary or overly complex things.


## Project Structure

Maintain:

```text
├── insights/
│   ├── 01_descriptive/
│   ├── 02_risk/
│   ├── 03_prescriptive/
│   └── 04_opportunity/
├── dashboards/
└── metrics/
    ├── README.md                      # Governança semântica e padrões de agregação
    ├── catalogo_kpis.md               # Catálogo Master de KPIs de Negócio e Fórmulas LaTeX
    ├── matriz_metricas_dimensoes.md   # Matriz Semântica Dimensional (Kimball DW)
    ├── arvore_metricas_driver_tree.md # Driver Tree da North Star Metric (Decomposição Causal)
    ├── metricas_data_quality_slo.md   # Métricas de Confiabilidade, Quarentena e SLOs de Dados
    └── metricas_ml_genai.md           # Avaliação de Modelos de ML (Item 8) e GenAI/LLM (Item 5)
```

Do not create empty or unnecessary files merely to fill the structure.

---

## Insight Template

Every insight Markdown file should follow:

```markdown
# [Insight Title]

## ❓ Pergunta de Negócio
[Business question]

## 📊 Métrica
- **KPI**: [name]
- **Fórmula**: [logical formula in natural language, not SQL]
- **Granularidade**: [day/week/month/customer/cart/etc.]
- **Dimensões**: [comparison dimensions]
- **Alvo**: [target, if known]

## 💡 Insight Esperado
[Expected pattern, hypothesis or anomaly]

## 📍 Dadosfera Config
- **Tipo**: [Exploração / View / Dashboard / Pipeline / Data App]
- **Camada**: [Raw / Processed / Enriched / Analytics]
- **Dados necessários**: [datasets/tables]
- **Campos necessários**: [fields]
- **Relacionamentos**: [logical relationships]

### Passos
1. [High-level transformation]
2. [Aggregation/comparison]
3. [Metric calculation]
4. [Visualization/interpretation]

## ✅ Como Validar
- [Validation rule]
- [Consistency check]
- [Expected range]
- [Reconciliation rule]

## 🎯 Recomendação Acionável
[Business action if the hypothesis is confirmed]

## 💰 ROI
[Financial impact, percentage impact, or calculation methodology]
```

> [!IMPORTANT]
> **Do not write SQL in these insight specification files.**

---

## Insight Categories

### 1. `insights/01_descriptive/` — O que aconteceu?
Describe what happened.
- **Typical analyses**: abandonment volume, abandonment rate, abandonment reasons, temporal patterns, device impact, session duration, recovery volume, recovery rate.

### 2. `insights/02_risk/` — O que está em risco?
Identify elevated risk and vulnerability patterns.
- **Typical analyses**: RFM segmentation, risk score, high-value carts at risk, product abandonment, churn risk, recovery probability.
- *Rule*: Prefer transparent business rules over unexplained ML models unless the user explicitly requests machine learning.

### 3. `insights/03_prescriptive/` — O que devemos fazer?
Determine what action should be taken.
- **Typical analyses**: channel effectiveness, optimal recovery timing, segment strategy, ROI per action, cross-sell opportunity.
- *Workflow connection*: **Observation → Decision → Action → Expected impact**

### 4. `insights/04_opportunity/` — O que podemos ganhar?
Estimate upside and prioritize improvements.
- **Typical analyses**: recovery potential, revenue at risk, recoverable revenue, improvement roadmap.
- *Rule*: Clearly distinguish observed, potential, recoverable, and incremental revenue.

### 5 Facts, Hypotheses and Recommendations

Clearly distinguish:
- **Fact**: Directly measured from the data.
- **Hypothesis**: Expected pattern to investigate.
- **Recommendation**: Action proposed after evidence.

*Never present an expected pattern as an observed result.*

---

## Dashboard Specifications

Files under `dashboards/` describe the desired analytical result, not implementation details:

```markdown
# [Dashboard Name]

## Objetivo
## Público
## KPIs
## Filtros
## Visualizações
## Insights Relacionados
## Regras de Atualização
## Alertas
## Critérios de Sucesso
```

---

For each transformation specify:
- **Source & Destination**
- **Fields involved**
- **Business transformation logic**
- **Expected output**
- **Validation rules**

## Validation & Quality Rules

Prefer domain/business validation. Examples:
- Recovery percentage is between 0% and 100%.
- Recovered carts have an associated recovery event.
- Recovery timestamp does not precede abandonment timestamp.
- Cart value is consistent with the sum of its items.
- Event customer matches cart customer.
- Category percentages reconcile to the expected total.

---

## Dadosfera Mapping

Every insight must specify its Dadosfera mapping:
```markdown
## 📍 Dadosfera Config
- **Tipo**: Exploração / View / Dashboard / Pipeline / Data App
- **Camada**: Raw / Processed / Enriched / Analytics
- **Dados necessários**: [tabelas]
- **Campos necessários**: [colunas]
- **Relacionamentos**: [joins lógicos]
```

---

## ROI Calculation

- Do not fabricate monetary results.
- If data supports it, document the calculation logic. Otherwise, state that the impact must be estimated after measuring incremental uplift.


---

## Scope & Boundaries

- **In Scope**: Business analytics specifications, metric definitions, insight Markdown files, validation rules, Dadosfera configuration mappings.
- **Out of Scope (Default)**: Manual SQL, DDL, migrations, database indexing, AWS infra (Kinesis, Firehose, Redis), production ML pipelines.

---

## Definition of Done

An insight is complete when a third party can clearly understand:
1. The business question.
2. The KPI and logical formula.
3. Required data and fields.
4. Logical transformations.
5. Expected result / hypothesis.
6. Validation rules.
7. Resulting actionable recommendation.
8. ROI / value methodology.
9. Mapping to the data platform (Dadosfera).
