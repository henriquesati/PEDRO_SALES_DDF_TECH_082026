# Especificação Visual & Técnica: Módulo de Governança, Dicionário de Dados & LGPD (`view-governanca`)

> **Momento do Roteiro**: **Ato 2 / Seção {3.1} — Governança e Dados: Dicionário de Dados, RBAC & Blindagem LGPD como Opt-in**  
> **Caminho da View**: `presentation/pitch/roteiro/view-03-dado-qualidades/view-governanca/`  
> **Padrão Visual**: Fundo Branco Puro (`#FFFFFF`), Proporção 16:9 Widescreen (300 DPI), Paleta Semântica Executiva (`charts-maker` standard).  
> **Fontes Estratégicas**: [`presentation/pitch/roteiro.txt`](../../roteiro.txt), [`data/catalogo/blueprint/blueprint_dicionario.md`](../../../../data/catalogo/blueprint/blueprint_dicionario.md) e [`data/catalogo/business-catalog-classification.md`](../../../../data/catalogo/business-catalog-classification.md).

---

## 🎯 1. Objetivo & Mensagem Estratégica no Pitch

Apresentar como a **Plataforma Dadosfera transforma segurança, compliance e governança de um gargalo burocrático de TI em um habilitador de negócios**, garantindo conformidade total com a LGPD através de opt-in mandatório, proteção ativa de dados pessoais (PII) e catálogo estruturado sem a complexidade de gerenciar códigos de infraestrutura (IAM JSON).

### 📌 Principais Mensagens de Fala:
1. **Dicionário de Dados Vivo & Padronizado (Regra de Ouro "A é um B que C")**:
   - Cada tabela e atributo possui definição formal de negócio, tipagem estrita, regras de validação e mapeamento de dependências upstream/downstream.
   - Vinculação direta aos **Data Asset IDs oficiais** da Dadosfera para descoberta autônoma por usuários de negócio.
2. **Blindagem LGPD "By Design" e Governança de Opt-in**:
   - **Tagging Semântico Automático**: Colunas sensíveis (`nome`, `email`, `telefone`) recebem classificação `Confidencial (PII / LGPD)` com políticas automáticas de anonimização e mascaramento.
   - **Opt-in Mandatório por Canal**: Disparos de recuperação exigem consentimento ativo (`permite_email = TRUE` e `permite_whatsapp = TRUE`).
   - **Interceptação Ativa (`ANOM-03`)**: Qualquer tentativa de envio sem consentimento formal é imediatamente isolada na camada de anomalias/quarentena antes de sair da plataforma, eliminando o risco de penalidades regulatórias.
3. **Fim do Gargalo de SecOps & Eliminação do "Shadow IT"**:
   - *Na AWS DIY*: Criar ou alterar acessos exige configurar políticas IAM em JSON, Lake Formation e chamados técnicos que levam de 3 a 6 semanas (induzindo equipes a exportar CSVs sem controle).
   - *Na Dadosfera*: RBAC intuitivo por perfis (Marketing, CRM, Analytics, Diretoria) em poucos cliques, liberando Data Views curadas com segurança total.

---

## 📚 2. Agrupamento & Referências Canônicas do Projeto

Tabela consolidada agrupando todos os scripts, especificações de catálogo, modelos de dados e artefatos visuais existentes no projeto referentes à Governança, Dicionário de Dados e LGPD:

| Categoria | Recurso / Artefato | Caminho do Arquivo | Descrição e Papel no Ecossistema |
| :--- | :--- | :--- | :--- |
| **Scripts de Catalogação** | 🐍 `catalog_assets.py` | [`api/dadosfera/05_catalogar/catalog_assets.py`](file:///C:/Users/pedro/OneDrive/Desktop/wheels/api/dadosfera/05_catalogar/catalog_assets.py) | Registra e vincula os 7 ativos de dados no Catálogo da Dadosfera via API Maestro com tags PII, descrições e schemas. |
| **Scripts de Execução** | 🐍 `run_pipeline.py` | [`api/dadosfera/run_pipeline.py`](file:///C:/Users/pedro/OneDrive/Desktop/wheels/api/dadosfera/run_pipeline.py) | Pipeline ponta a ponta integrando autenticação, tabelas, vinculação e catalogação na Dadosfera. |
| **Blueprint Normativo** | 📄 `blueprint_dicionario.md` | [`data/catalogo/blueprint/blueprint_dicionario.md`](file:///C:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/blueprint/blueprint_dicionario.md) | Modelo padronizado de documentação de dicionário de dados (identificação, visão de negócio, técnica, governança e formato JSON). |
| **Classificação de Dados** | 📄 `business-catalog-classification.md` | [`data/catalogo/business-catalog-classification.md`](file:///C:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/business-catalog-classification.md) | Diretrizes normativas de arquitetura Lakehouse, classificação de maturidade e governança Dual-Metadata (MD + JSON). |
| **Dicionário de Entidade** | 👤 `clientes.md` (Silver) | [`data/catalogo/qualify/clientes.md`](file:///C:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/clientes.md) | Dicionário canônico da entidade `CLIENTES` (Asset ID `0327fecc-...`), contendo regras "A é um B que C" e identificação de campos PII. |
| **Dicionários Relacionados** | 🛒 Entidades do Case | [`data/catalogo/qualify/`](file:///C:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/) | Dicionários de `carrinhos.md`, `pedidos.md`, `produtos.md`, `itens_carrinho.md`, `eventos_carrinho.md` e `eventos_resgate.md`. |
| **Dual-Metadata Contrato** | 📋 `metadata.md` & `json` | [`pipelines/datalakes/qualify/clientes_qualify/`](file:///C:/Users/pedro/OneDrive/Desktop/wheels/pipelines/datalakes/qualify/clientes_qualify/) | Arquivos de metadados humano e legível por máquina (`metadata.md` e `metadata.json`) da camada Qualify. |
| **Regras de Opt-in LGPD** | 🛡️ Data Quality ANOM-03 | [`pipelines/case-item-08/specs.md`](file:///C:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-08/specs.md) | Especificação das regras Great Expectations de bloqueio de disparos sem consentimento ativo (`permite_email`/`whatsapp`). |
| **Diagrama de Arquitetura** | 🏛️ Pilar 4 (Governança) | [`presentation/pitch/roteiro/arquitetura-view/arc-diagram-view/grafico-dadosfera-l2r.png`](file:///C:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/arquitetura-view/arc-diagram-view/grafico-dadosfera-l2r.png) | Diagrama consolidando o Pilar 4 (Governança Centralizada) substituindo Lake Formation e IAM JSON fragmentados. |
| **Gráfico Data Quality** | 🧪 Scorecard de Qualidade | [`presentation/pitch/06_data_quality_e_quarentena/chart_06_scorecard_data_quality.png`](file:///C:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/06_data_quality_e_quarentena/chart_06_scorecard_data_quality.png) | Scorecard executivo demonstrando 94.2% de conformidade e 5.8% de anomalias isoladas em quarentena. |
| **Gráfico Comparativo** | ⚖️ Eficiência Dadosfera | [`presentation/pitch/07_arquitetura_dadosfera_vs_aws/chart_07_arquitetura_dadosfera_vs_aws.png`](file:///C:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/07_arquitetura_dadosfera_vs_aws/chart_07_arquitetura_dadosfera_vs_aws.png) | Comparativo de governança: Redução de Lead Time de 6 semanas para < 3 dias (-86%) e fim do risco de Shadow IT. |

---

## 🎨 3. Sugestão de Composição da View (`chart_governanca_lgpd.png`)

A view executiva para esta seção foi projetada no formato **16:9 Widescreen (300 DPI)** com layout equilibrado (Split-Screen 50%/50%):

```text
+-------------------------------------------------------------------------------------------------------------------+
|  [ ATO 2 / SEÇÃO {3.1} ]  GOVERNANÇA, CATÁLOGO & LGPD                                                             |
|  Catálogo & Governança Ativa: Dicionário Vivo, RBAC Centralizado e Blindagem LGPD                                  |
|  Plataforma Dadosfera: Tagging PII automático, conformidade de opt-in mandatório e governança ágil self-service    |
+-------------------------------------------------------------------------------------------------------------------+
|  [CARD 1: ATIVOS CANÔNICOS]             [CARD 2: BLINDAGEM LGPD BY DESIGN]       [CARD 3: GOVERNANÇA ÁGIL & RBAC] |
|  7 Ativos Integrados                    100% Proteção PII                        < 3 Dias Lead Time               |
|  100% Linhagem Mapeada • Regra "A é B"  Opt-in Mandatório por Canal (ANOM-03)    Self-Service Seguro • Sem Silos  |
+-------------------------------------------------------------------------------------------------------------------+
|  [PAINEL ESQUERDO: DICIONÁRIO VIVO]                 |  [PAINEL DIREITO: CONTRATO EXECUTIVO DE METADADOS & RBAC]   |
|  • Cabeçalho: CLIENTES (Qualify / Silver)          |  • Cabeçalho: CONTRATO EXECUTIVO: METADADOS & RBAC (DEC-006)|
|  • Caixa Canônica ("A é um B que C"):               |  • Bloco 1: Identificação & Linhagem Ativa                  |
|    "Cliente é a pessoa física compradora..."        |    Asset ID: 0327fecc-... • Snowflake: CART_RECOVERY.CLIENTES|
|  • Tabela Estruturada de Atributos:                |  • Bloco 2: Matriz de Controle de Acesso por Papel (RBAC):  |
|    - cliente_id (VARCHAR)  [ Público / PK ]         |    - CRM_OPS             -> [ READ_MASKED ]                 |
|    - nome (VARCHAR)        [ PII Mascarado ]        |    - MARKETING_ANALYTICS -> [ AGGREGATED_ONLY ]             |
|    - email (VARCHAR)       [ PII / Opt-In ]         |    - DATA_ENGINEERING    -> [ FULL_AUDITED ]                |
|    - telefone (VARCHAR)    [ PII / Opt-In ]         |  • Bloco 3: Políticas de Blindagem LGPD & Quarentena:       |
|    - segmento (VARCHAR)    [ RFM Cluster ]          |    - Opt-in Mandatório: STRICT_ENFORCEMENT (ANOM-03)        |
|    - ltv_estimado (FLOAT)  [ Métrica Gold ]         |    - Anonimização Dinâmica: SHA256_DYNAMIC_SALT             |
|  • Tags de Governança no Rodapé                     |    - Ação de Quarentena: ISOLATE_INTO_ANOMALIES_TABLE       |
+-------------------------------------------------------------------------------------------------------------------+
|  [BANNER INFERIOR: CICLO DE VIDA DA GOVERNANÇA ATIVA]                                                             |
|  (1. Ingestão Bruta) ➔ (2. Tagging PII) ➔ (3. Validação Opt-In) ➔ (4. Quarentena Ativa) ➔ (5. Data Views Seguras)|
|  Fonte: Catálogo & Governança Dadosfera | Framework Normativo LGPD & Dual-Metadata (DEC-006) | charts-maker 300 DPI|
+-------------------------------------------------------------------------------------------------------------------+
```

---

## 📂 4. Estrutura de Arquivos do Módulo

Seguindo a regra de governança onde **pastas normais de view não contêm subdiretório `assets/`**:

```text
presentation/pitch/roteiro/view-03-dado-qualidades/view-governanca/
├── spec.md                     # 📄 Esta especificação técnica com narrativa e referências
├── generate_chart.py           # 🐍 Script declarativo pronto para renderização
└── chart_governanca_lgpd.png   # 📊 Artefato gráfico executivo em alta resolução (300 DPI)
```

