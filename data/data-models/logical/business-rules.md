# Regras de Negócio & Lógica de Domínio (Single Source of Truth)

> **Documento:** Master Source of Truth (SSOT) de Regras de Negócio, Invariantes Contábeis, Políticas de Automação e Lógicas Analíticas/BI.  
> **Escopo:** Regras **transversais (cross-entity)**, lógica de domínio, máquinas de estado, políticas de resgate e fórmulas oficiais de KPIs analíticos.  
> **Separação de Responsabilidades:** Constraints e especificações de colunas isoladas (DDL) estão documentadas em [`entities/`](entities/). Arquitetura e suítes de teste Great Expectations estão em [`docs/specifications/data-quality-specification.md`](../../../docs/specifications/data-quality-specification.md). Decisões e apresentações comerciais estão em [`presentation/pitch/`](../../../presentation/pitch/).

---

## 1. Estados, Enums & Valores Canônicos de Referência (SSOT)

### 1.1 Status do Carrinho (`carrinhos.status`)

| Status | Descrição de Negócio | Terminal? |
|---|---|:---:|
| `'ativo'` | Carrinho em uso pelo cliente (sessão aberta ou aguardando retorno dentro da tolerância) | Não |
| `'abandonado'` | Cliente saiu sem completar compra e atingiu o timeout de inatividade (30 min) | Não |
| `'recuperado'` | Cliente retornou ao carrinho e reativou a sessão via campanha de resgate | Não |
| `'comprado'` | Transação concluída com sucesso e convertida em pedido de venda | ✅ Sim |
| `'expirado'` | Mais de 90 dias sem interação após o abandono; encerramento de campanhas | ✅ Sim |

### 1.2 Segmentos RFM (`clientes.segmento_rfm`)

| Segmento | Recência | Frequência | Valor Monetário (LTV) |
|---|---|---|---|
| `'premium'` | Compra nos últimos 30 dias | $\ge 5$ compras | LTV > R$ 2.000 |
| `'regular'` | Compra nos últimos 90 dias | 2 a 4 compras | LTV R$ 500 a R$ 2.000 |
| `'dormant'` | Última compra > 90 dias | $\ge 1$ compra | LTV < R$ 500 |
| `'novo'` | Nunca comprou | 0 compras | LTV = R$ 0,00 |

### 1.3 Canais de Resgate & Custos Operacionais Oficiais (`eventos_resgate.canal`)

| Canal | Custo Médio / Envio | Latência Típica | Papel Estratégico no Resgate |
|---|:---:|:---:|---|
| `'email'` | **R$ 0,05** | Minutos | Canal de escala, alta margem líquida e base do volume |
| `'push_app'` | **R$ 0,02** | Imediato | Canal proprietário de custo marginal mínimo para usuários engajados |
| `'sms'` | **R$ 0,15** | Segundos | Canal direto de alta visibilidade; requer qualificação de público |
| `'whatsapp'` | **R$ 0,30** | Segundos | Canal VIP de alta conversão unitária; prioritário para cestas de alto valor |

### 1.4 Tipos de Eventos Comportamentais (`eventos_carrinho.tipo_evento`)

| Evento | Etapa do Funil | Descrição de Negócio |
|---|---|---|
| `'view_produto'` | Topo do Funil | Cliente visualizou a página de detalhes de um produto |
| `'add_carrinho'` | Meio do Funil | Inserção de uma ou mais unidades de um SKU no carrinho |
| `'remove_carrinho'` | Fricção / Ajuste | Exclusão voluntária de um item previamente adicionado |
| `'update_quantidade'` | Ajuste de Cesta | Alteração na quantidade de itens de uma linha |
| `'view_checkout'` | Fundo do Funil | Visualização da tela de checkout e revisão da compra |
| `'inicio_pagamento'` | Intenção Final | Início do preenchimento dos dados de pagamento |
| `'erro_pagamento'` | Fricção Crítica | Recusa do gateway, cartão negado ou timeout de transação |
| `'abandono'` | Encerramento | Timeout de inatividade (30 min) ou encerramento explícito |
| `'retorno'` | Reativação | Reabertura do carrinho após ação de marketing de resgate |

### 1.5 Motivos de Abandono (`carrinhos.motivo_abandono`)

| Motivo | Descrição | Fator Causal Principal |
|---|---|---|
| `'preco'` | Preço alto do produto ou falta de desconto percebida | Sensibilidade a preço / pesquisa concorrente |
| `'frete'` | Custo de frete considerado excessivo pelo consumidor | Atrito logístico no checkout |
| `'pagamento'` | Erro técnico, recusa de cartão ou falta de método de pagamento | Fricção financeira no gateway |
| `'indecisao'` | Desistência sem motivo técnico claro / salvando para depois | Dúvida sobre o produto ou necessidade |
| `'estoque'` | Produto tornou-se indisponível durante a sessão | Quebra de estoque no catálogo |
| `'nao_informado'` | Motivo não identificado deterministicamente | Falta de telemetria explícita |

### 1.6 Status do Pedido (`pedidos.status_pedido`)

| Status | Descrição de Negócio | Terminal? |
|---|---|:---:|
| `'confirmado'` | Pagamento aprovado pelo gateway e ordem de pedido gerada | Não |
| `'enviado'` | Mercadoria despachada pelo centro de distribuição | Não |
| `'entregue'` | Mercadoria entregue com sucesso no endereço do comprador | ✅ Sim |
| `'cancelado'` | Pedido cancelado por solicitação, fraude ou estorno financeiro | ✅ Sim |

---

## 2. Domínio: Ciclo de Vida do Carrinho (`carrinhos`)

### 2.1 Máquina de Estados e Transições

```text
┌─────────────────────────────────────────────────────────────┐
│ ativo ────────────→ comprado (compra direta sem abandono)   │
│   │                                                         │
│   ▼ (30 min inatividade)                                    │
│ abandonado ───────→ recuperado ───────→ comprado            │
│   │                    │                     ↑              │
│   │                    └─────────────────────┘              │
│   ▼ (> 90 dias inativo)                                     │
│ expirado                                                    │
└─────────────────────────────────────────────────────────────┘
```

**Transições Proibidas (Hard Invariants)**:
- `comprado → *` (estado terminal imutável).
- `expirado → *` (estado terminal; encerra qualquer ação de CRM).
- `ativo → recuperado` (apenas carrinhos abandonados podem ser recuperados).
- `recuperado → abandonado` (se o cliente abandonar novamente após retorno, uma nova sessão/evento de abandono é registrado).

### 2.2 Critério de Detecção de Abandono

Um carrinho ativo é classificado como `'abandonado'` quando:
1. O cliente sai da sessão sem completar o checkout **E**
2. Decorrem **30 minutos** sem nova atividade registrada em `data_ultima_atividade`.
3. O timestamp da transição é registrado em `data_abandono`.

### 2.3 Regra de Inferência de Causa-Raiz do Abandono

Quando o motivo não for explicitamente declarado, o sistema infere o `motivo_abandono` aplicando a seguinte precedência determinística:

| Prioridade | Condição / Telemetria Observada | Motivo Atribuído |
|:---:|---|---|
| **1ª** | Existência do evento `'erro_pagamento'` na sessão | `'pagamento'` |
| **2ª** | `valor_frete > 15% do valor_subtotal` ou cálculo de frete sem avanço | `'frete'` |
| **3ª** | Presença do evento `'view_checkout'` sem avanço para `'inicio_pagamento'` | `'indecisao'` |
| **4ª** | Item com estoque zerado (`produtos.em_estoque = FALSE`) durante a sessão | `'estoque'` |
| **5ª** | Visualização repetida de cupons ou saída na tela de cupom | `'preco'` |
| **6ª** | Nenhuma das condições anteriores | `'nao_informado'` |

### 2.4 Critério de Expiração

Um carrinho abandonado transiciona automaticamente para `'expirado'` quando:
$$\text{status} = \text{'abandonado'} \quad \text{E} \quad (\text{NOW}() - \text{data\_abandono}) > 90 \text{ dias}$$
Ao expirar, qualquer campanha de resgate agendada é cancelada imediatamente.

### 2.5 Critério de Recuperação e Reativação de Sessão

Um carrinho abandonado é classificado como `'recuperado'` quando:
1. O cliente clica no link de uma campanha de recuperação ativa vinculada ao `resgate_id`.
2. Um evento `'retorno'` é disparado, inicializando um novo `sessao_id` associado ao `carrinho_id` existente.
3. Se o carrinho for finalizado em compra, o status evolui para `'comprado'` com atribuição de resgate (`pedidos.origem_recuperacao = TRUE`).

---

## 3. Domínio: Itens & Composição da Cesta (`itens_carrinho`)

### 3.1 Invariante Matemática da Linha
O valor total da linha de cada item deve obrigatoriamente satisfazer:
$$\text{preco\_total} = \text{quantidade} \times \text{preco\_unitario}$$
Discrepâncias de cálculo decorrentes de arredondamento não podem exceder R$ 0,01.

### 3.2 Imutabilidade do Snapshot de Preço
O campo `itens_carrinho.preco_unitario` representa o valor de venda vigente do produto exatamente no instante `data_adicao`. Alterações posteriores no catálogo geral (`produtos.preco_atual`) **não afetam** o preço congelado no carrinho ativo.

### 3.3 Controle de Remoção e Exclusão do Subtotal
- Um item é considerado ativo no carrinho enquanto `data_remocao IS NULL`.
- Quando o cliente remove o item, registra-se `data_remocao >= data_adicao`.
- Itens com `data_remocao IS NOT NULL` são **estritamente desconsiderados** no cálculo de `carrinhos.valor_subtotal`.

### 3.4 Conciliação Contábil do Subtotal do Carrinho
$$\text{carrinhos.valor\_subtotal} = \sum_{\substack{\text{itens do carrinho} \\ \text{data\_remocao IS NULL}}} \text{itens\_carrinho.preco\_total}$$

### 3.5 Múltiplas Adições na Mesma Sessão
A chave composta `(carrinho_id, produto_id)` permite múltiplos registros cronológicos caso o cliente remova um item e posteriormente o adicione novamente na mesma sessão.

---

## 4. Domínio: Catálogo, Precificação & Produtos (`produtos`)

### 4.1 Coerência de Promoção e Preço
Quando o produto está sob condição promocional, o preço vigente deve ser menor ou igual ao preço de tabela original:
$$\text{preco\_atual} \le \text{preco\_original}$$
Casos com $\text{preco\_atual} > \text{preco\_original}$ constituem inconsistência comercial de precificação (promoção invertida).

### 4.2 Disponibilidade e Trava de Estoque no Checkout
- Produtos com `ativo = FALSE` ou `em_estoque = FALSE` são bloqueados para novas adições.
- Se um item do carrinho tiver seu estoque esgotado durante a sessão, o checkout deve alertar o cliente antes da confirmação de pagamento.

### 4.3 Consistência de Rating e Prova Social
- Se `total_avaliacoes = 0` $\rightarrow$ `avaliacao_media` deve ser `NULL`.
- Se `total_avaliacoes > 0` $\rightarrow$ `avaliacao_media` deve pertencer ao intervalo $[1.0, 5.0]$.

---

## 5. Domínio: Cliente, Segmentação RFM & Governança de Contato (`clientes`)

### 5.1 Regras de Atualização da Segmentação RFM e LTV
- O `segmento_rfm` é recalculado a cada novo pedido confirmado.
- $\text{clientes.total\_compras} = \text{COUNT}(\text{pedidos confirmados ou entregues})$.
- $\text{clientes.lifetime\_value} = \sum \text{pedidos.valor\_total}$ (excluindo pedidos cancelados).
- $\text{clientes.data\_ultima\_compra} = \max(\text{pedidos.data\_pedido})$.
- Um cliente `'novo'` que completa o 1º pedido transiciona imediatamente para `'regular'` ou `'premium'` conforme o montante faturado.
- Clientes sem compras há mais de 90 dias transicionam para `'dormant'`.

### 5.2 Governança de Contato e Opt-in Mandatório (LGPD de Negócio)
Nenhuma comunicação de resgate pode ser enviada por um canal sem o respectivo consentimento ativo registrado em `clientes`:
- **E-mail:** Exige `permite_email = TRUE` e `email IS NOT NULL`.
- **SMS:** Exige `permite_sms = TRUE` e `telefone IS NOT NULL`.
- **WhatsApp:** Exige `permite_sms = TRUE` (ou opt-in de mensageria) e `telefone IS NOT NULL`.
- **Push Notification:** Exige `permite_push = TRUE`.

### 5.3 Fallback Operacional de Canais
Se o cliente não possuir opt-in em nenhum canal de comunicação, o carrinho abandonado **não recebe disparos ativos de outbound**, permanecendo elegível apenas para retargeting passivo na webstore.

---

## 6. Domínio: Motor de Recuperação de Carrinho (`eventos_resgate`)

### 6.1 Matriz de Decisão de Resgate (Topologia 3D)

A estratégia de recuperação cruza **Perfil RFM**, **Valor do Carrinho** e **Motivo de Abandono**:

| Perfil RFM | Valor da Cesta | Prioridade | Timing 1º Toque | Canal Primário | Política de Desconto | Frete Grátis |
|---|---|:---:|:---:|---|---|:---:|
| **Premium** | Qualquer valor | 🔴 Máxima | +1h | WhatsApp / E-mail | ❌ **Nenhum** (Atendimento VIP) | Sim, se motivo = frete |
| **Regular** | > R$ 200 | 🟡 Alta | +4h | E-mail + Push | 5% a 10% (a partir do 3º toque) | Sim, se motivo = frete |
| **Regular** | $\le$ R$ 200 | 🟢 Normal | +24h | E-mail | 5% (no 3º toque) | Não |
| **Dormant** | > R$ 150 | 🟡 Alta | +24h | E-mail + SMS | 10% a 15% (incentivo de reativação) | Sim |
| **Dormant** | $\le$ R$ 150 | 🟢 Normal | +48h | E-mail | 10% | Não |
| **Novo** | Qualquer valor | 🟡 Alta | +4h | E-mail | Cupom de 1ª Compra (10%) | Sim |

### 6.2 Políticas de Preservação de Margem
1. **Regra de Ouro do Cliente Premium:** Clientes *Premium* possuem alta propensão orgânica de retorno; comunicações no primeiro toque oferecem suporte consultivo ("Precisa de ajuda?") sem cupom de desconto, preservando integralmente a margem de contribuição.
2. **Abandono por Erro de Pagamento:** Prioriza canais de assistência técnica e métodos alternativos (PIX / Boleto) antes de concessão de incentivo monetário.
3. **Abandono por Frete:** Prioriza benefício de frete grátis (ou desconto equivalente ao frete) em vez de desconto percentual sobre o produto.

### 6.3 Sequência Padrão de Comunicação (Régua de 4 Toques)

Cada carrinho abandonado pode receber no máximo **4 comunicações**:

| Toque (#) | Timing Pós-Abandono | Template (`tipo_comunicacao`) | Canal Padrão | Oferta Padrão | Objetivo da Mensagem |
|:---:|:---:|---|---|---|---|
| **1** | +1h a +4h | `'lembrete_1h'` | E-mail / WhatsApp (VIP) | Nenhuma | Lembrete de conveniência e suporte |
| **2** | +24h | `'lembrete_24h'` | E-mail + Push | Nenhuma | Alerta de escassez e reserva de estoque |
| **3** | +48h | `'desconto_48h'` | E-mail + SMS | 5% a 10% desconto | Quebra de objeção financeira |
| **4** | +72h | `'urgencia_72h'` | E-mail + WhatsApp | 10% a 15% + Frete Grátis | Última chamada / urgência final |

### 6.4 Regras Operacionais de Disparo & Cadência
- **Cancelamento por Conversão:** Se o cliente converter em qualquer toque (`sucesso = TRUE`), todos os disparos agendados posteriores para aquele carrinho são **cancelados automaticamente**.
- **Janela de Cooldown:** Intervalo mínimo obrigatório de **4 horas** entre comunicações para o mesmo cliente, evitando fadiga de contato.
- **Bloqueio Terminal:** Não despachar mensagens se `carrinhos.status IN ('comprado', 'expirado')`.

### 6.5 Modelo Econômico e ROI Unitário de Resgate
$$\text{ROI Unitário} = \begin{cases} \dfrac{\text{valor\_pedido\_final} - \text{desconto\_oferecido} - \text{custo\_envio}}{\text{custo\_envio}}, & \text{se } \text{sucesso} = \text{TRUE} \\ -1.00 \quad (100\% \text{ de perda do custo de envio}), & \text{se } \text{sucesso} = \text{FALSE} \end{cases}$$

---

## 7. Domínio: Pedidos, Conversão & Atribuição (`pedidos`)

### 7.1 Unicidade de Conversão (Cardinalidade Estrita 1:1)
Cada sessão de carrinho de compras pode originar no máximo um único pedido faturado. A coluna `pedidos.carrinho_id` possui restrição de unicidade (`UNIQUE`), proibindo duplicidades de conversão.

### 7.2 Fechamento da Equação Contábil do Faturamento
$$\text{pedidos.valor\_total} = \text{pedidos.valor\_subtotal} + \text{pedidos.valor\_frete} - \text{pedidos.valor\_desconto}$$
O valor final do pedido pode diferir de `carrinhos.valor_total` devido à aplicação de cupons ou ajustes de frete concedidos pela régua de resgate.

### 7.3 Atribuição Mandatária de Resgate
- Se `pedidos.origem_recuperacao = TRUE` $\rightarrow$ `resgate_id` deve ser **não-nulo** (`IS NOT NULL`) e referenciar o evento de resgate correspondente.
- Se `pedidos.origem_recuperacao = FALSE` $\rightarrow$ `resgate_id` deve ser **estritamente nulo** (`IS NULL`).
- Quando um pedido de resgate é confirmado, `eventos_resgate.sucesso` é atualizado para `TRUE` e `eventos_resgate.valor_pedido_final` é preenchido com o valor total do pedido.

### 7.4 Trigger Contábil de Atualização do LTV
A confirmação de um pedido com status `'confirmado'` aciona a atualização atômica de:
- `clientes.total_compras += 1`
- `clientes.lifetime_value += pedidos.valor_total`
- `clientes.data_ultima_compra = pedidos.data_pedido`

---

## 8. Invariantes Cross-Entity & Consistência Temporal

### 8.1 Ordenação Cronológica de Eventos e Transações

| Regra Temporal | Entidades Envolvidas | Racional de Negócio |
|---|---|---|
| $\text{data\_criacao} \le \text{data\_ultima\_atividade} \le \text{data\_abandono}$ | `carrinhos` | O abandono só pode ser diagnosticado após o início e inatividade da sessão |
| $\text{data\_schedule} \le \text{data\_envio} \le \text{data\_abertura} \le \text{data\_primeiro\_clique} \le \text{data\_conversao}$ | `eventos_resgate` | Funil natural de engajamento da mensagem de resgate |
| $\text{data\_adicao} \le \text{data\_remocao}$ (quando removido) | `itens_carrinho` | Um item não pode ser removido antes de ter sido adicionado |
| $\text{pedidos.data\_pedido} \ge \text{carrinhos.data\_criacao}$ | `pedidos` ↔ `carrinhos` | O pedido é posterior ou contemporâneo à inicialização do carrinho |
| $\text{pedidos.data\_pedido} \ge \text{eventos\_resgate.data\_envio}$ | `pedidos` ↔ `eventos_resgate` | Conversão de resgate só ocorre após o despacho da comunicação |
| $\text{carrinhos.data\_criacao} \le \text{eventos\_carrinho.timestamp\_evento}$ | `carrinhos` ↔ `eventos_carrinho` | Eventos de telemetria pertencem ao período de vida da sessão |
| $\text{clientes.data\_criacao} \le \text{clientes.data\_primeira\_compra} \le \text{clientes.data\_ultima\_compra}$ | `clientes` | O histórico de compras respeita o momento de cadastro do consumidor |

### 8.2 Conciliação Financeira Ponta a Ponta

```text
[itens_carrinho.preco_total (ativos)]
       │ (Soma)
       ▼
[carrinhos.valor_subtotal] + [valor_frete] - [valor_desconto] = [carrinhos.valor_total]
                                                                      │
                                   ┌──────────────────────────────────┘
                                   │ (Se abandonado e resgatado)
                                   ▼
                       [eventos_resgate.desconto_oferecido]
                                   │
                                   ▼
[pedidos.valor_subtotal] + [pedidos.valor_frete] - [pedidos.valor_desconto] = [pedidos.valor_total]
```

---

## 9. Lógica Canônica de BI & Fórmulas de Métricas de Negócio (Camada Analítica)

### 9.1 Camada 1: Conversão & Recuperação Global

#### KPI-01: Taxa de Abandono de Carrinho
$$\text{Taxa de Abandono (\%)} = \left( \frac{\text{COUNT}(\text{carrinhos com status = 'abandonado'})}{\text{COUNT}(\text{total geral de carrinhos criados})} \right) \times 100$$
- **Benchmark / Referência:** ~70% (Baymard Institute: 69.8%).

#### KPI-02: Taxa de Recuperação de Carrinhos Abandonados
$$\text{Taxa de Recuperação (\%)} = \left( \frac{\text{COUNT}(\text{carrinhos recuperados com pedidos.origem\_recuperacao = TRUE})}{\text{COUNT}(\text{carrinhos com status = 'abandonado'})} \right) \times 100$$
- **Benchmark / Referência:** 5% a 15% (Meta operacional do case: ~10.1%).

#### KPI-03: Lift de Conversão de Resgate
$$\text{Lift de Conversão (\%)} = \left( \frac{\text{Taxa de Conversão com Resgate} - \text{Taxa de Conversão Orgânica}}{\text{Taxa de Conversão Orgânica}} \right) \times 100$$
- **Meta Operacional:** $+50\%$ de incremento sobre a taxa base sem intervenção.

---

### 9.2 Camada 2: Eficiência por Canal de Resgate

#### KPI-04: Funil de Engajamento por Canal
- **Taxa de Abertura (%):** $\dfrac{\text{Total de Aberturas}}{\text{Total de Envios}} \times 100$
- **Taxa de Clique / CTR (%):** $\dfrac{\text{Total de Cliques}}{\text{Total de Aberturas}} \times 100$
- **Taxa de Conversão End-to-End (%):** $\dfrac{\text{Total de Pedidos Convertidos}}{\text{Total de Envios}} \times 100$

**Benchmarks Operacionais por Canal:**

| Canal | Abertura | CTR (Abertura $\rightarrow$ Clique) | Clique $\rightarrow$ Conversão | Conversão End-to-End |
|---|:---:|:---:|:---:|:---:|
| **E-mail** | ~42% | ~28% | ~15% | ~4.5% |
| **WhatsApp** | ~68% | ~35% | ~18% | ~2.5% |
| **SMS** | ~55% | ~22% | ~14% | ~1.8% |
| **Push App** | ~30% | ~18% | ~12% | ~1.2% |

---

### 9.3 Camada 3: Eficiência por Segmento RFM & LTV

#### KPI-05: Taxa de Recuperação por Segmento RFM
$$\text{Taxa Segmento (\%)} = \left( \frac{\text{Carrinhos Recuperados no Segmento}}{\text{Carrinhos Abandonados no Segmento}} \right) \times 100$$
- **Desempenho Alvo por Perfil:**
  - `Premium`: ~18% (alta responsividade / atendimento prioritário)
  - `Novo`: ~12% (reatividade ao cupom de 1ª compra)
  - `Regular`: ~10% (maior volume absoluto)
  - `Dormant`: ~6% (reativação de base inativa)
- **Ratio Premium / Dormant:** **3.0x** (comprova matematicamente a necessidade de segmentar a régua).

#### KPI-06: Valor Financeiro em Risco por Faixa de LTV
$$\text{Valor em Risco (R\$)} = \sum \text{carrinhos.valor\_total} \quad \text{onde } \text{status} = \text{'abandonado'} \quad (\text{agrupado por } \text{clientes.segmento\_rfm})$$

---

### 9.4 Camada 4: Eficiência Operacional & Financeira (ROI)

#### KPI-07: Retorno sobre Investimento de Resgate (ROI Líquido Global)
$$\text{ROI Global} = \frac{\sum \text{Receita dos Pedidos Recuperados} - \sum \text{Descontos Concedidos} - \sum \text{Custos de Envio}}{\sum \text{Custos de Envio}}$$
- **Meta Operacional:** Multiplicador de ROI consolidado $\ge 30\text{x}$ (Dataset opera em ~45x).

#### KPI-08: Custo de Aquisição por Resgate (CAC de Resgate)
$$\text{CAC de Resgate (R\$)} = \frac{\sum \text{Custos de Disparo do Canal}}{\text{Total de Pedidos Recuperados pelo Canal}}$$
- **Diretriz de Margem:** O CAC de Resgate deve representar **menos de 1%** do ticket médio recuperado.

---

### 9.5 Camada 5: Timing & Cadência de Sequência

#### KPI-09: Concentração de Conversão por Toque da Régua
- `1º Toque (lembrete_1h)`: Concentra ~35% das conversões totais.
- `2º Toque (lembrete_24h)`: Concentra ~30% das conversões.
- `3º Toque (desconto_48h)`: Concentra ~25% das conversões.
- `4º Toque (urgencia_72h)`: Concentra ~10% das conversões.

#### KPI-10: Tempo Médio de Resgate (Abandono $\rightarrow$ Conversão)
Tempo médio decorrido entre a detecção do abandono e a confirmação do pedido resgatado: **~28 horas**.

---

### 9.6 Score Heurístico de Risco da Sessão (`RISK_SCORE`)

Pontuação calculada durante a navegação para triagem em tempo real e priorização de atendimento:

$$\text{RISK\_SCORE} = \text{Fator\_Valor} + \text{Fator\_Dispositivo} + \text{Fator\_Relacionamento} + \text{Fator\_Inatividade\_Checkout} + \text{Fator\_Atrito}$$

1. **Fator Valor:** Se $\text{valor\_total} > \text{R\$ 500,00} \rightarrow +2$; senão $+1$.
2. **Fator Dispositivo:** Se $\text{dispositivo} = \text{'mobile'} \rightarrow +2$; senão $+1$.
3. **Fator Relacionamento:** Se $\text{cliente\_novo} = \text{TRUE} \rightarrow +2$; senão $+1$.
4. **Fator Inatividade no Checkout:** Se tempo parado na etapa de checkout $\ge 3\text{ min} \rightarrow +2$; senão $+1$.
5. **Fator Atrito / Erro Técnico:** Se evento `'erro_pagamento'` ou $\text{frete} > 15\% \text{ subtotal} \rightarrow +3$; senão $0$.

**Classificação do Risco:**
- 🔴 **`CRÍTICO`**: $\text{RISK\_SCORE} \ge 8$
- 🟠 **`ALTO`**: $6 \le \text{RISK\_SCORE} < 8$
- 🟡 **`MÉDIO`**: $4 \le \text{RISK\_SCORE} < 6$
- 🟢 **`BAIXO`**: $\text{RISK\_SCORE} < 4$

---

### 9.7 Score Prescritivo de Viabilidade de Recuperação (`RECOVERY_VIABILITY`)

Modelo de priorização econômica que calcula o retorno financeiro esperado antes de disparar uma campanha:

#### 1. Probabilidade Estimada de Recuperação ($P_{\text{recuperacao}}$):
$$P_{\text{recuperacao}} = \min\left(0.50, \max\left(0.01, P_{\text{base}}(\text{RFM}) \times \text{Fator\_Motivo} \times \text{Fator\_Valor}\right)\right)$$

- **$P_{\text{base}}(\text{RFM})$:** `premium` = 0.18, `novo` = 0.12, `regular` = 0.10, `dormant` = 0.06.
- **$\text{Fator\_Motivo}$:** `indecisao` = 1.2, `frete` = 1.1, `preco` = 1.0, `pagamento` = 0.8, `estoque` = 0.3, `outros` = 0.9.
- **$\text{Fator\_Valor}$:** $> \text{R\$ 500}$ = 1.1, $\ge \text{R\$ 100}$ = 1.0, $< \text{R\$ 100}$ = 0.9.

#### 2. Retorno Esperado & Expected ROI:
$$\text{Retorno Esperado (R\$)} = P_{\text{recuperacao}} \times \text{carrinhos.valor\_total}$$
$$\text{Expected ROI} = \frac{\text{Retorno Esperado}}{\text{Custo Estimado do Canal}}$$

#### 3. Matriz de Decisão Prescritiva:

| Faixa de Viabilidade | Critérios Financeiros | Ação Prescrita de Negócio |
|---|---|---|
| 🟢 **Alta Viabilidade** | $\text{Expected ROI} \ge 50\text{x} \quad \text{E} \quad \text{Retorno Esperado} \ge \text{R\$ 10,00}$ | **Disparo Imediato (+1h)** via canal de alto impacto (WhatsApp/E-mail VIP) |
| 🟡 **Média Viabilidade** | $\text{Expected ROI} \ge 10\text{x} \quad \text{E} \quad \text{Retorno Esperado} \ge \text{R\$ 2,00}$ | **Régua Padrão (+24h)** via automação de baixo custo (E-mail + Push) |
| 🔴 **Baixa Viabilidade** | $\text{Expected ROI} < 10\text{x} \quad \text{OU} \quad \text{Retorno Esperado} < \text{R\$ 2,00}$ | **Não disparar outbound**; direcionar apenas para retargeting passivo |
