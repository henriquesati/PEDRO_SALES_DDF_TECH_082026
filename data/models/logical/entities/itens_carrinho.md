# Entidade: `itens_carrinho`

**Descrição**: Itens adicionados a cada carrinho de compras. Armazena o snapshot de preço no momento da adição para preservar o contexto histórico (o preço do produto pode mudar depois).

---

## Atributos

| Campo | Tipo | PK/FK | Nullable | Default | Descrição |
|---|---|---|---|---|---|
| `item_id` | INT | PK | NOT NULL | AUTO | Identificador único do item |
| `carrinho_id` | INT | FK → carrinhos | NOT NULL | — | Carrinho ao qual o item pertence |
| `produto_id` | INT | FK → produtos | NOT NULL | — | Produto adicionado |
| `quantidade` | INT | — | NOT NULL | 1 | Quantidade do produto |
| `preco_unitario` | DECIMAL(10,2) | — | NOT NULL | — | Preço unitário no momento da adição (snapshot) |
| `preco_total` | DECIMAL(10,2) | — | NOT NULL | — | Valor total do item (quantidade × preço_unitario) |
| `data_adicao` | TIMESTAMPTZ | — | NOT NULL | NOW() | Timestamp da adição ao carrinho |
| `data_remocao` | TIMESTAMPTZ | — | NULL | — | Timestamp da remoção (NULL se ainda no carrinho) |

## Constraints

| Tipo | Campo(s) | Regra |
|---|---|---|
| CHECK | `quantidade` | `> 0` |
| CHECK | `preco_unitario` | `> 0` |
| CHECK | `preco_total` | `> 0` |
| NOT NULL | `carrinho_id`, `produto_id`, `quantidade`, `preco_unitario`, `preco_total`, `data_adicao` | Campos obrigatórios |

---

## Observações

- `preco_unitario` é um **snapshot** do preço no momento da adição — não muda se o preço do produto for alterado posteriormente
- `preco_total` é calculado pela aplicação como `quantidade * preco_unitario` (não como coluna gerada, para maior portabilidade)
- **Campos de engagement removidos**: `foi_visualizado_email`, `data_visualizacao_email`, `foi_clicado`, `foi_recomprado` foram movidos para `eventos_resgate` onde pertencem conceitualmente
- Um item com `data_remocao IS NOT NULL` foi removido do carrinho pelo cliente antes do abandono/compra
- A combinação `(carrinho_id, produto_id)` pode ter duplicatas se o cliente adicionou, removeu e re-adicionou o mesmo produto
