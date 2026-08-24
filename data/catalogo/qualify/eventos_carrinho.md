# Dicionário de Dados: eventos_carrinho

Dicionário de dados da entidade de Eventos do Carrinho, que registra toda a telemetria e o comportamento de navegação do cliente durante o funil de compras e carrinhos abandonados.

---

## 📌 Identificação do Ativo de Dados

- **Nome Físico:** `EVENTOS_CARRINHO`
- **Nome de Exibição (Display Name):** `eventos_carrinho`
- **Data Asset ID (Dadosfera):** `397c3ebc-15cb-42d2-a717-a3b5d150c3ea`
- **URL Direta no Catálogo:** [Acessar eventos_carrinho](https://app.dadosfera.ai/pt-BR/catalog/data-assets/397c3ebc-15cb-42d2-a717-a3b5d150c3ea)

---

## 💼 Visão de Negócio

### Descrição de Negócio
A tabela de eventos_carrinho armazena os logs brutos de eventos comportamentais da jornada do usuário. Ao mapear o momento de cliques, visualização de produto, início do preenchimento de formulários de pagamento e ocorrência de erros, é possível identificar gargalos de usabilidade, barreiras financeiras (frete e preço) ou problemas de gateway que provocam a desistência da compra. Ela é a maior tabela do case e serve como base para inteligência diagnóstica.

### Principais Casos de Uso
- Detectar qual o exato último evento efetuado pelo cliente antes de abandonar o carrinho (ex: `'erro_pagamento'`).
- Construir o funil de conversão completo: `Visualizar Produto` ➔ `Adicionar ao Carrinho` ➔ `Visualizar Checkout` ➔ `Iniciar Pagamento` ➔ `Finalizar Compra`.
- Fornecer dados comportamentais em tempo real para disparar triggers imediatos de recuperação (+1 hora de abandono).

---

## ⚙️ Visão Técnico-Operacional

### Especificações Gerais
- **Zona do Data Lakehouse:** Qualify (Silver)
- **Formato Físico:** Tabela Snowflake (com campo Variant para dados semiestruturados)
- **Localização Física:** `CART_RECOVERY.EVENTOS_CARRINHO`
- **Granularidade:** Um registro por interação/ação individual do usuário relacionada ao fluxo de compra.
- **Frequência de Atualização:** Batch diário.
- **Volume de Registros:** 72.026 registros (~11.4 MB).

### Integridade e Relacionamentos (Linhagem)
- **Origem (Lineage Upstream):** `/raw/recuperacao_carrinho/eventos_carrinho.csv` (ingestão mapeia `eventos.csv` para `eventos_carrinho.csv` no repositório)
- **Destino (Lineage Downstream):** 
  - Views analíticas de comportamento de navegação.
  - Modelos preditivos de propensão ao abandono.
- **Chave Primária (PK):** `evento_id`
- **Chaves Estrangeiras (FK):** 
  - `carrinho_id` ➔ `CART_RECOVERY.CARRINHOS.carrinho_id`
  - `cliente_id` ➔ `CART_RECOVERY.CLIENTES.cliente_id`
  - `produto_id` ➔ `CART_RECOVERY.PRODUTOS.produto_id` (opcional, pode ser nulo para eventos que não envolvem produto específico)

---

## 🛡️ Governança & Sensibilidade

- **Proprietário do Dado (Owner):** Engenharia de Dados & Time de Web Analytics/UX
- **Classificação de Sensibilidade:** Interno — Contém dados de comportamento do site de forma anônima e técnica.
- **Tags de Governança:** `carrinho_abandonado`, `eventos_carrinho`, `telemetria`, `raw`

---

## 📊 Dicionário de Atributos (Colunas)

| Campo Físico | Tipo de Dado | Chave | Nullable | Descrição de Negócio (A é um B que C) | Valores Válidos / Regras | Exemplo de Valor | PII? |
|:---|:---:|:---:|:---:|:---|:---|:---|:---:|
| `evento_id` | `VARCHAR` | `PK` | `Não` | O evento_id é o identificador exclusivo (UUID) da ocorrência de uma interação de telemetria no site. | UUIDv4 válido | `2287c93c-234b-4b1a-8cbd-2b0e7a3dcb1a` | `Não` |
| `carrinho_id` | `VARCHAR` | `FK` | `Não` | O carrinho_id indica o carrinho aberto na sessão atual com o qual o evento está relacionado. | Deve existir na tabela `CARRINHOS` | `aa87c93c-234b-4b1a-8cbd-2b0e7a3dcb1a` | `Não` |
| `cliente_id` | `VARCHAR` | `FK` | `Não` | O cliente_id é o identificador do cliente que realizou a ação no e-commerce. | Deve existir na tabela `CLIENTES` | `9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d` | `Não` |
| `tipo_evento` | `VARCHAR` | `-` | `Não` | O tipo_evento é a classificação da ação executada pelo cliente (visita, adição, checkout, erro). | Ver lista de tipos de evento abaixo | `view_checkout` | `Não` |
| `ocorrido_em` | `TIMESTAMP` | `-` | `Não` | A data ocorrido_em indica o momento exato em que a ação de navegação ocorreu no navegador ou aplicativo do cliente. | Data/hora válida | `2026-08-20 10:20:15` | `Não` |
| `canal` | `VARCHAR` | `-` | `Não` | O canal é a plataforma onde o evento ocorreu. | `'web'`, `'mobile'`, `'app'` | `web` | `Não` |
| `dispositivo` | `VARCHAR` | `-` | `Não` | O dispositivo especifica o aparelho físico que o usuário estava utilizando. | `'desktop'`, `'mobile'`, `'tablet'` | `desktop` | `Não` |
| `sessao_id` | `VARCHAR` | `-` | `Não` | O sessao_id identifica unicamente o período de atividade contínua do cliente no site (para agrupar cliques e ações). | Identificador alfanumérico ou UUID | `sess_9831d102ab` | `Não` |
| `produto_id` | `VARCHAR` | `FK` | `Sim` | O produto_id indica o produto envolvido no evento (ex: qual item foi visualizado ou adicionado). | Deve existir na tabela `PRODUTOS` ou nulo | `fb87a93c-234b-4b1a-8cbd-2b0e7a3dcb1a` | `Não` |
| `metadata` | `VARIANT` | `-` | `Sim` | O metadata é um objeto JSON que contém detalhes complementares e variáveis dinâmicas sobre o evento. | JSON válido ou nulo | `{"viewport": "1920x1080", "latency_ms": 120}` | `Não` |

### Valores de Referência para `tipo_evento`
- `'view_produto'`: Visualizou a página de detalhe de um produto.
- `'add_carrinho'`: Inseriu um item ao carrinho.
- `'remove_carrinho'`: Excluiu um item do carrinho.
- `'update_quantidade'`: Alterou a quantidade comprada do produto no carrinho.
- `'view_checkout'`: Entrou na página final de checkout (início do funil de conversão).
- `'inicio_pagamento'`: Começou o preenchimento de campos de dados de faturamento/pagamento.
- `'erro_pagamento'`: Aconteceu um erro sistêmico de rejeição do pagamento pelo gateway ou banco.
- `'abandono'`: Inatividade detectada sem finalização da compra.
- `'retorno'`: Acessou novamente o carrinho após um período de abandono (normalmente via resgate).

---

## 🧪 Regras de Qualidade de Dados (Data Quality)

As seguintes validações do Great Expectations/Soda Core são aplicadas a este ativo:
- **Unicidade:** O campo `evento_id` deve ser único.
- **Relacionamentos:**
  - `carrinho_id` deve existir na tabela de `CARRINHOS`.
  - `cliente_id` deve existir na tabela de `CLIENTES`.
  - `produto_id` (se preenchido) deve existir na tabela de `PRODUTOS`.
- **Restrição de Domínio:** O campo `tipo_evento` deve conter apenas as categorias válidas mapeadas nas regras de negócio.
- **Integridade Temporal:** O campo `ocorrido_em` de qualquer evento deve ser maior ou igual à data de criação do carrinho associado (`carrinhos.criado_em`).
