# Entidade: `produtos`

---

# 1. Data Definition

> Define a estrutura dos dados, seus tipos, chaves, atributos e significados técnicos.

## Atributos / Data Dictionary

| Campo | Tipo | PK/FK | Nullable | Default | Descrição | Valores / Regras | Exemplo |
|---|---|---|---|---|---|---|---|
| `produto_id` | INT | PK | `FALSE` | AUTO | Identificador único exclusivo do produto no catálogo | Inteiro sequencial único positivo | `101` |
| `nome` | VARCHAR(255) | — | `FALSE` | — | Nome comercial e título descritivo do produto | Texto livre descritivo | `Samsung Galaxy S24 Ultra` |
| `categoria` | VARCHAR(100) | — | `FALSE` | — | Macro-departamento / categoria principal do produto | `'Eletrônicos'`, `'Moda'`, `'Casa & Decoração'`, `'Esportes'`, `'Beleza'`, `'Livros'`, `'Brinquedos'` | `'Eletrônicos'` |
| `subcategoria` | VARCHAR(100) | — | `TRUE` | — | Classificação especializada da linha de produtos | `'Smartphones'`, `'Notebooks'`, `'Calçados'`, etc. | `'Smartphones'` |
| `marca` | VARCHAR(100) | — | `TRUE` | — | Marca, fabricante ou grife do produto | Texto livre | `'Samsung'` |
| `preco_atual` | DECIMAL(10,2) | — | `FALSE` | — | Preço vigente de venda no catálogo do marketplace | DECIMAL `> 0.00` | `5499.00` |
| `preco_original` | DECIMAL(10,2) | — | `TRUE` | — | Preço de referência antes do desconto/promoção | DECIMAL `>= preco_atual` ou nulo | `5999.00` |
| `em_estoque` | BOOLEAN | — | `FALSE` | `TRUE` | Flag indicando disponibilidade física para pronta entrega | `TRUE` / `FALSE` | `TRUE` |
| `avaliacao_media` | DECIMAL(2,1) | — | `TRUE` | — | Nota média de satisfação atribuída pelos compradores | `1.0` a `5.0` (ou nulo se sem reviews) | `4.8` |
| `total_avaliacoes` | INT | — | `FALSE` | `0` | Volume consolidado de avaliações recebidas | Inteiro `>= 0` | `1240` |
| `url_imagem` | VARCHAR(500) | — | `TRUE` | — | URL da imagem principal para exibição em vitrines e resgates | URL válida | `https://cdn.marketplace.com.br/img/101.jpg` |
| `data_cadastro` | TIMESTAMPTZ | — | `FALSE` | NOW() | Timestamp oficial de inclusão do SKU no catálogo | Data/hora UTC válida | `2025-11-20 09:30:00+00` |
| `ativo` | BOOLEAN | — | `FALSE` | `TRUE` | Flag lógica que habilita a exibição e venda no marketplace | `TRUE` / `FALSE` | `TRUE` |

### Foreign Keys

```text
produtos.produto_id
    ← itens_carrinho.produto_id
```

## SCHEMA RULES

### 01 — Unicidade e Não-Nulidade da Chave Primária (PK)
O campo `produto_id` é chave primária inteira sequencial auto-incremental (`INT PRIMARY KEY`), obrigatória (`NOT NULL`) e exclusiva (`UNIQUE`), identificando unicamente cada SKU no catálogo.

### 02 — Integridade Referencial Reversa (FKs)
O identificador `produto_id` é referenciado como Foreign Key pela tabela transacional `itens_carrinho(produto_id)` com política `ON DELETE RESTRICT`, impedindo a exclusão de produtos que possuam histórico de adição em carrinhos.

### 03 — Restrições de Domínio, Tipagem e Precisão (CHECK Constraints)
- `preco_atual`: tipado como `DECIMAL(10,2)` com restrição `CHECK (preco_atual > 0.00)`.
- `preco_original`: tipado como `DECIMAL(10,2)` com restrição `CHECK (preco_original >= 0.00 OR preco_original IS NULL)`.
- `avaliacao_media`: tipado como `DECIMAL(2,1)` com restrição `CHECK (avaliacao_media BETWEEN 1.0 AND 5.0 OR avaliacao_media IS NULL)`.
- `total_avaliacoes`: tipado como `INT` com restrição `CHECK (total_avaliacoes >= 0)`.
- `categoria`: tipado como `VARCHAR(100)` restrito aos macro-departamentos oficiais do marketplace.

### 04 — Nulabilidade e Valores Padrão (Defaults)
- **Campos Obrigatórios (NOT NULL)**: `produto_id`, `nome`, `categoria`, `preco_atual`, `em_estoque`, `total_avaliacoes`, `data_cadastro`, `ativo`.
- **Valores Padrão**: `em_estoque = TRUE`, `total_avaliacoes = 0`, `ativo = TRUE`, `data_cadastro = NOW()`.

---

# 2. Business Definition & Business Rules

## Identificação e Visão de Negócio

- **Nome físico:** `produtos` (Snowflake: `CART_RECOVERY.PRODUTOS`)
- **Nome de negócio:** Catálogo de Produtos & SKUs
- **Domínio:** Catálogo, Pricing & Merchandising / Marketplace E-commerce
- **Tipo:** Dimensão Conforme (Conformed Dimension) / Catálogo de Itens
- **Descrição:** Entidade central de dimensão que consolida todas as especificações técnicas, mercadológicas, de precificação e de reputação dos itens comercializados no marketplace.
- **Objetivo de negócio:** Permitir a análise detalhada dos produtos presentes em carrinhos abandonados, cruzar elasticidade de preço por categoria, mensurar o impacto da ruptura de estoque e calibrar ofertas de resgate (ex: frete grátis vs cupom percentual).
- **Casos de uso:**
  - Identificar os produtos e categorias com maior volume e valor financeiro retido em carrinhos abandonados.
  - Avaliar se indisponibilidade de estoque (`em_estoque = FALSE`) ou desativação de produto (`ativo = FALSE`) gerou atrito e abandono no checkout.
  - Personalizar comunicações de resgate (E-mail/WhatsApp) exibindo nome, foto (`url_imagem`), preço e avaliação do produto abandonado.
  - Alimentar agentes de IA e motores de recomendação para sugerir produtos similares quando o item original esgotar.

## Granularidade

- **Granularidade:** Uma linha por SKU / produto único cadastrado no catálogo do marketplace.
- **Regra:** `1 linha = 1 produto cadastrado`

## Papel no Domínio

- Atua como a **dimensão fundamental de sortimento** do marketplace.
- Conecta o interesse do consumidor (`eventos_carrinho`), a composição das compras (`itens_carrinho`) e a liquidação das vendas (`pedidos`).

## Relacionamentos

| Entidade relacionada | Cardinalidade | Relacionamento |
|---|---:|---|
| `itens_carrinho` | 1:N | Um produto pode ser adicionado em múltiplos carrinhos por diferentes clientes |
| `eventos_carrinho` | 1:N | Um produto recebe múltiplos eventos de visualização e adição |

## Ciclo de Vida

```text
[cadastro] ──→ [ativo / em estoque] ──(vendas / esgotamento)──→ [sem estoque]
   │                   │                                              │
   │                   ▼                                              ▼
   └───────────→ [inativo / descontinuado] ◄──────────────────────────┘
```

### Estados

| Status / Flag | Significado de Negócio |
|---|---|
| `ativo = TRUE` & `em_estoque = TRUE` | Produto disponível para busca, adição ao carrinho e compra imediata |
| `ativo = TRUE` & `em_estoque = FALSE` | Produto visível no catálogo, mas indisponível para checkout (gera alerta de estoque) |
| `ativo = FALSE` | Produto descontinuado ou suspenso comercialmente; bloqueado para qualquer transação |

## BUSINESS RULES

### 01 — Coerência de Promoção e Preço
Quando o produto está em oferta promocional, o preço vigente deve ser estritamente inferior ao preço de referência original (`preco_atual < preco_original`). Casos onde `preco_atual > preco_original` representam anomalia de precificação (promoção invertida) e devem ser auditados.

### 02 — Disponibilidade e Trava de Adição ao Carrinho
Produtos com `em_estoque = FALSE` ou `ativo = FALSE` não podem receber novas adições em carrinhos. Caso um item presente em carrinho ativo sofra esgotamento antes da conclusão da compra, o checkout deve sinalizar a indisponibilidade ao consumidor.

### 03 — Consistência de Prova Social e Avaliações
A pontuação de satisfação `avaliacao_media` reflete a média das notas recebidas:
- Se `total_avaliacoes = 0`, `avaliacao_media` deve ser `NULL`.
- Se `total_avaliacoes > 0`, `avaliacao_media` deve conter um valor válido no intervalo $[1.0, 5.0]$.

### 04 — Elasticidade de Resgate por Categoria
Produtos de alto ticket médio pertencentes a categorias com maior margem (ex: `Eletrônicos` acima de R$ 500) possuem maior propensão de conversão quando incentivados com frete grátis em comparação a descontos percentuais baixos.

### 05 — Imutabilidade do Snapshot de Preço
O campo `preco_atual` reflete a cotação dinâmica do catálogo. Quando o produto é adicionado a um carrinho, o valor vigente é registrado de forma imutável em `itens_carrinho.preco_unitario`, protegendo o consumidor e o marketplace contra flutuações concorrentes durante a sessão.

---

# 3. Data Quality, Transformation & Lineage

> Define como a entidade é validada, transformada e movimentada entre as camadas do pipeline.

## Validação

As regras de integridade, restrições e higienização são estruturadas como funções declarativas que compõem o pipeline de validação e qualidade dos dados:

### 01 — `validar_pk_produto_id(produto_id)`
Valida se o identificador `produto_id` é único, positivo e não nulo (`NOT NULL & UNIQUE`).

### 02 — `validar_campos_obrigatorios(produto_id, nome, categoria, preco_atual, em_estoque, total_avaliacoes, data_cadastro, ativo)`
Garante que todos os atributos fundamentais estejam preenchidos (`IS NOT NULL`).

### 03 — `validar_dominio_categoria(categoria)`
Verifica se a categoria informada pertence ao domínio fechado de macro-departamentos: `{'Eletrônicos', 'Moda', 'Casa & Decoração', 'Esportes', 'Beleza', 'Livros', 'Brinquedos'}`.

### 04 — `sanitizar_preco_produto(preco_atual)`
Valida que `preco_atual > 0.00`. Valores negativos ou zerados disparam captura de anomalia crítica.

### 05 — `validar_coerencia_promocao(preco_atual, preco_original)`
Valida se `preco_original IS NULL` ou `preco_atual <= preco_original`. Ocorrências de `preco_atual > preco_original` geram evidência de promoção invertida.

### 06 — `validar_rating_avaliacoes(avaliacao_media, total_avaliacoes)`
Valida a coerência entre o número de reviews e a média atribuída: se `total_avaliacoes = 0`, `avaliacao_media` deve ser nula; se `total_avaliacoes > 0`, `avaliacao_media` deve estar entre 1.0 e 5.0.

### 07 — `validar_consistencia_temporal_cadastro(data_cadastro)`
Assegura que a data de cadastro do produto seja anterior ou contemporânea ao timestamp atual (`data_cadastro <= NOW()`).

## Pipeline de Transformação

O pipeline estabelece uma **fronteira arquitetural clara entre a Plataforma de Dados e a Aplicação/Domínio**:
- **Papel da Plataforma de Dados**: Ingerir, detectar desvios de precificação e catálogo, classificar severidade, medir impacto, registrar evidências brutas (`payload_raw`) e comunicar anomalias.
- **Papel da Aplicação / Domínio**: Consumir os eventos de anomalia e executar as decisões de resolução (ajuste de precificação, saneamento de catálogo ou reativação de estoque).

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
 ├── [Registros Válidos/Higienizados] ──→ produtos_qualify (Silver Qualify)
 └── [Inconsistências Detectadas]    ──→ produtos_anomalies (Silver Anomaly)
```

### Raw → Qualify

Ingestão dos dados de catálogo brutos (CSV/Parquet), casting de tipos para padrões analíticos (DECIMAL, TIMESTAMPTZ), validação de departamentos, higienização de strings e validação de regras de precificação.

```text
produtos_raw
→ validar_schema_e_tipagem
→ extrair_e_rotear_anomalias (envia evidências para produtos_anomalies)
→ sanitizar_nomes_e_categorias
→ validar_limites_de_preco_e_promocao
→ validar_consistencia_de_avaliacoes
→ deduplicar_produto_id
→ produtos_qualify
```

### Raw → Anomaly

Mecanismo de captura, classificação e registro de desvios que representam risco comercial ou inconsistência de vitrine. A plataforma preserva o payload bruto original para auditoria e tomada de decisão pelo time comercial.

```text
produtos_raw
    ↓
[Motor de Detecção e Classificação de Anomalias]
    ├── ANOM-01: Preço Zerado ou Negativo (preco_atual <= 0)
    ├── ANOM-02: Promoção Invertida (preco_atual > preco_original)
    ├── ANOM-03: Inconsistência de Rating (avaliacao_media fora de 1.0-5.0 ou presente com 0 reviews)
    └── ANOM-04: Categoria Inválida ou Órfã no Catálogo
    ↓
produtos_anomalies (Repositório de Evidências & Alertas da Plataforma)
```

#### Regras de Anomalia de Negócio

| Código | Regra de Anomalia | Severidade | Risco de Negócio | Ação do Pipeline |
|---|---|:---:|---|---|
| `ANOM-01` | `preco_atual <= 0.00` | `CRÍTICA` | Risco financeiro severo de venda a valor nulo/negativo ou falha de ingestão | Encaminha evidência para Anomaly |
| `ANOM-02` | `preco_original IS NOT NULL AND preco_atual > preco_original` | `ALTA` | Propaganda enganosa, distorção de vitrine e quebra de confiança do consumidor | Encaminha evidência para Anomaly |
| `ANOM-03` | `(total_avaliacoes = 0 AND avaliacao_media IS NOT NULL)` ou `avaliacao_media NOT BETWEEN 1.0 AND 5.0` | `MÉDIA` | Falha de agregação de reviews e distorção em algoritmos de recomendação | Encaminha evidência para Anomaly |
| `ANOM-04` | `categoria NOT IN ('Eletrônicos', 'Moda', 'Casa & Decoração', 'Esportes', 'Beleza', 'Livros', 'Brinquedos')` | `MÉDIA` | Descategorização de sortimento e falha em relatórios de performance por setor | Encaminha evidência para Anomaly |

#### Estrutura do Artefato de Anomalias (`produtos_anomalies`)

A estrutura do artefato reflete as atribuições estritas da plataforma de dados (detecção, classificação e evidência):

| Campo | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `anomaly_id` | VARCHAR / UUID | Identificador exclusivo do evento de anomalia | `anom-9a4f2e1b-782c` |
| `produto_id` | INT | Identificador do produto afetado | `101` |
| `codigo_anomalia` | VARCHAR(20) | Código identificador da regra violada (`ANOM-01` a `ANOM-04`) | `ANOM-02` |
| `severidade` | VARCHAR(10) | Grau de risco atribuído: `'CRITICA'`, `'ALTA'`, `'MEDIA'`, `'BAIXA'` | `ALTA` |
| `descricao_risco` | VARCHAR(255) | Diagnóstico descritivo do desvio identificado | `Preço promocional atual (R$ 450) superior ao preço original (R$ 399)` |
| `payload_raw` | TEXT / JSON | Snapshot fiel do registro bruto recebido da camada Raw | `{"produto_id": 101, "preco_atual": 450.00, "preco_original": 399.00}` |
| `detected_at` | TIMESTAMPTZ | Timestamp de auditoria da detecção do desvio pela plataforma | `2026-03-15 14:25:00+00` |

### Qualify → Curated

Cruzamento dos dados de produtos com o volume agregado de adições e abandonos a partir de `itens_carrinho_qualify`, cômputo de taxas de conversão por categoria e marca, e disponibilização de views dimensionais para dashboards de sortimento e agentes de recomendação.

```text
produtos_qualify
    ↓
join agregado com itens_carrinho_qualify (taxa_abandono_produto, receita_repassada_carrinho)
    ↓
join com eventos_carrinho_qualify (total_views, taxa_conversao_visualizacao_para_carrinho)
    ↓
dim_produtos / fct_performance_sortimento_resgate (Curated Gold)
```

## Classificação por Camada

| Camada | Ativo | Característica |
|---|---|---|
| Raw / Bronze | `raw_produtos` (`/raw/recuperacao_carrinho/produtos.parquet`) | Dados brutos preservados diretamente do catálogo comercial |
| Qualify / Silver | `qualify_produtos` (`CART_RECOVERY.PRODUTOS`) | Dados de catálogo tipados, deduplicados, sanitizados e validados |
| Anomaly / Silver | `produtos_anomalies` (`CART_RECOVERY.PRODUTOS_ANOMALIES`) | Repositório de evidências, quarentena de anomalias e alertas de qualidade para atuação do Comercial/Catálogo |
| Curated / Gold | `dim_produtos`, `dim_produtos_performance`, `view_produtos_resgate` | Dados modelados dimensionalmente para consumo analítico e operacional |

## Lineage

### Upstream

```text
Catalog Management System / PIM / Pricing Engine API
    ↓
/raw/recuperacao_carrinho/produtos.parquet (Bronze)
```

### Qualification & Risk Routing (Transformation)

```text
raw_produtos
        ↓
Produtos Data Quality & Anomaly Detection Pipeline
        │
        ├── Registros válidos
        │       ↓
        │   produtos_qualify
        │
        └── Registros inválidos/anômalos
                ↓
            produtos_anomalies
```

### Downstream

```text
produtos_qualify
        ↓
Curated / Gold
        ↓
├── BI / Analytics de Sortimento & Abandono
├── Checkout & Vitrine de Produtos
├── Data App de Resgate de Carrinho
├── Modelos de Recomendação de Produtos
└── Agentes de IA

produtos_anomalies
        ↓
├── Data Quality Dashboard
├── Alertas de Engenharia & Pricing
└── Aplicação / Time de Catálogo Comercial
```

---

# 4. Governance & Consumption

## Governança

- **Owner:** Squad de Catálogo & Pricing E-commerce (`catalogo-pricing@marketplace.com`)
- **Classificação:** Interno
- **PII:** Não (contém exclusivamente dados mercadológicos e técnicos de produtos sem dados pessoais de usuários)
- **Tags:**
  - `produtos`
  - `catalogo`
  - `pricing`
  - `dimensao`
  - `silver`
  - `cart_recovery`

## Consumidores

- **Checkout & Frontend:** Renderização dos dados de produtos, fotos e cálculo de subtotal no checkout.
- **Analytics & BI:** Relatórios de perdas financeiras por departamento, produtos mais abandonados e impacto do frete por categoria.
- **Data App de Cart Recovery:** Exibição do resumo visual dos produtos ao operador durante campanhas manuais/assistidas de resgate.
- **Modelos Preditivos & Agentes de IA:** Algoritmos de recomendação de produtos substitutos para itens esgotados e precificação dinâmica de cupons.
- **Sistemas de Domínio & Gestão de Catálogo:** Consumo de `produtos_anomalies` para saneamento e correção rápida de preços na origem.

## Observações

- A tabela `produtos` serve como a dimensão oficial de sortimento e garante integridade relacional para todas as adições de itens em sessões de compra.
- O campo `url_imagem` é utilizado nas comunicações de marketing de resgate para aumentar a taxa de cliques (CTR) e o apelo visual do e-mail.
- O artefato de anomalias (`produtos_anomalies`) isola inconsistências graves como promoções invertidas ou preços negativos sem interromper a disponibilidade dos demais SKUs válidos na plataforma.
