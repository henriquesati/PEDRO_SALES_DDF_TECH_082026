# Entidade: `eventos_resgate`

---

# 1. Data Definition

> Define a estrutura dos dados, seus tipos, chaves, atributos e significados técnicos.

## Atributos / Data Dictionary

| Campo | Tipo | PK/FK | Nullable | Default | Descrição | Valores / Regras | Exemplo |
|---|---|---|---|---|---|---|---|
| `resgate_id` | BIGINT | PK | `FALSE` | AUTO | Identificador único exclusivo da tentativa de resgate | Inteiro sequencial de 64 bits único positivo | `3001` |
| `carrinho_id` | INT | FK | `FALSE` | — | Identificador do carrinho abandonado alvo da campanha | Deve existir na tabela `carrinhos` | `1001` |
| `cliente_id` | INT | FK | `FALSE` | — | Identificador do cliente destinatário da comunicação | Deve existir na tabela `clientes` | `42` |
| `canal` | VARCHAR(50) | — | `FALSE` | — | Canal de mensageria utilizado para o disparo | `'email'`, `'sms'`, `'push_app'`, `'whatsapp'` | `'email'` |
| `tipo_comunicacao` | VARCHAR(50) | — | `FALSE` | — | Template / momento da régua de resgate | `'lembrete_1h'`, `'lembrete_24h'`, `'desconto_48h'`, `'urgencia_72h'` | `'lembrete_1h'` |
| `data_schedule` | TIMESTAMPTZ | — | `FALSE` | — | Timestamp programado para o envio da mensagem | Data/hora UTC válida | `2026-03-15 16:15:00+00` |
| `data_envio` | TIMESTAMPTZ | — | `TRUE` | — | Timestamp em que a mensagem foi efetivamente despachada | `>= data_schedule` ou nulo (se pendente) | `2026-03-15 16:16:10+00` |
| `assunto` | VARCHAR(255) | — | `TRUE` | — | Assunto do e-mail ou título da notificação push/SMS | Texto descritivo | `'Você esqueceu algo no carrinho 🛒'` |
| `desconto_oferecido` | DECIMAL(10,2) | — | `TRUE` | `0.00` | Valor monetário de abatimento concedido na oferta | DECIMAL `>= 0.00` | `25.00` |
| `frete_gratis_oferecido` | BOOLEAN | — | `FALSE` | `FALSE` | Flag indicando se a oferta incluiu isenção de taxa de frete | `TRUE` / `FALSE` | `FALSE` |
| `custo_envio` | DECIMAL(10,2) | — | `FALSE` | — | Custo operacional unitário tarifado pelo canal de envio | DECIMAL `>= 0.00` | `0.05` |
| `data_abertura` | TIMESTAMPTZ | — | `TRUE` | — | Timestamp em que o cliente visualizou/abriu a mensagem | `>= data_envio` ou nulo | `2026-03-15 16:45:00+00` |
| `data_primeiro_clique` | TIMESTAMPTZ | — | `TRUE` | — | Timestamp em que o cliente clicou no link de resgate | `>= data_abertura` ou nulo | `2026-03-15 16:47:30+00` |
| `link_clicado` | VARCHAR(500) | — | `TRUE` | — | URL com parâmetros UTM de rastreamento de campanha | URL válida | `'https://marketplace.com.br/carrinho/1001?utm_source=email'` |
| `data_conversao` | TIMESTAMPTZ | — | `TRUE` | — | Timestamp de liquidação da compra a partir do resgate | `>= data_primeiro_clique` ou nulo | `2026-03-15 17:05:00+00` |
| `sucesso` | BOOLEAN | — | `FALSE` | `FALSE` | Flag indicando se a tentativa resultou em compra confirmada | `TRUE` / `FALSE` | `TRUE` |
| `valor_pedido_final` | DECIMAL(10,2) | — | `TRUE` | — | Valor total do pedido confirmado originado pelo resgate | DECIMAL `>= 0.00` ou nulo | `224.90` |
| `created_at` | TIMESTAMPTZ | — | `FALSE` | NOW() | Timestamp de auditoria de inserção do registro de resgate | Data/hora UTC | `2026-03-15 15:15:00+00` |

### Foreign Keys

```text
eventos_resgate.carrinho_id
    → carrinhos.carrinho_id

eventos_resgate.cliente_id
    → clientes.cliente_id

eventos_resgate.resgate_id
    ← pedidos.resgate_id
```

## SCHEMA RULES

### 01 — Unicidade e Não-Nulidade da Chave Primária (PK)
O campo `resgate_id` é chave primária inteira de alta capacidade (`BIGINT PRIMARY KEY BIGSERIAL`), obrigatória (`NOT NULL`) e exclusiva (`UNIQUE`), identificando unicamente cada tentativa e disparo de régua de recuperação.

### 02 — Integridade Referencial (FKs)
- `carrinho_id INT NOT NULL` referencia `carrinhos(carrinho_id)` com política `ON DELETE CASCADE`.
- `cliente_id INT NOT NULL` referencia `clientes(cliente_id)` com política `ON DELETE RESTRICT`.
- `resgate_id` é referenciado opcionalmente por `pedidos(resgate_id)` com política `ON DELETE SET NULL` para atribuição de conversão.

### 03 — Restrições de Domínio, Tipagem e Precisão Numérica (CHECK Constraints)
- `canal`: tipado como `VARCHAR(50)` com restrição `CHECK (canal IN ('email', 'sms', 'push_app', 'whatsapp'))`.
- `tipo_comunicacao`: tipado como `VARCHAR(50)` com restrição `CHECK (tipo_comunicacao IN ('lembrete_1h', 'lembrete_24h', 'desconto_48h', 'urgencia_72h'))`.
- `custo_envio`: tipado como `DECIMAL(10,2)` com restrição `CHECK (custo_envio >= 0.00)`.
- `desconto_oferecido`: tipado como `DECIMAL(10,2)` com restrição `CHECK (desconto_oferecido >= 0.00 OR desconto_oferecido IS NULL)`.
- `valor_pedido_final`: tipado como `DECIMAL(10,2)` com restrição `CHECK (valor_pedido_final >= 0.00 OR valor_pedido_final IS NULL)`.

### 04 — Nulabilidade e Valores Padrão (Defaults)
- **Campos Obrigatórios (NOT NULL)**: `resgate_id`, `carrinho_id`, `cliente_id`, `canal`, `tipo_comunicacao`, `data_schedule`, `custo_envio`, `frete_gratis_oferecido`, `sucesso`, `created_at`.
- **Valores Padrão**: `desconto_oferecido = 0.00`, `frete_gratis_oferecido = FALSE`, `sucesso = FALSE`, `created_at = NOW()`.

---

# 2. Business Definition & Business Rules

## Identificação e Visão de Negócio

- **Nome físico:** `eventos_resgate` (Snowflake: `CART_RECOVERY.EVENTOS_RESGATE`)
- **Nome de negócio:** Disparos & Engajamento de Campanhas de Recuperação
- **Domínio:** CRM, Growth Marketing & Recuperação de Receita / Marketplace E-commerce
- **Tipo:** Fato de Engajamento & Campanha (Campaign & Engagement Fact)
- **Descrição:** Tabela analítico-operacional que gerencia a esteira de comunicação ativa pós-abandono, rastreando o agendamento, despacho, taxas de abertura, cliques em links parametrizados, custos unitários e a atribuição de pedidos convertidos.
- **Objetivo de negócio:** Avaliar a eficácia de cada canal de contato, mensurar a elasticidade de incentivos promocionais (desconto progressivo vs frete grátis), controlar a fadiga do consumidor e calcular com exatidão o Retorno sobre o Investimento (ROI) das estratégias de resgate.
- **Casos de uso:**
  - Controlar o pipeline de cadência em 4 toques (`1h`, `24h`, `48h`, `72h`) para carrinhos abandonados.
  - Avaliar o canal de melhor ROI por segmento RFM (ex: WhatsApp para clientes `premium` vs E-mail para `regular`).
  - Auditar o respeito às regras de privacidade LGPD antes de cada envio.
  - Atribuir o faturamento recuperado à campanha específica para cálculo de performance da equipe de Growth.

## Granularidade

- **Granularidade:** Uma linha por tentativa ou disparo individual de mensagem de resgate enviada a um cliente referente a uma sessão de carrinho abandonado.
- **Regra:** `1 linha = 1 disparo de comunicação de resgate`

## Papel no Domínio

- Atua como o **motor central de reativação** do case de Cart Recovery.
- Conecta a detecção de inatividade em `carrinhos`, o perfil de consentimento em `clientes` e a efetivação final de receita em `pedidos`.

## Relacionamentos

| Entidade relacionada | Cardinalidade | Relacionamento |
|---|---:|---|
| `carrinhos` | N:1 | Cada disparo de resgate é direcionado a um carrinho abandonado específico |
| `clientes` | N:1 | Cada disparo é enviado a um cliente cadastrado |
| `pedidos` | 1:1 (opcional) | Um resgate bem-sucedido pode originar exatamente um pedido de compra confirmado |

## Ciclo de Vida da Régua de Resgate

```text
[data_schedule] ──→ [data_envio] ──→ [data_abertura] ──→ [data_primeiro_clique] ──→ [data_conversao]
        │                   │                 │                   │                        │
        ▼                   ▼                 ▼                   ▼                        ▼
(agendado)          (despachado)      (visualizado)          (clicado)            (sucesso = TRUE)
```

### Sequência Padrão de Toques

| Toque / Template | Janela Pós-Abandono | Canal Padrão | Tipo de Oferta | Estratégia |
|---|:---:|---|---|---|
| `lembrete_1h` | +1 hora | E-mail / Push | Lembrete Suave | Lembrete de conveniência sem concessão de desconto |
| `lembrete_24h` | +24 horas | E-mail / Push | Reserva de Itens | Alerta de escassez de estoque e reserva temporária |
| `desconto_48h` | +48 horas | E-mail / SMS | Desconto (5% a 10%) | Cupom financeiro para quebra de objeção de preço |
| `urgencia_72h` | +72 horas | E-mail / WhatsApp | Desconto + Frete Grátis | Oferta final agressiva com frete grátis e senso de urgência |

## BUSINESS RULES

### 01 — Conformidade com Opt-in e Governança de Canais (LGPD)
Nenhuma mensagem pode ser enviada por um canal sem o devido consentimento ativo registrado em `clientes`:
- Disparos via E-mail exigem `clientes.permite_email = TRUE`.
- Disparos via SMS ou WhatsApp exigem `clientes.permite_sms = TRUE` e telefone com DDD válido.
- Disparos via Push Notification exigem `clientes.permite_push = TRUE`.

### 02 — Sequência Cadenciada e Cancelamento por Conversão
O limite máximo é de 4 tentativas por carrinho abandonado. Caso o cliente converta em qualquer um dos toques (`sucesso = TRUE`), todos os agendamentos posteriores vinculados àquele `carrinho_id` são automaticamente cancelados para evitar comunicação redundante e spam.

### 03 — Sequenciamento Cronológico do Funil de Resgate
Os timestamps devem obedecer à ordem natural dos eventos:
$$\text{data\_schedule} \le \text{data\_envio} \le \text{data\_abertura} \le \text{data\_primeiro\_clique} \le \text{data\_conversao}$$
Registros onde a data de abertura antecede a data de envio representam dirty data e devem ser isolados na camada de anomalias.

### 04 — Atribuição de Receita e Cálculo de ROI Financeiro
Quando `sucesso = TRUE`, os campos `data_conversao` e `valor_pedido_final` tornam-se de preenchimento obrigatório. O ROI financeiro da ação é obtido pela equação:
$$\text{ROI} = \frac{\text{valor\_pedido\_final} - \text{desconto\_oferecido} - \text{custo\_envio}}{\text{custo\_envio}}$$

### 05 — Custo Operacional Unitário por Canal
Cada disparo gera um custo fixo de entrega tarifado pelo provedor de mensageria:
- `email`: R$ 0.05
- `push_app`: R$ 0.02
- `sms`: R$ 0.15
- `whatsapp`: R$ 0.30

---

# 3. Data Quality, Transformation & Lineage

> Define como a entidade é validada, transformada e movimentada entre as camadas do pipeline.

## Validação

As regras de integridade, restrições e higienização são estruturadas como funções declarativas que compõem o pipeline de validação e qualidade dos dados:

### 01 — `validar_pk_resgate_id(resgate_id)`
Valida se o identificador `resgate_id` é único, positivo e não nulo (`NOT NULL & UNIQUE`).

### 02 — `validar_fk_carrinho_id(carrinho_id)`
Valida se o `carrinho_id` existe na tabela `carrinhos`.

### 03 — `validar_fk_cliente_id(cliente_id)`
Valida se o `cliente_id` existe na tabela `clientes` e coincide com o proprietário do carrinho.

### 04 — `validar_campos_obrigatorios(resgate_id, carrinho_id, cliente_id, canal, tipo_comunicacao, data_schedule, custo_envio, frete_gratis_oferecido, sucesso, created_at)`
Garante que todos os atributos mandatários estejam preenchidos (`IS NOT NULL`).

### 05 — `validar_dominios_canal_e_tipo(canal, tipo_comunicacao)`
Valida se o canal e o template pertencem às listas fechadas homologadas no sistema.

### 06 — `validar_consistencia_temporal_funil_resgate(data_schedule, data_envio, data_abertura, data_primeiro_clique, data_conversao)`
Assegura que as marcas temporais obedeçam à cronologia: $\text{schedule} \le \text{envio} \le \text{abertura} \le \text{clique} \le \text{conversao}$.

### 07 — `validar_coerencia_sucesso_conversao(sucesso, data_conversao, valor_pedido_final)`
Valida que, se `sucesso = TRUE`, `data_conversao` e `valor_pedido_final` não sejam nulos e `valor_pedido_final > 0.00`.

## Pipeline de Transformação

O pipeline estabelece uma **fronteira arquitetural clara entre a Plataforma de Dados e a Aplicação/Domínio**:
- **Papel da Plataforma de Dados**: Ingerir webhooks de mensageria (SendGrid, Twilio, Meta WhatsApp API), validar sequenciamento temporal, correlacionar conversões e isolar inconsistências em `eventos_resgate_anomalies`.
- **Papel da Aplicação / Domínio**: Consumir os eventos de anomalia e executar as decisões de resolução (recalcular atribuição, pausar réguas com taxa alta de erro ou revalidar chaves de integração).

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
 ├── [Registros Válidos/Higienizados] ──→ eventos_resgate_qualify (Silver Qualify)
 └── [Inconsistências Detectadas]    ──→ eventos_resgate_anomalies (Silver Anomaly)
```

### Raw → Qualify

Ingestão dos logs de despacho e engajamento brutos (CSV/Parquet/Webhooks), casting de tipos (DECIMAL, TIMESTAMPTZ), validação de integridade referencial, cômputo de custos por canal e deduplicação.

```text
eventos_resgate_raw
→ validar_schema_e_tipagem
→ extrair_e_rotear_anomalias (envia evidências para eventos_resgate_anomalies)
→ validar_fks_carrinho_e_cliente
→ validar_dominios_canal_e_tipo
→ validar_consistencia_temporal_funil
→ validar_coerencia_sucesso_conversao
→ deduplicar_resgate_id
→ eventos_resgate_qualify
```

### Raw → Anomaly

Mecanismo de captura, classificação e registro de desvios temporais, disparos sem opt-in ou falhas de atribuição. A plataforma preserva o payload bruto original para auditoria e governança.

```text
eventos_resgate_raw
    ↓
[Motor de Detecção e Classificação de Anomalias]
    ├── ANOM-01: Inversão Temporal de Engajamento (data_abertura < data_envio ou data_clique < data_abertura)
    ├── ANOM-02: Divergência de Conversão (sucesso = TRUE com valor_pedido_final ou data_conversao nulos)
    ├── ANOM-03: Violação de Opt-in / Spam (Disparo para canal com consentimento desativado)
    └── ANOM-04: Custo Operacional Inválido (custo_envio < 0 ou nulo em canal tarifado)
    ↓
eventos_resgate_anomalies (Repositório de Evidências & Alertas da Plataforma)
```

#### Regras de Anomalia de Negócio

| Código | Regra de Anomalia | Severidade | Risco de Negócio | Ação do Pipeline |
|---|---|:---:|---|---|
| `ANOM-01` | `data_abertura < data_envio` ou `data_primeiro_clique < data_abertura` | `CRÍTICA` | Falha de sincronização de webhook de e-mail e distorção em métricas de tempo de resposta | Encaminha evidência para Anomaly |
| `ANOM-02` | `sucesso = TRUE AND (valor_pedido_final IS NULL OR data_conversao IS NULL)` | `ALTA` | Falha de reconciliação fiscal e impossibilidade de apuração de ROI financeiro | Encaminha evidência para Anomaly |
| `ANOM-03` | Disparo realizado para canal onde `clientes.permite_* = FALSE` | `ALTA` | Risco de penalidade regulatória por descumprimento de consentimento LGPD | Encaminha evidência para Anomaly |
| `ANOM-04` | `custo_envio < 0.00` | `MÉDIA` | Erro contábil de apuração de custo operacional de marketing | Encaminha evidência para Anomaly |

#### Estrutura do Artefato de Anomalias (`eventos_resgate_anomalies`)

A estrutura do artefato reflete as atribuições estritas da plataforma de dados (detecção, classificação e evidência):

| Campo | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `anomaly_id` | VARCHAR / UUID | Identificador exclusivo do evento de anomalia | `anom-8a2f1c3d-507e` |
| `resgate_id` | BIGINT | Identificador do evento de resgate afetado | `3042` |
| `carrinho_id` | INT | Identificador do carrinho associado | `1001` |
| `cliente_id` | INT | Identificador do cliente associado | `42` |
| `codigo_anomalia` | VARCHAR(20) | Código identificador da regra violada (`ANOM-01` a `ANOM-04`) | `ANOM-01` |
| `severidade` | VARCHAR(10) | Grau de risco atribuído: `'CRITICA'`, `'ALTA'`, `'MEDIA'`, `'BAIXA'` | `CRITICA` |
| `descricao_risco` | VARCHAR(255) | Diagnóstico descritivo do desvio identificado | `Data de abertura (14:00) anterior à data de envio (14:30)` |
| `payload_raw` | TEXT / JSON | Snapshot fiel do registro bruto recebido da camada Raw | `{"resgate_id": 3042, "data_envio": "2026-03-15 14:30:00", "data_abertura": "2026-03-15 14:00:00"}` |
| `detected_at` | TIMESTAMPTZ | Timestamp de auditoria da detecção do desvio pela plataforma | `2026-03-15 14:35:00+00` |

### Qualify → Curated

Agregação por canal e campanha para cômputo de taxas de conversão (CTR, Open Rate, CVR), ROI líquido por régua e consolidação das views analíticas para dashboards executivos e agentes de otimização de copy.

```text
eventos_resgate_qualify
    ↓
agregação por canal e tipo_comunicacao (taxa_abertura, taxa_clique, taxa_conversao, custo_total, receita_gerada)
    ↓
join com carrinhos_qualify (valor_total_recuperado)
    ↓
fct_campanhas_resgate / view_performance_roi_resgate (Curated Gold)
```

## Classificação por Camada

| Camada | Ativo | Característica |
|---|---|---|
| Raw / Bronze | `raw_eventos_resgate` (`/raw/recuperacao_carrinho/resgate.parquet`) | Logs brutos de envio e webhooks de marketing preservados da origem |
| Qualify / Silver | `qualify_eventos_resgate` (`CART_RECOVERY.EVENTOS_RESGATE`) | Dados de campanhas tipados, sanitizados e validados com integridade relacional |
| Anomaly / Silver | `eventos_resgate_anomalies` (`CART_RECOVERY.EVENTOS_RESGATE_ANOMALIES`) | Repositório de evidências, dead-letter e alertas de desvio de engajamento |
| Curated / Gold | `fct_campanhas_resgate`, `view_performance_roi_resgate` | Dados agregados em métricas de ROI e eficácia de marketing para BI |

## Lineage

### Upstream

```text
CRM Engine / Email Gateway (SendGrid) / SMS & WhatsApp API (Twilio)
    ↓
/raw/recuperacao_carrinho/resgate.parquet (Bronze)
```

### Qualification & Risk Routing (Transformation)

```text
raw_eventos_resgate
        ↓
Eventos de Resgate Data Quality & Anomaly Detection Pipeline
        │
        ├── Registros válidos
        │       ↓
        │   eventos_resgate_qualify
        │
        └── Registros inválidos/anômalos
                ↓
            eventos_resgate_anomalies
```

### Downstream

```text
eventos_resgate_qualify
        ↓
Curated / Gold
        ↓
├── BI / Dashboard de ROI de Recuperação
├── CRM / Painel de Eficácia de Canais
├── Data App de Cart Recovery
├── Algoritmos de Otimização de Copy & Horário
└── Agentes de IA

eventos_resgate_anomalies
        ↓
├── Data Quality Dashboard
├── Alertas de Integração de Webhooks
└── Aplicação / Time de CRM
```

---

# 4. Governance & Consumption

## Governança

- **Owner:** Squad de CRM Marketing & Growth Analytics (`growth-crm@marketplace.com`)
- **Classificação:** Interno
- **PII:** Não (contém metadados de mensageria, identificadores relacionais e valores financeiros sem exposição de dados pessoais diretos)
- **Tags:**
  - `eventos_resgate`
  - `campanhas`
  - `roi`
  - `mensageria`
  - `silver`
  - `cart_recovery`

## Consumidores

- **CRM & Automação de Marketing:** Acompanhamento do ciclo de vida dos disparos e cancelamento de réguas ativas pós-conversão.
- **Analytics & BI:** Relatórios executivos de ROI por canal, taxa de conversão por template e análise de custo de aquisição/resgate (CAC/Recovery).
- **Data App de Cart Recovery:** Monitoramento em tempo real do status das mensagens enviadas para cada carrinho.
- **Modelos Preditivos & Agentes de IA:** Algoritmos de aprendizado por reforço para seleção dinâmica do melhor canal e horário para cada perfil de cliente.
- **Sistemas de Domínio & Engenharia de Mensageria:** Consumo de `eventos_resgate_anomalies` para auditoria de falhas de entrega de webhooks.

## Observações

- O modelo calcula o ROI financeiro na camada de consumo a partir da composição de `valor_pedido_final`, `desconto_oferecido` e `custo_envio`.
- A chave primária `BIGINT` suporta grande escala de disparos multicanal ao longo dos ciclos sazonais do e-commerce.
- O artefato `eventos_resgate_anomalies` assegura rastreabilidade das falhas de webhook sem corromper a apuração contábil das campanhas convertidas.
