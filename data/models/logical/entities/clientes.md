# Entidade: `clientes`

**Descrição**: Compradores do marketplace. Armazena dados de identificação, segmentação RFM, histórico de compras e preferências de comunicação para personalização de campanhas de resgate.

---

## Atributos

| Campo | Tipo | PK/FK | Nullable | Default | Descrição |
|---|---|---|---|---|---|
| `cliente_id` | INT | PK | NOT NULL | AUTO | Identificador único do cliente |
| `primeiro_nome` | VARCHAR(100) | — | NOT NULL | — | Primeiro nome (usado em personalização de emails) |
| `ultimo_nome` | VARCHAR(100) | — | NULL | — | Sobrenome |
| `email` | VARCHAR(255) | UK | NOT NULL | — | Email do cliente (único) |
| `telefone` | VARCHAR(20) | — | NULL | — | Telefone com DDD |
| `segmento_rfm` | VARCHAR(20) | — | NULL | — | Segmento RFM: `'premium'`, `'regular'`, `'dormant'`, `'novo'` |
| `data_primeira_compra` | DATE | — | NULL | — | Data da primeira compra realizada |
| `data_ultima_compra` | DATE | — | NULL | — | Data da compra mais recente |
| `total_compras` | INT | — | NULL | 0 | Quantidade total de compras realizadas |
| `lifetime_value` | DECIMAL(12,2) | — | NULL | 0.00 | Valor total gasto pelo cliente |
| `permite_email` | BOOLEAN | — | NOT NULL | TRUE | Opt-in para receber emails |
| `permite_sms` | BOOLEAN | — | NOT NULL | FALSE | Opt-in para receber SMS |
| `permite_push` | BOOLEAN | — | NOT NULL | FALSE | Opt-in para receber push notifications |
| `status_ativo` | BOOLEAN | — | NOT NULL | TRUE | Cliente ativo na base |
| `data_criacao` | TIMESTAMPTZ | — | NOT NULL | NOW() | Data de cadastro do cliente |

## Constraints

| Tipo | Campo(s) | Regra |
|---|---|---|
| UNIQUE | `email` | Chave natural — um email por cliente |
| NOT NULL | `primeiro_nome`, `email`, `permite_email`, `permite_sms`, `permite_push`, `status_ativo`, `data_criacao` | Campos obrigatórios |
| CHECK | `segmento_rfm` | `∈ {'premium', 'regular', 'dormant', 'novo'}` ou NULL |

---

## Observações

- O `email` é a chave natural do cliente (UNIQUE constraint)
- `segmento_rfm` é calculado externamente e atualizado periodicamente
- `lifetime_value` e `total_compras` são atualizados a cada pedido confirmado
- `primeiro_nome` é essencial para personalização de campanhas de resgate ("Olá, Pedro!")
- Os campos `permite_*` controlam quais canais podem ser usados nas campanhas de resgate
