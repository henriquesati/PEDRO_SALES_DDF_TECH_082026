# Entidade: `pedidos`

**Descrição**: Pedidos finalizados no marketplace. Fecha o ciclo carrinho → pedido, permitindo calcular taxas reais de conversão e o valor monetário recuperado pelas campanhas de resgate.

---

## Atributos

| Campo | Tipo | PK/FK | Nullable | Default | Descrição |
|---|---|---|---|---|---|
| `pedido_id` | INT | PK | NOT NULL | AUTO | Identificador único do pedido |
| `carrinho_id` | INT | FK → carrinhos | NOT NULL | — | Carrinho de origem |
| `cliente_id` | INT | FK → clientes | NOT NULL | — | Cliente comprador |
| `data_pedido` | TIMESTAMPTZ | — | NOT NULL | NOW() | Data de criação do pedido |
| `valor_subtotal` | DECIMAL(10,2) | — | NOT NULL | — | Subtotal dos itens |
| `valor_frete` | DECIMAL(10,2) | — | NOT NULL | 0.00 | Valor do frete cobrado |
| `valor_desconto` | DECIMAL(10,2) | — | NOT NULL | 0.00 | Desconto aplicado |
| `valor_total` | DECIMAL(10,2) | — | NOT NULL | — | Valor final pago (subtotal + frete - desconto) |
| `metodo_pagamento` | VARCHAR(50) | — | NULL | — | Método: `'cartao_credito'`, `'cartao_debito'`, `'boleto'`, `'pix'` |
| `status_pedido` | VARCHAR(20) | — | NOT NULL | 'confirmado' | Status: `'confirmado'`, `'enviado'`, `'entregue'`, `'cancelado'` |
| `origem_recuperacao` | BOOLEAN | — | NOT NULL | FALSE | Se o pedido veio de campanha de resgate |
| `resgate_id` | BIGINT | FK → eventos_resgate | NULL | — | Qual campanha de resgate gerou este pedido (NULL se compra direta) |
| `created_at` | TIMESTAMPTZ | — | NOT NULL | NOW() | Audit: criação do registro |

## Constraints

| Tipo | Campo(s) | Regra |
|---|---|---|
| UNIQUE | `carrinho_id` | Um carrinho gera no máximo 1 pedido |
| CHECK | `status_pedido` | `∈ {'confirmado', 'enviado', 'entregue', 'cancelado'}` |
| CHECK | `metodo_pagamento` | `∈ {'cartao_credito', 'cartao_debito', 'boleto', 'pix'}` |
| CHECK | `valor_total` | `> 0` |
| NOT NULL | `carrinho_id`, `cliente_id`, `data_pedido`, `valor_subtotal`, `valor_frete`, `valor_desconto`, `valor_total`, `status_pedido`, `origem_recuperacao`, `created_at` | Campos obrigatórios |

---

## Observações

- Tabela **nova** — identificada como faltante no modelo original (mencionada no lifecycle mas nunca definida)
- `origem_recuperacao = TRUE` indica que o pedido é resultado de uma campanha de resgate (permite calcular valor recuperado)
- `resgate_id` liga o pedido diretamente à campanha que o gerou (essencial para ROI por campanha)
- Relação com carrinho é 1:1 (um carrinho gera no máximo um pedido)
- `status_pedido` simplificado para o escopo do case — sem tabela de histórico de status
- O campo `valor_total` deve ser consistente com o `valor_pedido_final` em `eventos_resgate` quando `origem_recuperacao = TRUE`
