# Entidade: `itens_carrinho`

---

# 1. Data Definition

> Define a estrutura dos dados, seus tipos, chaves, atributos e significados técnicos.

## Atributos / Data Dictionary

| Campo | Tipo | PK/FK | Nullable | Default | Descrição | Valores / Regras | Exemplo |
|---|---|---|---|---|---|---|---|
| `item_id` | INT | PK | `FALSE` | AUTO | Identificador único exclusivo da linha do item adicionado ao carrinho | Inteiro sequencial único positivo | `5001` |
| `carrinho_id` | INT | FK | `FALSE` | — | Identificador do carrinho pai proprietário da sessão de compra | Deve existir na tabela `carrinhos` | `1001` |
| `produto_id` | INT | FK | `FALSE` | — | Identificador do produto adicionado a partir do catálogo | Deve existir na tabela `produtos` | `101` |
| `quantidade` | INT | — | `FALSE` | `1` | Quantidade de unidades selecionadas para o item | Inteiro `>= 1` | `2` |
| `preco_unitario` | DECIMAL(10,2) | — | `FALSE` | — | Preço unitário no instante exato da adição (snapshot imutável) | DECIMAL `> 0.00` | `149.90` |
| `preco_total` | DECIMAL(10,2) | — | `FALSE` | — | Valor total da linha calculado (`quantidade * preco_unitario`) | DECIMAL `> 0.00` | `299.80` |
| `data_adicao` | TIMESTAMPTZ | — | `FALSE` | NOW() | Timestamp exato em que o item foi inserido no carrinho | Data/hora UTC válida | `2026-03-15 14:24:00+00` |
| `data_remocao` | TIMESTAMPTZ | — | `TRUE` | — | Timestamp em que o item foi removido pelo cliente (se aplicável) | Data/hora UTC `>= data_adicao` ou nulo | `2026-03-15 14:35:00+00` |

### Foreign Keys

```text
itens_carrinho.carrinho_id
    → carrinhos.carrinho_id

itens_carrinho.produto_id
    → produtos.produto_id
```

## SCHEMA RULES

### 01 — Unicidade e Não-Nulidade da Chave Primária (PK)
O campo `item_id` é chave primária inteira sequencial auto-incremental (`INT PRIMARY KEY`), obrigatória (`NOT NULL`) e exclusiva (`UNIQUE`), identificando unicamente cada linha de item adicionada a um carrinho.

### 02 — Integridade Referencial (FKs)
- O campo `carrinho_id` é chave estrangeira obrigatória (`INT NOT NULL`) referenciando `carrinhos(carrinho_id)` com política `ON DELETE CASCADE`, garantindo a exclusão de itens quando uma sessão de carrinho é descartada.
- O campo `produto_id` é chave estrangeira obrigatória (`INT NOT NULL`) referenciando `produtos(produto_id)` com política `ON DELETE RESTRICT`, impedindo a exclusão acidental de produtos do catálogo vinculados a históricos de carrinho.

### 03 — Restrições de Domínio, Tipagem e Precisão Numérica (CHECK Constraints)
- `quantidade`: tipado como `INT` com restrição `CHECK (quantidade >= 1)`.
- `preco_unitario`: tipado como `DECIMAL(10,2)` com restrição `CHECK (preco_unitario > 0.00)`.
- `preco_total`: tipado como `DECIMAL(10,2)` com restrição `CHECK (preco_total > 0.00)`.

### 04 — Nulabilidade e Valores Padrão (Defaults)
- **Campos Obrigatórios (NOT NULL)**: `item_id`, `carrinho_id`, `produto_id`, `quantidade`, `preco_unitario`, `preco_total`, `data_adicao`.
- **Valores Padrão**: `quantidade = 1`, `data_adicao = NOW()`.

---

# 2. Business Definition & Business Rules

## Identificação e Visão de Negócio

- **Nome físico:** `itens_carrinho` (Snowflake: `CART_RECOVERY.ITENS_CARRINHO`)
- **Nome de negócio:** Itens do Carrinho de Compras (Linhas de Produto da Sessão)
- **Domínio:** Transacional, Merchandising & Checkout / Marketplace E-commerce
- **Tipo:** Fato Transacional de Linha (Transaction Line Fact) / Tabela Associativa de Itens
- **Descrição:** Tabela transacional que armazena os produtos individuais adicionados por clientes durante uma sessão de compras, capturando o snapshot de preço unitário no momento da adição e registrando a permanência ou remoção do item antes da finalização do pedido.
- **Objetivo de negócio:** Rastrear a intenção de compra item a item, identificar produtos com maior taxa de descarte/remoção pré-checkout, alimentar réguas de resgate personalizadas (mencionando o SKU específico deixado no carrinho) e calcular o subtotal financeiro exato de carrinhos abandonados.
- **Casos de uso:**
  - Extrair o produto principal de maior valor em carrinhos abandonados para geração dinâmica de copy em campanhas de resgate ("Você esqueceu seu [Nome do Produto]").
  - Identificar padrões de abandono por cross-sell (ex: itens da categoria A abandonados com frequência quando combinados com itens da categoria B).
  - Medir a taxa de remoção de itens (`data_remocao IS NOT NULL`) como indicador de sensibilidade a preço ou atrito no cálculo de frete.
  - Reconciliar matematicamente o subtotal de cada carrinho com a soma dos itens ativos.

## Granularidade

- **Granularidade:** Uma linha por ocorrência de adição de um produto específico (SKU) em uma sessão de carrinho de compras.
- **Regra:** `1 linha = 1 item adicionado ao carrinho`

## Papel no Domínio

- Atua como a **ponte associativa detalhada** entre as sessões de carrinho (`carrinhos`) e os produtos do catálogo (`produtos`).
- Conecta a intenção de compra aos eventos comportamentais da telemetria (`eventos_carrinho`).

## Relacionamentos

| Entidade relacionada | Cardinalidade | Relacionamento |
|---|---:|---|
| `carrinhos` | N:1 | Cada linha de item pertence obrigatoriamente a um carrinho de compras |
| `produtos` | N:1 | Cada linha de item faz referência a um produto cadastrado no catálogo |

## Ciclo de Vida

```text
[adicionado] ──(cliente conclui checkout)──→ [comprado / convertido]
     │
     └──(cliente remove item da sessão)──→ [removido (data_remocao IS NOT NULL)]
```

### Estados

| Estado do Item | Condição | Significado de Negócio |
|---|---|---|
| `Ativo no Carrinho` | `data_remocao IS NULL` | O produto permanece dentro do carrinho e compõe o valor do subtotal da sessão |
| `Removido do Carrinho` | `data_remocao IS NOT NULL` | O item foi retirado da sessão antes da conversão/abandono; não soma no subtotal |

## BUSINESS RULES

### 01 — Imutabilidade do Snapshot de Preço
O campo `preco_unitario` representa o valor de venda vigente do produto exatamente no instante `data_adicao`. Caso o preço do SKU seja alterado posteriormente no catálogo geral (`produtos.preco_atual`), o valor registrado em `itens_carrinho.preco_unitario` permanece inalterado para preservar a integridade histórica da intenção de compra.

### 02 — Consistência Matemática da Linha
O valor `preco_total` deve obrigatoriamente satisfazer a relação matemática:
$$\text{preco\_total} = \text{quantidade} \times \text{preco\_unitario}$$
Discrepâncias de cálculo superiores a R$ 0.01 decorrentes de arredondamento ou dirty data devem ser isoladas na camada de anomalias.

### 03 — Controle de Remoção e Exclusão do Subtotal
Um item é considerado ativo no carrinho enquanto `data_remocao IS NULL`. Quando o cliente descarta o item na interface, a data e hora do descarte são persistidas em `data_remocao` com valor $\ge \text{data\_adicao}$. Itens com `data_remocao IS NOT NULL` são desconsiderados no cômputo de `carrinhos.valor_subtotal`.

### 04 — Múltiplas Adições na Mesma Sessão
A chave natural composta `(carrinho_id, produto_id)` não possui restrição de unicidade rígida, permitindo múltiplos registros se o cliente removeu o produto e subsequentemente o reinseriu na mesma sessão, preservando a rastreabilidade temporal.

### 05 — Conciliação Contábil com o Subtotal do Carrinho
A soma dos valores `preco_total` de todas as linhas com `data_remocao IS NULL` pertencentes a um determinado `carrinho_id` deve coincidir exatamente com o valor consolidado em `carrinhos.valor_subtotal`.

---

# 3. Data Quality, Transformation & Lineage

> Define como a entidade é validada, transformada e movimentada entre as camadas do pipeline.

## Validação

As regras de integridade, restrições e higienização são estruturadas como funções declarativas que compõem o pipeline de validação e qualidade dos dados:

### 01 — `validar_pk_item_id(item_id)`
Valida se o identificador `item_id` é único, positivo e não nulo (`NOT NULL & UNIQUE`).

### 02 — `validar_fk_carrinho_id(carrinho_id)`
Valida se o `carrinho_id` existe previamente na tabela `carrinhos`.

### 03 — `validar_fk_produto_id(produto_id)`
Valida se o `produto_id` existe previamente na tabela `produtos`.

### 04 — `validar_campos_obrigatorios(item_id, carrinho_id, produto_id, quantidade, preco_unitario, preco_total, data_adicao)`
Garante que todos os atributos mandatários estejam preenchidos (`IS NOT NULL`).

### 05 — `sanitizar_quantidade(quantidade)`
Valida que `quantidade >= 1`. Valores nulos, zerados ou negativos são tratados como anomalias.

### 06 — `validar_equacao_preco_total(quantidade, preco_unitario, preco_total)`
Valida a consistência matemática da linha: `abs(preco_total - (quantidade * preco_unitario)) <= 0.01`.

### 07 — `validar_consistencia_temporal_remocao(data_adicao, data_remocao)`
Assegura que `data_remocao IS NULL` ou `data_remocao >= data_adicao`. Discrepâncias onde a remoção antecede a adição geram evidência de anomalia temporal.

## Pipeline de Transformação

O pipeline estabelece uma **fronteira arquitetural clara entre a Plataforma de Dados e a Aplicação/Domínio**:
- **Papel da Plataforma de Dados**: Ingerir, verificar chaves relacionais, validar equações de preço, classificar severidade e persistir evidências brutas (`payload_raw`) em `itens_carrinho_anomalies`.
- **Papel da Aplicação / Domínio**: Consumir os eventos de anomalia e executar as decisões de resolução (recalcular linha, revalidar catálogo ou acionar suporte de checkout).

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
 ├── [Registros Válidos/Higienizados] ──→ itens_carrinho_qualify (Silver Qualify)
 └── [Inconsistências Detectadas]    ──→ itens_carrinho_anomalies (Silver Anomaly)
```

### Raw → Qualify

Ingestão dos registros brutos de itens (CSV/Parquet), casting de tipos para padrões analíticos (DECIMAL, TIMESTAMPTZ), validação de integridade referencial com carrinhos e produtos, recálculo de `preco_total` e deduplicação de identificadores.

```text
itens_carrinho_raw
→ validar_schema_e_tipagem
→ extrair_e_rotear_anomalias (envia evidências para itens_carrinho_anomalies)
→ validar_fks_carrinho_e_produto
→ validar_e_reconciliar_preco_total
→ validar_consistencia_temporal_remocao
→ deduplicar_item_id
→ itens_carrinho_qualify
```

### Raw → Anomaly

Mecanismo de captura, classificação e registro de desvios que representam divergência contábil, inversão temporal ou chave órfã. A plataforma preserva o payload bruto original para auditoria e governança.

```text
itens_carrinho_raw
    ↓
[Motor de Detecção e Classificação de Anomalias]
    ├── ANOM-01: Preço Unitário Zerado ou Negativo (preco_unitario <= 0)
    ├── ANOM-02: Divergência Matemática na Linha (preco_total != quantidade * preco_unitario)
    ├── ANOM-03: Inversão Temporal de Remoção (data_remocao < data_adicao)
    └── ANOM-04: Quantidade Inválida ou Zerada (quantidade < 1)
    ↓
itens_carrinho_anomalies (Repositório de Evidências & Alertas da Plataforma)
```

#### Regras de Anomalia de Negócio

| Código | Regra de Anomalia | Severidade | Risco de Negócio | Ação do Pipeline |
|---|---|:---:|---|---|
| `ANOM-01` | `preco_unitario <= 0.00` | `CRÍTICA` | Risco financeiro de adição gratuita ou corrupção de snapshot de preço | Encaminha evidência para Anomaly |
| `ANOM-02` | `abs(preco_total - (quantidade * preco_unitario)) > 0.01` | `ALTA` | Falha contábil de checkout e divergência na cobrança de subtotal | Encaminha evidência para Anomaly |
| `ANOM-03` | `data_remocao IS NOT NULL AND data_remocao < data_adicao` | `ALTA` | Falha de sincronização de relógio de sessão ou inconsistência de telemetria | Encaminha evidência para Anomaly |
| `ANOM-04` | `quantidade < 1` | `CRÍTICA` | Inconsistência estrutural de linha sem unidades selecionadas | Encaminha evidência para Anomaly |

#### Estrutura do Artefato de Anomalias (`itens_carrinho_anomalies`)

A estrutura do artefato reflete as atribuições estritas da plataforma de dados (detecção, classificação e evidência):

| Campo | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `anomaly_id` | VARCHAR / UUID | Identificador exclusivo do evento de anomalia | `anom-4b2e8c1a-609d` |
| `item_id` | INT | Identificador da linha de item afetada | `5042` |
| `carrinho_id` | INT | Identificador do carrinho associado | `1001` |
| `produto_id` | INT | Identificador do produto associado | `101` |
| `codigo_anomalia` | VARCHAR(20) | Código identificador da regra violada (`ANOM-01` a `ANOM-04`) | `ANOM-03` |
| `severidade` | VARCHAR(10) | Grau de risco atribuído: `'CRITICA'`, `'ALTA'`, `'MEDIA'`, `'BAIXA'` | `ALTA` |
| `descricao_risco` | VARCHAR(255) | Diagnóstico descritivo do desvio identificado | `Data de remoção (14:10) anterior à data de adição (14:24)` |
| `payload_raw` | TEXT / JSON | Snapshot fiel do registro bruto recebido da camada Raw | `{"item_id": 5042, "data_adicao": "2026-03-15 14:24:00", "data_remocao": "2026-03-15 14:10:00"}` |
| `detected_at` | TIMESTAMPTZ | Timestamp de auditoria da detecção do desvio pela plataforma | `2026-03-15 14:25:00+00` |

### Qualify → Curated

Enriquecimento dos itens com atributos dimensionais de produtos (categoria, marca, rating) e cruzamento com eventos de abandono para cômputo de perdas financeiras por departamento e geração de views analíticas de merchandising.

```text
itens_carrinho_qualify
    ↓
join com produtos_qualify (nome, categoria, subcategoria, marca, preco_original)
    ↓
join com carrinhos_qualify (status, data_abandono, cliente_id)
    ↓
fct_itens_carrinho / view_itens_abandonados_detalhe (Curated Gold)
```

## Classificação por Camada

| Camada | Ativo | Característica |
|---|---|---|
| Raw / Bronze | `raw_itens_carrinho` (`/raw/recuperacao_carrinho/itens_carrinho.parquet`) | Dados brutos preservados diretamente das adições transacionais |
| Qualify / Silver | `qualify_itens_carrinho` (`CART_RECOVERY.ITENS_CARRINHO`) | Dados de itens tipados, sanitizados e validados com integridade relacional |
| Anomaly / Silver | `itens_carrinho_anomalies` (`CART_RECOVERY.ITENS_CARRINHO_ANOMALIES`) | Repositório de evidências, quarentena de anomalias e alertas de integridade contábil/temporal |
| Curated / Gold | `fct_itens_carrinho`, `view_itens_abandonados_detalhe` | Dados modelados dimensionalmente para consumo analítico e operacional |

## Lineage

### Upstream

```text
Checkout Service / Cart Item API / Session Tracker
    ↓
/raw/recuperacao_carrinho/itens_carrinho.parquet (Bronze)
```

### Qualification & Risk Routing (Transformation)

```text
raw_itens_carrinho
        ↓
Itens do Carrinho Data Quality & Anomaly Detection Pipeline
        │
        ├── Registros válidos
        │       ↓
        │   itens_carrinho_qualify
        │
        └── Registros inválidos/anômalos
                ↓
            itens_carrinho_anomalies
```

### Downstream

```text
itens_carrinho_qualify
        ↓
Curated / Gold
        ↓
├── BI / Analytics de Composição de Carrinho
├── CRM / Personalização de E-mail de Resgate
├── Data App de Cart Recovery
├── Algoritmos de Recomendação de Cross-sell
└── Agentes de IA

itens_carrinho_anomalies
        ↓
├── Data Quality Dashboard
├── Alertas de Engenharia de Checkout
└── Aplicação / Time de Domínio
```

---

# 4. Governance & Consumption

## Governança

- **Owner:** Engenharia de Dados & Squad de Checkout / Merchandising (`checkout-data@marketplace.com`)
- **Classificação:** Interno
- **PII:** Não (contém apenas identificadores numéricos relacionais, quantidades e valores monetários)
- **Tags:**
  - `itens_carrinho`
  - `transacional`
  - `checkout`
  - `snapshot`
  - `silver`
  - `cart_recovery`

## Consumidores

- **CRM & Automação de E-mail/WhatsApp:** Inclusão dos dados e fotos dos produtos abandonados na mensagem enviada ao consumidor.
- **Analytics & BI:** Relatórios de itens mais abandonados, elasticidade de preços e análise de cesta de compras (market basket analysis).
- **Data App de Cart Recovery:** Exibição da lista discriminada de produtos de cada carrinho selecionado para resgate.
- **Modelos Preditivos & Agentes de IA:** Modelos de propensão a conversão baseados na composição de itens do carrinho.
- **Sistemas de Domínio & Resolução de Falhas:** Consumo de `itens_carrinho_anomalies` para auditoria de erros de precificação na esteira de checkout.

## Observações

- A preservação do campo `preco_unitario` como snapshot evita divergências caso o produto sofra reajustes no catálogo durante o período de abandono e resgate.
- O campo `data_remocao` viabiliza análises de funil e atrito na sessão, identificando produtos que foram descartados no último instante antes do abandono total.
- O artefato `itens_carrinho_anomalies` isola falhas matemáticas e inversões temporais sem prejudicar a apuração dos demais itens saudáveis da sessão.
