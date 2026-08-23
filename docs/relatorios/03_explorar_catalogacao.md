# Relatório — Item 3: Sobre a Dadosfera — Explorar e Catalogar

Este relatório documenta a entrega do **Item 3 (Fase de Exploração e Catalogação)** do case técnico de estágio da Dadosfera. Ele detalha a arquitetura de governança aplicada, as boas práticas de dicionário de dados adotadas e a automação de catalogação via API Maestro.

---

## 1. Organização do Data Lakehouse (Arquitetura de Zonas)

Seguindo as definições recomendadas pela Dadosfera, o ciclo de vida dos dados do case de **Recuperação de Carrinho Abandonado** está estruturado em 3 zonas de maturidade:

```
                  ┌──────────────────────────────────────────────┐
                  │          ZONAS DO DATA LAKEHOUSE             │
                  └──────────────────────┬───────────────────────┘
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        ▼                                ▼                                ▼
  [ ZONA RAW ]                  [ ZONA QUALIFY ]                 [ ZONA CURATED ]
  • Formato: CSV/Parquet        • Formato: Tabela Snowflake      • Formato: Snowflake Views
  • Origem: Ingestão Bruta      • Tratamento: Tipagem, DQ        • Consumo: BI (Metabase)
  • Storage: S3 Explorer        • Governança: Catalogado         • Lógica: RFM, KPIs, ROI
```

1. **Zona Raw (Bronze):** Armazena os arquivos de carga brutos gerados sinteticamente (`clientes.csv`, `produtos.csv`, `carrinhos.csv`, etc.) dentro do Storage Explorer da Dadosfera no caminho `/raw/recuperacao_carrinho/`.
2. **Zona Qualify (Silver):** Contém as tabelas estruturadas criadas e tipadas no Snowflake no schema `CART_RECOVERY`. É a zona onde os dados são validados por regras de integridade e catalogados oficialmente no módulo **Explorar** da Dadosfera.
3. **Zona Curated (Gold):** Reservada para as visões analíticas agregadas (Data Views / Views SQL no Snowflake) que cruzam as dimensões e tabelas de fatos para consumo direto no Metabase (Item 7) e no Data App (Item 9).

---

## 2. Boas Práticas de Dicionário de Dados

Para garantir a democratização, governança e conformidade regulatória (LGPD) dos ativos de dados, foi estruturado um pipeline de documentação baseado em um **Blueprint Central**.

### 2.1 O Blueprint de Governança
Desenvolvemos um modelo padrão estruturado em Markdown em [`blueprint_dicionario.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/blueprint/blueprint_dicionario.md) que exige que cada ativo de dados possua:
* **Metadados de Negócio:** Casos de uso práticos e descrição em linguagem acessível a usuários não-técnicos.
* **Metadados Técnicos:** Granularidade do dado, localização física, frequência de atualização e linhagem upstream/downstream.
* **Mapeamento de Relacionamentos:** Chaves primárias (PK) e chaves estrangeiras (FK) para rastreabilidade de linhagem de dados.
* **Metadados de Governança:** Classificação de sensibilidade e tags semânticas para busca no catálogo.
* **Dicionário de Atributos (Colunas):** Tipagem, nulabilidade, regras de domínio e descrição lógica.

### 2.2 Técnica de Definição Baseada em Classe
Seguindo a boa prática de engenharia de dados da Dadosfera, todas as descrições de colunas foram escritas utilizando a estrutura *"A é um B que C"*:
* *Exemplo (`clientes.email`):* *"O email é o endereço eletrônico (B) do cliente cadastrado (A) que serve como canal primário para envio de comunicações de resgate (C)."*

### 2.3 Governança de Dados Sensíveis (LGPD/PII)
Identificamos colunas com Dados Pessoais Identificáveis (PII) e mapeamos no dicionário:
* **Entidade `clientes`:** Colunas `nome`, `email` e `telefone` marcadas como sensíveis, exigindo restrições de visibilidade no catálogo de dados final para conformidade com a LGPD.

---

## 3. Catálogo Oficial de Ativos na Dadosfera

Todas as 7 entidades foram catalogadas e sincronizadas na plataforma via API Maestro com seus Dicionários de Dados completos. Abaixo o inventário consolidado:

| Entidade | Data Asset ID (Dadosfera) | Link Direto no Catálogo | Zona | Nível de Sensibilidade | Tags Semânticas | Dicionário Local |
|:---|:---|:---|:---:|:---:|:---|:---:|
| **`clientes`** | `0327fecc-f826-48fb-bb0a-1493fe18a32c` | [Acessar clientes](https://app.dadosfera.ai/pt-BR/catalog/data-assets/0327fecc-f826-48fb-bb0a-1493fe18a32c) | Qualify | 🔴 Confidencial (PII) | `carrinho_abandonado`, `clientes`, `marketplace`, `qualify`, `dimensao`, `pii_sensivel` | [clientes.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/clientes.md) |
| **`produtos`** | `65fcfa25-a6f3-4cb8-a444-7fd23df3fa84` | [Acessar produtos](https://app.dadosfera.ai/pt-BR/catalog/data-assets/65fcfa25-a6f3-4cb8-a444-7fd23df3fa84) | Qualify | 🟢 Interno | `carrinho_abandonado`, `produtos`, `catalogo`, `qualify`, `dimensao` | [produtos.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/produtos.md) |
| **`carrinhos`** | `e2d3b1bb-bf22-456e-bc66-4ac843deec82` | [Acessar carrinhos](https://app.dadosfera.ai/pt-BR/catalog/data-assets/e2d3b1bb-bf22-456e-bc66-4ac843deec82) | Qualify | 🟢 Interno | `carrinho_abandonado`, `carrinhos`, `transacional`, `qualify`, `fato_central` | [carrinhos.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/carrinhos.md) |
| **`itens_carrinho`** | `7649755a-c6e8-4b56-a092-be9eefde1dab` | [Acessar itens_carrinho](https://app.dadosfera.ai/pt-BR/catalog/data-assets/7649755a-c6e8-4b56-a092-be9eefde1dab) | Qualify | 🟢 Interno | `carrinho_abandonado`, `itens_carrinho`, `itens`, `qualify`, `fato_detalhe` | [itens_carrinho.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/itens_carrinho.md) |
| **`eventos_carrinho`** | `397c3ebc-15cb-42d2-a717-a3b5d150c3ea` | [Acessar eventos_carrinho](https://app.dadosfera.ai/pt-BR/catalog/data-assets/397c3ebc-15cb-42d2-a717-a3b5d150c3ea) | Qualify | 🟢 Interno | `carrinho_abandonado`, `eventos_carrinho`, `telemetria`, `qualify`, `timeseries` | [eventos_carrinho.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/eventos_carrinho.md) |
| **`eventos_resgate`** | `04739f6d-e8c3-4d6f-80b7-0f98c12a5798` | [Acessar eventos_resgate](https://app.dadosfera.ai/pt-BR/catalog/data-assets/04739f6d-e8c3-4d6f-80b7-0f98c12a5798) | Qualify | 🟢 Interno | `carrinho_abandonado`, `eventos_resgate`, `recuperacao`, `qualify`, `crm_marketing` | [eventos_resgate.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/eventos_resgate.md) |
| **`pedidos`** | `7f82a988-8e68-416a-b6fa-5007c4789d1a` | [Acessar pedidos](https://app.dadosfera.ai/pt-BR/catalog/data-assets/7f82a988-8e68-416a-b6fa-5007c4789d1a) | Qualify | 🟢 Interno | `carrinho_abandonado`, `pedidos`, `conversoes`, `qualify`, `faturamento` | [pedidos.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/pedidos.md) |

---

## 4. Item Bônus: Automação via API Dadosfera

A catalogação e governança foram integradas via código por meio da API Maestro da Dadosfera (Fase 5 do pipeline).

### 4.1 Descobertas e Correções Técnicas
Durante o desenvolvimento da integração via API, foram encontrados e solucionados os seguintes desafios técnicos:
1. **Formato de Autenticação (Header):** A API Maestro rejeitava o prefixo padrão `Bearer` no cabeçalho `Authorization`, resultando em erros `401 Unauthorized` nos scripts iniciais. O pipeline foi corrigido para enviar o token de acesso diretamente:
   ```http
   Authorization: eyJhbGciOiJFUzUxMiIs...
   ```
2. **Guarda de Deduplicação & Sincronização:** Como a API de criação de ativos (`POST /catalog`) não faz validação automática de duplicatas, implementamos uma lógica de sincronização no script [`catalog_assets.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/api/dadosfera/05_catalogar/catalog_assets.py):
   - Se o ativo já existe, faz `PUT /catalog/data-asset/{id}` atualizando as tags e o dicionário de dados em Markdown.
   - Se o ativo não existe, cria via `POST /catalog`.
3. **Gerenciamento de Duplicatas Existentes:** Os ativos órfãos criados nos testes preliminares foram renomeados sistematicamente para `[DUPLICATA - IGNORAR] <nome_ativo>` via `PUT /catalog/data-asset/{id}` e marcados com as tags `duplicata`, `ignorar`, `lixeira` para isolá-los e sinalizar a necessidade de expurgo manual na interface web da Dadosfera.

### 4.2 Mapeamento de Permissões da API (Conta de Estágio)
Auditar os limites da API ajudou a entender o comportamento de erros `403 Forbidden` na criação de tabelas e links. O perfil de permissões associado à nossa conta `pedro-sales` é:
* **Permissões Ativas (Catalog):** `GET /catalog`, `catalog:create`, `catalog:edit` (Permite listar, criar e atualizar metadados de ativos).
* **Permissões Ausentes (Storage Explorer):** `storage-explorer` (Operações de vinculação de arquivos, listagem e criação de tabelas Snowflake no banco de dados da plataforma resultam em `403 Forbidden` e devem ser operacionalizadas via interface web da Dadosfera).
* **Permissões Ausentes (Exclusão):** `catalog:delete` (Não permite exclusão definitiva de ativos via chamada HTTP `DELETE`, necessitando de intervenção na UI).

---

## 5. Referências Locais de Implementação

* **Blueprint de Governança:** [`blueprint_dicionario.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/blueprint/blueprint_dicionario.md)
* **Pipeline de Catalogação:** [`api/dadosfera/05_catalogar/catalog_assets.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/api/dadosfera/05_catalogar/catalog_assets.py)
* **Dicionários Completos Qualify:** [`data/catalogo/qualify/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/)
* **Documentação Técnica Geral da API:** [`agents_prompts_refs/dadosfera-api/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/agents_prompts_refs/dadosfera-api/)
* **Mapeamento JSON de Ativos:** [`assets_registry.json`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/agents_prompts_refs/dadosfera-api/output-mappers/assets_registry.json)
