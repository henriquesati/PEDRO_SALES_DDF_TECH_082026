# Entidade: `eventos_resgate`

**Descrição**: Registra cada ação de campanha de recuperação de carrinho: envio de comunicação, engajamento do cliente (abertura, clique) e resultado final (conversão ou não). Um carrinho abandonado pode receber múltiplas tentativas de resgate em diferentes canais.

---

## Atributos

| Campo | Tipo | PK/FK | Nullable | Default | Descrição |
|---|---|---|---|---|---|
| `resgate_id` | BIGINT | PK | NOT NULL | AUTO | Identificador único do evento de resgate |
| `carrinho_id` | INT | FK → carrinhos | NOT NULL | — | Carrinho alvo da recuperação |
| `cliente_id` | INT | FK → clientes | NOT NULL | — | Cliente alvo |
| `canal` | VARCHAR(50) | — | NOT NULL | — | Canal de comunicação: `'email'`, `'sms'`, `'push_app'`, `'whatsapp'` |
| `tipo_comunicacao` | VARCHAR(50) | — | NOT NULL | — | Template/timing: `'lembrete_1h'`, `'lembrete_24h'`, `'desconto_48h'`, `'urgencia_72h'` |
| `data_schedule` | TIMESTAMPTZ | — | NOT NULL | — | Quando o envio foi programado |
| `data_envio` | TIMESTAMPTZ | — | NULL | — | Quando foi efetivamente enviado (NULL = pendente) |
| `assunto` | VARCHAR(255) | — | NULL | — | Assunto/título da comunicação |
| `desconto_oferecido` | DECIMAL(10,2) | — | NULL | 0.00 | Valor de desconto oferecido na campanha |
| `frete_gratis_oferecido` | BOOLEAN | — | NOT NULL | FALSE | Se ofereceu frete grátis |
| `custo_envio` | DECIMAL(10,2) | — | NOT NULL | — | Custo do envio (varia por canal: email ~R$0.05, SMS ~R$0.15, WhatsApp ~R$0.30) |
| `data_abertura` | TIMESTAMPTZ | — | NULL | — | Quando o cliente abriu/visualizou a comunicação |
| `data_primeiro_clique` | TIMESTAMPTZ | — | NULL | — | Quando o cliente clicou no link |
| `link_clicado` | VARCHAR(500) | — | NULL | — | URL do link clicado |
| `data_conversao` | TIMESTAMPTZ | — | NULL | — | Quando o cliente finalizou a compra (se converteu) |
| `sucesso` | BOOLEAN | — | NOT NULL | FALSE | Se resultou em conversão |
| `valor_pedido_final` | DECIMAL(10,2) | — | NULL | — | Valor do pedido gerado (se converteu) |
| `created_at` | TIMESTAMPTZ | — | NOT NULL | NOW() | Audit: criação do registro |

## Constraints

| Tipo | Campo(s) | Regra |
|---|---|---|
| CHECK | `canal` | `∈ {'email', 'sms', 'push_app', 'whatsapp'}` |
| CHECK | `tipo_comunicacao` | `∈ {'lembrete_1h', 'lembrete_24h', 'desconto_48h', 'urgencia_72h'}` |
| CHECK | `custo_envio` | `>= 0` |
| NOT NULL | `carrinho_id`, `cliente_id`, `canal`, `tipo_comunicacao`, `data_schedule`, `custo_envio`, `frete_gratis_oferecido`, `sucesso`, `created_at` | Campos obrigatórios |

---

## Observações

- `tipo_comunicacao` renomeado de `tipo_email` — o modelo suporta múltiplos canais, não apenas email
- `custo_envio` substituiu a coluna calculada `roi` — o ROI agora é calculado na camada de análise com fórmula flexível: `(valor_pedido_final - desconto_oferecido - custo_envio) / custo_envio`
- `assunto` renomeado de `assunto_email` — generaliza para qualquer canal
- `frete_gratis_oferecido` renomeado de `valor_frete_gratis` (era BOOLEAN com nome de valor)
- Campos de engagement de `itens_carrinho` (`foi_visualizado_email`, etc.) foram absorvidos aqui nos campos `data_abertura`, `data_primeiro_clique` e `sucesso`
- Um carrinho pode ter **múltiplos eventos de resgate** (ex: email 1h + SMS 24h + email com desconto 48h)
