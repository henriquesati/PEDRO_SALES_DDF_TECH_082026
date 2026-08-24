# 🧭 Matriz Semântica Dimensional (Métricas × Dimensões Conformadas)

> **Módulo:** `metrics/`  
> **Arquitetura Subjacente:** Kimball Star Schema (Data Warehouse Gold Layer)  
> **Status:** ✅ Validado & Mapeado  
> **Referência Técnica:** [`pipelines/case-item-06/outputs/data_modeling_report.md`](../pipelines/case-item-06/outputs/data_modeling_report.md) (DEC-008)

---

## 📌 1. Visão Geral da Modelagem Dimensional (Gold DW)

Na arquitetura da Dadosfera, a camada **Gold** opera sob o padrão **Kimball Star Schema**, permitindo consultas analíticas ultrarrápidas (*1-Hop JOINs*) sem aninhamentos complexos. A Matriz Semântica Dimensional define formalmente **quais métricas podem ser fatiadas (*sliced & diced*) por quais dimensões**, evitando erros conceituais de agregação no Metabase (Item 7) ou no Data App Streamlit (Item 9).

```text
                                  ┌───────────────────────────┐
                                  │        dim_tempo          │
                                  └─────────────┬─────────────┘
                                                │
       ┌──────────────────────────┐             │             ┌──────────────────────────┐
       │       dim_clientes       ├─────────────┼────────────→│   fato_resgate (Fact)    │
       └──────────────────────────┘             │             │ (Grão: 1 disparo de CRM) │
                                                │             └─────────────┬────────────┘
                                                │                           │
                                                ▼                           ▼
┌───────────────────────────────┐     ┌───────────────────┐   ┌──────────────────────────┐
│     dim_dispositivo           ├────→│   fato_abandono   │   │     dim_canal_resgate    │
└───────────────────────────────┘     │      (Fact)       │   └──────────────────────────┘
                                      │ (Grão: 1 carrinho)│
┌───────────────────────────────┐     └─────────┬─────────┘   ┌──────────────────────────┐
│     dim_motivo_abandono       ├───────────────┘             │     dim_segmento_rfm     │
└───────────────────────────────┘                             └──────────────────────────┘
```

---

## 📊 2. Matriz de Fatiamento (KPIs × Dimensões Conformadas)

**Legenda:**
- ✅ **Permitido (1-Hop):** Fatiamento direto suportado pela tabela fato correspondente.
- ⚠️ **Indireto (Via Chave Estrangeira):** Fatiamento válido correlacionando a fato do disparo com a fato de abandono (`fato_resgate_sk` $\leftrightarrow$ `fato_abandono_sk`).
- ❌ **Não Aplicável:** Cruzamento conceitualmente inválido no grão atômico.

| ID | KPI / Métrica Analítica | Grão Atômico | Tabela Fato | Tipo de Aditividade | `dim_tempo` | `dim_clientes` | `dim_dispositivo` | `dim_motivo` | `dim_canal` | `dim_segmento_rfm` |
|:---:|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **KPI-01** | **Taxa de Abandono (%)** | 1 Carrinho | `fato_abandono` | Non-Additive | ✅ Diário/Mensal | ✅ Por Perfil | ✅ Mobile/Web | ✅ Por Motivo | ❌ Não houve resgate | ✅ Por RFM |
| **KPI-02** | **Taxa de Recuperação (%)** | 1 Carrinho | `fato_resgate` | Non-Additive | ✅ Data Resgate | ✅ Histórico | ⚠️ Via Abandono | ⚠️ Via Abandono | ✅ Por Canal | ✅ Por RFM |
| **KPI-03** | **Lift de Conversão (%)** | Agregado | `fato_resgate` | Non-Additive | ✅ Mensal | ❌ Global | ❌ Global | ❌ Global | ✅ Por Canal | ✅ Por RFM |
| **KPI-04** | **Taxa de Retenção de GMV (%)** | 1 Carrinho | `fato_resgate` | Non-Additive | ✅ Por Mês | ✅ Por Cliente | ⚠️ Via Abandono | ⚠️ Via Abandono | ✅ Por Canal | ✅ Por RFM |
| **KPI-05A** | **Taxa de Abertura (%)** | 1 Disparo | `fato_resgate` | Non-Additive | ✅ Data Envio | ✅ Por Opt-in | ❌ Não capta | ❌ Não capta | ✅ Por Canal | ✅ Por RFM |
| **KPI-05B** | **CTR / Taxa de Clique (%)** | 1 Disparo | `fato_resgate` | Non-Additive | ✅ Data Envio | ✅ Por Opt-in | ❌ Não capta | ❌ Não capta | ✅ Por Canal | ✅ Por RFM |
| **KPI-05C** | **Conversão Final (%)** | 1 Disparo | `fato_resgate` | Non-Additive | ✅ Data Envio | ✅ Por Opt-in | ⚠️ Via Abandono | ⚠️ Via Abandono | ✅ Por Canal | ✅ Por RFM |
| **KPI-06** | **CAC de Resgate (R$)** | 1 Pedido | `fato_resgate` | Non-Additive | ✅ Por Período | ✅ Por Segmento | ❌ Não capta | ❌ Não capta | ✅ Por Canal | ✅ Por RFM |
| **KPI-07** | **Taxa de Resgate por RFM (%)** | 1 Carrinho | `fato_resgate` | Non-Additive | ✅ Mensal | ✅ Direto | ⚠️ Via Abandono | ⚠️ Via Abandono | ✅ Por Canal | ✅ Eixo Principal |
| **KPI-08** | **Ratio Premium / Dormant** | Macro | `fato_resgate` | Non-Additive | ✅ Semestral | ❌ Macro | ❌ Macro | ❌ Macro | ❌ Macro | ✅ Eixo Principal |
| **KPI-09** | **GMV em Risco por LTV (R$)** | 1 Carrinho | `fato_abandono` | Fully Additive | ✅ Data Abandono | ✅ LTV Range | ✅ Por Device | ✅ Por Motivo | ❌ Não aplicável | ✅ Por RFM |
| **KPI-10** | **ROI de Resgate (Multiplicador)**| Agregado | `fato_resgate` | Non-Additive | ✅ Por Safra | ✅ Por Segmento | ⚠️ Via Abandono | ⚠️ Via Abandono | ✅ Por Canal | ✅ Por RFM |
| **KPI-11** | **Margem Preservada (%)** | 1 Resgate | `fato_resgate` | Non-Additive | ✅ Data Venda | ✅ Por Segmento | ❌ Não capta | ⚠️ Via Abandono | ✅ Por Canal | ✅ Por RFM |
| **KPI-12** | **Distribuição por Toque (%)** | 1 Disparo | `fato_resgate` | Non-Additive | ✅ +1h a +72h | ✅ Por Segmento | ❌ Não capta | ❌ Não capta | ✅ Por Canal | ✅ Por RFM |
| **KPI-13** | **Score de Viabilidade** | 1 Carrinho | `fato_abandono` | Non-Additive | ✅ Data Abandono | ✅ RFM Score | ✅ Device | ✅ Causa-Raiz | ✅ Canal Ideal | ✅ Por RFM |

---

## 🧱 3. Catálogo das Dimensões Conformadas

### 3.1 `dim_clientes`
- **Chave Primária:** `cliente_sk` (Surrogate Key inteira gerada via hash/sequência)
- **Chave Natural:** `cliente_id` (UUID)
- **Atributos de Fatiamento:** `segmento_rfm` (`premium`, `regular`, `dormant`, `novo`), `status_ativo`, `opt_in_email`, `opt_in_sms`, `opt_in_push`, `opt_in_whatsapp`, `recencia_dias`, `frequencia_compras`, `valor_monetario_ltv`, `rfm_score`, `churn_risk_score`, `propensity_recovery`.

### 3.2 `dim_tempo`
- **Chave Primária:** `data_sk` (Formato `YYYYMMDD`)
- **Atributos de Fatiamento:** `data`, `ano`, `mes`, `trimestre`, `ano_mes`, `dia_semana_nome`, `eh_fim_semana`, `eh_feriado`.

### 3.3 `dim_dispositivo`
- **Chave Primária:** `dispositivo_sk`
- **Atributos de Fatiamento:** `dispositivo` (`mobile`, `desktop`, `tablet`), `complexidade_checkout`, `fator_friccao_checkout`.

### 3.4 `dim_motivo_abandono`
- **Chave Primária:** `motivo_sk`
- **Atributos de Fatiamento:** `motivo` (`preco`, `frete`, `pagamento`, `indecisao`, `estoque`, `nao_informado`), `categoria_motivo`, `estrategia_resgate_padrao`.

### 3.5 `dim_canal_resgate`
- **Chave Primária:** `canal_sk`
- **Atributos de Fatiamento:** `canal` (`email`, `whatsapp`, `sms`, `push_app`), `custo_unitario_envio` (`0.05`, `0.30`, `0.15`, `0.02`), `taxa_abertura_benchmark`, `taxa_conversao_benchmark`.

### 3.6 `dim_segmento_rfm`
- **Chave Primária:** `segmento_sk`
- **Atributos de Fatiamento:** `segmento` (`premium`, `regular`, `dormant`, `novo`), `prioridade_resgate`, `estrategia_comunicacao`, `expectativa_roi`.

---

## 🎯 4. Diretrizes de Consulta OLAP no Metabase & Streamlit

1. **Evitar Média de Médias:** Ao agregar dados diários para mensais no Metabase, nunca use `AVG(taxa_recuperacao)`. Sempre calcule $\frac{\text{SUM}(resgates\_convertidos)}{\text{SUM}(carrinhos\_abandonados)}$.
2. **Performance 1-Hop:** Consultas analíticas devem sempre juntar uma única tabela fato (`fato_abandono` ou `fato_resgate`) com suas dimensões correspondentes através das surrogate keys (`_sk`), aproveitando o particionamento em colunas do Snowflake / Lakehouse.
3. **Visões Pré-Agregadas (Gold Views):** Para dashboards executivos de alta concorrência, consumir as visões analíticas canônicas:
   - `v_abandonment_summary`: Consolidação de abandono por RFM, dispositivo e causa.
   - `v_recovery_roi_by_segment`: Consolidação tática de eficiência, CAC e ROI por canal e cluster.
