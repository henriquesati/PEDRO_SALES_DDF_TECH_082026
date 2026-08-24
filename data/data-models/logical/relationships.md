# Relacionamentos & Cardinalidades

## Diagrama ER

```
┌──────────┐       ┌──────────────┐       ┌──────────┐
│ CLIENTES │1────N→│  CARRINHOS   │1───0,1→│ PEDIDOS  │
│          │       │              │        │          │
└────┬─────┘       └──┬───┬───┬──┘        └────┬─────┘
     │                │   │   │                │
     │1               │1  │1  │1               │0,1
     │                │   │   │                │
     ↓N               ↓N  ↓N  ↓N               ↑
┌──────────────┐  ┌────┐ ┌──┐ ┌──────────────┐ │
│EVENTOS_RESGATE│  │ITENS│ │EV│ │EVENTOS_RESGATE│─┘
└──────────────┘  │CARR.│ │C.│ └──────────────┘
                  └──┬──┘ └──┘
                     │N
                     ↑
                  ┌──┴──────┐
                  │PRODUTOS │
                  └─────────┘
```

---

## Relacionamentos Detalhados

### 1. `clientes` (1) → (N) `carrinhos`
- **FK**: `carrinhos.cliente_id → clientes.cliente_id`
- **Regra de exclusão**: `RESTRICT` — não permite excluir cliente com carrinhos
- **Descrição**: Um cliente pode criar múltiplos carrinhos ao longo do tempo

### 2. `clientes` (1) → (N) `eventos_resgate`
- **FK**: `eventos_resgate.cliente_id → clientes.cliente_id`
- **Regra de exclusão**: `RESTRICT`
- **Descrição**: Um cliente recebe múltiplas comunicações de resgate

### 3. `carrinhos` (1) → (N) `itens_carrinho`
- **FK**: `itens_carrinho.carrinho_id → carrinhos.carrinho_id`
- **Regra de exclusão**: `CASCADE` — excluir carrinho exclui seus itens
- **Descrição**: Um carrinho contém um ou mais itens

### 4. `carrinhos` (1) → (N) `eventos_carrinho`
- **FK**: `eventos_carrinho.carrinho_id → carrinhos.carrinho_id`
- **Regra de exclusão**: `CASCADE` — excluir carrinho exclui seus eventos
- **Descrição**: Um carrinho gera múltiplos eventos comportamentais

### 5. `carrinhos` (1) → (N) `eventos_resgate`
- **FK**: `eventos_resgate.carrinho_id → carrinhos.carrinho_id`
- **Regra de exclusão**: `CASCADE`
- **Descrição**: Um carrinho abandonado pode receber múltiplas tentativas de resgate

### 6. `carrinhos` (1) → (0,1) `pedidos`
- **FK**: `pedidos.carrinho_id → carrinhos.carrinho_id`
- **Regra de exclusão**: `RESTRICT` — não excluir carrinho se gerou pedido
- **Descrição**: Um carrinho gera no máximo um pedido (quando convertido)
- **Constraint**: UNIQUE em `pedidos.carrinho_id`

### 7. `produtos` (1) → (N) `itens_carrinho`
- **FK**: `itens_carrinho.produto_id → produtos.produto_id`
- **Regra de exclusão**: `CASCADE` — excluir produto remove automaticamente os itens de carrinho que o referenciam
- **Descrição**: Um produto pode aparecer em múltiplos carrinhos. O produto pode ser excluído do catálogo a qualquer momento — o carrinho é responsável por tratar a remoção dos seus itens

### 8. `eventos_resgate` (1) → (0,1) `pedidos`
- **FK**: `pedidos.resgate_id → eventos_resgate.resgate_id`
- **Regra de exclusão**: `SET NULL` — se deletar resgate, pedido mantém mas perde referência
- **Descrição**: Uma campanha de resgate pode gerar no máximo um pedido
- **Condição**: Apenas quando `pedidos.origem_recuperacao = TRUE`

### 9. `clientes` (1) → (N) `eventos_carrinho`
- **FK**: `eventos_carrinho.cliente_id → clientes.cliente_id`
- **Regra de exclusão**: `RESTRICT`
- **Descrição**: Desnormalização intencional para facilitar queries de comportamento por cliente sem JOIN com carrinhos

---

## Resumo de Cardinalidades

| Entidade A | Card. | Entidade B | FK em |
|---|---|---|---|
| `clientes` | 1:N | `carrinhos` | `carrinhos` |
| `clientes` | 1:N | `eventos_resgate` | `eventos_resgate` |
| `clientes` | 1:N | `eventos_carrinho` | `eventos_carrinho` |
| `carrinhos` | 1:N | `itens_carrinho` | `itens_carrinho` |
| `carrinhos` | 1:N | `eventos_carrinho` | `eventos_carrinho` |
| `carrinhos` | 1:N | `eventos_resgate` | `eventos_resgate` |
| `carrinhos` | 1:0,1 | `pedidos` | `pedidos` |
| `produtos` | 1:N | `itens_carrinho` | `itens_carrinho` |
| `eventos_resgate` | 1:0,1 | `pedidos` | `pedidos` |
