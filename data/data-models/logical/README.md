# Modelo de Dados — Recuperação de Carrinho Abandonado (Marketplace)

## Visão Geral do Domínio

**Projeto**: Case de Recuperação de Carrinho Abandonado para cliente Marketplace  
**SGBD Alvo**: PostgreSQL  
**Objetivo**: Modelar a jornada completa do carrinho de compras — desde a criação até o abandono, campanhas de resgate e eventual conversão em pedido — para alimentar análises descritivas, prescritivas e o case principal de recuperação de carrinho.

---

## Problema de Negócio

- **Taxa de abandono**: ~70% dos carrinhos são abandonados antes da compra
- **Valor perdido**: Média de R$ 50–300 por carrinho abandonado
- **Escala anual estimada**: R$ 5M–50M em vendas potenciais perdidas
- **Solução**: Identificar, segmentar e recuperar carrinhos abandonados com intervenções personalizadas (email, SMS, push, WhatsApp) para maximizar taxa de conversão e ROI

---

## Entidades do Modelo

| # | Entidade | Descrição | Arquivo |
|---|---|---|---|
| 1 | `clientes` | Compradores do marketplace com segmentação RFM e preferências de contato | [clientes.md](entities/clientes.md) |
| 2 | `produtos` | Catálogo de produtos com categoria, marca, preço e disponibilidade | [produtos.md](entities/produtos.md) |
| 3 | `carrinhos` | Tabela central do domínio — lifecycle do carrinho com status, valores e contexto de sessão | [carrinhos.md](entities/carrinhos.md) |
| 4 | `itens_carrinho` | Itens adicionados a cada carrinho com snapshot de preço no momento da adição | [itens_carrinho.md](entities/itens_carrinho.md) |
| 5 | `eventos_carrinho` | Time series comportamental — ações do cliente na sessão de compra | [eventos_carrinho.md](entities/eventos_carrinho.md) |
| 6 | `eventos_resgate` | Campanhas de recuperação: envios, engajamento e resultado por canal | [eventos_resgate.md](entities/eventos_resgate.md) |
| 7 | `pedidos` | Pedidos finalizados — fecham o ciclo carrinho → conversão | [pedidos.md](entities/pedidos.md) |

---

## Documentação Complementar

- **Blueprint Canônico de Entidade**: [blueprint-entities-archive.md](entities/blueprint-entities-archive.md)
- **Relacionamentos & Cardinalidades**: [relationships.md](relationships.md)
- **Regras de Negócio & Validações**: [business-rules.md](business-rules.md)
- **DDL SQL (PostgreSQL)**: [`data/database/sql/`](../../database/sql/)

---

## Período dos Dados

- **Intervalo**: Janeiro 2026 – Junho 2026 (6 meses)
- **Granularidade temporal**: Timestamps com timezone (`TIMESTAMPTZ`)

## Volumes Estimados (Mock)

| Entidade | Volume |
|---|---|
| Clientes | ~1.000 |
| Produtos | ~200 |
| Carrinhos | ~5.000 (70% abandonados) |
| Itens de Carrinho | ~15.000 |
| Eventos de Carrinho | ~50.000 |
| Eventos de Resgate | ~3.500 |
| Pedidos | ~1.500 |
