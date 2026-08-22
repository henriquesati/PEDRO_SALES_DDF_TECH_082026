# Entidade: `carrinhos`

---

# 1. Data Definition

> Define a estrutura dos dados, seus tipos, chaves, atributos e significados técnicos.

## Atributos / Data Dictionary

| Campo | Tipo | PK/FK | Nullable | Default | Descrição | Valores / Regras | Exemplo |
|---|---|---|---|---|---|---|---|
| `carrinho_id` | INT | PK | Não | AUTO | Identificador único exclusivo da sessão do carrinho | Inteiro sequencial único positivo | `1001` |
| `cliente_id` | INT | FK | Não | — | Identificador do cliente proprietário do carrinho | Deve existir na tabela `clientes` | `42` |
| `data_criacao` | TIMESTAMPTZ | — | Não | NOW() | Timestamp exato em que o carrinho foi inicializado | Data/hora UTC válida | `2026-03-15 14:23:10+00` |
| `data_ultima_atividade` | TIMESTAMPTZ | — | Sim | — | Timestamp da última interação (adição/remoção/checkout) | `>= data_criacao` | `2026-03-15 14:45:00+00` |
| `data_abandono` | TIMESTAMPTZ | — | Sim | — | Timestamp em que a inatividade foi classificada como abandono | `>= data_criacao` | `2026-03-15 15:15:00+00` |
| `status` | VARCHAR(20) | — | Não | `'ativo'` | Estado atual do carrinho no ciclo de vida | `'ativo'`, `'abandonado'`, `'recuperado'`, `'comprado'`, `'expirado'` | `'abandonado'` |
| `motivo_abandono` | VARCHAR(100) | — | Sim | — | Causa diagnosticada ou informada para o abandono | `'preco'`, `'frete'`, `'pagamento'`, `'indecisao'`, `'estoque'`, `'nao_informado'` | `'frete'` |
| `valor_subtotal` | DECIMAL(10,2) | — | Sim | `0.00` | Soma dos valores unitários dos itens sem frete e sem desconto | `>= 0.00` | `249.90` |
| `valor_frete` | DECIMAL(10,2) | — | Sim | `0.00` | Custo de frete calculado para a entrega | `>= 0.00` | `25.50` |
| `valor_desconto` | DECIMAL(10,2) | — | Sim | `0.00` | Valor de abatimento promocional ou cupom aplicado | `>= 0.00` | `20.00` |
| `valor_total` | DECIMAL(10,2) | — | Sim | `0.00` | Valor líquido total (`subtotal + frete - desconto`) | `>= 0.00` | `255.40` |
| `duracao_sessao_minutos` | INT | — | Sim | — | Duração total da sessão de navegação em minutos | Inteiro `>= 0` | `22` |
| `dispositivo` | VARCHAR(50) | — | Sim | — | Tipo de dispositivo utilizado na sessão | `'mobile'`, `'desktop'`, `'tablet'` | `'mobile'` |
| `browser` | VARCHAR(50) | — | Sim | — | Navegador web ou aplicativo utilizado | `'Chrome'`, `'Safari'`, `'Firefox'`, `'Edge'` | `'Chrome'` |
| `canal_origem` | VARCHAR(100) | — | Sim | — | Canal de aquisição ou origem do tráfego | `'google'`, `'facebook'`, `'direct'`, `'email'`, `'instagram'` | `'google'` |
| `cliente_novo` | BOOLEAN | — | Não | `FALSE` | Indica se o cliente está realizando sua primeira compra | `TRUE` / `FALSE` | `TRUE` |
| `tem_conta_criada` | BOOLEAN | — | Não | `FALSE` | Indica se o cliente possui cadastro formal (vs. guest) | `TRUE` / `FALSE` | `TRUE` |
| `created_at` | TIMESTAMPTZ | — | Não | NOW() | Timestamp de auditoria de inserção do registro | Data/hora UTC | `2026-03-15 14:23:10+00` |
| `updated_at` | TIMESTAMPTZ | — | Não | NOW() | Timestamp de auditoria da última atualização do registro | Data/hora UTC | `2026-03-15 15:15:00+00` |

### Foreign Keys

```text
carrinhos.cliente_id
    → clientes.cliente_id
```

---

# 2. Business Definition & Business Rules

## Identificação e Visão de Negócio

- **Nome físico:** `carrinhos` (Snowflake: `CART_RECOVERY.CARRINHOS`)
- **Nome de negócio:** Carrinhos de Compras (Sessões Transacionais)
- **Domínio:** Recuperação de Carrinhos Abandonados / Marketplace E-commerce
- **Tipo:** Fato Transacional / Fato de Ciclo de Vida (Lifecycle Fact)
- **Descrição:** Tabela central do domínio. Representa cada sessão de carrinho de compras criada no marketplace, rastreando seu ciclo de vida completo desde a inicialização até o abandono, recuperação ou conversão direta em pedido.
- **Objetivo de negócio:** Centralizar a jornada transacional do cliente para identificar pontos de atrito no checkout, acionar réguas inteligentes de recuperação de receita e alimentar a camada analítica com métricas de conversão e abandono.
- **Casos de uso:**
  - Filtrar e segmentar carrinhos com status `'abandonado'` para disparar campanhas de resgate via CRM, WhatsApp e E-mail.
  - Calcular KPIs operacionais: taxa de abandono, taxa de recuperação, tempo médio até o abandono e ticket médio.
  - Avaliar o impacto e ROI de incentivos promocionais (cupons/descontos de resgate) na margem final.
  - Alimentar modelos preditivos e agentes autônomos de propensão de conversão e clustering de clientes.

## Granularidade

- **Granularidade:** Uma linha por sessão única de carrinho de compras criada por um cliente no marketplace.
- **Regra:** `1 linha = 1 carrinho criado`

## Papel no Domínio

- Atua como a **entidade âncora** de todo o ecossistema de Cart Recovery.
- Conecta a intenção de navegação (`eventos_carrinho`), os produtos de interesse (`itens_carrinho`), os perfis cadastrais (`clientes`), as tentativas de reativação (`eventos_resgate`) e a efetivação da venda (`pedidos`).

## Relacionamentos

| Entidade relacionada | Cardinalidade | Relacionamento |
|---|---:|---|
| `clientes` | N:1 | Cada carrinho pertence a exatamente um cliente |
| `itens_carrinho` | 1:N | Um carrinho contém um ou múltiplos itens adicionados |
| `eventos_carrinho` | 1:N | Um carrinho gera múltiplos eventos de telemetria e interação |
| `eventos_resgate` | 1:N | Um carrinho abandonado pode receber múltiplas comunicações de resgate |
| `pedidos` | 1:1 | Um carrinho convertido ou recuperado origina um pedido de venda |

## Ciclo de Vida

```text
ativo → abandonado → recuperado → comprado
  │                                   ↑
  └───────────────────────────────────┘ (compra direta)

abandonado → expirado (após 90 dias sem interação)
```

### Estados

| Status | Significado |
|---|---|
| `ativo` | Carrinho em aberto e sessão em andamento pelo cliente no marketplace |
| `abandonado` | Sessão interrompida sem checkout concluído após a janela de tolerância (30 min) |
| `recuperado` | Carrinho reaberto e reativado através de uma ação/campanha de resgate |
| `comprado` | Transação concluída com sucesso e convertida em pedido de venda |
| `expirado` | Carrinho abandonado há mais de 90 dias, encerrando ações de marketing |

## BUSINESS RULES

### 01 — Critério de Detecção de Abandono
Um carrinho com status `'ativo'` que permanece sem nenhuma nova interação (`data_ultima_atividade`) por mais de 30 minutos, sem conclusão de compra, deve ter seu status atualizado para `'abandonado'`, marcando o timestamp em `data_abandono`.

### 02 — Consistência da Equação Contábil
O `valor_total` deve obrigatoriamente satisfazer a relação matemática:
$$\text{valor\_total} = \max(0, \text{valor\_subtotal} + \text{valor\_frete} - \text{valor\_desconto})$$
Fretes com valores negativos ou descontos superiores ao subtotal devem ser sanitizados e corrigidos antes da disponibilização nas camadas de consumo.

### 03 — Elegibilidade para Disparo de Resgate
São elegíveis para a esteira de reativação de marketing apenas os registros com:
- `status = 'abandonado'`
- `valor_total > 0`
- `cliente_id` válido e vinculado a canal de contato
- Intervalo entre `NOW()` e `data_abandono` inferior a 90 dias

### 04 — Expiração de Carrinhos Inativos
Carrinhos no estado `'abandonado'` que atingem 90 dias sem retorno, interação ou resgate bem-sucedido devem transicionar automaticamente para o estado `'expirado'`, cessando disparos de comunicação.

### 05 — Atribuição de Recuperação
Quando um carrinho com histórico de abandono gera um pedido confirmado por intermédio de um link de resgate, seu status evolui para `'recuperado'` (e subsequentemente `'comprado'`), registrando a atribuição para cálculo de ROI da campanha.

---

# 3. Data Quality, Transformation & Lineage

> Define como a entidade é validada, transformada e movimentada entre as camadas do pipeline.

## Validação

As regras de integridade, restrições e higienização são estruturadas como funções declarativas que compõem o pipeline de validação e qualidade dos dados:

### 01 — `validar_pk_carrinho_id(carrinho_id)`
Valida se o identificador `carrinho_id` é único, positivo e não nulo (`NOT NULL & UNIQUE`). Rejeita registros duplicados ou sem chave primária.

### 02 — `validar_fk_cliente(cliente_id)`
Valida se o `cliente_id` existe previamente na tabela `clientes`. Garante a integridade referencial entre o carrinho e o consumidor cadastrado.

### 03 — `validar_campos_obrigatorios(cliente_id, data_criacao, status, cliente_novo, tem_conta_criada, created_at, updated_at)`
Garante que todos os atributos mandatários não contenham valores nulos (`IS NOT NULL`).

### 04 — `validar_dominio_status(status)`
Verifica se o `status` informado pertence ao domínio enum válido: `{'ativo', 'abandonado', 'recuperado', 'comprado', 'expirado'}`. Registros com status desconhecido disparam alerta de schema drift.

### 05 — `validar_dominio_dispositivo(dispositivo)`
Assegura que o tipo de dispositivo seja padronizado em `{'mobile', 'desktop', 'tablet'}` ou nulo. Aplica fallback ou enriquecimento caso venha de user-agent bruto.

### 06 — `validar_dominio_motivo_abandono(motivo_abandono)`
Valida se a causa registrada de abandono está contida no domínio `{'preco', 'frete', 'pagamento', 'indecisao', 'estoque', 'nao_informado'}`.

### 07 — `validar_dominio_canal_origem(canal_origem)`
Valida se o canal de aquisição de tráfego é reconhecido entre `{'google', 'facebook', 'direct', 'email', 'instagram'}`.

### 08 — `sanitizar_valor_frete(valor_frete)`
Garante a não-negatividade do frete (`valor_frete >= 0.00`). Caso venha negativo por dirty data da origem transacional, encaminha a evidência bruta para a tabela de anomalias da plataforma.

### 09 — `sanitizar_valor_desconto(valor_desconto, valor_subtotal)`
Valida que o desconto seja não-negativo (`valor_desconto >= 0.00`) e não exceda o `valor_subtotal`. Discrepâncias geram registro no artefato de anomalias.

### 11 — `validar_duracao_sessao(duracao_sessao_minutos)`
Valida que o tempo de permanência seja um valor inteiro maior ou igual a zero (`duracao_sessao_minutos >= 0`).

### 12 — `validar_consistencia_temporal(data_criacao, data_ultima_atividade, data_abandono, created_at, updated_at)`
Assegura que as marcas temporais obedeçam à ordem cronológica dos eventos: `data_ultima_atividade >= data_criacao`, `data_abandono >= data_criacao` e `updated_at >= created_at`.

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
 ├── [Registros Válidos/Higienizados] ──→ carrinhos_qualify (Silver Qualify)
 └── [Inconsistências Detectadas]    ──→ carrinhos_anomalies (Silver Anomaly)
```

### Raw → Qualify

Ingestão dos arquivos brutos transacionais (CSV/Parquet), execução de casting de tipos para padrões analíticos (TIMESTAMPTZ, DECIMAL), normalização de strings de domínio, deduplicação e validação de chaves relacionais.

```text
carrinhos_raw
→ validar_schema_e_tipagem
→ extrair_e_rotear_anomalias (envia evidências para carrinhos_anomalies)
→ sanitizar_frete_negativo
→ recalcular_valor_total
→ validar_dominio_status_e_dispositivo
→ validar_integridade_fk_cliente
→ deduplicar_carrinho_id
→ carrinhos_qualify
```

### Raw → Anomaly

Mecanismo de captura, classificação e registro de desvios que representam risco operacional ou financeiro. A plataforma preserva o payload bruto original para auditoria e tomada de decisão pelo time/aplicação responsável.

```text
carrinhos_raw
    ↓
[Motor de Detecção e Classificação de Anomalias]
    ├── ANOM-01: Frete Negativo (valor_frete < 0)
    ├── ANOM-02: Preço/Subtotal Negativo ou Zerado (valor_subtotal <= 0)
    ├── ANOM-03: Desconto Abusivo/Excessivo (valor_desconto > valor_subtotal ou < 0)
    └── ANOM-04: Divergência Contábil no Total (valor_total != subtotal + frete - desconto)
    ↓
carrinhos_anomalies (Repositório de Evidências & Alertas da Plataforma)
```

#### Regras de Anomalia de Negócio

| Código | Regra de Anomalia | Severidade | Risco de Negócio | Ação do Pipeline |
|---|---|:---:|---|---|
| `ANOM-01` | `valor_frete < 0.00` | `ALTA` | Risco financeiro de subfaturamento no checkout e prejuízo logístico | Encaminha evidência para Anomaly |
| `ANOM-02` | `valor_subtotal <= 0.00` | `CRÍTICA` | Bug no catálogo de preços, fraude de produto gratuito ou erro de payload | Encaminha evidência para Anomaly |
| `ANOM-03` | `valor_desconto > valor_subtotal` ou `< 0.00` | `CRÍTICA` | Exploit de cupons cumulativos indevidos ou valor líquido negativo | Encaminha evidência para Anomaly |
| `ANOM-04` | `abs(valor_total - (subtotal + frete - desconto)) > 0.01` | `ALTA` | Falha de conciliação fiscal e divergência contábil de checkout | Encaminha evidência para Anomaly |

#### Estrutura do Artefato de Anomalias (`carrinhos_anomalies`)

A estrutura do artefato reflete as atribuições estritas da plataforma de dados (detecção, classificação e evidência):

| Campo | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `anomaly_id` | VARCHAR / UUID | Identificador exclusivo do evento de anomalia | `anom-8f3a1b2c-901e` |
| `carrinho_id` | INT | Identificador do carrinho afetado | `1042` |
| `cliente_id` | INT | Identificador do cliente proprietário | `42` |
| `codigo_anomalia` | VARCHAR(20) | Código identificador da regra violada (`ANOM-01` a `ANOM-04`) | `ANOM-01` |
| `severidade` | VARCHAR(10) | Grau de risco atribuído: `'CRITICA'`, `'ALTA'`, `'MEDIA'`, `'BAIXA'` | `ALTA` |
| `descricao_risco` | VARCHAR(255) | Diagnóstico descritivo do problema identificado | `Frete com valor negativo detectado (-15.50), gerando risco logístico` |
| `payload_raw` | TEXT / JSON | Snapshot fiel do registro bruto recebido da camada Raw | `{"carrinho_id": 1042, "valor_frete": -15.50, "valor_subtotal": 120.00, "valor_total": 104.50}` |
| `detected_at` | TIMESTAMPTZ | Timestamp de auditoria da detecção do desvio pela plataforma | `2026-03-15 14:25:00+00` |

### Qualify → Curated

Enriquecimento dos dados do carrinho com atributos comportamentais de clientes (segmento RFM, LTV), consolidação volumétrica de itens adicionados a partir de `itens_carrinho`, cruzamento com telemetria de resgate para cômputo de tempo de reação e publicação das views analíticas orientadas a BI e aplicações de IA.

```text
carrinhos_qualify
    ↓
join com clientes_qualify (segmento_rfm, score_engajamento)
    ↓
join agregado com itens_carrinho_qualify (total_skus, categorias_predominantes)
    ↓
join com eventos_resgate_qualify (canal_resgate, status_envio, taxa_sucesso)
    ↓
dim_carrinhos / fct_recuperacao_carrinho (Curated Gold)
```

## Classificação por Camada

| Camada | Ativo | Característica |
|---|---|---|
| Raw / Bronze | `raw_carrinhos` (`/raw/recuperacao_carrinho/carrinhos.parquet`) | Dados brutos preservados diretamente da origem transacional |
| Qualify / Silver | `qualify_carrinhos` (`CART_RECOVERY.CARRINHOS`) | Dados tipados, deduplicados, sanitizados e validados com integridade relacional |
| Anomaly / Silver | `carrinhos_anomalies` (`CART_RECOVERY.CARRINHOS_ANOMALIES`) | Repositório de evidências, dead-letter e alertas de qualidade para atuação do domínio |
| Curated / Gold | `dim_carrinhos`, `fct_recuperacao_carrinho`, `view_carrinhos_resgate` | Dados modelados dimensionalmente, enriquecidos e prontos para consumo analítico e operacional |

## Lineage

### Upstream

```text
E-commerce Platform / Checkout API / Session Tracker
    ↓
/raw/recuperacao_carrinho/carrinhos.parquet (Bronze)
```

### Qualification & Risk Routing (Transformation)

```text
raw_carrinhos
        ↓
Carrinhos Data Quality & Anomaly Detection Pipeline
        │
        ├── Registros válidos
        │       ↓
        │   carrinhos_qualify
        │
        └── Registros inválidos/anômalos
                ↓
            carrinhos_anomalies
```

### Downstream

```text
carrinhos_qualify
        ↓
Curated / Gold
        ↓
├── BI / Analytics
├── CRM / Marketing
├── Data App
├── ML
└── Agentes de IA

carrinhos_anomalies
        ↓
├── Data Quality Dashboard
├── Alertas de Engenharia
└── Aplicação / Domínio
```

# 4. Governance & Consumption

## Governança

- **Owner:** Engenharia de Dados & Squad de Growth / E-commerce Analytics (`data-engineering@marketplace.com`)
- **Classificação:** Interno
- **PII:** Não (contém identificadores numéricos e métricas transacionais sem exposição direta de dados sensíveis como CPF ou e-mail)
- **Tags:**
  - `carrinho_abandonado`
  - `carrinhos`
  - `transacional`
  - `lifecycle`
  - `silver`
  - `anomalias`
  - `cart_recovery`

## Consumidores

- **CRM & Automação de Mensageria:** Disparos de réguas de resgate via WhatsApp, E-mail e Push.
- **Analytics & BI:** Dashboards gerenciais de conversão, abandono por categoria, dispositivo e canal de aquisição.
- **Data App de Recuperação:** Aplicação operacional para acompanhamento em tempo real de carrinhos abandonados e acionamento manual/automático.
- **Modelos Preditivos & Agentes de IA:** Algoritmos de recomendação de cupons dinâmicos e predição de propensão ao churn/abandono.
- **Sistemas de Domínio & Resolução de Fraudes:** Consumo de `carrinhos_anomalies` para decisões operacionais de negócio sobre pedidos e carrinhos inconsistentes.

## Observações

- A marcação de `data_abandono` é acionada por job analítico/stream após a expiração do timeout de 30 minutos de inatividade da sessão.
- O campo `valor_total` é persistido explicitamente (não apenas computado em runtime) para garantir consistência contábil e auditoria financeira de cupons aplicados.
- As flags `cliente_novo` e `tem_conta_criada` foram desenhadas para permitir segmentações de alta performance nas réguas de comunicação sem a necessidade de joins complexos em tempo real.
- O artefato de anomalias (`carrinhos_anomalies`) preserva o dado bruto com foco estrito em detecção, classificação e evidência, delegando a decisão e resolução para a camada da aplicação/domínio.
