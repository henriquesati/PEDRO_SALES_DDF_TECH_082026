# Entidade: `clientes`

---

# 1. Data Definition

> Define a estrutura dos dados, seus tipos, chaves, atributos e significados técnicos.

## Atributos / Data Dictionary

| Campo | Tipo | PK/FK | Nullable | Default | Descrição | Valores / Regras | Exemplo |
|---|---|---|---|---|---|---|---|
| `cliente_id` | INT | PK | `FALSE` | AUTO | Identificador único exclusivo do cliente | Inteiro sequencial único positivo | `42` |
| `primeiro_nome` | VARCHAR(100) | — | `FALSE` | — | Primeiro nome do cliente (usado para personalização) | Texto sem caracteres especiais | `Maria` |
| `ultimo_nome` | VARCHAR(100) | — | `TRUE` | — | Sobrenome do cliente | Texto ou nulo | `Silva` |
| `email` | VARCHAR(255) | UK | `FALSE` | — | Endereço eletrônico e chave natural única do cliente | Formato válido `*@*.*`, lowercase | `maria.silva@email.com` |
| `telefone` | VARCHAR(20) | — | `TRUE` | — | Número de telefone com DDD para canais móveis | Padrão `(XX) 9XXXX-XXXX` ou E.164 | `(11) 98765-4321` |
| `segmento_rfm` | VARCHAR(20) | — | `TRUE` | `'novo'` | Segmento comportamental baseado em Recência, Frequência e Valor | `'premium'`, `'regular'`, `'dormant'`, `'novo'` | `'premium'` |
| `data_primeira_compra` | DATE | — | `TRUE` | — | Data da primeira compra convertida na plataforma | Data válida `<= data_ultima_compra` | `2025-08-10` |
| `data_ultima_compra` | DATE | — | `TRUE` | — | Data da compra mais recente concluída | Data válida `>= data_primeira_compra` | `2026-05-14` |
| `total_compras` | INT | — | `FALSE` | `0` | Quantidade acumulada de pedidos pagos e confirmados | Inteiro `>= 0` | `8` |
| `lifetime_value` | DECIMAL(12,2) | — | `FALSE` | `0.00` | Valor monetário acumulado gasto pelo cliente (LTV) | DECIMAL `>= 0.00` | `3450.80` |
| `permite_email` | BOOLEAN | — | `FALSE` | `TRUE` | Opt-in formal para recebimento de comunicações via E-mail | `TRUE` / `FALSE` | `TRUE` |
| `permite_sms` | BOOLEAN | — | `FALSE` | `FALSE` | Opt-in formal para recebimento de campanhas via SMS | `TRUE` / `FALSE` | `FALSE` |
| `permite_push` | BOOLEAN | — | `FALSE` | `FALSE` | Opt-in formal para notificações push no aplicativo | `TRUE` / `FALSE` | `TRUE` |
| `status_ativo` | BOOLEAN | — | `FALSE` | `TRUE` | Flag indicando se a conta do cliente está ativa na base | `TRUE` / `FALSE` | `TRUE` |
| `data_criacao` | TIMESTAMPTZ | — | `FALSE` | NOW() | Timestamp de criação do cadastro do cliente | Data/hora UTC | `2025-08-10 10:15:30+00` |

### Foreign Keys

```text
clientes.cliente_id
    ← carrinhos.cliente_id
    ← pedidos.cliente_id
    ← eventos_resgate.cliente_id
    ← eventos_carrinho.cliente_id
```

## SCHEMA RULES

### 01 — Unicidade e Não-Nulidade da Chave Primária (PK)
O campo `cliente_id` é chave primária inteira sequencial auto-incremental (`INT PRIMARY KEY`), obrigatória (`NOT NULL`) e exclusiva (`UNIQUE`), identificando unicamente cada registro.

### 02 — Unicidade e Obrigatoriedade da Chave Natural (UK)
O campo `email` possui restrição de unicidade (`UNIQUE NOT NULL`), atuando como chave natural no catálogo para impedir duplicidade de cadastros com o mesmo endereço eletrônico.

### 03 — Restrição de Domínio de Segmentação RFM (CHECK Constraint)
O atributo `segmento_rfm` possui restrição de verificação `CHECK (segmento_rfm IN ('premium', 'regular', 'dormant', 'novo') OR segmento_rfm IS NULL)`, aceitando apenas valores predefinidos da taxonomia RFM.

### 04 — Não-Negatividade do Volume de Compras (CHECK Constraint)
O campo `total_compras` possui restrição `CHECK (total_compras >= 0)`, impedindo contagens negativas de pedidos no schema.

### 05 — Não-Negatividade e Precisão Monetária do LTV (CHECK Constraint)
O campo `lifetime_value` é tipado como `DECIMAL(12,2)` com restrição `CHECK (lifetime_value >= 0.00)`, garantindo precisão contábil e impedindo valores monetários negativos.

### 06 — Integridade de Consentimentos e Valores Padrão (Defaults)
Os campos de consentimento de mensageria possuem tipagem booleana com valores padrão explícitos: `permite_email BOOLEAN NOT NULL DEFAULT TRUE`, `permite_sms BOOLEAN NOT NULL DEFAULT FALSE` e `permite_push BOOLEAN NOT NULL DEFAULT FALSE`.

### 07 — Estado Inicial de Cadastro e Ativação
O campo `status_ativo` possui restrição `BOOLEAN NOT NULL DEFAULT TRUE`, e `data_criacao` é tipado como `TIMESTAMPTZ NOT NULL DEFAULT NOW()`, registrando a data e hora UTC oficial de criação do registro no banco.

### 08 — Integridade Referencial Reversa (Foreign Keys)
O identificador `cliente_id` é referenciado como Foreign Key pelas tabelas transacionais `carrinhos(cliente_id)`, `pedidos(cliente_id)`, `eventos_carrinho(cliente_id)` e `eventos_resgate(cliente_id)`, todas com política de integridade `ON DELETE RESTRICT` para evitar exclusão de clientes com histórico transacional.

---

# 2. Business Definition & Business Rules

## Identificação e Visão de Negócio

- **Nome físico:** `clientes` (Snowflake: `CART_RECOVERY.CLIENTES`)
- **Nome de negócio:** Clientes & Perfil Comportamental (Compradores Cadastrados)
- **Domínio:** CRM, Identidade & Recuperação de Carrinho / Marketplace E-commerce
- **Tipo:** Dimensão Conforme (Conformed Dimension) / Perfil do Usuário
- **Descrição:** Entidade central de dimensão que consolida os dados cadastrais, preferências de privacidade/opt-in e histórico transacional de cada comprador, permitindo segmentação estratégica e personalização de réguas de resgate.
- **Objetivo de negócio:** Viabilizar a personalização das campanhas de recuperação de carrinho por canal preferencial, priorizar clientes de alto valor (LTV) e garantir estrita conformidade com as diretrizes de privacidade e consentimento (LGPD).
- **Casos de uso:**
  - Segmentar o público-alvo para disparo de ofertas personalizadas (ex: cupons mais agressivos para clientes `dormant` vs. lembretes sutis para `premium`).
  - Filtrar canais de contato permitidos (`permite_email`, `permite_sms`, `permite_push`) antes do acionamento de réguas automatizadas.
  - Personalizar mensagens de resgate com nome do cliente para aumento de taxas de abertura e conversão.
  - Calcular métricas de valor do cliente: LTV, frequência de recompra e taxa de reativação de clientes inativos.

## Granularidade

- **Granularidade:** Uma linha por cliente único cadastrado no ecossistema do marketplace.
- **Regra:** `1 linha = 1 cliente cadastrado`

## Papel no Domínio

- Atua como a **dimensão mestra** de identidade e relacionamento do marketplace.
- Conecta todas as interações do consumidor: sessões de compra (`carrinhos`), telemetria em tempo real (`eventos_carrinho`), histórico de campanhas recebidas (`eventos_resgate`) e fechamento de vendas (`pedidos`).

## Relacionamentos

| Entidade relacionada | Cardinalidade | Relacionamento |
|---|---:|---|
| `carrinhos` | 1:N | Um cliente pode abrir múltiplos carrinhos ao longo do tempo |
| `pedidos` | 1:N | Um cliente pode realizar múltiplos pedidos de compra |
| `eventos_carrinho` | 1:N | Um cliente gera múltiplos eventos comportamentais nas sessões |
| `eventos_resgate` | 1:N | Um cliente pode receber múltiplas tentativas de comunicação de resgate |

## Ciclo de Vida

```text
[novo] ──(1ª compra)──→ [regular] ──(LTV > R$ 2k & 5+ compras)──→ [premium]
   │                         │                                        │
   │ (sem compras > 180d)     │ (sem compras > 180d)                  │ (sem compras > 180d)
   ▼                         ▼                                        ▼
   └───────────────────→ [dormant] ──(resgate com sucesso)────────────┘
```

### Estados

| Status | Significado |
|---|---|
| `novo` | Cliente recém-cadastrado que ainda não realizou nenhuma compra confirmada (`total_compras = 0`) |
| `regular` | Cliente com compras recorrentes intermediárias (2 a 4 compras) e LTV entre R$ 500 e R$ 2.000 |
| `premium` | Cliente de alto valor acumulado (LTV > R$ 2.000 e 5+ compras), elegível a atendimento e condições prioritárias |
| `dormant` | Cliente que realizou compras no passado mas não interage há mais de 180 dias, alvo de reativação |

## BUSINESS RULES

### 01 — Conformidade com Opt-in e Governança de Canais (LGPD)
Nenhuma comunicação de resgate automatizada pode ser disparada através de um canal para o qual o cliente não concedeu permissão expressa:
- Disparos de E-mail exigem `permite_email = TRUE` e `email IS NOT NULL`.
- Disparos de SMS e WhatsApp exigem `permite_sms = TRUE` e `telefone IS NOT NULL`.
- Disparos de Push Notification exigem `permite_push = TRUE`.

### 02 — Consistência Contábil de Histórico e LTV
Os indicadores de compra acumulados devem respeitar as invariantes contábeis:
- Se `total_compras = 0`, então `lifetime_value = 0.00`, `data_primeira_compra IS NULL` e `data_ultima_compra IS NULL`.
- Se `total_compras > 0`, então `lifetime_value > 0.00` e `data_primeira_compra IS NOT NULL`.
- Inconsistências identificadas devem ser encaminhadas para auditoria na camada de anomalias.

### 03 — Unicidade e Normalização da Chave Natural (E-mail)
O campo `email` é a chave natural única do cliente. Antes da persistência, o e-mail deve ser sanitizado (remoção de espaços em branco, conversão integral para minúsculas) para evitar duplicidades geradas por inconsistência de digitação.

### 04 — Atualização Periódica de Segmentação RFM
A segmentação `segmento_rfm` é recalculada periodicamente com base na recência (`data_ultima_compra`), frequência (`total_compras`) e valor monetário (`lifetime_value`). Clientes inativos há mais de 180 dias transicionam para `'dormant'` independentemente do volume anterior de compras.

### 05 — Ordem Cronológica Transacional
A data da primeira compra deve ser sempre igual ou anterior à data da última compra (`data_primeira_compra <= data_ultima_compra`) e ambas devem ser posteriores ou contemporâneas à `data_criacao` da conta.

---

# 3. Data Quality, Transformation & Lineage

> Define como a entidade é validada, transformada e movimentada entre as camadas do pipeline.

## Validação

As regras de integridade, restrições e higienização são estruturadas como funções declarativas que compõem o pipeline de validação e qualidade dos dados:

### 01 — `validar_pk_cliente_id(cliente_id)`
Valida se o identificador `cliente_id` é único, positivo e não nulo (`NOT NULL & UNIQUE`).

### 02 — `validar_formato_email(email)`
Valida se o endereço de e-mail possui sintaxe padrão (`^[\w\.-]+@[\w\.-]+\.\w+$`) e não contém caracteres inválidos.

### 03 — `sanitizar_email(email)`
Aplica `TRIM()` e converte para minúsculas (`LOWER()`) para assegurar unicidade canônica e consistência nas campanhas.

### 04 — `validar_campos_obrigatorios(cliente_id, primeiro_nome, email, status_ativo, data_criacao)`
Garante que todos os atributos mandatários estejam preenchidos (`IS NOT NULL`).

### 05 — `validar_dominio_segmento_rfm(segmento_rfm)`
Verifica se o segmento RFM pertence ao conjunto `{'premium', 'regular', 'dormant', 'novo'}` ou nulo.

### 06 — `sanitizar_telefone(telefone)`
Remove caracteres não-numéricos indesejados, preservando formato estruturado com DDD e DDI para envio de SMS e WhatsApp.

### 07 — `validar_consistencia_compras_ltv(total_compras, lifetime_value)`
Valida se a relação entre compras e LTV é coerente: `total_compras >= 0` e `lifetime_value >= 0.00`. Alerta se `total_compras = 0` e `lifetime_value > 0`.

### 08 — `validar_consistencia_temporal_cliente(data_criacao, data_primeira_compra, data_ultima_compra)`
Assegura que `data_primeira_compra <= data_ultima_compra` e que nenhuma data de compra preceda o cadastro do cliente (`data_primeira_compra >= data_criacao::DATE`).

## Pipeline de Transformação

O pipeline estabelece uma **fronteira arquitetural clara entre a Plataforma de Dados e a Aplicação/Domínio**:
- **Papel da Plataforma de Dados**: Ingerir, detectar desvios, classificar severidade, medir impacto, registrar evidências brutas (`payload_raw`) e comunicar anomalias.
- **Papel da Aplicação / Domínio**: Consumir os eventos de anomalia e executar as decisões de resolução (recadastramento, higienização cadastral ou acionamento de esteiras de enriquecimento).

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
 ├── [Registros Válidos/Higienizados] ──→ clientes_qualify (Silver Qualify)
 └── [Inconsistências Detectadas]    ──→ clientes_anomalies (Silver Anomaly)
```

### Raw → Qualify

Ingestão dos dados cadastrais brutos (CSV/Parquet), normalização de e-mails, padronização de telefones, casting de tipos (DECIMAL, DATE, TIMESTAMPTZ), deduplicação por chave natural e validação de regras de consentimento.

```text
clientes_raw
→ validar_schema_e_tipagem
→ extrair_e_rotear_anomalias (envia evidências para clientes_anomalies)
→ sanitizar_email (lower, trim)
→ padronizar_telefone_e_mascaras
→ validar_consistencia_ltv_e_pedidos
→ validar_consistencia_datas_compra
→ deduplicar_por_email_e_id
→ clientes_qualify
```

### Raw → Anomaly

Mecanismo de captura, classificação e registro de desvios que impactam a entregabilidade de campanhas e a integridade analítica do LTV. A plataforma preserva o payload bruto original para auditoria e governança.

```text
clientes_raw
    ↓
[Motor de Detecção e Classificação de Anomalias]
    ├── ANOM-01: E-mail Malformado / Inválido (sintaxe quebrada ou domínio ilegível)
    ├── ANOM-02: Divergência LTV vs Compras (LTV > 0 com total_compras = 0 ou LTV < 0)
    ├── ANOM-03: Inversão Cronológica de Compras (data_primeira_compra > data_ultima_compra)
    └── ANOM-04: Telefone com Formato Inválido / Sem DDD (impede réguas móveis)
    ↓
clientes_anomalies (Repositório de Evidências & Alertas da Plataforma)
```

#### Regras de Anomalia de Negócio

| Código | Regra de Anomalia | Severidade | Risco de Negócio | Ação do Pipeline |
|---|---|:---:|---|---|
| `ANOM-01` | `email NOT LIKE '%@%.%'` ou sintaxe inválida | `CRÍTICA` | Falha total de entrega em campanhas de resgate e impossibilidade de contato | Encaminha evidência para Anomaly |
| `ANOM-02` | `(total_compras = 0 AND lifetime_value > 0)` ou `lifetime_value < 0` | `ALTA` | Distorção nas métricas de LTV e alocação incorreta em campanhas VIP | Encaminha evidência para Anomaly |
| `ANOM-03` | `data_primeira_compra > data_ultima_compra` ou `< data_criacao::DATE` | `ALTA` | Falha na cronologia transacional e quebra de relatórios de cohort | Encaminha evidência para Anomaly |
| `ANOM-04` | `telefone IS NOT NULL AND LENGTH(REGEXP_REPLACE(telefone, '\D', '')) < 10` | `MÉDIA` | Desperdício de créditos de SMS e bounce em disparos via WhatsApp | Encaminha evidência para Anomaly |

#### Estrutura do Artefato de Anomalias (`clientes_anomalies`)

A estrutura do artefato reflete as atribuições estritas da plataforma de dados (detecção, classificação e evidência):

| Campo | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `anomaly_id` | VARCHAR / UUID | Identificador exclusivo do evento de anomalia | `anom-c1a7e8f2-309a` |
| `cliente_id` | INT | Identificador do cliente afetado | `42` |
| `codigo_anomalia` | VARCHAR(20) | Código identificador da regra violada (`ANOM-01` a `ANOM-04`) | `ANOM-01` |
| `severidade` | VARCHAR(10) | Grau de risco atribuído: `'CRITICA'`, `'ALTA'`, `'MEDIA'`, `'BAIXA'` | `CRITICA` |
| `descricao_risco` | VARCHAR(255) | Diagnóstico descritivo do desvio identificado | `E-mail com sintaxe inválida (maria.silva@@email..com), inviabilizando canal de resgate` |
| `payload_raw` | TEXT / JSON | Snapshot fiel do registro bruto recebido da camada Raw | `{"cliente_id": 42, "email": "maria.silva@@email..com", "telefone": "119999"}` |
| `detected_at` | TIMESTAMPTZ | Timestamp de auditoria da detecção do desvio pela plataforma | `2026-03-15 14:25:00+00` |

### Qualify → Curated

Enriquecimento dos dados de clientes com métricas consolidadas de carrinhos abandonados, taxas individuais de conversão e propensão a resposta por canal para alimentação de dashboards de CRM e agentes de IA.

```text
clientes_qualify
    ↓
join agregado com carrinhos_qualify (taxa_abandono_cliente, total_carrinhos_criados)
    ↓
join agregado com eventos_resgate_qualify (taxa_abertura_email, canal_mais_efetivo)
    ↓
dim_clientes / fct_perfil_cliente_360 (Curated Gold)
```

## Classificação por Camada

| Camada | Ativo | Característica |
|---|---|---|
| Raw / Bronze | `raw_clientes` (`/raw/recuperacao_carrinho/clientes.parquet`) | Dados brutos preservados diretamente da origem cadastral transacional |
| Qualify / Silver | `qualify_clientes` (`CART_RECOVERY.CLIENTES`) | Dados cadastrais tipados, deduplicados, sanitizados e validados com permissões |
| Anomaly / Silver | `clientes_anomalies` (`CART_RECOVERY.CLIENTES_ANOMALIES`) | Repositório de evidências, dead-letter e alertas de qualidade para atuação do CRM/Domínio |
| Curated / Gold | `dim_clientes`, `dim_clientes_rfm`, `view_clientes_resgate` | Dados modelados dimensionalmente, enriquecidos com comportamento 360° |

## Lineage

### Upstream

```text
E-commerce Identity Service / CRM / User Registration API
    ↓
/raw/recuperacao_carrinho/clientes.parquet (Bronze)
```

### Qualification & Risk Routing (Transformation)

```text
raw_clientes
        ↓
Clientes Data Quality & Anomaly Detection Pipeline
        │
        ├── Registros válidos
        │       ↓
        │   clientes_qualify
        │
        └── Registros inválidos/anômalos
                ↓
            clientes_anomalies
```

### Downstream

```text
clientes_qualify
        ↓
Curated / Gold
        ↓
├── BI / Analytics & LTV Cohorts
├── CRM / Automação de Marketing
├── Data App de Resgate
├── Modelos de Propensão & Churn
└── Agentes de IA

clientes_anomalies
        ↓
├── Data Quality Dashboard
├── Alertas de Higienização Cadastral
└── Aplicação / CRM de Atendimento
```

---

# 4. Governance & Consumption

## Governança

- **Owner:** Engenharia de Dados & CRM Analytics (`crm-analytics@marketplace.com`)
- **Classificação:** Confidencial / Sensível (LGPD)
- **PII:** Sim (contém Dados Pessoais Identificáveis: `primeiro_nome`, `ultimo_nome`, `email`, `telefone`)
- **Tags:**
  - `clientes`
  - `dimensao`
  - `rfm`
  - `pii`
  - `lgpd`
  - `silver`
  - `cart_recovery`

## Consumidores

- **CRM & Réguas de Comunicação:** Alimentação de automações de e-mail marketing, push e WhatsApp respeitando os opt-ins cadastrados.
- **Analytics & BI:** Relatórios de performance de clientes por coorte, distribuição RFM e evolução de LTV.
- **Data App de Cart Recovery:** Visualização do perfil do cliente e histórico de interações durante a recuperação de carrinhos.
- **Modelos Preditivos & Agentes de IA:** Algoritmos de propensão de compra e personalização dinâmica de ofertas com base em segmento RFM.
- **Sistemas de Domínio & Atendimento:** Consumo de `clientes_anomalies` para recadastramento de clientes com dados de contato inválidos.

## Observações

- O campo `email` funciona como a chave natural de relacionamento no ecossistema e passa por normalização automática (`lowercase` + `trim`).
- O consentimento explícito (`permite_email`, `permite_sms`, `permite_push`) deve ser rigorosamente auditado a cada disparo para conformidade regulatória.
- As métricas financeiras (`lifetime_value` e `total_compras`) são atualizadas a partir da liquidação de registros da tabela `pedidos`.
- O artefato de anomalias (`clientes_anomalies`) assegura rastreabilidade das falhas de contato sem descartar silenciosamente registros ou gerar falhas catastróficas em downstream.
