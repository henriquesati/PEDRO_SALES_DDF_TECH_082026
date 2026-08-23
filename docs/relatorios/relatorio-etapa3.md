# Relatório — Etapa 3: Catálogo, Governança & Data Lakehouse Dadosfera

Este relatório documenta a entrega da **Etapa 3 (Item 3: Sobre a Dadosfera — Explorar e Catalogar)** do case técnico de estágio da Dadosfera para o domínio de **Recuperação de Carrinho Abandonado**.

---

## 1. Organização do Data Lakehouse (Zonas de Maturidade)

Seguindo as melhores práticas da Dadosfera, os dados do case estão estruturados em 3 zonas:

```text
[ ZONA RAW (Bronze) ]       ──► [ ZONA QUALIFY (Silver) ]   ──► [ ZONA CURATED (Gold) ]
• Formato: CSV/Parquet          • Formato: Tabela Snowflake     • Formato: Views Snowflake
• Origem: Ingestão Bruta        • Tratamento: Tipagem, DQ       • Consumo: Metabase & Data App
• Storage: S3 Explorer          • Governança: Catalogado        • Lógica: RFM, Conversão, ROI
```

---

## 2. Boas Práticas de Dicionário & Governança

- **Blueprint de Governança**: Documentação estruturada em [`data/catalogo/blueprint/blueprint_dicionario.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/blueprint/blueprint_dicionario.md) com metadados de negócio, técnicos, linhagem, integridade e regras de Data Quality.
- **Técnica de Definição Baseada em Classe**: Todas as descrições de colunas foram redigidas no formato *"A é um B que C"*.
- **Governança LGPD / PII**: Identificação e isolamento de atributos sensíveis (`nome`, `email`, `telefone` na entidade `clientes`).
- **Prevenção de Duplicatas (DEC-005)**: Automação via API Maestro com verificação prévia de ativos (`catalog_assets.py`) para evitar geração descontrolada de IDs duplicados.

---

## 3. Inventário Oficial de Ativos na Dadosfera

Todos os 7 ativos foram integrados, catalogados e sincronizados via API Maestro no catálogo oficial da Dadosfera:

| Entidade | Data Asset ID (Dadosfera) | Link Direto no Catálogo | Zona | Sensibilidade | Tags Principais | Dicionário Local |
|---|---|:---:|:---:|:---:|---|:---:|
| `clientes` | `0327fecc-f826-48fb-bb0a-1493fe18a32c` | [Acessar](https://app.dadosfera.ai/pt-BR/catalog/data-assets/0327fecc-f826-48fb-bb0a-1493fe18a32c) | Qualify | 🔴 Confidencial (PII) | `carrinho_abandonado`, `clientes`, `qualify`, `pii_sensivel` | [clientes.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/clientes.md) |
| `produtos` | `65fcfa25-a6f3-4cb8-a444-7fd23df3fa84` | [Acessar](https://app.dadosfera.ai/pt-BR/catalog/data-assets/65fcfa25-a6f3-4cb8-a444-7fd23df3fa84) | Qualify | 🟢 Interno | `carrinho_abandonado`, `produtos`, `qualify`, `dimensao` | [produtos.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/produtos.md) |
| `carrinhos` | `e2d3b1bb-bf22-456e-bc66-4ac843deec82` | [Acessar](https://app.dadosfera.ai/pt-BR/catalog/data-assets/e2d3b1bb-bf22-456e-bc66-4ac843deec82) | Qualify | 🟢 Interno | `carrinho_abandonado`, `carrinhos`, `qualify`, `fato_central` | [carrinhos.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/carrinhos.md) |
| `itens_carrinho` | `432822a1-e346-4cb4-9fae-e2e4ff7f45c4` | [Acessar](https://app.dadosfera.ai/pt-BR/catalog/data-assets/432822a1-e346-4cb4-9fae-e2e4ff7f45c4) | Qualify | 🟢 Interno | `carrinho_abandonado`, `itens_carrinho`, `qualify`, `fato_itens` | [itens_carrinho.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/itens_carrinho.md) |
| `eventos_carrinho` | `aa766468-b80c-43f1-bd12-f705574aa9d7` | [Acessar](https://app.dadosfera.ai/pt-BR/catalog/data-assets/aa766468-b80c-43f1-bd12-f705574aa9d7) | Qualify | 🟢 Interno | `carrinho_abandonado`, `eventos_carrinho`, `qualify`, `telemetria` | [eventos_carrinho.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/eventos_carrinho.md) |
| `eventos_resgate` | `9b3aa5a4-58ff-4217-bfd2-eb41870bbcf0` | [Acessar](https://app.dadosfera.ai/pt-BR/catalog/data-assets/9b3aa5a4-58ff-4217-bfd2-eb41870bbcf0) | Qualify | 🟢 Interno | `carrinho_abandonado`, `eventos_resgate`, `qualify`, `marketing_crm` | [eventos_resgate.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/eventos_resgate.md) |
| `pedidos` | `9b5d2036-7c09-42b7-86c4-640a324b1a45` | [Acessar](https://app.dadosfera.ai/pt-BR/catalog/data-assets/9b5d2036-7c09-42b7-86c4-640a324b1a45) | Qualify | 🟢 Interno | `carrinho_abandonado`, `pedidos`, `qualify`, `conversao_fato` | [pedidos.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/pedidos.md) |

---

## 4. Artefatos Produzidos

- **Dicionários Locais**: `data/catalogo/qualify/` (7 arquivos detalhados)
- **Blueprint de Catálogo**: `data/catalogo/blueprint/blueprint_dicionario.md`
- **Output Mappers & IDs Oficiais**: `agents_prompts_refs/dadosfera-api/output-mappers/assets_registry.md` e `.json`
- **Scripts de Integração com a API Maestro**: `api/dadosfera/` (`05_catalogar/catalog_assets.py`)
