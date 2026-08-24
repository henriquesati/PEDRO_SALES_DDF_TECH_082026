# 📘 Catálogo Master de KPIs e Métricas de Negócio

> **Domínio:** Recuperação de Carrinho Abandonado (E-commerce / Marketplace)  
> **Status:** ✅ Consolidado com o Modelo Lógico, Star Schema Kimball (Gold Layer) e Pitch de Vendas  
> **Framework Normativo:** [`DEC-001`](../docs/relatorios/decision-making/pitch/pitch.txt) (% e Ratios) • [`DEC-004`](../docs/specifications/data-platform-specification.md) (Sem SQL Local) • [`DEC-008`](../docs/relatorios/decision-making/dec-008-kimball-star-schema-simplicity.md) (Kimball DW)  
> **Master Source of Truth:** [`data/data-models/logical/business-rules.md`](../data/data-models/logical/business-rules.md)

---

## 📐 1. Hierarquia de Métricas em 5 Camadas (DEC-001)

Em conformidade com a decisão estratégica `DEC-001`, todas as métricas do projeto priorizam **taxas, proporções, multiplicadores e eficiência**, desacoplando o argumento analítico do ticket médio específico do cliente:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│  Camada 1: Conversão & Recuperação Global (Métricas Macro de Eficiência)    │
├─────────────────────────────────────────────────────────────────────────────┤
│  Camada 2: Eficiência do Funil por Canal de Resgate (Email, WhatsApp, etc.) │
├─────────────────────────────────────────────────────────────────────────────┤
│  Camada 3: Eficiência da Segmentação RFM & LTV (Preservação de Margem)      │
├─────────────────────────────────────────────────────────────────────────────┤
│  Camada 4: Eficiência Operacional & Financeira (ROI e CAC de Resgate)       │
├─────────────────────────────────────────────────────────────────────────────┤
│  Camada 5: Timing & Cadência de Sequência (Curva de Decaimento Temporal)    │
├─────────────────────────────────────────────────────────────────────────────┤
│  Camada Prescritiva: Score de Viabilidade de Recuperação (Triagem Dinâmica) │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 1️⃣ Camada 1: Conversão & Recuperação Global

### KPI-01: Taxa de Abandono de Carrinho (`ABANDONMENT_RATE`)
- **Definição de Negócio:** Proporção de carrinhos iniciados que permaneceram inativos por mais de 30 minutos sem confirmação de checkout.
- **Fórmula Matemática ($\LaTeX$):**
  $$\text{Taxa de Abandono (\%)} = \left( \frac{\text{COUNT}(\text{carrinhos com status = 'abandonado'})}{\text{COUNT}(\text{total geral de carrinhos criados})} \right) \times 100$$
- **Tabelas & Grão:** `fato_abandono` / `dim_tempo` (Grão: 1 linha por sessão de carrinho).
- **Target / Benchmark:** ~70.9% no dataset (Benchmark Baymard Institute: ~69.8%).
- **Aditividade:** Não-Aditiva (recalcular via razão de contagens).
- **Referência:** [`business-rules.md#91`](../data/data-models/logical/business-rules.md#91-camada-1-conversao--recuperacao-global).

---

### KPI-02: Taxa de Recuperação de Carrinhos Abandonados (`RECOVERY_RATE`)
- **Definição de Negócio:** Percentual de carrinhos abandonados convertidos em compra através das réguas ativas de resgate da Dadosfera.
- **Fórmula Matemática ($\LaTeX$):**
  $$\text{Taxa de Recuperação (\%)} = \left( \frac{\text{COUNT}(\text{carrinhos recuperados com pedidos.origem\_recuperacao = TRUE})}{\text{COUNT}(\text{total de carrinhos abandonados})} \right) \times 100$$
- **Tabelas & Grão:** `fato_abandono` ↔ `fato_resgate` (Grão: carrinho abandonado).
- **Target / Benchmark:** ~10.1% dos abandonados (Benchmark de Mercado Salesforce/Klaviyo: 5% a 15%).
- **Impacto no Pitch:** Prova o valor da PoC e capacidade de resgate sem expansão linear de equipe.

---

### KPI-03: Lift de Conversão de Resgate (`RESCUE_CONVERSION_LIFT`)
- **Definição de Negócio:** Incremento relativo de conversão gerado pela estratégia de CRM da Dadosfera em relação à taxa basal orgânica (sem intervenção).
- **Fórmula Matemática ($\LaTeX$):**
  $$\text{Lift (\%)} = \left( \frac{\text{Taxa de Conversão Global com Resgate} - \text{Taxa de Conversão Basal}}{\text{Taxa de Conversão Basal}} \right) \times 100$$
- **Target:** $+50\%$ de incremento sobre a taxa base sem réguas ativas.

---

### KPI-04: Taxa de Retenção de Receita Bruta (`REVENUE_RECOVERY_RATE`)
- **Definição de Negócio:** Proporção do montante financeiro em risco que foi efetivamente resgatado em pedidos confirmados.
- **Fórmula Matemática ($\LaTeX$):**
  $$\text{Taxa Retenção (\%)} = \left( \frac{\sum \text{fato\_resgate.valor\_pedido\_recuperado}}{\sum \text{fato\_abandono.valor\_total\_em\_risco}} \right) \times 100$$
- **Target / Benchmark:** ~11.5% do GMV represado recuperado.

---

## 2️⃣ Camada 2: Eficiência por Canal de Resgate

### KPI-05: Taxas do Funil de Engajamento de Resgate
- **Definições & Fórmulas ($\LaTeX$):**
  - **Taxa de Entrega:** $\text{Taxa Entrega (\%)} = \left( \frac{\text{COUNT}(\text{flag\_entregue = TRUE})}{\text{COUNT}(\text{disparos totais})} \right) \times 100$
  - **Taxa de Abertura:** $\text{Taxa Abertura (\%)} = \left( \frac{\text{COUNT}(\text{flag\_aberto = TRUE})}{\text{COUNT}(\text{flag\_entregue = TRUE})} \right) \times 100$
  - **Taxa de Clique (CTR):** $\text{CTR (\%)} = \left( \frac{\text{COUNT}(\text{flag\_clicado = TRUE})}{\text{COUNT}(\text{flag\_aberto = TRUE})} \right) \times 100$
  - **Conversão Final End-to-End:** $\text{Conv. Final (\%)} = \left( \frac{\text{COUNT}(\text{flag\_convertido = TRUE})}{\text{COUNT}(\text{disparos totais})} \right) \times 100$
- **Benchmarks Oficiais por Canal:**
  | Canal | Custo Unitário | Abertura | CTR (Abertura $\rightarrow$ Clique) | Conversão Final | Papel Estratégico |
  |---|:---:|:---:|:---:|:---:|---|
  | **Email** | **R$ 0,05** | ~42% | ~28% | **~4.5%** | Canal de tração em escala e maior ROI absoluto |
  | **WhatsApp** | **R$ 0,30** | ~68% | ~35% | **~2.5%** | Canal VIP para carrinhos de alto valor e clientes Premium |
  | **SMS** | **R$ 0,15** | ~55% | ~22% | **~1.8%** | Canal direto de alta visibilidade; requer opt-in rígido |
  | **Push App** | **R$ 0,02** | ~30% | ~18% | **~1.2%** | Custo marginal zero para usuários de aplicativo |

---

### KPI-06: Custo Médio por Conversão Efetiva / CAC de Resgate (`RESCUE_CAC`)
- **Definição de Negócio:** Custo total de infraestrutura e mensageria investido para converter exatamente 1 carrinho abandonado.
- **Fórmula Matemática ($\LaTeX$):**
  $$\text{CAC de Resgate} = \frac{\sum \text{fato\_resgate.custo\_disparo\_envio}}{\text{COUNT}(\text{fato\_resgate.flag\_convertido = TRUE})}$$
- **Resultados Empíricos por Canal:** Email **R$ 1,02**, Push **R$ 1,67**, SMS **R$ 3,00**, WhatsApp **R$ 12,00**.
- **Target:** Custo médio ponderado de resgate $< 1\%$ do ticket médio recuperado.

---

## 3️⃣ Camada 3: Eficiência por Segmento RFM & LTV

### KPI-07: Taxa de Recuperação por Segmento RFM (`RECOVERY_BY_RFM`)
- **Fórmula Matemática ($\LaTeX$):**
  $$\text{Taxa Segmento (\%)} = \left( \frac{\text{COUNT}(\text{carrinhos recuperados do segmento})}{\text{COUNT}(\text{carrinhos abandonados do segmento})} \right) \times 100$$
- **Distribuição Observada no Lakehouse:**
  - `Premium`: **~18%** (alta propensão de compra e resposta ao suporte)
  - `Novo`: **~12%** (reatividade com cupom de primeira compra)
  - `Regular`: **~10%** (maior volume absoluto da base)
  - `Dormant`: **~6%** (reativação de cliente inativo)

---

### KPI-08: Ratio de Eficiência Premium / Dormant (`RFM_RATIO`)
- **Definição:** Multiplicador de responsividade entre o segmento de maior valor e o segmento inativo.
- **Fórmula Matemática ($\LaTeX$):**
  $$\text{Ratio Premium/Dormant} = \frac{\text{Taxa de Recuperação (Premium)}}{\text{Taxa de Recuperação (Dormant)}} = \frac{18\%}{6\%} = \mathbf{3.0\text{x}}$$
- **Conclusão de Negócio:** Comprova que segmentar o resgate compensa; disparos genéricos desperdiçam orçamento e desgastam a base.

---

### KPI-09: Valor Financeiro em Risco por Faixa de LTV (`LTV_VALUE_AT_RISK`)
- **Definição:** Volume bruto em R$ represado em carrinhos abandonados agrupado por faixa histórica de valor do cliente (`dim_clientes.valor_monetario_ltv`).
- **Fórmula Matemática ($\LaTeX$):**
  $$\text{GMV em Risco (Faixa } F\text{)} = \sum_{\text{cliente} \in F} \text{fato\_abandono.valor\_total\_em\_risco}$$

---

## 4️⃣ Camada 4: Eficiência Operacional & Financeira (ROI)

### KPI-10: Retorno sobre Investimento de Resgate (`RESCUE_ROI`)
- **Definição de Negócio:** Múltiplo financeiro líquido gerado para cada R$ 1,00 gasto em comunicação de resgate.
- **Fórmula Matemática ($\LaTeX$):**
  $$\text{ROI} = \frac{\sum \text{valor\_pedido\_recuperado} - \sum \text{descontos\_concedidos} - \sum \text{custo\_disparos}}{\sum \text{custo\_disparos}}$$
- **Target / Resultado no Lakehouse:** **~45x multiplicador** (para cada R$ 1,00 em mensagens, retornam R$ 45,00 líquidos).

---

### KPI-11: Margem de Contribuição Preservada (`PRESERVED_MARGIN_RATE`)
- **Definição:** Proporção de carrinhos recuperados sem concessão de cupom de desconto (aplicada na política VIP de clientes Premium).
- **Fórmula Matemática ($\LaTeX$):**
  $$\text{Margem Preservada (\%)} = \left( \frac{\text{COUNT}(\text{resgates convertidos com desconto = 0})}{\text{COUNT}(\text{total de resgates convertidos})} \right) \times 100$$
- **Target:** $> 40\%$ das conversões realizadas com margem cheia.

---

## 5️⃣ Camada 5: Timing & Cadência de Sequência

### KPI-12: Distribuição de Conversões por Toque da Régua
- **Fórmula Matemática ($\LaTeX$):**
  $$\text{Distribuição Toque } T\text{ (\%)} = \left( \frac{\text{COUNT}(\text{conversões no toque } T)}{\text{COUNT}(\text{total geral de conversões})} \right) \times 100$$
- **Distribuição Observada:**
  - **1º Toque (`+1h`, Lembrete Suporte):** **~86.4%** do volume acumulado de conversões (janela ótima)
  - **2º Toque (`+24h`, Lembrete Estoque):** **~8.5%** das conversões
  - **3º Toque (`+48h`, Desconto):** **~3.5%** das conversões
  - **4º Toque (`+72h`, Urgência Final):** **~1.6%** das conversões
- **Tempo Médio Abandono $\rightarrow$ Conversão:** **~28 horas**.

---

## 🎯 6. Métrica Prescritiva: Score de Viabilidade de Recuperação

### KPI-13: Score de Viabilidade por Carrinho (`RECOVERY_VIABILITY_SCORE`)
- **Definição:** Algoritmo determinístico de priorização em tempo real para alocação eficiente do canal de resgate no Data App Streamlit.
- **Fórmulas Matemáticas ($\LaTeX$):**
  $$\text{P\_RECUPERACAO} = \text{P\_BASE(RFM)} \times \text{FATOR\_MOTIVO} \times \text{FATOR\_VALOR} \times \text{FATOR\_TEMPO}$$
  $$\text{RETORNO\_ESPERADO} = \text{P\_RECUPERACAO} \times \text{fato\_abandono.valor\_total\_em\_risco}$$
  $$\text{ROI\_ESPERADO} = \frac{\text{RETORNO\_ESPERADO}}{\text{CUSTO\_ESTIMADO\_CANAL}}$$
- **Classificação Prescritiva:**
  - 🟢 **`ALTA`**: $\text{ROI\_ESPERADO} \ge 50\text{x}$ e $\text{RETORNO\_ESPERADO} \ge \text{R\$ 10,00}$ $\rightarrow$ Disparo prioritário multicanal.
  - 🟡 **`MEDIA`**: $\text{ROI\_ESPERADO} \ge 10\text{x}$ e $\text{RETORNO\_ESPERADO} \ge \text{R\$ 2,00}$ $\rightarrow$ Disparo padrão por Email.
  - 🔴 **`BAIXA`**: $\text{ROI\_ESPERADO} < 10\text{x}$ ou $\text{RETORNO\_ESPERADO} < \text{R\$ 2,00}$ $\rightarrow$ Retargeting passivo (sem custo ativo de disparo).
