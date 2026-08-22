# Blueprint — Arquivo de Entidade

# Entidade: `[nome_entidade]`

---

# 1. Data Definition

> Define a estrutura dos dados, seus tipos, chaves, atributos e significados técnicos.

## Atributos / Data Dictionary

| Campo | Tipo | PK/FK | Nullable | Default | Descrição | Valores / Regras | Exemplo |
|---|---|---|---|---|---|---|---|
| `[campo]` | `[tipo]` | `[PK/FK]` | `[Não/Sim]` | `[default]` | `[descrição]` | `[regra / valores permitidos]` | `[exemplo]` |

### Foreign Keys

```text
[entidade].[campo_fk]
    → [entidade_destino].[campo_pk]
```

---

# 2. Business Definition & Business Rules

## Identificação e Visão de Negócio

- **Nome físico:** `[nome_tabela]` (Snowflake: `[DATABASE.SCHEMA.TABELA]`)
- **Nome de negócio:** `[nome amigável]`
- **Domínio:** `[domínio de negócio]`
- **Tipo:** `[Dimensão / Fato / Telemetria / Fato de Ciclo de Vida / etc.]`
- **Descrição:** `[descrição do papel da entidade]`
- **Objetivo de negócio:** `[por que essa entidade existe e qual valor ela gera]`
- **Casos de uso:**
  - `[caso de uso 1]`
  - `[caso de uso 2]`

## Granularidade

- **Granularidade:** `[o que representa uma linha]`
- **Regra:** `1 linha = 1 [evento/cliente/carrinho/pedido/etc.]`

## Papel no Domínio

- `[papel da entidade no domínio e contexto operacional]`
- `[como ela conecta os fluxos de dados de outras entidades]`

## Relacionamentos

| Entidade relacionada | Cardinalidade | Relacionamento |
|---|---:|---|
| `[entidade_relacionada]` | `[1:N / N:1 / 1:1]` | `[descrição semântica do relacionamento]` |

## Ciclo de Vida

```text
[estado_inicial] → [estado_intermediario] → [estado_final]
```

### Estados

| Status | Significado |
|---|---|
| `[status]` | `[significado semântico no negócio]` |

## BUSINESS RULES

### 01 — [Nome da Regra]
[Descrição detalhada da regra de negócio, thresholds e impactos]

### 02 — [Nome da Regra]
[Descrição detalhada da regra de negócio, thresholds e impactos]

---

# 3. Data Quality, Transformation & Lineage

> Define como a entidade é validada, transformada e movimentada entre as camadas do pipeline.

## Validação

As regras de integridade, restrições e higienização são estruturadas como funções declarativas que compõem o pipeline de validação e qualidade dos dados:

### 01 — `validar_pk_[campo_id]([campo_id])`
[Validação de chave primária única, positiva e não nula (NOT NULL & UNIQUE)]

### 02 — `validar_fk_[campo_fk]([campo_fk])`
[Validação de integridade referencial com a tabela de origem]

### 03 — `validar_campos_obrigatorios([campos_obrigatorios...])`
[Garantia de preenchimento de atributos obrigatórios IS NOT NULL]

### 04 — `validar_dominio_[campo]([campo])`
[Validação de valores permitidos em listas/enums definidos]

### 05 — `sanitizar_[campo_metrico]([campo_metrico])`
[Higienização e tratamento de dirty data / limites numéricos]

### 06 — `validar_consistencia_temporal([campos_timestamp...])`
[Validação de ordem cronológica e integridade de datas]

## Pipeline de Transformação

O pipeline estabelece uma **fronteira arquitetural clara entre a Plataforma de Dados e a Aplicação/Domínio**:
- **Papel da Plataforma de Dados**: Ingerir, detectar desvios, classificar severidade, medir impacto, registrar evidências brutas (`payload_raw`) e comunicar anomalias.
- **Papel da Aplicação / Domínio**: Consumir os eventos de anomalia e executar as decisões de resolução (corrigir, rejeitar, recalcular ou acionar serviços externos).

```text
RAW (Origem)
 │
 ▼
Quality / Anomaly Detection (Plataforma de Dados)
 ├── Detecta o problema
 ├── Classifica o código e severidade
 ├── Registra evidência e snapshot bruto
 └── Comunica o downstream
 │
 ├── [Registros Válidos/Higienizados] ──→ [entidade]_qualify (Silver Qualify)
 └── [Inconsistências Detectadas]    ──→ [entidade]_anomalies (Silver Anomaly)
```

### Raw → Qualify

[descrever em texto corrido as transformações realizadas]

```text
[entidade]_raw
→ validar_schema_e_tipagem
→ extrair_e_rotear_anomalias (envia evidências para [entidade]_anomalies)
→ sanitizar_dirty_data
→ normalizar_tipos_e_strings
→ validar_dominios
→ validar_integridade_referencial
→ deduplicar_chaves
→ [entidade]_qualify
```

### Raw → Anomaly

Mecanismo de captura, classificação e registro de desvios que representam risco operacional ou financeiro. A plataforma preserva o payload bruto original para auditoria e tomada de decisão pelo time/aplicação responsável.

```text
[entidade]_raw
    ↓
[Motor de Detecção e Classificação de Anomalias]
    ├── ANOM-01: [Regra 1]
    ├── ANOM-02: [Regra 2]
    └── ANOM-03: [Regra 3]
    ↓
[entidade]_anomalies (Repositório de Evidências & Alertas da Plataforma)
```

#### Regras de Anomalia de Negócio

| Código | Regra de Anomalia | Severidade | Risco de Negócio | Ação do Pipeline |
|---|---|:---:|---|---|
| `ANOM-01` | `[expressão lógica de violação]` | `[CRÍTICA/ALTA/MÉDIA/BAIXA]` | `[impacto no negócio/risco financeiro]` | Encaminha evidência para Anomaly |
| `ANOM-02` | `[expressão lógica de violação]` | `[CRÍTICA/ALTA/MÉDIA/BAIXA]` | `[impacto no negócio/risco financeiro]` | Encaminha evidência para Anomaly |

#### Estrutura do Artefato de Anomalias (`[entidade]_anomalies`)

A estrutura do artefato reflete as atribuições estritas da plataforma de dados (detecção, classificação e evidência):

| Campo | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `anomaly_id` | VARCHAR / UUID | Identificador exclusivo do evento de anomalia | `anom-8f3a1b2c-901e` |
| `[entidade]_id` | INT / VARCHAR | Identificador da entidade afetada | `1042` |
| `[entidade_pai]_id` | INT / VARCHAR | Identificador relacional associado (ex: cliente_id) | `42` |
| `codigo_anomalia` | VARCHAR(20) | Código identificador da regra violada (`ANOM-01`, etc.) | `ANOM-01` |
| `severidade` | VARCHAR(10) | Grau de risco atribuído: `'CRITICA'`, `'ALTA'`, `'MEDIA'`, `'BAIXA'` | `ALTA` |
| `descricao_risco` | VARCHAR(255) | Diagnóstico descritivo do problema identificado | `[descrição do desvio]` |
| `payload_raw` | TEXT / JSON | Snapshot fiel do registro bruto recebido da camada Raw | `{"campo": "valor_invalido"}` |
| `detected_at` | TIMESTAMPTZ | Timestamp de auditoria da detecção do desvio pela plataforma | `2026-03-15 14:25:00+00` |

### Qualify → Curated

[descrever enriquecimentos, joins, agregações ou regras de negócio]

```text
[entidade]_qualify
    ↓
[enriquecimentos / joins dimensionais]
    ↓
[agregações / métricas consolidadas]
    ↓
[dim/fct/view]_curated (Curated Gold)
```

## Classificação por Camada

| Camada | Ativo | Característica |
|---|---|---|
| Raw / Bronze | `raw_[entidade]` | Dados brutos preservados diretamente da origem transacional |
| Qualify / Silver | `qualify_[entidade]` | Dados tipados, deduplicados, sanitizados e validados com integridade relacional |
| Anomaly / Silver | `[entidade]_anomalies` | Repositório de evidências, dead-letter e alertas de qualidade para atuação do domínio |
| Curated / Gold | `[dim/fct/view]_[entidade]` | Dados modelados dimensionalmente, enriquecidos e prontos para consumo analítico e operacional |

## Lineage

### Upstream

```text
[Fonte de Dados / Checkout API / Logs]
    ↓
/raw/[dominio]/[entidade].parquet (Bronze)
```

### Qualification & Risk Routing (Transformation)

```text
raw_[entidade]
        ↓
[Entidade] Data Quality & Anomaly Detection Pipeline
        │
        ├── Registros válidos
        │       ↓
        │   [entidade]_qualify
        │
        └── Registros inválidos/anômalos
                ↓
            [entidade]_anomalies
```

### Downstream

```text
[entidade]_qualify
        ↓
Curated / Gold
        ↓
├── BI / Analytics
├── CRM / Marketing
├── Data App
├── ML
└── Agentes de IA

[entidade]_anomalies
        ↓
├── Data Quality Dashboard
├── Alertas de Engenharia
└── Aplicação / Domínio
```

---

# 4. Governance & Consumption

## Governança

- **Owner:** [Área / Squad Responsável (`email@empresa.com`)]
- **Classificação:** [Público / Interno / Confidencial / Sensível]
- **PII:** [Sim / Não]
- **Tags:**
  - `[tag_dominio]`
  - `[tag_entidade]`
  - `[tag_camada]`

## Consumidores

- **CRM & Automação:** `[casos de uso de mensageria / CRM]`
- **Analytics & BI:** `[dashboards e relatórios analíticos]`
- **Data App:** `[aplicações operacionais]`
- **Modelos / Agentes:** `[modelos preditivos e IA]`
- **Sistemas de Domínio:** `[serviços que consom o artefato de anomalias para tomada de decisão]`

## Observações

- `[observação técnica 1]`
- `[decisão de modelagem 2]`
- `[fronteira arquitetural e considerações operacionais]`
