# Entidade: `pedidos`

---

# 1. Data Definition

> Define a estrutura dos dados, seus tipos, chaves, atributos e significados técnicos.

## Atributos / Data Dictionary

| Campo | Tipo | PK/FK | Nullable | Default | Descrição | Valores / Regras | Exemplo |
|---|---|---|---|---|---|---|---|
| `pedido_id` | INT | PK | `FALSE` | AUTO | Identificador único exclusivo da ordem de pedido finalizada | Inteiro sequencial único positivo | `2001` |
| `carrinho_id` | INT | FK, UK | `FALSE` | — | Identificador do carrinho original de compra (relação 1:1) | Deve existir na tabela `carrinhos` e ser único | `1001` |
| `cliente_id` | INT | FK | `FALSE` | — | Identificador do cliente comprador titular da transação | Deve existir na tabela `clientes` | `42` |
| `data_pedido` | TIMESTAMPTZ | — | `FALSE` | NOW() | Timestamp oficial de confirmação e checkout do pedido | Data/hora UTC válida `>= carrinhos.data_criacao` | `2026-03-15 17:05:00+00` |
| `valor_subtotal` | DECIMAL(10,2) | — | `FALSE` | — | Soma dos valores unitários dos itens adquiridos | DECIMAL `>= 0.00` | `249.90` |
| `valor_frete` | DECIMAL(10,2) | — | `FALSE` | `0.00` | Custo de entrega cobrado na liquidação do pedido | DECIMAL `>= 0.00` | `0.00` |
| `valor_desconto` | DECIMAL(10,2) | — | `FALSE` | `0.00` | Total de descontos e abatimentos aplicados | DECIMAL `>= 0.00` | `25.00` |
| `valor_total` | DECIMAL(10,2) | — | `FALSE` | — | Valor líquido final pago (`subtotal + frete - desconto`) | DECIMAL `> 0.00` | `224.90` |
| `metodo_pagamento` | VARCHAR(50) | — | `TRUE` | — | Meio de liquidação financeira utilizado na transação | `'cartao_credito'`, `'cartao_debito'`, `'boleto'`, `'pix'` | `'pix'` |
| `status_pedido` | VARCHAR(20) | — | `FALSE` | `'confirmado'` | Situação corrente do pedido na esteira de atendimento | `'confirmado'`, `'enviado'`, `'entregue'`, `'cancelado'` | `'confirmado'` |
| `origem_recuperacao` | BOOLEAN | — | `FALSE` | `FALSE` | Flag indicando se a compra resultou de ação de resgate | `TRUE` / `FALSE` | `TRUE` |
| `resgate_id` | BIGINT | FK | `TRUE` | — | Identificador da campanha de resgate que converteu a venda | Deve existir em `eventos_resgate` (se recuperado) | `3001` |
| `created_at` | TIMESTAMPTZ | — | `FALSE` | NOW() | Timestamp de auditoria de inserção do registro | Data/hora UTC | `2026-03-15 17:05:00+00` |

### Foreign Keys

```text
pedidos.carrinho_id
    → carrinhos.carrinho_id (1:1, UNIQUE)

pedidos.cliente_id
    → clientes.cliente_id

pedidos.resgate_id
    → eventos_resgate.resgate_id (opcional)
```

## SCHEMA RULES

### 01 — Unicidade e Não-Nulidade da Chave Primária e Chave de Carrinho (PK/UK)
- `pedido_id`: chave primária inteira sequencial auto-incremental (`INT PRIMARY KEY`), obrigatória (`NOT NULL`) e exclusiva (`UNIQUE`).
- `carrinho_id`: chave estrangeira única (`INT NOT NULL UNIQUE`), impondo restrição estrita de 1:1 onde cada carrinho aberto gera no máximo um pedido liquidado.

### 02 — Integridade Referencial (FKs)
- `carrinho_id INT NOT NULL` referencia `carrinhos(carrinho_id)` com política `ON DELETE RESTRICT`.
- `cliente_id INT NOT NULL` referencia `clientes(cliente_id)` com política `ON DELETE RESTRICT`.
- `resgate_id BIGINT` referencia `eventos_resgate(resgate_id)` com política `ON DELETE SET NULL`.

### 03 — Restrições de Domínio, Tipagem e Precisão Numérica (CHECK Constraints)
- `status_pedido`: tipado como `VARCHAR(20)` com restrição `CHECK (status_pedido IN ('confirmado', 'enviado', 'entregue', 'cancelado'))`.
- `metodo_pagamento`: tipado como `VARCHAR(50)` com restrição `CHECK (metodo_pagamento IN ('cartao_credito', 'cartao_debito', 'boleto', 'pix') OR metodo_pagamento IS NULL)`.
- `valor_subtotal`, `valor_frete`, `valor_desconto`: tipados como `DECIMAL(10,2)` com restrição `CHECK (valor >= 0.00)`.
- `valor_total`: tipado como `DECIMAL(10,2)` com restrição `CHECK (valor_total > 0.00)`.

### 04 — Nulabilidade e Valores Padrão (Defaults)
- **Campos Obrigatórios (NOT NULL)**: `pedido_id`, `carrinho_id`, `cliente_id`, `data_pedido`, `valor_subtotal`, `valor_frete`, `valor_desconto`, `valor_total`, `status_pedido`, `origem_recuperacao`, `created_at`.
- **Valores Padrão**: `valor_frete = 0.00`, `valor_desconto = 0.00`, `status_pedido = 'confirmado'`, `origem_recuperacao = FALSE`, `data_pedido = NOW()`, `created_at = NOW()`.

---

# 2. Business Definition & Business Rules

## Identificação e Visão de Negócio

- **Nome físico:** `pedidos` (Snowflake: `CART_RECOVERY.PEDIDOS`)
- **Nome de negócio:** Pedidos Confirmados & Conversões de Checkout
- **Domínio:** Vendas, Faturamento & Conversão / Marketplace E-commerce
- **Tipo:** Fato Transacional de Conversão (Checkout & Conversion Transaction Fact)
- **Descrição:** Entidade financeira que consolida todas as compras efetivadas no marketplace, fechando formalmente o ciclo transacional carrinho $\rightarrow$ pedido e permitindo apurar a receita convertida de forma direta ou atribuída a campanhas de recuperação.
- **Objetivo de negócio:** Centralizar as métricas de faturamento líquido e bruto, mensurar a taxa real de conversão do funil de e-commerce, alimentar a apuração de ROI das réguas de marketing e rastrear os meios de pagamento preferidos em compras recuperadas.
- **Casos de uso:**
  - Medir a receita líquida e o volume de pedidos convertidos a partir de campanhas de resgate (`origem_recuperacao = TRUE`).
  - Analisar a distribuição e o share de meios de pagamento (`pix`, `cartao_credito`, `boleto`) em compras diretas vs. compras recuperadas.
  - Conciliar os valores cobrados de frete e descontos promocionais aplicados durante o checkout.
  - Atualizar os indicadores de valor acumulado (LTV) e frequência de compra dos clientes cadastrados.

## Granularidade

- **Granularidade:** Uma linha por ordem de compra confirmada e aprovada pelo gateway de pagamento no marketplace.
- **Regra:** `1 linha = 1 pedido de venda confirmado`

## Papel no Domínio

- Atua como a **entidade de fechamento financeiro** de todo o ecossistema de Cart Recovery.
- Conecta a intenção de compra de `carrinhos`, o histórico cadastral de `clientes` e a eficácia de marketing de `eventos_resgate`.

## Relacionamentos

| Entidade relacionada | Cardinalidade | Relacionamento |
|---|---:|---|
| `carrinhos` | 1:1 | Cada pedido pertence a exatamente um carrinho de compras de origem |
| `clientes` | N:1 | Cada pedido pertence ao cliente cadastrado que efetuou o pagamento |
| `eventos_resgate` | 1:1 (opcional) | Pedidos recuperados por campanha vinculam-se ao respectivo disparo de resgate |

## Ciclo de Vida do Pedido

```text
[confirmado] ──→ [enviado] ──→ [entregue]
      │
      └──(estorno / cancelamento)──→ [cancelado]
```

### Estados do Pedido

| Status | Significado de Negócio |
|---|---|
| `confirmado` | Pagamento aprovado pelo gateway financeiro e ordem de pedido gerada |
| `enviado` | Produtos despachados pelo centro de distribuição com código de rastreio |
| `entregue` | Mercadoria entregue com sucesso no endereço do comprador |
| `cancelado` | Pedido cancelado por solicitação do cliente, fraude ou estorno de pagamento |

## BUSINESS RULES

### 01 — Unicidade de Conversão de Carrinho (Relação 1:1)
Cada sessão de carrinho de compras pode originar no máximo um único pedido confirmado no sistema. A coluna `carrinho_id` possui constraint de unicidade (`UNIQUE`), impedindo a criação de pedidos duplicados para o mesmo carrinho.

### 02 — Fechamento da Equação Contábil do Pedido
O valor final do pedido deve obrigatoriamente satisfazer a fórmula de faturamento líquido:
$$\text{valor\_total} = \text{valor\_subtotal} + \text{valor\_frete} - \text{valor\_desconto}$$
Pedidos com `valor_total <= 0.00` ou divergências superiores a R$ 0.01 em relação aos componentes de frete/desconto representam anomalia contábil e devem ser auditados.

### 03 — Atribuição Mandatária de Resgate
Se um pedido for marcado como originado de recuperação (`origem_recuperacao = TRUE`), o campo `resgate_id` deve ser obrigatoriamente preenchido com a chave da campanha correspondente e `carrinhos.status` deve transicionar para `'recuperado'` (e subsequentemente `'comprado'`). Se `origem_recuperacao = FALSE`, `resgate_id` deve ser `NULL`.

### 04 — Consistência Temporal de Liquidação
O timestamp `data_pedido` deve ser sempre contemporâneo ou posterior à criação do carrinho (`carrinhos.data_criacao`). Em pedidos recuperados por campanha, `data_pedido` deve ser posterior ou igual a `eventos_resgate.data_envio`.

### 05 — Atualização de Métricas Acumuladas do Cliente (LTV)
A liquidação de um pedido com status `'confirmado'` aciona a atualização dos agregados em `clientes`:
- Incremento de `clientes.total_compras` (+1).
- Adição de `valor_total` em `clientes.lifetime_value`.
- Atualização de `clientes.data_ultima_compra` com a data do pedido.

---

# 3. Data Quality, Transformation & Lineage

> Define como a entidade é validada, transformada e movimentada entre as camadas do pipeline.

## Validação

As regras de integridade, restrições e higienização são estruturadas como funções declarativas que compõem o pipeline de validação e qualidade dos dados:

### 01 — `validar_pk_pedido_id(pedido_id)`
Valida se o identificador `pedido_id` é único, positivo e não nulo (`NOT NULL & UNIQUE`).

### 02 — `validar_uk_carrinho_id(carrinho_id)`
Garante a unicidade da chave `carrinho_id`, assegurando a cardinalidade estrita 1:1.

### 03 — `validar_fks_pedido(carrinho_id, cliente_id, resgate_id)`
Valida a existência prévia de `carrinho_id` em `carrinhos`, `cliente_id` em `clientes` e `resgate_id` em `eventos_resgate` (se preenchido).

### 04 — `validar_campos_obrigatorios(pedido_id, carrinho_id, cliente_id, data_pedido, valor_subtotal, valor_frete, valor_desconto, valor_total, status_pedido, origem_recuperacao, created_at)`
Garante que todos os atributos mandatários estejam preenchidos (`IS NOT NULL`).

### 05 — `validar_equacao_valor_total(valor_subtotal, valor_frete, valor_desconto, valor_total)`
Valida se `abs(valor_total - (valor_subtotal + valor_frete - valor_desconto)) <= 0.01` e se `valor_total > 0.00`.

### 06 — `validar_coerencia_origem_resgate(origem_recuperacao, resgate_id)`
Valida se `origem_recuperacao = TRUE` implica `resgate_id IS NOT NULL`, e se `origem_recuperacao = FALSE` implica `resgate_id IS NULL`.

### 07 — `validar_consistencia_temporal_pedido(data_pedido, carrinhos_data_criacao)`
Assegura que `data_pedido >= carrinhos_data_criacao`.

## Pipeline de Transformação

O pipeline estabelece uma **fronteira arquitetural clara entre a Plataforma de Dados e a Aplicação/Domínio**:
- **Papel da Plataforma de Dados**: Ingerir dados de liquidação financeira (ERP/Checkout API), validar equações contábeis, conciliar atribuição de resgate e isolar desvios em `pedidos_anomalies`.
- **Papel da Aplicação / Domínio**: Consumir os eventos de anomalia e executar as decisões de resolução (conciliação financeira, reprocessamento fiscal ou ajuste de estorno).

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
 ├── [Registros Válidos/Higienizados] ──→ pedidos_qualify (Silver Qualify)
 └── [Inconsistências Detectadas]    ──→ pedidos_anomalies (Silver Anomaly)
```

### Raw → Qualify

Ingestão dos registros de pedidos brutos (CSV/Parquet), casting de tipos para padrões analíticos (DECIMAL, TIMESTAMPTZ), validação de integridade referencial, conciliação de descontos e deduplicação de chaves.

```text
pedidos_raw
→ validar_schema_e_tipagem
→ extrair_e_rotear_anomalias (envia evidências para pedidos_anomalies)
→ validar_fks_carrinho_cliente_resgate
→ validar_equacao_contabil_total
→ validar_consistencia_atribuicao_resgate
→ validar_consistencia_temporal
→ deduplicar_pedido_id_e_carrinho_id
→ pedidos_qualify
```

### Raw → Anomaly

Mecanismo de captura, classificação e registro de divergências fiscais, valores totais inválidos ou inconsistências de atribuição de campanha. A plataforma preserva o payload bruto original para auditoria e governança.

```text
pedidos_raw
    ↓
[Motor de Detecção e Classificação de Anomalias]
    ├── ANOM-01: Divergência Contábil de Total (valor_total != subtotal + frete - desconto)
    ├── ANOM-02: Valor Total Zerado ou Negativo (valor_total <= 0)
    ├── ANOM-03: Divergência de Atribuição de Resgate (origem_recuperacao != (resgate_id IS NOT NULL))
    └── ANOM-04: Inversão Temporal de Pedido (data_pedido < carrinhos.data_criacao)
    ↓
pedidos_anomalies (Repositório de Evidências & Alertas da Plataforma)
```

#### Regras de Anomalia de Negócio

| Código | Regra de Anomalia | Severidade | Risco de Negócio | Ação do Pipeline |
|---|---|:---:|---|---|
| `ANOM-01` | `abs(valor_total - (valor_subtotal + valor_frete - valor_desconto)) > 0.01` | `CRÍTICA` | Divergência contábil no faturamento e falha de conciliação fiscal | Encaminha evidência para Anomaly |
| `ANOM-02` | `valor_total <= 0.00` | `CRÍTICA` | Venda com valor nulo ou prejuízo por exploit de cupom | Encaminha evidência para Anomaly |
| `ANOM-03` | `(origem_recuperacao = TRUE AND resgate_id IS NULL)` ou `(origem_recuperacao = FALSE AND resgate_id IS NOT NULL)` | `ALTA` | Distorção nas métricas de ROI de campanhas de resgate | Encaminha evidência para Anomaly |
| `ANOM-04` | `data_pedido < carrinhos.data_criacao` | `ALTA` | Inversão cronológica e falha de sincronização de relógio de transação | Encaminha evidência para Anomaly |

#### Estrutura do Artefato de Anomalias (`pedidos_anomalies`)

A estrutura do artefato reflete as atribuições estritas da plataforma de dados (detecção, classificação e evidência):

| Campo | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `anomaly_id` | VARCHAR / UUID | Identificador exclusivo do evento de anomalia | `anom-2d9a4b8c-103e` |
| `pedido_id` | INT | Identificador do pedido afetado | `2042` |
| `carrinho_id` | INT | Identificador do carrinho associado | `1001` |
| `cliente_id` | INT | Identificador do cliente associado | `42` |
| `codigo_anomalia` | VARCHAR(20) | Código identificador da regra violada (`ANOM-01` a `ANOM-04`) | `ANOM-01` |
| `severidade` | VARCHAR(10) | Grau de risco atribuído: `'CRITICA'`, `'ALTA'`, `'MEDIA'`, `'BAIXA'` | `CRITICA` |
| `descricao_risco` | VARCHAR(255) | Diagnóstico descritivo do desvio identificado | `Divergência contábil: total informado R$ 200 vs calculado R$ 225` |
| `payload_raw` | TEXT / JSON | Snapshot fiel do registro bruto recebido da camada Raw | `{"pedido_id": 2042, "valor_subtotal": 200.0, "valor_frete": 25.0, "valor_total": 200.0}` |
| `detected_at` | TIMESTAMPTZ | Timestamp de auditoria da detecção do desvio pela plataforma | `2026-03-15 17:10:00+00` |

### Qualify → Curated

Cruzamento dos dados de pedidos com atributos demográficos de clientes, métricas de campanhas de resgate e agregação temporal para disponibilização das views analíticas de receita e faturamento no Data Lakehouse.

```text
pedidos_qualify
    ↓
join com clientes_qualify (segmento_rfm, lifetime_value)
    ↓
join com eventos_resgate_qualify (canal_resgate, custo_envio)
    ↓
fct_pedidos / view_receita_recuperada_mensal (Curated Gold)
```

## Classificação por Camada

| Camada | Ativo | Característica |
|---|---|---|
| Raw / Bronze | `raw_pedidos` (`/raw/recuperacao_carrinho/pedidos.parquet`) | Dados brutos de liquidação transacional preservados diretamente da origem |
| Qualify / Silver | `qualify_pedidos` (`CART_RECOVERY.PEDIDOS`) | Dados de pedidos tipados, sanitizados e validados com integridade contábil |
| Anomaly / Silver | `pedidos_anomalies` (`CART_RECOVERY.PEDIDOS_ANOMALIES`) | Repositório de evidências, quarentena de anomalias e alertas de qualidade fiscal/atribuição |
| Curated / Gold | `fct_pedidos`, `view_receita_recuperada_mensal`, `dim_conversao_checkout` | Dados modelados dimensionalmente para consumo financeiro e executivo |

## Lineage

### Upstream

```text
Checkout Service / Payment Gateway (Stripe/Pagar.me) / ERP de Vendas
    ↓
/raw/recuperacao_carrinho/pedidos.parquet (Bronze)
```

### Qualification & Risk Routing (Transformation)

```text
raw_pedidos
        ↓
Pedidos Data Quality & Anomaly Detection Pipeline
        │
        ├── Registros válidos
        │       ↓
        │   pedidos_qualify
        │
        └── Registros inválidos/anômalos
                ↓
            pedidos_anomalies
```

### Downstream

```text
pedidos_qualify
        ↓
Curated / Gold
        ↓
├── BI / Painéis Executivos de Faturamento & Conversão
├── CRM / Dashboard de Receita Recuperada
├── Data App de Cart Recovery
├── Conciliação Contábil & Financeira
└── Agentes de IA

pedidos_anomalies
        ↓
├── Data Quality Dashboard
├── Alertas de Engenharia Financeira
└── Aplicação / Controladoria
```

---

# 4. Governance & Consumption

## Governança

- **Owner:** Squad Financeiro & Engenharia de Dados (`finance-data@marketplace.com`)
- **Classificação:** Confidencial / Financeiro
- **PII:** Não (contém apenas identificadores relacionais, valores contábeis e status operacionais)
- **Tags:**
  - `pedidos`
  - `transacional`
  - `conversoes`
  - `financeiro`
  - `silver`
  - `cart_recovery`

## Consumidores

- **Controladoria & Financeiro:** Apuração de receita bruta e líquida, conferência de gateway e relatórios fiscais.
- **Analytics & BI:** Relatórios executivos de conversão de checkout, ticket médio e taxa de recuperação global.
- **CRM & Growth Marketing:** Monitoramento da receita atribuída a campanhas e cálculo de ROI das réguas de resgate.
- **Data App de Cart Recovery:** Exibição do status de conversão e link para o pedido gerado.
- **Sistemas de Domínio & Auditoria Financeira:** Consumo de `pedidos_anomalies` para saneamento e conciliação de transações divergentes.

## Observações

- A restrição de unicidade em `carrinho_id` assegura que uma sessão de carrinho nunca seja convertida em múltiplos pedidos simultâneos.
- O campo `origem_recuperacao` e o vínculo `resgate_id` permitem segregar o faturamento orgânico do faturamento incremental gerado pelas campanhas de resgate.
- O artefato `pedidos_anomalies` preserva a integridade contábil do Data Lakehouse, evitando que transações com valores incorretos distorçam os relatórios executivos de faturamento.
