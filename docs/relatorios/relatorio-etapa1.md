# Relatório — Etapa 1: Modelagem Lógica & DDL SQL

Este relatório documenta a entrega da **Etapa 1 (Modelagem Lógica e DDL)** do case técnico de estágio da Dadosfera para o domínio de **Recuperação de Carrinho Abandonado**.

---

## 1. Visão Geral do Domínio

O modelo de dados foi concebido para mapear de ponta a ponta a jornada do cliente em um e-commerce marketplace:
- Navegação e telemetria de sessão
- Composição e montantes do carrinho de compras
- Gatilhos de abandono e réguas de resgate omnicanal
- Conversão final em pedidos e geração de receita

---

## 2. Entidades do Modelo (7 Ativos)

| # | Entidade | Tipo | Descrição de Negócio |
|:---:|---|:---:|---|
| **1** | `clientes` | Dimensão | Cadastro de consumidores com segmentação comportamental RFM e canais de contato |
| **2** | `produtos` | Dimensão | Catálogo de SKUs com categorias, marcas, precificação e status de estoque |
| **3** | `carrinhos` | Fato Transacional | Entidade âncora que rastreia o ciclo de vida da sessão (ativo → abandonado → recuperado → comprado) |
| **4** | `itens_carrinho` | Fato / Linha | Itens unitários adicionados a cada sessão com snapshot do preço de inclusão |
| **5** | `eventos_carrinho` | Telemetria | Série temporal comportamental de micro-interações do usuário no funil |
| **6** | `eventos_resgate` | Fato de Comunicação | Execução de réguas de reativação via E-mail, WhatsApp, SMS e Push |
| **7** | `pedidos` | Fato de Venda | Transações concluídas que fecham a atribuição de conversão direta ou recuperada |

---

## 3. Padrão de Especificação — Blueprint Canônico

Todas as entidades lógicas são documentadas sob a estrutura canônica de 4 divisões em [`data/data-models/logical/entities/blueprint-entities-archive.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/data-models/logical/entities/blueprint-entities-archive.md):

1. **Data Definition**: Dicionário de dados completo com colunas, tipos, PK/FK, defaults e mapeamento relacional.
2. **Business Definition & Business Rules**: Granularidade, papel no domínio, ciclo de vida e regras de negócio numeradas (`01`, `02`...).
3. **Data Quality, Transformation & Lineage**: Validações declarativas por funções, Dual-Artifact Pipeline (Qualify vs. Anomaly) e linhagem em árvore ASCII.
4. **Governance & Consumption**: Owner, classificação de sensibilidade, política LGPD/PII e mapeamento de sistemas consumidores.

---

## 4. Decisões Arquiteturais da Etapa

- **DEC-004 (Execução Exclusiva na Dadosfera)**: Proibição de arquivos `.sql` manuais em produção. O SQL local (`data/database/sql/`) serviu estritamente como prototipação de schema.
- **DEC-006 (Dual-Artifact Pipeline & Separação Plataforma vs. Domínio)**: A plataforma de dados detecta desvios e registra evidências brutas no artefato de anomalias sem impor mutações operacionais arbitrárias.

---

## 5. Artefatos Produzidos

- **Modelagem Conceitual/Lógica**: `data/data-models/logical/`
- **Especificações de Entidades**: `data/data-models/logical/entities/`
- **Relacionamentos & Cardinalidades**: `data/data-models/logical/relationships.md`
- **Regras de Negócio Globais**: `data/data-models/logical/business-rules.md`
- **DDL SQL Inicial**: `data/database/sql/` (scripts `001_create_tables.sql` a `004_seed_test.sql`)
