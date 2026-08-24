# Especificação: Exploração & Catalogação de Ativos na Plataforma Dadosfera

**Doc ID**: `spec_catalog_governance_001`  
**Versão**: 1.1  
**Módulo:** `pipelines/case-item-03/`  
**Case Oficial Dadosfera:** Item 3 — Sobre a Dadosfera: Explorar e Catalogar  
**Escopo**: Case Técnico de Estágio em Engenharia de Soluções / Dados (Dadosfera)  
**Status**: Concluído & Sincronizado via API  

---

## 📋 1. Requisitos Oficiais da Empresa (Dadosfera)

> Fonte: [`specs-internship.txt`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/agents_prompts_refs/case-internship-files/specs-internship.txt)

```text
Item 3 - Sobre a Dadosfera - Explorar
Usando os seus conhecimentos e da documentação da Dadosfera, faça a carga desse dataset, catalogue-o com as informações mais relevantes, seguindo boas práticas de Dicionário de Dados.  

Lembre-se de organizar os dados seguindo as definições comuns de um Data Lake. Abaixo um desenho das zonas que comumente são usadas pela Dadosfera para organização dos dados (Raw -> Qualify -> Curated).

Bônus: Usar a API da Dadosfera para Catalogar os ativos gerados automaticamente.
```

### Escala de Avaliação do Case
- **Mínimo:** Dicionário de dados básico no catálogo web da Dadosfera.
- **Avançado:** Organização completa em 3 zonas de Data Lake (Raw, Qualify, Curated) e conformidade com LGPD/PII.
- **Excelente / Outlier:** Automação total de catalogação via API Maestro (`https://maestro.dadosfera.ai`), 7 ativos registrados e vinculados com Data Asset IDs oficiais, técnica de descrição baseada em classe (*"A é um B que C"*), e isolamento preventivo de duplicatas órfãs (DEC-005).

---

## 🏛️ 2. Arquitetura de Zonas do Data Lakehouse

```text
                  ┌──────────────────────────────────────────────┐
                  │          ZONAS DO DATA LAKEHOUSE             │
                  └──────────────────────┬───────────────────────┘
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        ▼                                ▼                                ▼
  [ ZONA RAW ]                  [ ZONA QUALIFY ]                 [ ZONA CURATED ]
  • Formato: Parquet / CSV      • Formato: Tabela Snowflake      • Formato: Snowflake Views
  • Origem: Ingestão Bruta      • Tratamento: Tipagem, DQ        • Consumo: BI (Metabase)
  • Storage: S3 Explorer        • Governança: Catalogado         • Lógica: RFM, KPIs, ROI
```

1. **Zona Raw (Bronze):** Arquivos brutos gerados sinteticamente armazenados no Storage Explorer da Dadosfera no caminho `/raw/recuperacao_carrinho/`.
2. **Zona Qualify (Silver):** Tabelas estruturadas criadas e tipadas no Snowflake no schema `CART_RECOVERY`, validadas pelo pipeline de Data Quality e catalogadas no módulo **Explorar** da Dadosfera.
3. **Zona Curated (Gold):** Visões analíticas agregadas (Data Views) que cruzam dimensões e fatos para consumo direto no Metabase (Item 7) e no Data App (Item 9).

---

## 📚 3. Padrão de Dicionário de Dados & Governança LGPD

### 3.1 Técnica de Definição Baseada em Classe
Todas as descrições de colunas adotam a estrutura formal:
> *"A é um B que C"*  
> *(Ex: "O email é o endereço eletrônico [B] do cliente cadastrado [A] que serve como canal primário para envio de comunicações de resgate [C].")*

### 3.2 Governança de PII e Conformidade LGPD
- **Entidade `clientes`:** Colunas `nome`, `email` e `telefone` classificadas com nível de sensibilidade 🔴 **Confidencial (PII)** e etiquetadas com a tag `pii_sensivel`.
- Demais entidades (`produtos`, `carrinhos`, `itens_carrinho`, `eventos_carrinho`, `eventos_resgate`, `pedidos`): Classificadas com nível 🟢 **Interno**.

---

## 🌐 4. Catálogo de Ativos Registrados na Dadosfera (Source of Truth)

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

## ⚡ 5. Automação via API Maestro (DEC-005)

1. **Autenticação:** Header HTTP `Authorization: <token_jwt>` direto (sem prefixo `Bearer`).
2. **Deduplicação / Sincronização:** Verificação prévia de ID para atualização via `PUT /catalog/data-asset/{id}` e prevenção de duplicatas via `POST /catalog`.
3. **Isolamento de Duplicatas:** Tratamento programático de duplicatas órfãs renomeando para `[DUPLICATA - IGNORAR]` e tagueamento com `duplicata`, `ignorar`, `lixeira`.
