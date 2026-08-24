# Dicionário de Dados: itens_carrinho

Dicionário de dados da entidade de Itens do Carrinho, representando os produtos específicos vinculados a cada sessão de carrinho e suas respectivas quantidades e preços.

---

## 📌 Identificação do Ativo de Dados

- **Nome Físico:** `ITENS_CARRINHO`
- **Nome de Exibição (Display Name):** `itens_carrinho`
- **Data Asset ID (Dadosfera):** `7649755a-c6e8-4b56-a092-be9eefde1dab`
- **URL Direta no Catálogo:** [Acessar itens_carrinho](https://app.dadosfera.ai/pt-BR/catalog/data-assets/7649755a-c6e8-4b56-a092-be9eefde1dab)

---

## 💼 Visão de Negócio

### Descrição de Negócio
A tabela de itens_carrinho serve para detalhar o conteúdo específico de cada carrinho de compras no e-commerce. Ela conecta carrinhos e produtos e ajuda a entender quais combinações de produtos são frequentemente abandonadas juntas e qual o impacto financeiro (subtotal e descontos aplicados) de itens individuais na decisão de abandonar ou comprar do cliente.

### Principais Casos de Uso
- Listar produtos abandonados em um carrinho específico para personalizar a campanha de comunicação (ex: "Você deixou seu Smartphone Samsung no carrinho").
- Identificar categorias de produtos com maior valor financeiro em carrinhos pendentes para otimização de campanhas.
- Analisar a elasticidade de preço de itens nos carrinhos de acordo com descontos aplicados.

---

## ⚙️ Visão Técnico-Operacional

### Especificações Gerais
- **Zona do Data Lakehouse:** Qualify (Silver)
- **Formato Físico:** Tabela Snowflake
- **Localização Física:** `CART_RECOVERY.ITENS_CARRINHO`
- **Granularidade:** Uma linha por item específico inserido em um determinado carrinho.
- **Frequência de Atualização:** Batch diário.
- **Volume de Registros:** 22.500 registros (~1.2 MB).

### Integridade e Relacionamentos (Linhagem)
- **Origem (Lineage Upstream):** `/raw/recuperacao_carrinho/itens_carrinho.csv` (ingestão mapeia `itens.csv` para `itens_carrinho.csv` no repositório)
- **Destino (Lineage Downstream):** 
  - Consultas analíticas e views de cruzamento de conversão.
- **Chave Primária (PK):** `item_id`
- **Chaves Estrangeiras (FK):** 
  - `carrinho_id` ➔ `CART_RECOVERY.CARRINHOS.carrinho_id`
  - `produto_id` ➔ `CART_RECOVERY.PRODUTOS.produto_id`

---

## 🛡️ Governança & Sensibilidade

- **Proprietário do Dado (Owner):** Engenharia de Dados & Produto Analytics
- **Classificação de Sensibilidade:** Interno — Contém dados transacionais e quantitativos internos.
- **Tags de Governança:** `carrinho_abandonado`, `itens_carrinho`, `itens`, `raw`

---

## 📊 Dicionário de Atributos (Colunas)

| Campo Físico | Tipo de Dado | Chave | Nullable | Descrição de Negócio (A é um B que C) | Valores Válidos / Regras | Exemplo de Valor | PII? |
|:---|:---:|:---:|:---:|:---|:---|:---|:---:|
| `item_id` | `VARCHAR` | `PK` | `Não` | O item_id é o identificador exclusivo (UUID) da linha que representa um produto específico inserido em um carrinho. | UUIDv4 válido | `1187c93c-234b-4b1a-8cbd-2b0e7a3dcb1a` | `Não` |
| `carrinho_id` | `VARCHAR` | `FK` | `Não` | O carrinho_id é a referência ao carrinho pai ao qual este item pertence. | Deve existir na tabela `CARRINHOS` | `aa87c93c-234b-4b1a-8cbd-2b0e7a3dcb1a` | `Não` |
| `produto_id` | `VARCHAR` | `FK` | `Não` | O produto_id é a referência ao produto do catálogo cadastrado que foi adicionado. | Deve existir na tabela `PRODUTOS` | `fb87a93c-234b-4b1a-8cbd-2b0e7a3dcb1a` | `Não` |
| `quantidade` | `INTEGER` | `-` | `Não` | A quantidade indica o número de unidades do mesmo produto que foram adicionadas no carrinho. | Inteiro >= 1 | `2` | `Não` |
| `preco_unitario` | `FLOAT` | `-` | `Não` | O preco_unitario é o valor de venda de uma única unidade do produto no momento exato em que foi colocado no carrinho. | Valor positivo >= 0.01 | `150.00` | `Não` |
| `subtotal` | `FLOAT` | `-` | `Não` | O subtotal é o valor financeiro total do item antes de descontos (quantidade x preco_unitario). | `subtotal = quantidade * preco_unitario` | `300.00` | `Não` |
| `adicionado_em` | `TIMESTAMP` | `-` | `Não` | A data adicionado_em registra o instante exato em que o produto foi inserido pelo cliente no carrinho. | Data/hora válida | `2026-08-20 10:18:00` | `Não` |
| `desconto_aplicado` | `FLOAT` | `-` | `Não` | O desconto_aplicado registra o valor total de desconto em Reais (R$) subtraído do subtotal deste item. | Valor >= 0.00 | `30.00` | `Não` |

---

## 🧪 Regras de Qualidade de Dados (Data Quality)

As seguintes validações do Great Expectations/Soda Core são aplicadas a este ativo:
- **Unicidade:** O campo `item_id` deve ser único.
- **Relacionamentos:** 
  - Todo `carrinho_id` deve existir na tabela de `CARRINHOS`.
  - Todo `produto_id` deve existir na tabela de `PRODUTOS`.
- **Integridade Numérica:** 
  - `quantidade` deve ser maior ou igual a 1.
  - `preco_unitario` deve ser maior ou igual a 0.01.
  - O `subtotal` deve bater exatamente com a multiplicação de `quantidade * preco_unitario`.
  - O `desconto_aplicado` deve ser menor ou igual ao `subtotal` e maior ou igual a zero.
- **Coerência Temporal:** O campo `adicionado_em` deve ser maior ou igual ao `criado_em` do seu carrinho pai.
