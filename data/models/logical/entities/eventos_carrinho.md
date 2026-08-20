# Entidade: `eventos_carrinho`

**Descrição**: Time series comportamental que registra cada ação do cliente durante a sessão de compra. Essencial para análise de funil, detecção de abandono e modelos preditivos.

---

## Atributos

| Campo | Tipo | PK/FK | Nullable | Default | Descrição |
|---|---|---|---|---|---|
| `evento_id` | BIGINT | PK | NOT NULL | AUTO | Identificador único do evento |
| `carrinho_id` | INT | FK → carrinhos | NOT NULL | — | Carrinho associado |
| `cliente_id` | INT | FK → clientes | NOT NULL | — | Cliente que realizou a ação |
| `sessao_id` | VARCHAR(50) | — | NULL | — | Identificador da sessão (agrupa eventos de uma mesma visita) |
| `timestamp_evento` | TIMESTAMPTZ | — | NOT NULL | NOW() | Momento exato do evento |
| `tipo_evento` | VARCHAR(50) | — | NOT NULL | — | Tipo do evento (ver lista abaixo) |
| `duracao_evento_segundos` | INT | — | NULL | — | Tempo gasto no evento (ex: tempo na página de checkout) |
| `dados_evento` | JSONB | — | NULL | — | Dados contextuais customizados por tipo de evento |

---

## Tipos de Evento (`tipo_evento`)

| Valor | Descrição |
|---|---|
| `'view_produto'` | Cliente visualizou um produto |
| `'add_carrinho'` | Adicionou item ao carrinho |
| `'remove_carrinho'` | Removeu item do carrinho |
| `'update_quantidade'` | Alterou quantidade de um item |
| `'view_checkout'` | Visualizou a página de checkout |
| `'inicio_pagamento'` | Começou a preencher dados de pagamento |
| `'erro_pagamento'` | Ocorreu erro ao tentar pagar |
| `'abandono'` | Saiu sem completar a compra |
| `'retorno'` | Voltou ao carrinho após período de inatividade |

---

## Exemplo de `dados_evento` (JSONB)

```json
{
  "produto_id": 12345,
  "categoria": "Eletrônicos",
  "preco": 299.99,
  "estoque_disponivel": true,
  "tempo_no_site_segundos": 45
}
```

## Constraints

| Tipo | Campo(s) | Regra |
|---|---|---|
| CHECK | `tipo_evento` | `∈ {'view_produto', 'add_carrinho', 'remove_carrinho', 'update_quantidade', 'view_checkout', 'inicio_pagamento', 'erro_pagamento', 'abandono', 'retorno'}` |
| NOT NULL | `carrinho_id`, `cliente_id`, `timestamp_evento`, `tipo_evento` | Campos obrigatórios |

---

## Observações

- `sessao_id` foi adicionado para agrupar eventos de uma mesma visita (permite análise de sessão sem tabela separada)
- `timestamp_evento` renomeado de `timestamp` para evitar conflito com palavra reservada SQL
- `JSONB` (PostgreSQL) em vez de `JSON` para permitir indexação e consultas dentro do campo
- Removido `PARTITION BY RANGE` do modelo — desnecessário para o volume de dados de demo/pitch
- Alto volume esperado (~50.000 registros para 6 meses de dados mock)
