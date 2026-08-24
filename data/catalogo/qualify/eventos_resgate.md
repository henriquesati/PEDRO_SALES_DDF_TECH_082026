# Dicionário de Dados: eventos_resgate

Dicionário de dados da entidade de Eventos de Resgate, contendo informações sobre as tentativas de contato ativas enviadas para clientes com carrinhos abandonados, canais utilizados, ofertas e taxa de conversão.

---

## 📌 Identificação do Ativo de Dados

- **Nome Físico:** `EVENTOS_RESGATE`
- **Nome de Exibição (Display Name):** `eventos_resgate`
- **Data Asset ID (Dadosfera):** `04739f6d-e8c3-4d6f-80b7-0f98c12a5798`
- **URL Direta no Catálogo:** [Acessar eventos_resgate](https://app.dadosfera.ai/pt-BR/catalog/data-assets/04739f6d-e8c3-4d6f-80b7-0f98c12a5798)

---

## 💼 Visão de Negócio

### Descrição de Negócio
A tabela de eventos_resgate registra o envio e a performance das comunicações ativas efetuadas para resgatar vendas de carrinhos abandonados. Ela consolida as métricas do funil de marketing pós-abandono (Envio ➔ Abertura ➔ Clique ➔ Conversão), os descontos oferecidos e o custo financeiro do disparo. É a entidade fundamental para avaliar o Retorno sobre o Investimento (ROI) das campanhas.

### Principais Casos de Uso
- Calcular a taxa de conversão por canal de resgate (Email, SMS, Push, WhatsApp).
- Medir o ROI financeiro das campanhas comparando o custo de envio com o valor recuperado.
- Controlar o limite de comunicações por cliente para evitar fadiga e spam (+4 comunicações no total).

---

## ⚙️ Visão Técnico-Operacional

### Especificações Gerais
- **Zona do Data Lakehouse:** Qualify (Silver)
- **Formato Físico:** Tabela Snowflake
- **Localização Física:** `CART_RECOVERY.EVENTOS_RESGATE`
- **Granularidade:** Uma linha por mensagem/comunicação disparada para um cliente referente a um carrinho abandonado.
- **Frequência de Atualização:** Batch diário.
- **Volume de Registros:** 2.500 registros (~1.3 MB).

### Integridade e Relacionamentos (Linhagem)
- **Origem (Lineage Upstream):** `/raw/recuperacao_carrinho/resgate.csv` (ingestão mapeia `eventos_resgate.csv` para `resgate.csv` no Data Lake)
- **Destino (Lineage Downstream):** 
  - `CART_RECOVERY.PEDIDOS` (via `resgate_id` para pedidos convertidos por campanhas)
- **Chave Primária (PK):** `resgate_id`
- **Chaves Estrangeiras (FK):** 
  - `carrinho_id` ➔ `CART_RECOVERY.CARRINHOS.carrinho_id`
  - `cliente_id` ➔ `CART_RECOVERY.CLIENTES.cliente_id`

---

## 🛡️ Governança & Sensibilidade

- **Proprietário do Dado (Owner):** Engenharia de Dados & Growth/CRM Marketing
- **Classificação de Sensibilidade:** Interno — Mapeamento operacional e de ROI do CRM.
- **Tags de Governança:** `carrinho_abandonado`, `eventos_resgate`, `recuperacao`, `raw`

---

## 📊 Dicionário de Atributos (Colunas)

| Campo Físico | Tipo de Dado | Chave | Nullable | Descrição de Negócio (A é um B que C) | Valores Válidos / Regras | Exemplo de Valor | PII? |
|:---|:---:|:---:|:---:|:---|:---|:---|:---:|
| `resgate_id` | `VARCHAR` | `PK` | `Não` | O resgate_id é o identificador exclusivo (UUID) de um disparo de comunicação de resgate enviado ao cliente. | UUIDv4 válido | `3387c93c-234b-4b1a-8cbd-2b0e7a3dcb1a` | `Não` |
| `carrinho_id` | `VARCHAR` | `FK` | `Não` | O carrinho_id indica o carrinho abandonado que motivou este disparo de comunicação. | Deve existir na tabela `CARRINHOS` | `aa87c93c-234b-4b1a-8cbd-2b0e7a3dcb1a` | `Não` |
| `cliente_id` | `VARCHAR` | `FK` | `Não` | O cliente_id aponta o cliente destinatário da comunicação de resgate. | Deve existir na tabela `CLIENTES` | `9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d` | `Não` |
| `canal_resgate` | `VARCHAR` | `-` | `Não` | O canal_resgate indica a via de comunicação utilizada para enviar a mensagem. | `'email'`, `'sms'`, `'push_app'`, `'whatsapp'` | `email` | `Não` |
| `enviado_em` | `TIMESTAMP` | `-` | `Não` | A data enviado_em registra o instante exato em que a mensagem de resgate foi enviada. | Data/hora válida | `2026-08-21 15:00:00` | `Não` |
| `aberto_em` | `TIMESTAMP` | `-` | `Sim` | A data aberto_em registra o instante em que o cliente abriu a mensagem enviada (se aplicável ao canal). | `aberto_em >= enviado_em` ou nulo | `2026-08-21 15:12:00` | `Não` |
| `clicado_em` | `TIMESTAMP` | `-` | `Sim` | A data clicado_em registra o instante em que o cliente clicou no link contido na mensagem (se ocorreu). | `clicado_em >= aberto_em` ou nulo | `2026-08-21 15:15:00` | `Não` |
| `convertido` | `BOOLEAN` | `-` | `Não` | O campo convertido é a flag lógica que indica se o cliente realizou a compra a partir deste disparo. | `TRUE` / `FALSE` | `TRUE` | `Não` |
| `convertido_em` | `TIMESTAMP` | `-` | `Sim` | A data convertido_em registra o instante em que o pagamento do pedido recuperado foi aprovado. | `convertido_em >= clicado_em` ou nulo | `2026-08-21 15:30:00` | `Não` |
| `valor_recuperado` | `FLOAT` | `-` | `Sim` | O valor_recuperado registra o valor total em Reais (R$) do pedido final pago pelo cliente (se convertido = TRUE). | Valor positivo >= 0 ou nulo | `319.90` | `Não` |
| `tipo_oferta` | `VARCHAR` | `-` | `Não` | O tipo_oferta define o benefício concedido para incentivar o cliente a concluir a compra. | `'desconto'`, `'frete_gratis'`, `'lembrete'` | `desconto` | `Não` |
| `desconto_oferecido` | `FLOAT` | `-` | `Não` | O desconto_oferecido registra o percentual de desconto no valor de catálogo do carrinho concedido na comunicação. | Decimal de 0.00 a 100.00 | `10.0` | `Não` |

---

## 🧪 Regras de Qualidade de Dados (Data Quality)

As seguintes validações do Great Expectations/Soda Core são aplicadas a este ativo:
- **Unicidade:** O campo `resgate_id` deve ser único.
- **Relacionamentos:**
  - `carrinho_id` deve existir na tabela de `CARRINHOS`.
  - `cliente_id` deve existir na tabela de `CLIENTES`.
- **Integridade Temporal:**
  - `enviado_em` deve ser posterior à data de abandono do carrinho associado (`carrinhos.abandono_em`).
  - A ordenação cronológica obrigatória deve ser respeitada: `enviado_em` ➔ `aberto_em` ➔ `clicado_em` ➔ `convertido_em` (quando esses eventos não-nulos ocorrerem).
- **Restrição de Domínio:** O campo `canal_resgate` deve conter apenas as opções `'email'`, `'sms'`, `'push_app'`, `'whatsapp'`. O campo `tipo_oferta` deve conter apenas `'desconto'`, `'frete_gratis'`, `'lembrete'`.
- **Coerência de Conversão:** Se `convertido = FALSE`, então `convertido_em` e `valor_recuperado` devem ser obrigatoriamente nulos. Se `convertido = TRUE`, `valor_recuperado` deve ser preenchido com valor maior que zero.
