# Dicionário de Dados: carrinhos

Dicionário de dados da entidade de Carrinhos, que representa as sessões transacionais de compra iniciadas pelos clientes, incluindo status de conversão ou abandono.

---

## 📌 Identificação do Ativo de Dados

- **Nome Físico:** `CARRINHOS`
- **Nome de Exibição (Display Name):** `carrinhos`
- **Data Asset ID (Dadosfera):** `e2d3b1bb-bf22-456e-bc66-4ac843deec82`
- **URL Direta no Catálogo:** [Acessar carrinhos](https://app.dadosfera.ai/pt-BR/catalog/data-assets/e2d3b1bb-bf22-456e-bc66-4ac843deec82)

---

## 💼 Visão de Negócio

### Descrição de Negócio
A tabela de carrinhos registra as transações e o estado da intenção de compra de cada cliente. Ela rastreia quais carrinhos foram convertidos diretamente, quais foram abandonados e quais puderam ser resgatados com sucesso através de nossas comunicações. Esse é o ativo central do case de marketing para medir o impacto de ROI direto.

### Principais Casos de Uso
- Filtrar carrinhos com status `'abandonado'` para iniciar a cadeia de comunicação de resgate.
- Calcular taxas de conversão (carrinhos convertidos / total de carrinhos) e de abandono (carrinhos abandonados / total).
- Analisar o tempo de inatividade que antecede a classificação de abandono.

---

## ⚙️ Visão Técnico-Operacional

### Especificações Gerais
- **Zona do Data Lakehouse:** Qualify (Silver)
- **Formato Físico:** Tabela Snowflake
- **Localização Física:** `CART_RECOVERY.CARRINHOS`
- **Granularidade:** Uma linha por sessão única de carrinho criada por um cliente.
- **Frequência de Atualização:** Batch diário.
- **Volume de Registros:** 15.000 registros (~1.6 MB).

### Integridade e Relacionamentos (Linhagem)
- **Origem (Lineage Upstream):** `/raw/recuperacao_carrinho/carrinhos.csv`
- **Destino (Lineage Downstream):** 
  - `CART_RECOVERY.ITENS_CARRINHO` (via `carrinho_id`)
  - `CART_RECOVERY.EVENTOS_CARRINHO` (via `carrinho_id`)
  - `CART_RECOVERY.EVENTOS_RESGATE` (via `carrinho_id`)
  - `CART_RECOVERY.PEDIDOS` (via `carrinho_id`)
- **Chave Primária (PK):** `carrinho_id`
- **Chaves Estrangeiras (FK):** 
  - `cliente_id` ➔ `CART_RECOVERY.CLIENTES.cliente_id`

---

## 🛡️ Governança & Sensibilidade

- **Proprietário do Dado (Owner):** Engenharia de Dados & Produto Analytics
- **Classificação de Sensibilidade:** Interno — Contém chaves e valores transacionais de negócio sem dados pessoais legíveis diretamente.
- **Tags de Governança:** `carrinho_abandonado`, `carrinhos`, `transacional`, `raw`

---

## 📊 Dicionário de Atributos (Colunas)

| Campo Físico | Tipo de Dado | Chave | Nullable | Descrição de Negócio (A é um B que C) | Valores Válidos / Regras | Exemplo de Valor | PII? |
|:---|:---:|:---:|:---:|:---|:---|:---|:---:|
| `carrinho_id` | `VARCHAR` | `PK` | `Não` | O carrinho_id é o identificador exclusivo (UUID) de uma sessão de carrinho aberta pelo cliente no e-commerce. | UUIDv4 válido | `aa87c93c-234b-4b1a-8cbd-2b0e7a3dcb1a` | `Não` |
| `cliente_id` | `VARCHAR` | `FK` | `Não` | O cliente_id é o identificador único do cliente associado ao carrinho (proprietário da sessão). | Deve existir na tabela `CLIENTES` | `9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d` | `Não` |
| `criado_em` | `TIMESTAMP` | `-` | `Não` | A data criado_em registra o instante exato em que o primeiro item foi adicionado e o carrinho foi inicializado. | Data/hora válida | `2026-08-20 10:15:00` | `Não` |
| `atualizado_em` | `TIMESTAMP` | `-` | `Não` | A data atualizado_em registra o instante da última interação do cliente com o carrinho (adição, remoção, alteração). | `atualizado_em >= criado_em` | `2026-08-20 10:30:00` | `Não` |
| `status` | `VARCHAR` | `-` | `Não` | O status indica a situação corrente do carrinho no seu ciclo de vida. | `'ativo'`, `'abandonado'`, `'recuperado'`, `'comprado'`, `'expirado'` | `abandonado` | `Não` |
| `valor_total` | `FLOAT` | `-` | `Não` | O valor_total é o somatório dos preços dos itens do carrinho deduzidos de descontos e acrescidos de frete se aplicável. | Valor >= 0.00 | `349.90` | `Não` |
| `num_itens` | `INTEGER` | `-` | `Não` | O num_itens é o número total de unidades físicas de produtos presentes no carrinho. | Inteiro >= 0 | `3` | `Não` |
| `canal` | `VARCHAR` | `-` | `Não` | O canal indica qual plataforma o cliente usou para criar a sessão do carrinho. | `'web'`, `'mobile'`, `'app'` | `web` | `Não` |
| `abandono_em` | `TIMESTAMP` | `-` | `Sim` | A data abandono_em registra a marcação temporal de quando o carrinho foi considerado abandonado (30min inativo). | `abandono_em >= atualizado_em` | `2026-08-20 11:00:00` | `Não` |
| `tempo_ate_abandono_min` | `FLOAT` | `-` | `Sim` | O tempo_ate_abandono_min é o tempo total gasto em minutos desde a criação até a inatividade ou abandono. | Valor >= 0.00 (calculado) | `45.2` | `Não` |

---

## 🧪 Regras de Qualidade de Dados (Data Quality)

As seguintes validações do Great Expectations/Soda Core são aplicadas a este ativo:
- **Unicidade:** O campo `carrinho_id` deve ser único.
- **Relacionamento:** Todo `cliente_id` nesta tabela deve existir na tabela de `CLIENTES`.
- **Integridade Temporal:** O campo `atualizado_em` deve ser maior ou igual a `criado_em`. E `abandono_em` (se existir) deve ser maior ou igual a `atualizado_em`.
- **Restrição de Domínio:** O campo `status` deve conter apenas valores na lista `'ativo'`, `'abandonado'`, `'recuperado'`, `'comprado'`, `'expirado'`.
- **Não-Negatividade:** O campo `valor_total` e `num_itens` devem ser maiores ou iguais a zero.
