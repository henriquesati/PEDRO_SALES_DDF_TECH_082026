# Relatório — Item 3: Sobre a Dadosfera — Explorar e Catalogar (Outputs Autocontidos)

> **Módulo:** `pipelines/case-item-03/outputs/`  
> **Status:** ✅ 7 Ativos Catalogados e Sincronizados com Dicionários de Dados  
> **Tenant Oficial:** `pedro-sales`  
> **API de Sincronização:** API Maestro (`https://maestro.dadosfera.ai`)  

---

## 1. Organização do Data Lakehouse (Arquitetura de Zonas)

Seguindo as definições recomendadas pela Dadosfera, o ciclo de vida dos dados do case de **Recuperação de Carrinho Abandonado** está estruturado em 3 zonas de maturidade:

```text
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

1. **Zona Raw (Bronze):** Armazena os arquivos de carga brutos gerados sinteticamente (`clientes.parquet`, `produtos.parquet`, `carrinhos.parquet`, etc.) dentro do Storage Explorer da Dadosfera no caminho `/raw/recuperacao_carrinho/`.
2. **Zona Qualify (Silver):** Contém as tabelas estruturadas criadas e tipadas no Snowflake no schema `CART_RECOVERY`. É a zona onde os dados são validados por regras de integridade e catalogados oficialmente no módulo **Explorar** da Dadosfera.
3. **Zona Curated (Gold):** Reservada para as visões analíticas agregadas (Data Views / Views SQL no Snowflake) que cruzam as dimensões e tabelas de fatos para consumo direto no Metabase (Item 7) e no Data App (Item 9).

---

## 2. Boas Práticas de Dicionário de Dados

Para garantir a democratização, governança e conformidade regulatória (LGPD) dos ativos de dados, foi estruturado um pipeline de documentação baseado em um **Blueprint Central**.

### 2.1 O Blueprint de Governança
Desenvolvemos um modelo padrão estruturado em Markdown que exige que cada ativo de dados possua:
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

Todas as 7 entidades foram catalogadas e sincronizadas na plataforma via API Maestro com seus Dicionários de Dados completos:

| Entidade | Data Asset ID (Dadosfera) | Link Direto no Catálogo | Zona | Nível de Sensibilidade | Tags Semânticas |
|:---|:---|:---|:---:|:---:|:---|
| **`clientes`** | `0327fecc-f826-48fb-bb0a-1493fe18a32c` | [Acessar clientes](https://app.dadosfera.ai/pt-BR/catalog/data-assets/0327fecc-f826-48fb-bb0a-1493fe18a32c) | Qualify | 🔴 Confidencial (PII) | `carrinho_abandonado`, `clientes`, `marketplace`, `qualify`, `dimensao`, `pii_sensivel` |
| **`produtos`** | `65fcfa25-a6f3-4cb8-a444-7fd23df3fa84` | [Acessar produtos](https://app.dadosfera.ai/pt-BR/catalog/data-assets/65fcfa25-a6f3-4cb8-a444-7fd23df3fa84) | Qualify | 🟢 Interno | `carrinho_abandonado`, `produtos`, `catalogo`, `qualify`, `dimensao` |
| **`carrinhos`** | `e2d3b1bb-bf22-456e-bc66-4ac843deec82` | [Acessar carrinhos](https://app.dadosfera.ai/pt-BR/catalog/data-assets/e2d3b1bb-bf22-456e-bc66-4ac843deec82) | Qualify | 🟢 Interno | `carrinho_abandonado`, `carrinhos`, `transacional`, `qualify`, `fato_central` |
| **`itens_carrinho`** | `7649755a-c6e8-4b56-a092-be9eefde1dab` | [Acessar itens_carrinho](https://app.dadosfera.ai/pt-BR/catalog/data-assets/7649755a-c6e8-4b56-a092-be9eefde1dab) | Qualify | 🟢 Interno | `carrinho_abandonado`, `itens_carrinho`, `itens`, `qualify`, `fato_detalhe` |
| **`eventos_carrinho`** | `397c3ebc-15cb-42d2-a717-a3b5d150c3ea` | [Acessar eventos_carrinho](https://app.dadosfera.ai/pt-BR/catalog/data-assets/397c3ebc-15cb-42d2-a717-a3b5d150c3ea) | Qualify | 🟢 Interno | `carrinho_abandonado`, `eventos_carrinho`, `telemetria`, `qualify`, `timeseries` |
| **`eventos_resgate`** | `04739f6d-e8c3-4d6f-80b7-0f98c12a5798` | [Acessar eventos_resgate](https://app.dadosfera.ai/pt-BR/catalog/data-assets/04739f6d-e8c3-4d6f-80b7-0f98c12a5798) | Qualify | 🟢 Interno | `carrinho_abandonado`, `eventos_resgate`, `recuperacao`, `qualify`, `crm_marketing` |
| **`pedidos`** | `7f82a988-8e68-416a-b6fa-5007c4789d1a` | [Acessar pedidos](https://app.dadosfera.ai/pt-BR/catalog/data-assets/7f82a988-8e68-416a-b6fa-5007c4789d1a) | Qualify | 🟢 Interno | `carrinho_abandonado`, `pedidos`, `conversoes`, `qualify`, `faturamento` |

---

## 4. Item Bônus: Automação via API Dadosfera

A catalogação e governança foram integradas via código por meio da API Maestro da Dadosfera.

### 4.1 Descobertas e Correções Técnicas (DEC-005)
1. **Formato de Autenticação (Header):** A API Maestro rejeita o prefixo `Bearer` no cabeçalho `Authorization`, resultando em `401 Unauthorized`. O envio é feito diretamente:
   ```http
   Authorization: <token_jwt>
   ```
2. **Guarda de Deduplicação & Sincronização:** Lógica idempotente via script Python:
   - Se o ativo já existe, executa `PUT /catalog/data-asset/{id}` atualizando tags e dicionário de dados em Markdown.
   - Se não existe, cria via `POST /catalog`.
3. **Gerenciamento de Duplicatas:** Ativos órfãos de testes foram isolados programaticamente com o prefixo `[DUPLICATA - IGNORAR]` e marcados com tags de lixeira.
