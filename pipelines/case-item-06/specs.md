# Especificação: Modelagem de Dados Dimensional (Kimball Star Schema) — Recuperação de Carrinho Abandonado

**Doc ID**: `spec_data_modeling_001`  
**Versão**: 1.2  
**Módulo:** `pipelines/case-item-06/`  
**Case Oficial Dadosfera:** Item 6 — Sobre Modelagem de Dados  
**Framework Normativo:** Kimball Star Schema + Padrão Canônico de 4 Divisões (DEC-006) + Métricas Relativas (DEC-001)  
**Status**: Ready for Agent Execution  
**Escopo**: Case Técnico de Estágio em Solutions Engineering / Dados (Dadosfera)  

---

## 📋 1. EXECUTIVE SUMMARY

**Objetivo Estratégico:**  
Definir a arquitetura dimensional (DW Gold Layer) para o case de **Recuperação de Carrinho Abandonado**, integrando os dados qualificados da camada Silver para responder com alta performance às 4 perguntas críticas de negócio:
1. **Descritiva:** *"Quantos carrinhos foram abandonados, qual a taxa relativa de perda e como o abandono se distribui por segmento, canal e dispositivo?"*
2. **Diagnóstica / Risco:** *"Quais perfis e clusters de clientes possuem maior propensão de churn e risco financeiro de abandono?"*
3. **Prescritiva:** *"Qual canal de resgate (E-mail, SMS, Push, WhatsApp) e estratégia de abordagem entrega a maior eficiência e ROI por segmento RFM?"*
4. **Oportunidade:** *"Quanto de receita adicional pode ser recuperada otimizando réguas de comunicação e reduzindo a fricção de checkout?"*

**Abordagem Escolhida: Kimball Star Schema**
- ✅ **Performance Analítica Otimizada**: Minimização de JOINs complexos para consultas rápidas no Snowflake e dashboards no Metabase.
- ✅ **BI & Data App Ready**: Modelo dimensional diretamente compatível com Metabase (Item 7) e Streamlit (Item 9).
- ✅ **Facilidade de Consulta Ad-Hoc**: Chaves surrogate conformadas e grão atômico bem declarado.
- ❌ **Não Usar Data Vault 2.0**: Complexidade excessiva de modelagem (Hubs, Links, Satellites) com over-engineering desnecessário para o escopo do case.
- ❌ **Não Usar 3NF Relacional (Inmon)**: Ineficiente para agregações multidimensionais e consultas analíticas em larga escala.

---

## 🎯 2. CONTEXTO DO CASE & ALINHAMENTO COM AGENTES

### 2.1 Requisitos Oficiais da Empresa (`case-context-specialist`)
- **Base de Dados**: 115.777+ registros em Parquet/CSV na camada Bronze (CUMPRIDO).
- **Zonas do Lakehouse**: Organização em camadas Medallion (*Bronze Raw → Silver Qualify/Anomalies → Gold Dimensional*).
- **Entregáveis do Item 6**: Modelagem dimensional Kimball, justificativa teórica vs. outras abordagens, 2 visões analíticas de dados e diagrama DW em camadas.

### 2.2 Entidades de Origem (`project-context-specialist` / `datamaker`)
```text
Camada Bronze (RAW Parquet):
  ├─ clientes (1.500 registros)
  ├─ produtos (300 SKUs)
  ├─ carrinhos (7.500 sessões)
  ├─ itens_carrinho (18.888 itens)
  ├─ eventos_carrinho (78.931 telemetrias)
  ├─ eventos_resgate (6.427 disparos de CRM)
  └─ pedidos (2.229 conversões finalizadas)

Camada Silver Qualify (Validada pelo Item 4 - DEC-006):
  ├─ clientes.parquet (1.386 conformes | 114 anomalias isoladas)
  ├─ produtos.parquet (286 conformes | 14 anomalias isoladas)
  ├─ carrinhos.parquet (6.525 conformes | 988 anomalias isoladas)
  ├─ itens_carrinho.parquet (18.690 conformes | 198 anomalias isoladas)
  ├─ eventos_carrinho.parquet (78.931 conformes | 0 anomalias)
  ├─ eventos_resgate.parquet (6.289 conformes | 138 anomalias isoladas)
  └─ pedidos.parquet (2.229 conformes | 0 anomalias)
```

### 2.3 Decisões Arquiteturais Ativas Aplicadas ao Modelo
- **DEC-001**: Métricas e visões estruturadas prioritariamente em **taxas percentuais (%) e ratios relativos** (conversão, abertura, abandono, ROI), mantendo valores monetários como métricas complementares.
- **DEC-003**: Especificações de insights e views estruturadas em Markdown (desacopladas de implementações físicas locais).
- **DEC-004**: Proibição de arquivos `.sql` locais; consultas e views implementadas na camada de inteligência da Dadosfera / Snowflake.
- **DEC-006**: Dual-Artifact Pipeline (Camada Gold consome exclusivamente dados aprovados da Silver Qualify, sem contaminação por registros em quarentena).
- **DEC-007**: Verossimilhança estatística com distribuições fracionárias auditáveis.

---

## 🏗️ 3. JUSTIFICATIVA ARQUITETURAL: POR QUE KIMBALL?

### Comparativo Técnico de Abordagens

| Critério | Kimball (Star Schema) | Data Vault 2.0 | 3NF Relacional (Inmon) |
|---|:---:|:---:|:---:|
| **Complexidade Conceitual** | ⭐ Baixa / Direta | ⭐⭐⭐⭐⭐ Muito Alta (Hubs/Links/Sats) | ⭐⭐⭐ Média |
| **Performance em Consultas OLAP** | ⭐⭐⭐⭐⭐ Máxima (1-Hop JOINs) | ⭐⭐⭐ Moderada (Multi-Hop JOINs) | ⭐⭐ Lenta (JOINs em cascata) |
| **Curva de Aprendizado / Implementação** | ⭐ Rápida e Pragmática | ⭐⭐⭐⭐⭐ Lenta e Burocrática | ⭐⭐⭐ Média |
| **Aderência ao Metabase / BI** | ⭐⭐⭐⭐⭐ Perfeita e Nativa | ⭐⭐⭐ Requer camada intermediária | ⭐ Fraca para usuários de negócio |
| **Adequação ao Case Dadosfera** | ✅ **RECOMENDADA (Ideal)** | ❌ Overkill para escopo de estágio | ❌ Inadequada para Analytics Moderno |

### Princípios de Kimball Aplicados no Case:
1. **Conformed Dimensions**: `dim_clientes`, `dim_tempo`, `dim_canal_resgate` compartilhadas e padronizadas entre múltiplos fatos.
2. **Grain Declaration**:
   - `fato_abandono`: 1 linha por carrinho com evento de abandono (`grain: 1 cart abandonment session`).
   - `fato_resgate`: 1 linha por disparo de régua de comunicação (`grain: 1 recovery attempt event`).
3. **Additive vs Non-Additive Measures**: `valor_total`, `receita_recuperada`, `custo_envio` são aditivas; taxas percentuais (`% conversão`, `% abandono`) são semi/não-aditivas.
4. **SCD Type 2 Ready**: Rastreabilidade temporal de evolução de status RFM de clientes sem perda de histórico analítico.

---

## 📊 4. ESPECIFICAÇÃO DAS TABELAS DO MODELO DIMENSIONAL

### 4.1 DIMENSÕES CONFORMADAS (Lookup & Context)

#### 1. `dim_clientes`
**Propósito**: Contextualizar o perfil cadastral, comportamento e segmentação RFM do cliente.  
**Grão**: 1 linha por cliente único.  
**SCD Type**: 2 (rastreia transições de segmento RFM).

```yaml
dim_clientes:
  keys:
    cliente_sk: "Surrogate Key (BIGINT AUTOINCREMENT)"
    cliente_id: "Natural Key / UUID (from silver qualify)"
  
  attributes:
    # Identificação & Contato
    - email: "string (validado por regex)"
    - segmento_rfm: "string (premium | regular | dormant | novo)"
    - status_ativo: "boolean (TRUE | FALSE)"
    - opt_in_email: "boolean (TRUE | FALSE)"
    - opt_in_sms: "boolean (TRUE | FALSE)"
    - opt_in_push: "boolean (TRUE | FALSE)"
    - opt_in_whatsapp: "boolean (TRUE | FALSE)"
    
    # Comportamento & RFM
    - recencia_dias: "integer (dias desde a última compra)"
    - frequencia_compras: "integer (total de compras históricas)"
    - valor_monetario_ltv: "numeric(12,2) (LTV consolidado)"
    - rfm_score: "integer (111 a 555)"
    - churn_risk_score: "numeric(5,2) (0.00 a 100.00)"
    - propensity_recovery: "numeric(5,2) (probabilidade preditiva 0.00 a 100.00)"
    
    # Auditoria & SCD Type 2
    - dw_valid_from: "timestamp_ntz"
    - dw_valid_to: "timestamp_ntz (NULL se atual)"
    - is_current: "boolean (TRUE | FALSE)"
```

#### 2. `dim_tempo`
**Propósito**: Dimensão de tempo conformada para análises temporais e de sazonalidade.  
**Grão**: 1 linha por dia civil.

```yaml
dim_tempo:
  keys:
    data_sk: "integer (formato YYYYMMDD, ex: 20240115)"
    data: "date (Data ISO)"
  
  attributes:
    - ano: "integer (ex: 2024)"
    - mes: "integer (1 a 12)"
    - mes_nome: "string (Janeiro, Fevereiro...)"
    - trimestre: "integer (1 a 4)"
    - ano_mes: "string (YYYY-MM)"
    - dia_mes: "integer (1 a 31)"
    - dia_semana: "integer (1=Segunda a 7=Domingo)"
    - dia_semana_nome: "string (Segunda-feira, Terça-feira...)"
    - eh_fim_semana: "boolean (TRUE | FALSE)"
    - eh_feriado: "boolean (TRUE | FALSE)"
```

#### 3. `dim_dispositivo`
**Propósito**: Classificação técnica do dispositivo de acesso e fricção de checkout.  
**Grão**: 1 linha por tipo de dispositivo.

```yaml
dim_dispositivo:
  keys:
    dispositivo_sk: "integer (1=Mobile, 2=Desktop, 3=Tablet)"
  
  attributes:
    - dispositivo: "string (mobile | desktop | tablet)"
    - complexidade_checkout: "string (alta | media | baixa)"
    - fator_friccao_checkout: "numeric(4,2) (multiplicador de risco relativo)"
```

#### 4. `dim_motivo_abandono`
**Propósito**: Taxonomia e categorização do motivo raiz do abandono de sessão.  
**Grão**: 1 linha por motivo de abandono.

```yaml
dim_motivo_abandono:
  keys:
    motivo_sk: "integer (1 a 5)"
  
  attributes:
    - motivo: "string (preco | frete | pagamento | indecisao | estoque)"
    - categoria_motivo: "string (comercial | logistica | tecnica | comportamental)"
    - nivel_impacto: "string (alto | medio | critico)"
    - estrategia_resgate_padrao: "string (cupom_desconto | frete_gratis | suporte_pagamento | lembrete)"
```

#### 5. `dim_canal_resgate`
**Propósito**: Catálogo dos canais de comunicação multicanal da régua de resgate.  
**Grão**: 1 linha por canal de comunicação.

```yaml
dim_canal_resgate:
  keys:
    canal_sk: "integer (1=email, 2=sms, 3=push_app, 4=whatsapp)"
  
  attributes:
    - canal: "string (email | sms | push_app | whatsapp)"
    - custo_unitario_envio: "numeric(6,2) (R$ 0.05 email, R$ 0.15 sms, R$ 0.02 push, R$ 0.30 whatsapp)"
    - taxa_abertura_benchmark: "numeric(5,2) (% esperada)"
    - taxa_conversao_benchmark: "numeric(5,2) (% esperada)"
```

#### 6. `dim_segmento_rfm`
**Propósito**: Agrupamento estratégico de clientes por valor e prioridade de atendimento.  
**Grão**: 1 linha por cluster RFM.

```yaml
dim_segmento_rfm:
  keys:
    segmento_sk: "integer (1=Champions/Premium, 2=Regular, 3=Dormant, 4=Novo)"
  
  attributes:
    - segmento: "string (premium | regular | dormant | novo)"
    - prioridade_resgate: "integer (1=Máxima prioridade a 4=Baixa prioridade)"
    - estrategia_comunicacao: "string (high_touch_vip | padrao_desconto | reativacao_oferta | boas_vindas)"
    - expectativa_roi: "string (alto | medio | baixo)"
```

---

### 4.2 TABELAS DE FATOS GRANULARES

#### 1. `fato_abandono`
**Propósito**: Registrar cada sessão transacional onde ocorreu abandono de carrinho.  
**Grão**: 1 linha por carrinho abandonado.  
**Relacionamento**: N:1 com as dimensões conformadas.

```yaml
fato_abandono:
  keys:
    fato_abandono_sk: "BIGINT AUTOINCREMENT (PK)"
    carrinho_id: "UUID (Natural FK from silver qualify)"
    cliente_sk: "BIGINT (FK -> dim_clientes)"
    data_abandono_sk: "INTEGER (FK -> dim_tempo)"
    dispositivo_sk: "INTEGER (FK -> dim_dispositivo)"
    motivo_sk: "INTEGER (FK -> dim_motivo_abandono)"
  
  measures_additive:
    - valor_subtotal: "numeric(12,2)"
    - valor_frete: "numeric(12,2)"
    - valor_desconto: "numeric(12,2)"
    - valor_total_em_risco: "numeric(12,2) (subtotal + frete - desconto)"
    - quantidade_itens: "integer"
  
  measures_semi_additive:
    - duracao_sessao_minutos: "numeric(8,2)"
    - tempo_ate_abandono_segundos: "integer"
  
  attributes_descritivos:
    - flag_cliente_novo: "boolean (TRUE | FALSE)"
    - canal_origem: "string (google_ads | meta_ads | organico | email | direto)"
```

#### 2. `fato_resgate`
**Propósito**: Registrar cada disparo de régua de comunicação e retorno financeiro.  
**Grão**: 1 linha por tentativa de resgate enviada.  
**Relacionamento**: N:1 com dimensões e 1:1/N:1 com fato_abandono.

```yaml
fato_resgate:
  keys:
    fato_resgate_sk: "BIGINT AUTOINCREMENT (PK)"
    resgate_id: "UUID (Natural FK from silver qualify)"
    cliente_sk: "BIGINT (FK -> dim_clientes)"
    data_envio_sk: "INTEGER (FK -> dim_tempo)"
    canal_sk: "INTEGER (FK -> dim_canal_resgate)"
    fato_abandono_sk: "BIGINT (FK -> fato_abandono)"
  
  measures_funil_crm:
    - flag_entregue: "integer (0 ou 1)"
    - flag_aberto: "integer (0 ou 1)"
    - flag_clicado: "integer (0 ou 1)"
    - flag_convertido: "integer (0 ou 1)"
  
  measures_financeiras:
    - custo_disparo_envio: "numeric(8,2)"
    - valor_pedido_recuperado: "numeric(12,2) (0.00 se não convertido)"
    - roi_liquido_disparo: "numeric(12,2) (valor_pedido_recuperado - custo_disparo)"
  
  attributes_descritivos:
    - numero_toque_regua: "integer (1 a 4)"
    - tipo_comunicacao: "string (lembrete_1h | cupom_24h | frete_gratis_48h | ultima_chamada_72h)"
```

---

## 🎯 5. ESPECIFICAÇÃO DAS 2 VISÕES ANALÍTICAS FINAIS (GOLD)

### Visão 1: `v_abandonment_summary` (Visão Executiva & Perfil de Abandono)
**Propósito**: Consolidar volume, taxas e montante financeiro em risco por segmento, canal e dispositivo para acompanhamento da liderança.  
**Perguntas de Negócio Respondidas**: Descritiva (Volume/Taxas) e Diagnóstica (Risco de Churn).

```sql
-- Especificação Conceitual de Lógica para Snowflake / Metabase:
SELECT
    c.segmento_rfm,
    d.dispositivo,
    m.motivo AS motivo_abandono,
    t.ano_mes,
    
    -- Métricas Aditivas e Volumetria
    COUNT(DISTINCT fa.fato_abandono_sk) AS total_carrinhos_abandonados,
    SUM(fa.valor_total_em_risco) AS valor_total_em_risco,
    AVG(fa.valor_total_em_risco) AS ticket_medio_abandonado,
    AVG(fa.duracao_sessao_minutos) AS duracao_media_sessao_min,
    
    -- Taxas Percentuais e Ratios (DEC-001)
    ROUND(COUNT(DISTINCT fa.fato_abandono_sk) * 100.0 / NULLIF(SUM(COUNT(DISTINCT fa.fato_abandono_sk)) OVER (PARTITION BY t.ano_mes), 0), 2) AS taxa_concentracao_abandono_pct,
    
    -- Diagnóstico de Risco
    AVG(c.churn_risk_score) AS churn_risk_score_medio,
    COUNT(DISTINCT CASE WHEN c.churn_risk_score > 70 THEN c.cliente_sk END) AS clientes_alto_risco,
    COUNT(DISTINCT c.cliente_sk) AS total_clientes_afetados

FROM fato_abandono fa
    JOIN dim_clientes c ON fa.cliente_sk = c.cliente_sk
    JOIN dim_dispositivo d ON fa.dispositivo_sk = d.dispositivo_sk
    JOIN dim_motivo_abandono m ON fa.motivo_sk = m.motivo_sk
    JOIN dim_tempo t ON fa.data_abandono_sk = t.data_sk

GROUP BY c.segmento_rfm, d.dispositivo, m.motivo, t.ano_mes;
```

---

### Visão 2: `v_recovery_roi_by_segment` (Visão Tática / Tomada de Decisão de Resgate)
**Propósito**: Mensurar o retorno financeiro (ROI) e taxas de conversão de cada canal por cluster RFM, orientando a alocação ótima de orçamento de CRM.  
**Perguntas de Negócio Respondidas**: Prescritiva (Melhor Canal/Ação) e Oportunidade (Receita Recuperável).

```sql
-- Especificação Conceitual de Lógica para Snowflake / Metabase:
SELECT
    c.segmento_rfm,
    cr.canal AS canal_resgate,
    
    -- Volumetria de Disparos e Engajamento
    COUNT(DISTINCT fr.fato_resgate_sk) AS total_disparos_enviados,
    SUM(fr.flag_aberto) AS total_aberturas,
    ROUND(SUM(fr.flag_aberto) * 100.0 / NULLIF(COUNT(DISTINCT fr.fato_resgate_sk), 0), 2) AS taxa_abertura_pct,
    
    -- Conversão (DEC-001)
    SUM(fr.flag_convertido) AS total_conversoes,
    ROUND(SUM(fr.flag_convertido) * 100.0 / NULLIF(COUNT(DISTINCT fr.fato_resgate_sk), 0), 2) AS taxa_conversao_pct,
    
    -- Economia e ROI
    SUM(fr.custo_disparo_envio) AS custo_total_comunicacao,
    SUM(fr.valor_pedido_recuperado) AS receita_total_recuperada,
    SUM(fr.roi_liquido_disparo) AS lucro_liquido_recuperado,
    
    -- ROI Relativo e Recomendação Prescritiva
    ROUND((SUM(fr.roi_liquido_disparo) * 100.0) / NULLIF(SUM(fr.custo_disparo_envio), 0), 2) AS roi_eficiencia_pct,
    CASE 
        WHEN (SUM(fr.roi_liquido_disparo) * 100.0) / NULLIF(SUM(fr.custo_disparo_envio), 0) >= 1000 THEN 'ALTAMENTE_LUCRATIVO'
        WHEN (SUM(fr.roi_liquido_disparo) * 100.0) / NULLIF(SUM(fr.custo_disparo_envio), 0) > 0 THEN 'MODERADAMENTE_VIAVEL'
        ELSE 'DEFICITARIO_RESTRINGIR'
    END AS recomendacao_estrategica

FROM fato_resgate fr
    JOIN dim_clientes c ON fr.cliente_sk = c.cliente_sk
    JOIN dim_canal_resgate cr ON fr.canal_sk = cr.canal_sk

GROUP BY c.segmento_rfm, cr.canal;
```

---

## 📐 6. DIAGRAMA DE ARQUITETURA DW (STAR SCHEMA & MEDALLION)

```text
=============================================================================
                    ARQUITETURA EM CAMADAS MEDALLION
=============================================================================
 [ BRONZE / RAW ]  -->  [ SILVER QUALIFY ]  -->  [ GOLD DIMENSIONAL ]
 (Parquet 115k+)        (Qualificados Item 4)    (Star Schema Kimball)
=============================================================================

                               ┌─────────────────┐
                               │  dim_clientes   │ (PK: cliente_sk)
                               │  (1.386 linhas) │
                               └────────┬────────┘
                                        │
                   ┌────────────────────┴────────────────────┐
                   │                                         │
       ┌───────────┴───────────┐                 ┌───────────┴───────────┐
       │ fato_abandono         │                 │ fato_resgate          │
       │ (6.525 linhas)        │                 │ (6.289 linhas)        │
       │ FK: cliente_sk        │                 │ FK: cliente_sk        │
       │ FK: data_abandono_sk  │                 │ FK: data_envio_sk     │
       │ FK: dispositivo_sk    │                 │ FK: canal_sk          │
       │ FK: motivo_sk         │                 │ FK: fato_abandono_sk  │
       └───────────┬───────────┘                 └───────────┬───────────┘
                   │                                         │
                   ├──→ dim_tempo (731)                      ├──→ dim_tempo (731)
                   ├──→ dim_dispositivo (3)                  └──→ dim_canal_resgate (4)
                   ├──→ dim_motivo_abandono (5)
                   └──→ dim_segmento_rfm (4)

=============================================================================
                      VIEWS ANALÍTICAS CONSOLIDADAS
=============================================================================
├── v_abandonment_summary       (Dimensões × Fato Abandono -> Perfil & Risco)
└── v_recovery_roi_by_segment   (Fato Resgate × Dimensões -> Eficiência & ROI)
```

---

## 7. Data Warehouse Layered Architecture Diagram

### 7.1 Objetivo

O Item 6 deve produzir um diagrama arquitetural representando as camadas finais do Data Warehouse proposto para o caso de Cart Recovery.

O diagrama deve representar visualmente a evolução dos dados desde sua origem até as estruturas finais de consumo analítico, evidenciando:

- fontes de dados;
- camada Bronze / Raw;
- camada Silver / Qualify;
- artefatos de Data Quality / Anomaly quando aplicável;
- camada Gold / Curated / Dimensional;
- dimensões conformadas;
- tabelas de fatos;
- views analíticas;
- principais consumidores downstream.

O diagrama deve ser derivado das estruturas e especificações já existentes no projeto, não devendo introduzir entidades, tabelas ou camadas que não estejam justificadas pelos artefatos do case.

### 7.2 Escopo Arquitetural

O diagrama deverá representar, no mínimo, o seguinte fluxo lógico:

```text
Data Sources
     │
     ▼
Bronze / Raw
     │
     ▼
Silver / Qualify
     │
     ├──────────────► Data Quality / Anomaly
     │
     ▼
Gold / Curated / Dimensional
     │
     ├── Dimensions
     ├── Facts
     └── Analytical Views
             │
             ▼
      Downstream Consumers
```

A representação final deverá refletir as estruturas efetivamente definidas nas especificações do projeto.

### 7.3 Camada Gold / Dimensional

O diagrama deverá destacar a modelagem dimensional definida para o Item 6, incluindo as dimensões conformadas:

- `dim_clientes`
- `dim_tempo`
- `dim_dispositivo`
- `dim_motivo_abandono`
- `dim_canal_resgate`
- `dim_segmento_rfm`

e as tabelas de fatos:

- `fato_abandono`
- `fato_resgate`

As relações entre fatos e dimensões devem ser representadas por suas respectivas chaves substitutas (`_sk`) quando aplicável.

Também deverão ser representadas as views analíticas Gold:

- `v_abandonment_summary`
- `v_recovery_roi_by_segment`

### 7.4 Downstream

O diagrama deverá representar os principais consumidores previstos para a camada Gold, considerando o contexto geral do projeto, incluindo quando aplicável:

- BI / Analytics (Metabase);
- Data App de Recuperação (Streamlit);
- Modelos de ML;
- Agentes de IA / GenAI;
- Análises de negócio.

Os consumidores devem ser representados como destinos dos dados e não como componentes internos do Data Warehouse.

### 7.5 Relação com Data Quality

A camada de Anomaly / Data Quality deve ser representada como um artefato paralelo de observabilidade e tratamento de qualidade, e não como uma camada obrigatória pela qual todos os registros precisam passar antes de alcançar a camada Gold.

O diagrama deve preservar a distinção entre:

```text
Dados qualificados
       │
       ▼
Gold / Curated
```

e:

```text
Inconsistências detectadas
       │
       ▼
Anomaly / Quality Evidence
```

A representação deve ser consistente com o modelo de Data Quality definido no Item 4.

### 7.6 Fonte da Verdade

O diagrama deve ser construído a partir das especificações, schemas, planos de implementação e demais artefatos existentes no projeto.

Antes de gerar o artefato, o agente deve inspecionar os arquivos relevantes para identificar:

- entidades existentes;
- nomes canônicos;
- camadas existentes;
- relacionamentos;
- granularidade;
- tabelas de fatos;
- dimensões;
- views;
- consumidores;
- convenções de nomenclatura.

O agente não deve criar estruturas exclusivamente para preencher o diagrama.

Caso exista divergência entre documentos, o agente deve utilizar a especificação mais recente/canônica definida pelo projeto e registrar a divergência no relatório do Item 6.

### 7.7 Artefatos

O diagrama deverá ser produzido em formato adequado para documentação técnica e apresentação do case.

Artefato principal:
`pipelines/case-item-06/outputs/assets/data_warehouse_architecture.png`

Quando apropriado, poderá também ser produzido um formato editável ou textual complementar, por exemplo:
`pipelines/case-item-06/outputs/assets/data_warehouse_architecture.mmd` ou equivalente.

O artefato visual deverá ser autocontido e legível sem necessidade de consultar o código-fonte.

### 7.8 Critérios de Qualidade do Diagrama

O diagrama será considerado válido quando:

- representar corretamente as camadas Bronze, Silver e Gold definidas no projeto;
- distinguir Qualify de Anomaly;
- representar as dimensões e fatos definidos no Item 6;
- representar as views analíticas Gold;
- representar os principais consumidores downstream;
- manter os nomes das entidades consistentes com as specs;
- não introduzir estruturas não especificadas;
- permitir compreender o fluxo de dados sem consultar o código;
- estar armazenado exclusivamente em `pipelines/case-item-06/outputs/`;
- estar referenciado no relatório final do Item 6.

---

## 📋 8. TAREFAS DE EXECUÇÃO POR AGENTES ESPECIALIZADOS

```yaml
tasks:
  - task_1:
      name: "Validação de Requisitos Estratégicos"
      agent: "case-context-specialist"
      checklist:
        - "Validar que as 6 dimensões conformadas atendem todos os requisitos do Item 6"
        - "Validar que as 2 tabelas de fatos refletem fielmente o funil de abandono e recuperação"
        - "Validar que as métricas estão em conformidade com DEC-001 (foco em taxas %)"

  - task_2:
      name: "Mapeamento dos Dados da Camada Silver Qualify"
      agent: "scout"
      checklist:
        - "Inspecionar os schemas de pipelines/case-item-04/outputs/qualify/*.parquet (ou data/mock/output_cleaned/parquet/*.parquet)"
        - "Confirmar integridade referencial entre clientes, carrinhos, eventos_resgate e pedidos"
        - "Validar que não existem campos nulos críticos nas chaves naturais"

  - task_3:
      name: "Registro da Decisão de Arquitetura Dimensional"
      agent: "project-context-specialist"
      checklist:
        - "Registrar o modelo dimensional Kimball como padrão oficial da camada Gold"
        - "Vincular a entrega com o Item 6 da escala de avaliação do case"

  - task_4:
      name: "Validação do Framework Analítico de Negócio"
      agent: "data-strategy-analyst"
      checklist:
        - "Confirmar que v_abandonment_summary atende análises Descritivas e de Risco"
        - "Confirmar que v_recovery_roi_by_segment atende análises Prescritivas e de Oportunidade"

  - task_5:
      name: "Especificação de Views para BI e Metabase"
      agent: "cart-recovery-insights"
      checklist:
        - "Documentar especificações de colunas e regras de cálculo em Markdown"
        - "Definir queries de teste conceituais para Metabase (Item 7)"
```

---

## 🔒 9. REGRAS DE ISOLAMENTO DE OUTPUTS

> [!IMPORTANT]
> Todos os arquivos, especificações, esquemas DDL e diagramas gerados para o Item 6 residem **exclusivamente** em:
> - `pipelines/case-item-06/outputs/`
> - Não haverá replicação para diretórios externos sem autorização prévia.
