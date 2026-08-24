# Regras de Negócio & Validações

> Este documento contém exclusivamente regras de negócio **transversais** (cross-entity) e lógica de domínio.  
> Constraints específicas de cada entidade (valores válidos, unicidade, checks) estão documentadas nos respectivos arquivos em [`entities/`](entities/).

---

## 1. Estados & Valores de Referência (Single Source of Truth)

### 1.1 Status do Carrinho (`carrinhos.status`)

| Status | Descrição | Terminal? |
|---|---|---|
| `'ativo'` | Carrinho em uso pelo cliente (sessão ativa ou aguardando retorno) | Não |
| `'abandonado'` | Cliente saiu sem completar compra e atingiu o timeout de inatividade | Não |
| `'recuperado'` | Cliente retornou ao carrinho via campanha de resgate | Não |
| `'comprado'` | Carrinho convertido em pedido (compra finalizada) | ✅ Sim |
| `'expirado'` | Mais de 90 dias sem interação após abandono | ✅ Sim |

### 1.2 Segmentos RFM (`clientes.segmento_rfm`)

| Segmento | Recency | Frequency | Monetary |
|---|---|---|---|
| `'premium'` | Compra nos últimos 30 dias | 5+ compras | LTV > R$ 2.000 |
| `'regular'` | Compra nos últimos 90 dias | 2–4 compras | LTV R$ 500–2.000 |
| `'dormant'` | Última compra > 90 dias | 1 compra | LTV < R$ 500 |
| `'novo'` | Nunca comprou | 0 compras | LTV = 0 |

### 1.3 Canais de Resgate (`eventos_resgate.canal`)

| Canal | Custo Médio/Envio | Latência Típica |
|---|---|---|
| `'email'` | R$ 0,05 | Minutos |
| `'sms'` | R$ 0,15 | Segundos |
| `'push_app'` | R$ 0,02 | Imediato |
| `'whatsapp'` | R$ 0,30 | Segundos |

### 1.4 Tipos de Evento (`eventos_carrinho.tipo_evento`)

| Evento | Descrição |
|---|---|
| `'view_produto'` | Cliente visualizou um produto |
| `'add_carrinho'` | Adicionou item ao carrinho |
| `'remove_carrinho'` | Removeu item do carrinho |
| `'update_quantidade'` | Alterou quantidade de um item |
| `'view_checkout'` | Visualizou a página de checkout |
| `'inicio_pagamento'` | Começou a preencher pagamento |
| `'erro_pagamento'` | Erro ao tentar pagar |
| `'abandono'` | Saiu sem completar a compra |
| `'retorno'` | Voltou ao carrinho após inatividade |

### 1.5 Motivos de Abandono (`carrinhos.motivo_abandono`)

| Motivo | Descrição |
|---|---|
| `'preco'` | Preço alto ou falta de desconto |
| `'frete'` | Valor de frete inaceitável |
| `'pagamento'` | Erro ou dificuldade no pagamento |
| `'indecisao'` | Desistência sem motivo claro |
| `'estoque'` | Produto ficou indisponível |
| `'nao_informado'` | Motivo não identificável |

---

## 2. Domínio: Carrinho

### 2.1 Ciclo de Vida — Transições de Status

```
ativo      → abandonado   (inatividade ou saída sem compra)
ativo      → comprado     (compra direta sem abandono)
abandonado → recuperado   (cliente retorna via campanha de resgate)
recuperado → comprado     (cliente finaliza compra após retorno)
abandonado → expirado     (90 dias sem interação)
```

**Transições proibidas**:
- `comprado → *` (estado terminal)
- `expirado → *` (estado terminal)
- `ativo → recuperado` (só carrinhos abandonados podem ser recuperados)
- `recuperado → abandonado` (se abandonar novamente, gera novo carrinho/evento)

### 2.2 Regras de Classificação

#### 2.2.1 Classificação de Abandono

Um carrinho é classificado como `'abandonado'` quando:
1. O cliente sai da sessão sem completar a compra **E**
2. Passam-se **30 minutos** sem nova atividade

O `motivo_abandono` é inferido pelo último evento antes do abandono:

| Último Evento / Condição | Motivo Atribuído |
|---|---|
| `'erro_pagamento'` | `'pagamento'` |
| `'view_checkout'` sem `'inicio_pagamento'` | `'indecisao'` |
| `valor_frete > 15% do valor_subtotal` | `'frete'` |
| Nenhuma condição acima | `'nao_informado'` |

#### 2.2.2 Classificação de Expiração

Um carrinho abandonado é classificado como `'expirado'` quando:
- `status = 'abandonado'` **E** `NOW() - data_abandono > 90 dias`
- Todas as campanhas de resgate cessam automaticamente

#### 2.2.3 Classificação de Recuperação

Um carrinho é classificado como `'recuperado'` quando:
- `status = 'abandonado'` **E** o cliente retorna ao carrinho (evento `'retorno'`)
- O retorno deve estar vinculado a uma campanha de resgate (`resgate_id` no evento ou na sessão)

---

## 3. Domínio: Recuperação de Carrinho

### 3.1 Topologia de Resgate

> A estratégia de resgate **não é igual** à segmentação RFM.  
> RFM classifica **quem é o cliente**. A topologia de resgate define **o que fazer** combinando múltiplas dimensões.

A decisão de resgate é uma **matriz de 3 dimensões**:

| Dimensão | Fonte | Pergunta que responde |
|---|---|---|
| **Perfil do Cliente** | `clientes.segmento_rfm` | Quem é? Qual prioridade? |
| **Valor do Carrinho** | `carrinhos.valor_total` | Vale o investimento? |
| **Motivo do Abandono** | `carrinhos.motivo_abandono` | Qual abordagem usar? |

#### Matriz de Decisão

| Perfil (RFM) | Valor Carrinho | Prioridade | Timing 1ª Ação | Desconto | Frete Grátis |
|---|---|---|---|---|---|
| Premium | Qualquer | 🔴 Máxima | +1h | Não necessário | Sim, se motivo = frete |
| Regular | > R$ 200 | 🟡 Alta | +4h | 5–10% | Sim, se motivo = frete |
| Regular | ≤ R$ 200 | 🟢 Normal | +24h | 5% | Não |
| Dormant | > R$ 150 | 🟡 Alta | +24h | 10–15% | Sim |
| Dormant | ≤ R$ 150 | 🟢 Normal | +48h | 10% | Não |
| Novo | Qualquer | 🟡 Alta | +4h | Cupom 1ª compra (10%) | Sim |

#### Adaptação por Motivo de Abandono

| Motivo | Ajuste na Estratégia |
|---|---|
| `'frete'` | Priorizar oferta de frete grátis, independente do perfil |
| `'pagamento'` | Destacar métodos alternativos (PIX, boleto) na comunicação |
| `'preco'` | Aplicar desconto progressivo na sequência de resgate |
| `'indecisao'` | Usar social proof (avaliações, "X pessoas compraram") |
| `'estoque'` | Notificar quando produto voltar ao estoque |

### 3.2 Sequência de Comunicação

Cada carrinho abandonado pode receber no máximo **4 comunicações** seguindo a escalada:

| # | Timing | Template (`tipo_comunicacao`) | Canal Primário | Oferta Padrão |
|---|---|---|---|---|
| 1 | +1h a +4h | `'lembrete_1h'` | email | Nenhum |
| 2 | +24h | `'lembrete_24h'` | email + push | Nenhum |
| 3 | +48h | `'desconto_48h'` | email + SMS | 5–10% desconto |
| 4 | +72h | `'urgencia_72h'` | email + WhatsApp | 10–15% + frete grátis |

**Regras de envio**:
- Respeitar opt-in do cliente (`permite_email`, `permite_sms`, `permite_push`)
- Intervalo mínimo de **4 horas** entre comunicações para o mesmo cliente
- Não enviar se `carrinhos.status ∈ {'comprado', 'expirado'}`
- Timing do 1º envio é ajustado pela topologia de resgate (seção 3.1)

### 3.3 Propriedades Financeiras do Resgate

#### ROI (Return on Investment)

| Propriedade | Definição |
|---|---|
| **Fórmula** | `(valor_pedido_final - desconto_oferecido - custo_envio) / custo_envio` |
| **Quando `sucesso = TRUE`** | Calculado pela fórmula acima |
| **Quando `sucesso = FALSE`** | `-1` (100% de perda do custo investido) |
| **Camada de cálculo** | Análise (view SQL / BI) — não armazenado como coluna |
| **Granularidade** | Por evento de resgate individual |

#### Custo por Canal

| Canal | Custo/Envio | Fonte |
|---|---|---|
| email | R$ 0,05 | `eventos_resgate.custo_envio` |
| sms | R$ 0,15 | `eventos_resgate.custo_envio` |
| push_app | R$ 0,02 | `eventos_resgate.custo_envio` |
| whatsapp | R$ 0,30 | `eventos_resgate.custo_envio` |

---

## 4. Domínio: Cliente

### 4.1 Segmentação RFM

Os critérios de classificação estão definidos na seção 1.2 (SSOT). Aqui documentamos as **regras de atualização**:

- `segmento_rfm` é recalculado a cada novo pedido confirmado
- `lifetime_value` = soma de `pedidos.valor_total` onde `status_pedido ≠ 'cancelado'`
- `total_compras` = contagem de `pedidos` onde `status_pedido ≠ 'cancelado'`
- `data_ultima_compra` = MAX(`pedidos.data_pedido`)
- Um cliente `'novo'` que realiza a primeira compra transiciona para `'regular'` ou `'premium'` conforme o valor

### 4.2 Preferências de Contato

- Os campos `permite_email`, `permite_sms`, `permite_push` são **hard constraints** — uma campanha NUNCA deve ser enviada em canal não autorizado
- Se o cliente não autoriza nenhum canal, o carrinho abandonado não recebe resgate
- Default: apenas `permite_email = TRUE`

---

## 5. Regras Transversais

### 5.1 Valores Monetários

- Todos os valores monetários usam `DECIMAL(10,2)` — nunca `FLOAT`
- Arredondamento: `ROUND(valor, 2)` em todas as operações
- `valor_desconto ≤ valor_subtotal` (desconto não pode superar o valor dos itens)
- `valor_frete ≥ 0`, `valor_total ≥ 0`

### 5.2 Cálculos Derivados

| Cálculo | Fórmula | Entidade |
|---|---|---|
| Subtotal do carrinho | `SUM(itens_carrinho.preco_total)` para itens sem `data_remocao` | `carrinhos` |
| Total do carrinho | `valor_subtotal + valor_frete - valor_desconto` | `carrinhos` |
| Total do item | `quantidade × preco_unitario` | `itens_carrinho` |

### 5.3 Consistência Temporal

Regras de ordenação temporal entre entidades:

| Regra | Entidades Envolvidas |
|---|---|
| `data_criacao ≤ data_ultima_atividade ≤ data_abandono` | `carrinhos` |
| `data_schedule ≤ data_envio ≤ data_abertura ≤ data_primeiro_clique ≤ data_conversao` | `eventos_resgate` |
| `data_adicao ≤ data_remocao` (quando removido) | `itens_carrinho` |
| `pedidos.data_pedido ≥ carrinhos.data_criacao` | `pedidos` ↔ `carrinhos` |
| `carrinhos.data_criacao ≤ eventos_carrinho.timestamp_evento` | `carrinhos` ↔ `eventos_carrinho` |

### 5.4 Consistência Carrinho ↔ Pedido

- Quando `carrinhos.status = 'comprado'`: deve existir exatamente 1 registro em `pedidos` com mesmo `carrinho_id`
- `pedidos.valor_total` **pode diferir** de `carrinhos.valor_total` (desconto de resgate aplicado no checkout)
- Quando `pedidos.origem_recuperacao = TRUE`: `pedidos.valor_total` deve ser consistente com `eventos_resgate.valor_pedido_final`
