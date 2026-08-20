# Entidade: `carrinhos`

**Descrição**: Tabela central do domínio. Representa cada carrinho de compras criado no marketplace, rastreando seu ciclo de vida completo desde a criação até o abandono, recuperação ou conversão.

---

## Atributos

| Campo | Tipo | PK/FK | Nullable | Default | Descrição |
|---|---|---|---|---|---|
| `carrinho_id` | INT | PK | NOT NULL | AUTO | Identificador único do carrinho |
| `cliente_id` | INT | FK → clientes | NOT NULL | — | Cliente dono do carrinho |
| `data_criacao` | TIMESTAMPTZ | — | NOT NULL | NOW() | Timestamp de criação do carrinho |
| `data_ultima_atividade` | TIMESTAMPTZ | — | NULL | — | Timestamp da última interação (add/remove item, view checkout) |
| `data_abandono` | TIMESTAMPTZ | — | NULL | — | Timestamp em que o carrinho foi classificado como abandonado |
| `status` | VARCHAR(20) | — | NOT NULL | 'ativo' | Status do lifecycle: `'ativo'`, `'abandonado'`, `'recuperado'`, `'comprado'`, `'expirado'` |
| `motivo_abandono` | VARCHAR(100) | — | NULL | — | Motivo do abandono: `'preco'`, `'frete'`, `'pagamento'`, `'indecisao'`, `'estoque'`, `'nao_informado'` |
| `valor_subtotal` | DECIMAL(10,2) | — | NULL | — | Soma dos itens sem frete/desconto |
| `valor_frete` | DECIMAL(10,2) | — | NULL | — | Custo de frete calculado |
| `valor_desconto` | DECIMAL(10,2) | — | NULL | 0.00 | Valor de desconto aplicado |
| `valor_total` | DECIMAL(10,2) | — | NULL | — | Valor final (subtotal + frete - desconto) |
| `duracao_sessao_minutos` | INT | — | NULL | — | Duração da sessão em minutos |
| `dispositivo` | VARCHAR(50) | — | NULL | — | Dispositivo: `'mobile'`, `'desktop'`, `'tablet'` |
| `browser` | VARCHAR(50) | — | NULL | — | Navegador utilizado |
| `canal_origem` | VARCHAR(100) | — | NULL | — | Canal de aquisição: `'google'`, `'facebook'`, `'direct'`, `'email'`, `'instagram'` |
| `cliente_novo` | BOOLEAN | — | NOT NULL | FALSE | Cliente na primeira compra? |
| `tem_conta_criada` | BOOLEAN | — | NOT NULL | FALSE | Cliente tem conta (vs. checkout como guest) |
| `created_at` | TIMESTAMPTZ | — | NOT NULL | NOW() | Audit: data de criação do registro |
| `updated_at` | TIMESTAMPTZ | — | NOT NULL | NOW() | Audit: data de última atualização |

---

## Ciclo de Vida (Status)

```
ativo → abandonado → recuperado → comprado
  │                                    ↑
  └────────────────────────────────────┘  (compra direta)
  
abandonado → expirado  (após 90 dias sem interação)
```

## Constraints

| Tipo | Campo(s) | Regra |
|---|---|---|
| CHECK | `status` | `∈ {'ativo', 'abandonado', 'recuperado', 'comprado', 'expirado'}` |
| CHECK | `dispositivo` | `∈ {'mobile', 'desktop', 'tablet'}` |
| CHECK | `valor_frete` | `>= 0` |
| CHECK | `valor_desconto` | `>= 0` |
| CHECK | `valor_total` | `>= 0` |
| NOT NULL | `cliente_id`, `data_criacao`, `status`, `cliente_novo`, `tem_conta_criada`, `created_at`, `updated_at` | Campos obrigatórios |

---

## Observações

- `data_abandono` é populado quando o sistema detecta inatividade ou saída sem compra
- `status = 'expirado'` encerra campanhas de resgate (regra: 90 dias após abandono)
- `canal_origem` renomeado de `source_origem` para evitar redundância pt/en
- `valor_total` não é coluna calculada — é atualizado pela aplicação para permitir ajustes manuais
- `cliente_novo` + `tem_conta_criada` são flags úteis para segmentação de campanhas
