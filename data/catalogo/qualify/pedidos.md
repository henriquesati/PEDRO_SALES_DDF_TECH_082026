# Dicionário de Dados: pedidos

Dicionário de dados da entidade de Pedidos, representando os carrinhos convertidos em compras finalizadas, métodos de pagamento, custos de frete e rastreio de origem de campanhas de resgate.

---

## 📌 Identificação do Ativo de Dados

- **Nome Físico:** `PEDIDOS`
- **Nome de Exibição (Display Name):** `pedidos`
- **Data Asset ID (Dadosfera):** `7f82a988-8e68-416a-b6fa-5007c4789d1a`
- **URL Direta no Catálogo:** [Acessar pedidos](https://app.dadosfera.ai/pt-BR/catalog/data-assets/7f82a988-8e68-416a-b6fa-5007c4789d1a)

---

## 💼 Visão de Negócio

### Descrição de Negócio
A tabela de pedidos consolida todas as compras efetivadas no marketplace, sendo a entidade principal para o cálculo de receita gerada e faturamento do e-commerce. Ela conecta os pedidos ao carrinho original de compras e ao evento de resgate (se aplicável), permitindo ao time financeiro e de marketing atribuir conversões diretamente a campanhas de e-mail, SMS, push e WhatsApp.

### Principais Casos de Uso
- Calcular a receita total gerada a partir de campanhas de recuperação de carrinho abandonado (`origem_resgate = TRUE`).
- Analisar a distribuição de métodos de pagamento preferidos (Pix, Cartão, Boleto) e parcelamentos nas compras recuperadas.
- Rastrear a taxa de conversão final e a receita líquida deduzindo descontos e fretes.

---

## ⚙️ Visão Técnico-Operacional

### Especificações Gerais
- **Zona do Data Lakehouse:** Qualify (Silver)
- **Formato Físico:** Tabela Snowflake
- **Localização Física:** `CART_RECOVERY.PEDIDOS`
- **Granularidade:** Uma linha por pedido único de compra aprovado ou registrado.
- **Frequência de Atualização:** Batch diário.
- **Volume de Registros:** 2.000 registros (~258 KB).

### Integridade e Relacionamentos (Linhagem)
- **Origem (Lineage Upstream):** `/raw/recuperacao_carrinho/pedidos.csv`
- **Destino (Lineage Downstream):** 
  - Views analíticas de receita, faturamento e métricas de ROI.
- **Chave Primária (PK):** `pedido_id`
- **Chaves Estrangeiras (FK):** 
  - `carrinho_id` ➔ `CART_RECOVERY.CARRINHOS.carrinho_id`
  - `cliente_id` ➔ `CART_RECOVERY.CLIENTES.cliente_id`
  - `resgate_id` ➔ `CART_RECOVERY.EVENTOS_RESGATE.resgate_id` (opcional, aplicável se o pedido originou-se de uma campanha de resgate)

---

## 🛡️ Governança & Sensibilidade

- **Proprietário do Dado (Owner):** Área Financeira & Engenharia de Dados
- **Classificação de Sensibilidade:** Interno — Contém transações financeiras operacionais internas de vendas.
- **Tags de Governança:** `carrinho_abandonado`, `pedidos`, `conversoes`, `raw`

---

## 📊 Dicionário de Atributos (Colunas)

| Campo Físico | Tipo de Dado | Chave | Nullable | Descrição de Negócio (A é um B que C) | Valores Válidos / Regras | Exemplo de Valor | PII? |
|:---|:---:|:---:|:---:|:---|:---|:---|:---:|
| `pedido_id` | `VARCHAR` | `PK` | `Não` | O pedido_id é o identificador exclusivo (UUID) da compra finalizada pelo cliente. | UUIDv4 válido | `4487c93c-234b-4b1a-8cbd-2b0e7a3dcb1a` | `Não` |
| `carrinho_id` | `VARCHAR` | `FK` | `Não` | O carrinho_id é a referência ao carrinho original que continha os itens adquiridos nesta compra. | Deve existir na tabela `CARRINHOS` | `aa87c93c-234b-4b1a-8cbd-2b0e7a3dcb1a` | `Não` |
| `cliente_id` | `VARCHAR` | `FK` | `Não` | O cliente_id aponta o cliente que realizou a compra e efetuou o pagamento. | Deve existir na tabela `CLIENTES` | `9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d` | `Não` |
| `criado_em` | `TIMESTAMP` | `-` | `Não` | A data criado_em registra o instante exato em que o cliente confirmou o checkout e gerou a ordem de pedido. | Data/hora válida | `2026-08-21 15:30:00` | `Não` |
| `valor_total` | `FLOAT` | `-` | `Não` | O valor_total é o valor financeiro líquido final pago pelo cliente (subtotal do carrinho - desconto + frete). | Valor positivo >= 0.00 | `319.90` | `Não` |
| `desconto_total` | `FLOAT` | `-` | `Não` | O desconto_total é a soma de todos os abatimentos e cupons de descontos aplicados à compra. | Valor positivo >= 0.00 | `30.00` | `Não` |
| `valor_frete` | `FLOAT` | `-` | `Não` | O valor_frete registra o custo cobrado para entrega dos produtos no endereço do cliente. | Valor positivo >= 0.00 | `15.00` | `Não` |
| `status` | `VARCHAR` | `-` | `Não` | O status indica a situação corrente de entrega e processamento financeiro do pedido. | `'aprovado'`, `'enviado'`, `'entregue'`, `'cancelado'` | `aprovado` | `Não` |
| `metodo_pagamento` | `VARCHAR` | `-` | `Não` | O metodo_pagamento indica a via de pagamento escolhida pelo cliente para liquidar a transação. | `'cartao'`, `'boleto'`, `'pix'` | `pix` | `Não` |
| `num_parcelas` | `INTEGER` | `-` | `Sim` | O num_parcelas registra a quantidade de parcelamentos da compra (aplicável apenas se metodo_pagamento = 'cartao'). | Inteiro de 1 a 12 (se cartão) ou nulo | `3` | `Não` |
| `origem_resgate` | `BOOLEAN` | `-` | `Não` | A flag origem_resgate indica se a compra foi finalizada diretamente a partir de um link de campanha de resgate. | `TRUE` / `FALSE` | `TRUE` | `Não` |
| `resgate_id` | `VARCHAR` | `FK` | `Sim` | O resgate_id aponta a campanha de resgate específica de recuperação de carrinho que converteu esta venda. | Deve existir na tabela `EVENTOS_RESGATE` | `3387c93c-234b-4b1a-8cbd-2b0e7a3dcb1a` | `Não` |

---

## 🧪 Regras de Qualidade de Dados (Data Quality)

As seguintes validações do Great Expectations/Soda Core são aplicadas a este ativo:
- **Unicidade:** O campo `pedido_id` deve ser único.
- **Relacionamentos:**
  - `carrinho_id` deve existir na tabela de `CARRINHOS`.
  - `cliente_id` deve existir na tabela de `CLIENTES`.
  - `resgate_id` (se preenchido) deve existir na tabela de `EVENTOS_RESGATE`.
- **Integridade Temporal:** O campo `criado_em` do pedido deve ser posterior ou igual à data de criação do carrinho original (`carrinhos.criado_em`).
- **Restrição de Domínio:** O campo `status` deve conter apenas as categorias `'aprovado'`, `'enviado'`, `'entregue'`, `'cancelado'`. O campo `metodo_pagamento` deve conter apenas `'cartao'`, `'boleto'`, `'pix'`.
- **Coerência de Resgate:** Se `origem_resgate = TRUE`, o campo `resgate_id` deve ser obrigatoriamente preenchido. Se `origem_resgate = FALSE`, `resgate_id` deve ser nulo.
- **Restrição de Cartão:** Se `metodo_pagamento = 'cartao'`, `num_parcelas` deve ser preenchido com valor entre 1 e 12. Para outros métodos, deve ser nulo.
