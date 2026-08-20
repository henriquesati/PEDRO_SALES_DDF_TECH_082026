# Entidade: `produtos`

**Descrição**: Catálogo de produtos do marketplace. Fornece dados de categoria, marca, preço e disponibilidade para análises de recuperação de carrinho segmentadas por tipo de produto.

---

## Atributos

| Campo | Tipo | PK/FK | Nullable | Default | Descrição |
|---|---|---|---|---|---|
| `produto_id` | INT | PK | NOT NULL | AUTO | Identificador único do produto |
| `nome` | VARCHAR(255) | — | NOT NULL | — | Nome do produto |
| `categoria` | VARCHAR(100) | — | NOT NULL | — | Categoria principal (ex: Eletrônicos, Moda, Casa) |
| `subcategoria` | VARCHAR(100) | — | NULL | — | Subcategoria (ex: Smartphones, Camisetas) |
| `marca` | VARCHAR(100) | — | NULL | — | Marca ou fabricante |
| `preco_atual` | DECIMAL(10,2) | — | NOT NULL | — | Preço vigente no catálogo |
| `preco_original` | DECIMAL(10,2) | — | NULL | — | Preço antes de promoção (NULL se não está em promoção) |
| `em_estoque` | BOOLEAN | — | NOT NULL | TRUE | Disponibilidade do produto |
| `avaliacao_media` | DECIMAL(2,1) | — | NULL | — | Rating médio (1.0 a 5.0) |
| `total_avaliacoes` | INT | — | NOT NULL | 0 | Quantidade de avaliações recebidas |
| `url_imagem` | VARCHAR(500) | — | NULL | — | URL da imagem principal do produto |
| `data_cadastro` | TIMESTAMPTZ | — | NOT NULL | NOW() | Data de cadastro no catálogo |
| `ativo` | BOOLEAN | — | NOT NULL | TRUE | Produto ativo no marketplace |

## Constraints

| Tipo | Campo(s) | Regra |
|---|---|---|
| CHECK | `preco_atual` | `> 0` |
| CHECK | `avaliacao_media` | `NULL` ou `>= 1.0 AND <= 5.0` |
| NOT NULL | `nome`, `categoria`, `preco_atual`, `em_estoque`, `total_avaliacoes`, `data_cadastro`, `ativo` | Campos obrigatórios |

---

## Observações

- Tabela **nova** — identificada como faltante na análise do modelo original
- `preco_atual` vs `preco_original`: permite identificar produtos em promoção (quando `preco_original IS NOT NULL AND preco_original > preco_atual`)
- `categoria` é essencial para análises do pitch (ex: "Carrinhos de Eletrônicos > R$500 recuperam melhor com frete grátis")
- Não há histórico de preços — o snapshot é capturado em `itens_carrinho.preco_unitario` no momento da adição
- `avaliacao_media` e `total_avaliacoes` podem influenciar a decisão de compra e são úteis para modelos prescritivos
