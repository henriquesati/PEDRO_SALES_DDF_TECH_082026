# Dicionário de Dados: produtos_enriquecidos

Dicionário de dados da entidade de Produtos Enriquecidos com GenAI & LLMs, contendo especificações técnicas normalizadas, diagnósticos semânticos de atrito de checkout e copies prescritivas de resgate para CRM.

---

## 📌 Identificação do Ativo de Dados

- **Nome Físico:** `PRODUTOS_ENRIQUECIDOS`
- **Nome de Exibição (Display Name):** `produtos_enriquecidos`
- **Data Asset ID (Dadosfera):** `78aeef12-9c41-4da2-b118-8ee12cf4da99`
- **URL Direta no Catálogo:** [Acessar produtos_enriquecidos](https://app.dadosfera.ai/pt-BR/catalog/data-assets/78aeef12-9c41-4da2-b118-8ee12cf4da99)

---

## 💼 Visão de Negócio

### Descrição de Negócio
A tabela `produtos_enriquecidos` é uma entidade de dimensão analítica avançada na camada Silver Qualify. Ela transforma descrições técnicas extensas e feedbacks de clientes pós-abandono em **atributos estruturados de inteligência de catálogo e CRM**. Permite correlacionar complexidade de especificações com taxas de abandono, além de fornecer copies persuasivas prontas para automação de mensagens de resgate (Email / WhatsApp).

### Principais Casos de Uso
- Diagnosticar se dúvidas de compatibilidade ou especificações confusas estão gerando atrito no checkout.
- Segmentar campanhas de recuperação por sensibilidade a preço e urgência sem degradar a margem com descontos excessivos.
- Alimentar o simulador de recuperação de receita no Data App Streamlit (Item 9) e visualizações no Metabase (Item 7).

---

## ⚙️ Visão Técnico-Operacional

### Especificações Gerais
- **Zona do Data Lakehouse:** Qualify (Silver)
- **Formato Físico:** Tabela Snowflake / Parquet
- **Localização Física no Lakehouse:** `pipelines/datalakes/qualify/produtos_enriquecidos_qualify/`
- **Tabela Snowflake:** `CART_RECOVERY.PRODUTOS_ENRIQUECIDOS`
- **Granularidade:** Uma linha por SKU enriquecido com diagnóstico semântico.
- **Frequência de Atualização:** Execução sob demanda / Batch diário de enriquecimento GenAI.

### Integridade e Relacionamentos (Linhagem)
- **Origem (Lineage Upstream):**
  - `CART_RECOVERY.PRODUTOS` (dados cadastrais)
  - Pesquisas e feedbacks de checkout pós-abandono em texto livre
  - Tickets e registros de atendimento ao cliente (SAC)
- **Destino (Lineage Downstream):**
  - Camada Curated / Gold (`v_recovery_roi_by_segment`)
  - Dashboards de BI no Metabase (Item 7)
  - Data App Streamlit (Item 9) e Vitrines GenAI
- **Chave Primária (PK):** `produto_id`

---

## 🛡️ Governança & Sensibilidade

- **Proprietário do Dado (Owner):** Inteligência de IA, CRM & Merchandising
- **Classificação de Sensibilidade:** Interno — Não contém dados pessoais (PII).
- **Tags de Governança:** `genai`, `llm`, `features_semanticas`, `produtos`, `qualify`, `silver`, `carrinho_abandonado`

---

## 📊 Dicionário de Atributos (Colunas)

| Campo Físico | Tipo de Dado | Chave | Nullable | Descrição de Negócio (A é um B que C) | Valores Válidos / Regras | Exemplo de Valor | PII? |
|:---|:---:|:---:|:---:|:---|:---|:---|:---:|
| `produto_id` | `INTEGER` | `PK` | `Não` | O produto_id é um identificador numérico que referencia de forma unívoca o SKU do catálogo de produtos. | Inteiro positivo $> 0$ | `101` | `Não` |
| `nome_bruto` | `VARCHAR(255)` | — | `Não` | O nome_bruto é a descrição comercial original do produto conforme cadastrada no catálogo. | Texto livre | `Samsung Galaxy S24 Ultra 512GB` | `Não` |
| `preco_atual` | `DECIMAL(10,2)` | — | `Não` | O preco_atual é o valor monetário vigente de venda do item em Reais (BRL). | Valor positivo $> 0.00$ | `6899.00` | `Não` |
| `categoria_normalizada` | `VARCHAR(100)` | — | `Não` | A categoria_normalizada é uma taxonomia padronizada por IA que agrupa o produto no marketplace. | `Eletrônicos`, `Informática`, `Áudio e Fones`, etc. | `Eletrônicos` | `Não` |
| `subcategoria` | `VARCHAR(100)` | — | `Não` | A subcategoria é um agrupamento de segundo nível que especifica a família técnica do item. | Texto descritivo | `Smartphones Flagship` | `Não` |
| `marca` | `VARCHAR(100)` | — | `Não` | A marca é o nome do fabricante extraído e padronizado pelo modelo de linguagem. | Texto padronizado | `Samsung` | `Não` |
| `material_construcao` | `VARCHAR(255)` | — | `Não` | O material_construcao é um atributo físico que descreve os materiais e acabamentos predominantes. | Texto livre | `Titânio e Vidro Gorilla Armor` | `Não` |
| `diferencial_tecnico` | `VARCHAR(255)` | — | `Não` | O diferencial_tecnico é a especificação-chave de maior valor agregado do produto. | Texto conciso | `Câmera 200MP + S-Pen + Zoom 100x` | `Não` |
| `faixa_posicionamento` | `VARCHAR(50)` | — | `Não` | A faixa_posicionamento é uma classificação de mercado que define o tier do produto. | `Entrada`, `Intermediario`, `Premium`, `Luxo` | `Luxo` | `Não` |
| `requer_compatibilidade` | `BOOLEAN` | — | `Não` | O requer_compatibilidade é uma flag booleana que indica se o produto depende de voltagem ou dimensões específicas. | `TRUE`, `FALSE` | `FALSE` | `Não` |
| `motivo_raiz` | `VARCHAR(255)` | — | `Não` | O motivo_raiz é a causa semântica fundamental do abandono de checkout diagnosticada pela IA. | Texto explicativo | `Frete Alto / Prazo Longo` | `Não` |
| `sentimento` | `VARCHAR(50)` | — | `Não` | O sentimento é a polaridade emocional do cliente detectada no feedback de checkout. | `Positivo`, `Neutro`, `Hesitante`, `Frustrado` | `Hesitante` | `Não` |
| `nivel_urgencia` | `VARCHAR(50)` | — | `Não` | O nivel_urgencia é a intensidade temporal da necessidade de compra inferida pelo modelo. | `Baixo`, `Medio`, `Alto` | `Alto` | `Não` |
| `sensibilidade_preco` | `VARCHAR(50)` | — | `Não` | A sensibilidade_preco é a elasticidade-preço percebida no comportamento do comprador. | `Baixa`, `Media`, `Alta` | `Media` | `Não` |
| `estrategia_recomendada` | `VARCHAR(255)` | — | `Não` | A estrategia_recomendada é uma diretriz prescritiva para a equipe de CRM recuperar o carrinho. | Texto de ação | `Oferecer frete grátis expresso` | `Não` |
| `gatilho_mental` | `VARCHAR(50)` | — | `Não` | O gatilho_mental é o apelo persuasivo principal a ser empregado na comunicação. | `Escassez`, `Urgencia`, `Prova Social`, `Desconto`, `Suporte`, `Frete Gratis` | `Frete Gratis` | `Não` |
| `copy_resgate_email` | `TEXT` | — | `Não` | A copy_resgate_email é o texto completo gerado pela IA para envio via Email Marketing. | Texto persuasivo | *"Seu Galaxy S24 Ultra está reservado..."* | `Não` |
| `copy_resgate_whatsapp` | `TEXT` | — | `Não` | A copy_resgate_whatsapp é a mensagem curta gerada para abordagem via WhatsApp. | Texto conciso | *"Olá! Vimos que o Galaxy S24 Ultra..."* | `Não` |
