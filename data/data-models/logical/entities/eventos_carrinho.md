# Entidade: `eventos_carrinho`

---

# 1. Data Definition

> Define a estrutura dos dados, seus tipos, chaves, atributos e significados técnicos.

## Atributos / Data Dictionary

| Campo | Tipo | PK/FK | Nullable | Default | Descrição | Valores / Regras | Exemplo |
|---|---|---|---|---|---|---|---|
| `evento_id` | BIGINT | PK | `FALSE` | AUTO | Identificador único exclusivo da ocorrência do evento de telemetria | Inteiro sequencial de 64 bits único positivo | `1002042` |
| `carrinho_id` | INT | FK | `FALSE` | — | Identificador do carrinho associado à sessão em andamento | Deve existir na tabela `carrinhos` | `1001` |
| `cliente_id` | INT | FK | `FALSE` | — | Identificador do cliente proprietário da ação (desnormalização) | Deve existir na tabela `clientes` | `42` |
| `sessao_id` | VARCHAR(50) | — | `TRUE` | — | Identificador da visita para agregação temporal contínua | String alfanumérica única da sessão | `'sess_a8f3b29c1d'` |
| `timestamp_evento` | TIMESTAMPTZ | — | `FALSE` | NOW() | Timestamp exato da ocorrência da interação no site/app | Data/hora UTC válida | `2026-03-15 14:23:15+00` |
| `tipo_evento` | VARCHAR(50) | — | `FALSE` | — | Classificação da ação comportamental executada no funil | `'view_produto'`, `'add_carrinho'`, `'remove_carrinho'`, `'update_quantidade'`, `'view_checkout'`, `'inicio_pagamento'`, `'erro_pagamento'`, `'abandono'`, `'retorno'` | `'view_checkout'` |
| `duracao_evento_segundos` | INT | — | `TRUE` | — | Tempo de permanência do usuário na etapa/tela em segundos | Inteiro `>= 0` ou nulo | `45` |
| `dados_evento` | JSONB | — | `TRUE` | — | Payload semiestruturado com contexto dinâmico da ação | Objeto JSON válido ou nulo | `{"etapa": "pagamento", "metodo": "cartao_credito"}` |

### Foreign Keys

```text
eventos_carrinho.carrinho_id
    → carrinhos.carrinho_id

eventos_carrinho.cliente_id
    → clientes.cliente_id
```

## SCHEMA RULES

### 01 — Unicidade e Não-Nulidade da Chave Primária (PK)
O campo `evento_id` é chave primária inteira de alta capacidade (`BIGINT PRIMARY KEY BIGSERIAL`), obrigatória (`NOT NULL`) e exclusiva (`UNIQUE`), identificando unicamente cada log de telemetria da plataforma.

### 02 — Integridade Referencial e Desnormalização de Performance (FKs)
- O campo `carrinho_id` é chave estrangeira obrigatória (`INT NOT NULL`) referenciando `carrinhos(carrinho_id)` com política `ON DELETE CASCADE`.
- O campo `cliente_id` é chave estrangeira obrigatória (`INT NOT NULL`) referenciando `clientes(cliente_id)` com política `ON DELETE RESTRICT`, configurando desnormalização analítica intencional para eliminar joins custosos em queries de funil.

### 03 — Restrições de Domínio, Tipagem e Estrutura Semiestruturada (CHECK Constraints)
- `tipo_evento`: tipado como `VARCHAR(50)` com restrição `CHECK (tipo_evento IN ('view_produto', 'add_carrinho', 'remove_carrinho', 'update_quantidade', 'view_checkout', 'inicio_pagamento', 'erro_pagamento', 'abandono', 'retorno'))`.
- `duracao_evento_segundos`: tipado como `INT` com restrição `CHECK (duracao_evento_segundos >= 0 OR duracao_evento_segundos IS NULL)`.
- `dados_evento`: tipado como `JSONB` (PostgreSQL) / `VARIANT` (Snowflake), armazenando metadados contextuais dinâmicos.

### 04 — Nulabilidade e Valores Padrão (Defaults)
- **Campos Obrigatórios (NOT NULL)**: `evento_id`, `carrinho_id`, `cliente_id`, `timestamp_evento`, `tipo_evento`.
- **Valores Padrão**: `timestamp_evento = NOW()`.

---

# 2. Business Definition & Business Rules

## Identificação e Visão de Negócio

- **Nome físico:** `eventos_carrinho` (Snowflake: `CART_RECOVERY.EVENTOS_CARRINHO`)
- **Nome de negócio:** Telemetria & Eventos Comportamentais da Jornada de Compra
- **Domínio:** Telemetria, Web Analytics & Funil de Conversão / Marketplace E-commerce
- **Tipo:** Fato de Telemetria / Série Temporal Comportamental (Behavioral Time Series Fact)
- **Descrição:** Tabela de telemetria de alta granularidade que registra cada evento, clique e transição de estado realizada pelo consumidor durante a sessão de navegação, desde a visualização inicial de itens até as etapas de pagamento, erro ou abandono.
- **Objetivo de negócio:** Reconstruir o funil de checkout com precisão cirúrgica, mapear a etapa exata de fricção causadora do abandono, priorizar réguas de resgate técnicas (em caso de falha de pagamento) e alimentar modelos de machine learning com variáveis de tempo de permanência e engajamento.
- **Casos de uso:**
  - Identificar carrinhos abandonados imediatamente após eventos de `'erro_pagamento'` para acionamento de suporte proativo e recuperação via WhatsApp/SMS.
  - Calcular as taxas de passagem entre etapas: `Visualização de Produto` $\rightarrow$ `Adição` $\rightarrow$ `Checkout` $\rightarrow$ `Início de Pagamento` $\rightarrow$ `Conversão`.
  - Mensurar o tempo médio de hesitação antes do abandono através de `duracao_evento_segundos`.
  - Detectar o evento de `'retorno'` quando um cliente reativa uma sessão após clicar em um link de campanha de resgate.

## Granularidade

- **Granularidade:** Uma linha por interação ou evento discreto registrado pela telemetria na sessão de compras.
- **Regra:** `1 linha = 1 evento de navegação/sessão`

## Papel no Domínio

- Atua como a **fonte primária de comportamento dinâmico** do ecossistema de Cart Recovery.
- Fornece a dimensão temporal e diagnóstica para explicar o motivo pelo qual as sessões transacionais em `carrinhos` foram abandonadas ou recuperadas.

## Relacionamentos

| Entidade relacionada | Cardinalidade | Relacionamento |
|---|---:|---|
| `carrinhos` | N:1 | Cada evento está vinculado a exatamente uma sessão de carrinho de compras |
| `clientes` | N:1 | Cada evento está associado ao consumidor que executou a ação |

## Ciclo de Vida do Funil de Navegação

```text
[view_produto] ──→ [add_carrinho] ──→ [view_checkout] ──→ [inicio_pagamento] ──→ [comprado]
      │                   │                 │                   │
      ▼                   ▼                 ▼                   ▼
  [abandono]          [abandono]        [abandono]      [erro_pagamento] ──→ [abandono]
                                                                │
                                                                ▼
                                                        [retorno via resgate]
```

### Estados e Tipos de Evento

| Tipo de Evento | Etapa do Funil | Significado de Negócio |
|---|---|---|
| `view_produto` | Topo do Funil | Visualização da página de detalhes de um produto |
| `add_carrinho` | Meio do Funil | Inserção de uma ou mais unidades de um SKU no carrinho |
| `remove_carrinho` | Fricção / Ajuste | Exclusão voluntária de um item previamente adicionado |
| `update_quantidade` | Ajuste de Cesta | Alteração na quantidade de itens de uma linha |
| `view_checkout` | Fundo do Funil | Abertura da tela de checkout e revisão do pedido |
| `inicio_pagamento` | Intenção Final | Início do preenchimento dos dados financeiros de pagamento |
| `erro_pagamento` | Fricção Crítica | Recusa do gateway, cartão negado ou timeout de transação |
| `abandono` | Encerramento | Timeout de inatividade (30 min) ou saída explícita da sessão |
| `retorno` | Reativação | Reabertura do carrinho após ação de marketing de resgate |

## BUSINESS RULES

### 01 — Sequenciamento e Cronologia do Funil
Os eventos de uma sessão devem respeitar a ordem lógica da navegação humana no e-commerce. Ações avançadas como `view_checkout` ou `inicio_pagamento` não devem anteceder eventos de `add_carrinho` no histórico da mesma sessão.

### 02 — Prioridade no Diagnóstico de `erro_pagamento`
Quando uma sessão registra um evento `'erro_pagamento'`, a causa raiz da falha (`codigo_erro` e `metodo` em `dados_evento`) deve ser sinalizada com prioridade máxima para a esteira de CRM, disparando réguas de assistência técnica antes de descontos financeiros.

### 03 — Rastreamento de Sessão e Reativação (`retorno`)
O campo `sessao_id` identifica o bloco contínuo de navegação. Quando o cliente reabre um carrinho abandonado após clicar no link de uma campanha de recuperação, é gerado um evento `'retorno'` que inicializa um novo `sessao_id` associado ao mesmo `carrinho_id`.

### 04 — Consistência Temporal com a Criação do Carrinho
Nenhum evento pode possuir `timestamp_evento` anterior à data oficial de inicialização da sessão transacional (`carrinhos.data_criacao`).

### 05 — Estruturação Flexível do Contexto via `dados_evento`
Atributos variáveis por tipo de ação devem ser persistidos em formato semiestruturado (`JSONB`/`VARIANT`):
- `view_produto`: `{"produto_id": 101, "tempo_visualizacao_s": 45, "scroll_depth": 0.85}`
- `erro_pagamento`: `{"codigo_erro": "cartao_recusado", "metodo": "cartao_credito"}`
- `retorno`: `{"origem_retorno": "whatsapp_link", "horas_desde_abandono": 24}`

---

# 3. Data Quality, Transformation & Lineage

> Define como a entidade é validada, transformada e movimentada entre as camadas do pipeline.

## Validação

As regras de integridade, restrições e higienização são estruturadas como funções declarativas que compõem o pipeline de validação e qualidade dos dados:

### 01 — `validar_pk_evento_id(evento_id)`
Valida se o identificador `evento_id` é único, positivo e não nulo (`NOT NULL & UNIQUE`).

### 02 — `validar_fk_carrinho_id(carrinho_id)`
Valida se o `carrinho_id` existe na tabela `carrinhos`.

### 03 — `validar_fk_cliente_id(cliente_id)`
Valida se o `cliente_id` existe na tabela `clientes` e coincide com o proprietário do carrinho.

### 04 — `validar_campos_obrigatorios(evento_id, carrinho_id, cliente_id, timestamp_evento, tipo_evento)`
Garante que todos os atributos mandatários estejam preenchidos (`IS NOT NULL`).

### 05 — `validar_dominio_tipo_evento(tipo_evento)`
Verifica se o tipo do evento pertence à taxonomia oficial de 9 tipos reconhecidos pela plataforma.

### 06 — `validar_formato_jsonb(dados_evento)`
Assegura que o payload semiestruturado seja um JSON sintaticamente válido ou nulo.

### 07 — `validar_consistencia_temporal_evento(timestamp_evento, carrinhos_data_criacao)`
Assegura que `timestamp_evento >= carrinhos_data_criacao`. Inconsistências temporais são isoladas na camada de anomalias.

## Pipeline de Transformação

O pipeline estabelece uma **fronteira arquitetural clara entre a Plataforma de Dados e a Aplicação/Domínio**:
- **Papel da Plataforma de Dados**: Ingerir telemetria de alta frequência (stream/micro-batch), validar tipos e domínios, isolar payloads corrompidos em `eventos_carrinho_anomalies` e registrar evidências brutas (`payload_raw`).
- **Papel da Aplicação / Domínio**: Consumir os eventos de anomalia e executar as decisões de resolução (descartar logs de bot, calibrar SDK de telemetria ou acionar suporte de checkout).

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
 ├── [Registros Válidos/Higienizados] ──→ eventos_carrinho_qualify (Silver Qualify)
 └── [Inconsistências Detectadas]    ──→ eventos_carrinho_anomalies (Silver Anomaly)
```

### Raw → Qualify

Ingestão de logs de telemetria brutos (CSV/Parquet/JSON), casting de tipos para TIMESTAMPTZ e JSONB, validação de chaves relacionais com carrinhos e clientes, normalização de strings de eventos e deduplicação.

```text
eventos_carrinho_raw
→ validar_schema_e_tipagem
→ extrair_e_rotear_anomalias (envia evidências para eventos_carrinho_anomalies)
→ validar_fks_carrinho_e_cliente
→ validar_dominio_tipo_evento
→ validar_sintaxe_jsonb_dados_evento
→ validar_consistencia_temporal
→ deduplicar_evento_id
→ eventos_carrinho_qualify
```

### Raw → Anomaly

Mecanismo de captura, classificação e registro de eventos corrompidos, schema drift ou divergências de sincronização de relógio. A plataforma preserva o payload bruto original para auditoria e governança.

```text
eventos_carrinho_raw
    ↓
[Motor de Detecção e Classificação de Anomalias]
    ├── ANOM-01: Tipo de Evento Inválido / Schema Drift (tipo_evento fora do domínio)
    ├── ANOM-02: Inversão Temporal (timestamp_evento < carrinhos.data_criacao)
    ├── ANOM-03: Divergência de Identidade (cliente_id do evento != dono do carrinho)
    └── ANOM-04: Payload JSONB Malformado ou Corrompido
    ↓
eventos_carrinho_anomalies (Repositório de Evidências & Alertas da Plataforma)
```

#### Regras de Anomalia de Negócio

| Código | Regra de Anomalia | Severidade | Risco de Negócio | Ação do Pipeline |
|---|---|:---:|---|---|
| `ANOM-01` | `tipo_evento NOT IN ('view_produto', 'add_carrinho', 'remove_carrinho', 'update_quantidade', 'view_checkout', 'inicio_pagamento', 'erro_pagamento', 'abandono', 'retorno')` | `CRÍTICA` | Schema drift na telemetria, quebra de dashboards de funil e falha em triggers | Encaminha evidência para Anomaly |
| `ANOM-02` | `timestamp_evento < carrinhos.data_criacao` | `ALTA` | Falha de sincronização de relógio de clientes/SDK e corrupção de métricas de sessão | Encaminha evidência para Anomaly |
| `ANOM-03` | `eventos_carrinho.cliente_id != carrinhos.cliente_id` | `ALTA` | Poluição de sessão por troca de usuário em dispositivo compartilhado ou bug de token | Encaminha evidência para Anomaly |
| `ANOM-04` | `dados_evento IS NOT NULL AND NOT IS_VALID_JSON(dados_evento)` | `MÉDIA` | Impossibilidade de parsing de atributos contextuais e perda de diagnóstico técnico | Encaminha evidência para Anomaly |

#### Estrutura do Artefato de Anomalias (`eventos_carrinho_anomalies`)

A estrutura do artefato reflete as atribuições estritas da plataforma de dados (detecção, classificação e evidência):

| Campo | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `anomaly_id` | VARCHAR / UUID | Identificador exclusivo do evento de anomalia | `anom-7c1e3a9f-408d` |
| `evento_id` | BIGINT | Identificador da linha de telemetria afetada | `1002042` |
| `carrinho_id` | INT | Identificador do carrinho associado | `1001` |
| `cliente_id` | INT | Identificador do cliente associado | `42` |
| `codigo_anomalia` | VARCHAR(20) | Código identificador da regra violada (`ANOM-01` a `ANOM-04`) | `ANOM-01` |
| `severidade` | VARCHAR(10) | Grau de risco atribuído: `'CRITICA'`, `'ALTA'`, `'MEDIA'`, `'BAIXA'` | `CRITICA` |
| `descricao_risco` | VARCHAR(255) | Diagnóstico descritivo do desvio identificado | `Tipo de evento desconhecido ('click_banner_promocional') recebido` |
| `payload_raw` | TEXT / JSON | Snapshot fiel do registro bruto recebido da camada Raw | `{"evento_id": 1002042, "tipo_evento": "click_banner_promocional"}` |
| `detected_at` | TIMESTAMPTZ | Timestamp de auditoria da detecção do desvio pela plataforma | `2026-03-15 14:25:00+00` |

### Qualify → Curated

Agregação temporal por carrinho e sessão para cômputo do último evento antes do abandono, tempo total no checkout, contagem de erros de gateway e geração de views analíticas de funil de conversão.

```text
eventos_carrinho_qualify
    ↓
agregação temporal por carrinho_id (ultimo_evento, total_erros_pagamento, duracao_checkout_s)
    ↓
join com carrinhos_qualify (status, valor_total)
    ↓
fct_funil_carrinho / view_jornada_abandono (Curated Gold)
```

## Classificação por Camada

| Camada | Ativo | Característica |
|---|---|---|
| Raw / Bronze | `raw_eventos_carrinho` (`/raw/recuperacao_carrinho/eventos_carrinho.parquet`) | Logs brutos de telemetria preservados diretamente da camada de captura |
| Qualify / Silver | `qualify_eventos_carrinho` (`CART_RECOVERY.EVENTOS_CARRINHO`) | Dados de eventos tipados, sanitizados e validados com integridade relacional |
| Anomaly / Silver | `eventos_carrinho_anomalies` (`CART_RECOVERY.EVENTOS_CARRINHO_ANOMALIES`) | Repositório de evidências, quarentena de anomalias e alertas de schema drift de telemetria |
| Curated / Gold | `fct_funil_carrinho`, `view_jornada_abandono`, `fct_atrito_checkout` | Dados agregados em funil para consumo analítico e operacional |

## Lineage

### Upstream

```text
Web SDK / Mobile Telemetry Tracker / Checkout Event Stream
    ↓
/raw/recuperacao_carrinho/eventos_carrinho.parquet (Bronze)
```

### Qualification & Risk Routing (Transformation)

```text
raw_eventos_carrinho
        ↓
Eventos de Telemetria Data Quality & Anomaly Detection Pipeline
        │
        ├── Registros válidos
        │       ↓
        │   eventos_carrinho_qualify
        │
        └── Registros inválidos/anômalos
                ↓
            eventos_carrinho_anomalies
```

### Downstream

```text
eventos_carrinho_qualify
        ↓
Curated / Gold
        ↓
├── BI / Analytics de Funil de Conversão
├── Triggers em Tempo Real de Resgate (+1h)
├── Modelos Preditivos de Churn / Abandono
└── Agentes de IA

eventos_carrinho_anomalies
        ↓
├── Data Quality Dashboard
├── Alertas de Schema Drift de Web SDK
└── Aplicação / Time de Telemetria
```

---

# 4. Governance & Consumption

## Governança

- **Owner:** Engenharia de Dados & Squad de Telemetria / Web Analytics (`telemetry-data@marketplace.com`)
- **Classificação:** Interno
- **PII:** Não (contém identificadores relacionais, timestamps e métricas de navegação sem dados pessoais diretos)
- **Tags:**
  - `eventos_carrinho`
  - `telemetria`
  - `time_series`
  - `funil`
  - `silver`
  - `cart_recovery`

## Consumidores

- **Triggers de Automação de Marketing:** Acionamento de réguas imediatas (1h pós-abandono) com base no último evento registrado.
- **Analytics & BI:** Relatórios de funil de conversão, taxa de queda por tela e mapa de calor de atrito no checkout.
- **Data App de Cart Recovery:** Exibição da timeline visual de ações do cliente antes do abandono.
- **Modelos Preditivos & Agentes de IA:** Algoritmos preditivos que utilizam a sequência e duração dos eventos para prever probabilidade de resgate.
- **Sistemas de Domínio & Engenharia de Frontend:** Consumo de `eventos_carrinho_anomalies` para correção rápida de bugs no SDK do site.

## Observações

- A tabela `eventos_carrinho` representa a maior volumetria do modelo analítico e adota chave primária `BIGINT` para suporte a centenas de milhões de registros.
- O campo `dados_evento` em `JSONB`/`VARIANT` permite acoplar novos parâmetros de rastreamento sem necessidade de refatorações estruturais ou migrações de banco.
- O artefato `eventos_carrinho_anomalies` garante resiliência na esteira de dados, absorvendo eventos malformados de browsers obsoletos sem interromper o pipeline analítico principal.
