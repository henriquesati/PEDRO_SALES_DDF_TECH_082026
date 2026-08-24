# Dicionário de Dados: clientes

Dicionário de dados da entidade de Clientes, contendo informações cadastrais, demográficas e métricas de LTV para análise comportamental do marketplace.

---

## 📌 Identificação do Ativo de Dados

- **Nome Físico:** `CLIENTES`
- **Nome de Exibição (Display Name):** `clientes`
- **Data Asset ID (Dadosfera):** `0327fecc-f826-48fb-bb0a-1493fe18a32c`
- **URL Direta no Catálogo:** [Acessar clientes](https://app.dadosfera.ai/pt-BR/catalog/data-assets/0327fecc-f826-48fb-bb0a-1493fe18a32c)

---

## 💼 Visão de Negócio

### Descrição de Negócio
A tabela de clientes é uma entidade de dimensão que consolida os dados demográficos e de relacionamento comercial de cada usuário cadastrado na plataforma de e-commerce. Ela serve para segmentar clientes, mapear os canais que geram maior valor, e identificar clientes inativos para campanhas direcionadas de marketing e recuperação de carrinho.

### Principais Casos de Uso
- Filtrar campanhas de recuperação de carrinho por segmento comportamental (Premium, Regular, Dormant).
- Avaliar a efetividade dos canais de aquisição no Lifetime Value (LTV).
- Analisar a distribuição demográfica dos clientes afetados por carrinhos abandonados.

---

## ⚙️ Visão Técnico-Operacional

### Especificações Gerais
- **Zona do Data Lakehouse:** Qualify (Silver)
- **Formato Físico:** Tabela Snowflake
- **Localização Física:** `CART_RECOVERY.CLIENTES`
- **Granularidade:** Uma linha por cliente único cadastrado.
- **Frequência de Atualização:** Batch diário (processado no final do dia).
- **Volume de Registros:** 2.000 registros (~224 KB).

### Integridade e Relacionamentos (Linhagem)
- **Origem (Lineage Upstream):** `/raw/recuperacao_carrinho/clientes.csv`
- **Destino (Lineage Downstream):** 
  - `CART_RECOVERY.CARRINHOS` (via `cliente_id`)
  - `CART_RECOVERY.PEDIDOS` (via `cliente_id`)
  - `CART_RECOVERY.EVENTOS_RESGATE` (via `cliente_id`)
  - `CART_RECOVERY.EVENTOS_CARRINHO` (via `cliente_id`)
- **Chave Primária (PK):** `cliente_id`
- **Chaves Estrangeiras (FK):** Nenhuma.

---

## 🛡️ Governança & Sensibilidade

- **Proprietário do Dado (Owner):** Engenharia de Dados & Marketing Analytics
- **Classificação de Sensibilidade:** Confidencial / Sensível (LGPD) — Contém PII (Dados Pessoais Identificáveis).
- **Tags de Governança:** `carrinho_abandonado`, `clientes`, `marketplace`, `raw`

---

## 📊 Dicionário de Atributos (Colunas)

| Campo Físico | Tipo de Dado | Chave | Nullable | Descrição de Negócio (A é um B que C) | Valores Válidos / Regras | Exemplo de Valor | PII? |
|:---|:---:|:---:|:---:|:---|:---|:---|:---:|
| `cliente_id` | `VARCHAR` | `PK` | `Não` | O cliente_id é um código UUID único que identifica de forma inequívoca cada cliente cadastrado no e-commerce. | UUIDv4 válido | `9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d` | `Não` |
| `nome` | `VARCHAR` | `-` | `Não` | O nome é o nome completo do cliente, utilizado para personalização de mensagens de comunicação de resgate. | Texto livre, sem caracteres especiais estranhos | `João da Silva` | `Sim` |
| `email` | `VARCHAR` | `-` | `Não` | O email é o endereço eletrônico do cliente, utilizado como canal primário para envio de lembretes e descontos. | Formato de email válido (`*@*.*`) | `joao.silva@email.com` | `Sim` |
| `telefone` | `VARCHAR` | `-` | `Sim` | O telefone é o número de telefone celular do cliente, utilizado para contato via WhatsApp ou SMS. | Formato de telefone DDI+DDD+Número | `+5511999999999` | `Sim` |
| `cidade` | `VARCHAR` | `-` | `Não` | A cidade é o município de residência do cliente cadastrado, utilizado para análise de distribuição geográfica. | Cidades brasileiras válidas | `São Paulo` | `Não` |
| `estado` | `VARCHAR` | `-` | `Não` | O estado é a Unidade Federativa (UF) do endereço do cliente, utilizado para precificação de fretes e segmentação regional. | Siglas de estados brasileiros (2 caracteres) | `SP` | `Não` |
| `data_cadastro` | `TIMESTAMP` | `-` | `Não` | A data_cadastro é a data e hora em que o cliente realizou seu registro na plataforma de e-commerce. | Data válida, anterior à data atual | `2025-06-15 14:32:00` | `Não` |
| `segmento` | `VARCHAR` | `-` | `Não` | O segmento é a classificação comportamental RFM do cliente no marketplace, calculada com base no seu histórico. | `'premium'`, `'regular'`, `'dormant'`, `'novo'` | `regular` | `Não` |
| `canal_aquisicao` | `VARCHAR` | `-` | `Não` | O canal_aquisicao é o canal de marketing pelo qual o cliente foi atraído para o e-commerce. | `'organico'`, `'pago'`, `'rede_social'`, `'indicacao'` | `organico` | `Não` |
| `ltv_estimado` | `FLOAT` | `-` | `Não` | O ltv_estimado é a estimativa do valor financeiro total que o cliente gastará no e-commerce durante sua vida útil. | Valor positivo >= 0 | `1250.50` | `Não` |
| `total_pedidos` | `INTEGER` | `-` | `Não` | O total_pedidos é o número total de compras bem-sucedidas realizadas pelo cliente no marketplace. | Valor inteiro >= 0 | `5` | `Não` |
| `ticket_medio` | `FLOAT` | `-` | `Não` | O ticket_medio é o valor financeiro médio gasto pelo cliente por pedido (LTV / Total Pedidos). | Valor positivo >= 0 | `250.10` | `Não` |

---

## 🧪 Regras de Qualidade de Dados (Data Quality)

As seguintes validações do Great Expectations/Soda Core são aplicadas a este ativo:
- **Unicidade:** O campo `cliente_id` deve ser único (100% de valores distintos).
- **Não-Nulidade:** Os campos `cliente_id`, `nome`, `email`, `cidade`, `estado`, `data_cadastro`, `segmento`, `canal_aquisicao`, `ltv_estimado`, `total_pedidos` e `ticket_medio` não podem conter valores nulos.
- **Valores Permitidos:** O campo `estado` deve conter apenas siglas de UFs com 2 caracteres. O campo `segmento` deve conter apenas os valores `'premium'`, `'regular'`, `'dormant'`, `'novo'`.
