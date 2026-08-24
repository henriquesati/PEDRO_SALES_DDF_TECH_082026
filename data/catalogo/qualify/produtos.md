# Dicionário de Dados: produtos

Dicionário de dados da entidade de Produtos, contendo especificações de catálogo, preços, controle de estoque e avaliações dos itens à venda no e-commerce.

---

## 📌 Identificação do Ativo de Dados

- **Nome Físico:** `PRODUTOS`
- **Nome de Exibição (Display Name):** `produtos`
- **Data Asset ID (Dadosfera):** `65fcfa25-a6f3-4cb8-a444-7fd23df3fa84`
- **URL Direta no Catálogo:** [Acessar produtos](https://app.dadosfera.ai/pt-BR/catalog/data-assets/65fcfa25-a6f3-4cb8-a444-7fd23df3fa84)

---

## 💼 Visão de Negócio

### Descrição de Negócio
A tabela de produtos é uma entidade de dimensão que serve como fonte central para todas as informações cadastrais dos produtos comercializados no marketplace. Ela permite calcular a atratividade de itens baseada em avaliações e faixa de preço, monitorar a disponibilidade de itens em estoque, e mapear quais categorias são mais propensas ao abandono de carrinho.

### Principais Casos de Uso
- Categorizar os carrinhos abandonados de acordo com a categoria e subcategoria de produtos.
- Identificar se indisponibilidade de estoque (`estoque = 0` ou `ativo = FALSE`) é causa raiz de abandonos.
- Cruzar preços dos itens do carrinho com cupons de descontos recomendados nas estratégias de resgate.

---

## ⚙️ Visão Técnico-Operacional

### Especificações Gerais
- **Zona do Data Lakehouse:** Qualify (Silver)
- **Formato Físico:** Tabela Snowflake
- **Localização Física:** `CART_RECOVERY.PRODUTOS`
- **Granularidade:** Uma linha por produto único cadastrado.
- **Frequência de Atualização:** Batch diário.
- **Volume de Registros:** 500 registros (~47 KB).

### Integridade e Relacionamentos (Linhagem)
- **Origem (Lineage Upstream):** `/raw/recuperacao_carrinho/produtos.csv`
- **Destino (Lineage Downstream):** 
  - `CART_RECOVERY.ITENS_CARRINHO` (via `produto_id`)
  - `CART_RECOVERY.EVENTOS_CARRINHO` (via `produto_id`)
- **Chave Primária (PK):** `produto_id`
- **Chaves Estrangeiras (FK):** Nenhuma.

---

## 🛡️ Governança & Sensibilidade

- **Proprietário do Dado (Owner):** Área de Catálogo & Comercial E-commerce
- **Classificação de Sensibilidade:** Interno — Não contém dados pessoais.
- **Tags de Governança:** `carrinho_abandonado`, `produtos`, `catalogo`, `raw`

---

## 📊 Dicionário de Atributos (Colunas)

| Campo Físico | Tipo de Dado | Chave | Nullable | Descrição de Negócio (A é um B que C) | Valores Válidos / Regras | Exemplo de Valor | PII? |
|:---|:---:|:---:|:---:|:---|:---|:---|:---:|
| `produto_id` | `VARCHAR` | `PK` | `Não` | O produto_id é um código único (UUID) que identifica de forma exclusiva cada produto comercializado no marketplace. | UUIDv4 válido | `fb87a93c-234b-4b1a-8cbd-2b0e7a3dcb1a` | `Não` |
| `nome` | `VARCHAR` | `-` | `Não` | O nome é o título descritivo do produto visível para o cliente no site. | Texto livre | `Smartphone Samsung Galaxy S24` | `Não` |
| `categoria` | `VARCHAR` | `-` | `Não` | A categoria é a classificação de nível macro da linha de produtos (ex: Eletrônicos, Moda, Casa). | Lista fechada de departamentos | `Eletrônicos` | `Não` |
| `subcategoria` | `VARCHAR` | `-` | `Não` | A subcategoria é a classificação detalhada do tipo de produto (ex: Celulares, Calçados, Utensílios). | Subcategorias mapeadas | `Celulares` | `Não` |
| `preco` | `FLOAT` | `-` | `Não` | O preco é o valor de venda em Reais (R$) do produto no catálogo do e-commerce. | Valor positivo >= 0.01 | `3999.90` | `Não` |
| `estoque` | `INTEGER` | `-` | `Não` | O estoque é a quantidade física do produto disponível para envio imediato no centro de distribuição. | Inteiro >= 0 | `150` | `Não` |
| `marca` | `VARCHAR` | `-` | `Não` | A marca é o nome do fabricante ou marca comercial do produto. | Marcas cadastradas | `Samsung` | `Não` |
| `avaliacao_media` | `FLOAT` | `-` | `Não` | A avaliacao_media é a pontuação média de satisfação do cliente (de 0 a 5 estrelas) dada ao produto. | Decimal de 0 a 5 | `4.7` | `Não` |
| `num_avaliacoes` | `INTEGER` | `-` | `Não` | O num_avaliacoes é a quantidade de clientes que avaliaram o produto na plataforma. | Inteiro >= 0 | `1240` | `Não` |
| `ativo` | `BOOLEAN` | `-` | `Não` | O campo ativo é a flag lógica que indica se o produto está disponível para venda no marketplace. | `TRUE` / `FALSE` | `TRUE` | `Não` |

---

## 🧪 Regras de Qualidade de Dados (Data Quality)

As seguintes validações do Great Expectations/Soda Core são aplicadas a este ativo:
- **Unicidade:** O campo `produto_id` deve ser único.
- **Não-Nulidade:** Todos os campos nesta entidade são obrigatórios e não devem conter valores nulos.
- **Faixas Permitidas:** O campo `preco` deve ser maior que zero. O campo `avaliacao_media` deve estar no intervalo de `0` a `5`. O campo `estoque` e `num_avaliacoes` devem ser inteiros maiores ou iguais a zero.
