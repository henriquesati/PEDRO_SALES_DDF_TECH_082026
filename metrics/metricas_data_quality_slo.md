# 🛡️ Métricas de Qualidade de Dados, Quarentena & SLOs da Plataforma

> **Módulo:** `metrics/`  
> **Papel Arquitetural:** Governança de Confiabilidade de Dados (Data Observability, SRE de Dados & Data Contracts)  
> **Framework Normativo:** [`DEC-006`](../docs/specifications/data-quality-specification.md) (Dual-Artifact Pipeline: Silver Qualify vs Silver Anomalies) • [`DEC-007`](../docs/relatorios/decision-making/dec-007-natural-broken-rates.md) (Taxas Naturais)  
> **Evidências de Auditoria:** [`pipelines/case-item-04/outputs/data_quality_report.md`](../pipelines/case-item-04/outputs/data_quality_report.md)

---

## 📌 1. Visão Geral e Princípios de Data Quality

Na arquitetura da **Dadosfera**, a confiabilidade das métricas de negócio depende diretamente da integridade dos dados que transitam pelo Lakehouse. Conforme a decisão arquitetural `DEC-006`, o pipeline de Data Quality adota a abordagem **Dual-Artifact**: dados em conformidade avançam para a camada **Silver Qualify** (e posteriormente Gold DW), enquanto registros inconsistentes são isolados na **Silver Anomalies (Quarentena Auditável)** sem poluir os dashboards nem quebrar o pipeline.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CAMADA BRONZE (RAW DATA)                           │
│                          115.775 registros brutos                           │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│               MOTOR DE VALIDAÇÃO DADOSFERA (Great Expectations)             │
│            18 Regras Contratuais de Validação e Integridade                 │
└──────────────────┬──────────────────────────────────────┬───────────────────┘
                   │ (98.76% Conformes)                   │ (1.24% Desvios)
                   ▼                                      ▼
┌──────────────────────────────────────┐  ┌───────────────────────────────────┐
│        CAMADA SILVER QUALIFY         │  │      CAMADA SILVER ANOMALIES      │
│      114.336 registros aprovados     │  │   1.439 registros em quarentena   │
│   (Alimenta Gold DW & Metabase)      │  │  (Auditoria de Risco & Segurança) │
└──────────────────────────────────────┘  └───────────────────────────────────┘
```

---

## 📊 2. Métricas Consolidadas de Qualidade por Entidade

Os dados abaixo refletem a execução auditada do pipeline de qualificação do **Item 4**:

| Entidade | Registros RAW (Bronze) | Registros Qualify (Silver) | Anomalias Isoladas (Quarentena) | Taxa de Rejeição (%) | Principais Anomalias Detectadas |
|---|:---:|:---:|:---:|:---:|---|
| `carrinhos` | 7.500 | 6.525 | 988 | **13.0%** | Frete negativo, subtotal zerado, total divergente, desconto > subtotal |
| `clientes` | 1.500 | 1.386 | 114 | **7.6%** | E-mail nulo, regex malformado, LTV inconsistente sem compras |
| `produtos` | 300 | 286 | 14 | **4.67%** | Preço promocional invertido (`preco_atual > preco_original`) |
| `eventos_resgate` | 6.427 | 6.289 | 138 | **2.15%** | Inversão temporal (`data_abertura < data_envio`) |
| `itens_carrinho` | 18.888 | 18.690 | 198 | **1.05%** | Inversão temporal de adição/remoção, produto órfão |
| `eventos_carrinho` | 78.931 | 78.931 | 0 | **0.0%** | Telemetria íntegra e ordenada |
| `pedidos` | 2.229 | 2.229 | 0 | **0.0%** | Conciliação contábil 1:1 perfeita |
| **TOTAL GERAL** | **115.775** | **114.336** | **1.439** | **1.24%** | **Conformidade Global: 98.76%** |

---

## 📐 3. As 6 Dimensões Clássicas de Data Quality

Para monitoramento contínuo da saúde dos dados, são calculados 6 indicadores dimensionais:

### 3.1 Completude (Completeness Score)
- **Definição:** Percentual de campos obrigatórios (*NOT NULL*) devidamente preenchidos.
- **Fórmula:** $\text{Completeness (\%)} = \left( 1 - \frac{\text{COUNT}(\text{campos críticos nulos})}{\text{Total de campos avaliados}} \right) \times 100$
- **Resultado:** **99.35%** (isolamento de e-mails nulos em clientes).

### 3.2 Validade & Sintaxe (Validity Score)
- **Definição:** Percentual de valores em conformidade com regex e regras de domínio (ex.: formato de e-mail, máscara de telefone, faixas de preço).
- **Fórmula:** $\text{Validity (\%)} = \left( \frac{\text{COUNT}(\text{registros válidos por regex/range})}{\text{Total de registros}} \right) \times 100$
- **Resultado:** **98.80%**.

### 3.3 Unicidade (Uniqueness Score)
- **Definição:** Inexistência de registros duplicados em chaves primárias e naturais (`carrinho_id`, `cliente_id`, `pedido_id`).
- **Resultado:** **100.0%** (zero duplicidade após deduplicação via `catalog_assets.py` / `DEC-005`).

### 3.4 Acurácia Contábil (Accuracy Score)
- **Definição:** Concordância matemática exata entre equações contábeis de fechamento ($\text{valor\_total} = \text{subtotal} + \text{frete} - \text{desconto}$).
- **Resultado:** **98.92%** (5.0% de anomalias contábeis injetadas e isoladas com sucesso).

### 3.5 Consistência Temporal (Timeliness & Chronology Score)
- **Definição:** Respeito absoluto à cronologia de eventos ($\text{data\_criacao} \le \text{data\_envio} \le \text{data\_abertura} \le \text{data\_conversao}$).
- **Resultado:** **99.51%**.

### 3.6 Integridade Referencial (Referential Integrity Score)
- **Definição:** Existência de chaves estrangeiras válidas (sem registros órfãos entre itens e produtos/carrinhos).
- **Resultado:** **100.0%** na camada Qualify.

---

## ⏱️ 4. Service Level Objectives (SLOs) & SLAs de Pipeline

A tabela abaixo define os acordos de nível de serviço operacional da plataforma de dados:

| Indicador de Confiabilidade (SLI) | Service Level Objective (SLO) | SLA Limite Tolerável | Ação em Caso de Violação |
|---|:---:|:---:|---|
| **Conformidade Global de DQ** | $\ge 98.0\%$ | $\ge 95.0\%$ | Alerta automático no canal de Engenharia de Dados |
| **Taxa de Quarentena (Anomalias)** | $\le 2.0\%$ | $\le 5.0\%$ | Notificação para time de produto/origem dos dados |
| **Latência do Pipeline Batch (Item 8)** | $< 3.0 \text{ segundos}$ | $< 10.0 \text{ segundos}$ | Otimização de queries e particionamento colunar |
| **Data Freshness (Camada Gold)** | $< 1 \text{ hora}$ | $< 4 \text{ horas}$ | Reexecução automática de pipeline no Maestro |
| **Disponibilidade de Consulta OLAP** | $99.9\%$ | $99.5\%$ | Failover e escalonamento elétrico de nós Snowflake |

---

## 🎯 5. Impacto de Negócio da Governança de DQ

1. **Prevenção de Spam e Danos de Reputação:** Isolar e-mails inválidos e telefones sem máscara impede que a plataforma realize disparos com erro, protegendo o *sender score* de e-mail e evitando custos de SMS/WhatsApp rejeitados pela operadora.
2. **Proteção Financeira e de Margem:** Isolar carrinhos com frete negativo ou desconto superior ao subtotal evita faturar pedidos deficitários.
3. **Métricas Não-Poluídas no Metabase:** A camada Gold e os dashboards do **Item 7** consom exclusivamente a camada **Silver Qualify**, garantindo que nenhum indicador executivo seja distorcido por dados corrompidos.
