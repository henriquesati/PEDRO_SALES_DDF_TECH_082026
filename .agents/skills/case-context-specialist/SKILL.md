---
name: case-context-specialist
description: Fonte central de contexto estratégico, requisitos e direção geral do case técnico de estágio na Dadosfera. Consulta os materiais fornecidos pela empresa e orienta outros agentes sobre objetivos, expectativas, análises e decisões do projeto.
---

# Skill: Case Context Specialist

## 🎯 Objetivo & Missão
Atuar como a **fonte central de contexto estratégico do case de estágio**. Esta skill armazena o entendimento consolidado do que a empresa propôs, qual problema de negócio está sendo tratado, quais análises são esperadas e quais decisões já foram tomadas.

Serve como fonte de contexto para outros agentes que precisam entender **por quê** o projeto está sendo construído, **o que** precisa ser entregue e **como** as decisões técnicas devem se alinhar com os objetivos do case.

---

## 📌 Contexto Consolidado do Case

### Empresa
- **Dadosfera**: Plataforma SaaS de dados fundada em 2019 (ex-DataSprints).
- **Proposta**: Sistema operacional de dados que centraliza ingestão, transformação, catálogo, governança, analytics e GenAI.

### Cenário do Case
- **Papel do candidato**: Profissional de Dados da Dadosfera construindo um projeto de implementação da plataforma em um cliente.
- **Cliente fictício**: Grande empresa de e-commerce construindo uma Plataforma de Dados para análises descritivas e prescritivas com agilidade e baixo custo.
- **Problema central proposto por Pedro**: **Recuperação de Carrinho Abandonado** como case carro-chefe (demonstração direta de valor: ROI e conversão).

### Por que Recuperação de Carrinho?
- Fácil demonstração de valor e ROI mensurável.
- Cenário de e-commerce se encaixa perfeitamente na narrativa do case.
- Permite showcasing de todo o ciclo de vida dos dados (Integrar → IA Generativa).
- Base gerada sinteticamente com 116k+ registros (acima do mínimo de 100k exigido).

---

## 📋 Itens do Case (Requisitos da Empresa)

> Fonte: [`specs-internship.txt`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/agents_prompts_refs/case-internship-files/specs-internship.txt)

### Escala de Avaliação
| Nível | Requisito |
|---|---|
| **Mínimo** | Itens 2, 3, 4 e 7 + Github |
| **Intermediário** | Mínimo + Item 1 (apresentação em vídeo) |
| **Avançado** | Intermediário + Item 9 (Data Apps) |
| **Excelente** | Avançado + case bônus |
| **Outlier** | Extrapolar o que foi pedido |

### Checklist Detalhado

| Item | Tema | Fase do Ciclo | Descrição Resumida | Status |
|---|---|---|---|---|
| 0 | Agilidade & Planejamento | — | Artefato de planejamento (PMBOK): fluxo iterativo, gantt/kanban/checklist | ✅ Concluído |
| 1 | Base de Dados | Integrar | Propor/gerar base de dados (mín. 100k registros) | ✅ Concluído (115.777+ registros via gerador modular declarativo em Parquet/CSV) |
| 2.1 | Dadosfera - Integrar | Integrar | Carregar dados na plataforma Dadosfera via módulo de Coleta | ⏳ Planejado |
| 3 | Dadosfera - Explorar | Explorar | Catalogar dataset com dicionário de dados, organizar por zonas do Data Lake | ✅ Concluído (Blueprint + Qualify + API) |
| 4 | Data Quality | Processar | Relatório e evidências de qualidade geradas no módulo do notebook (`notebooks/pipelines/quality_report/outputs/data_quality_report.md`), notebook de qualificação (`notebooks/pipelines/quality_report/qualification_raw.ipynb`), suíte Great Expectations (18 regras) e quarentena de anomalias em Parquet | ✅ Concluído |
| 5 | GenAI & LLMs - Processar | Processar | Transformar dados desestruturados em features usando IA | ⏳ Planejado |
| 6 | Modelagem de Dados | Analisar | Modelagem lógica canônica (4 divisões, SCHEMA RULES numerado, TRUE/FALSE, 6 entidades) | ✅ Concluído |
| 7 | Análise de Dados | Analisar | Dashboard com análise de categorias + série temporal. 6 visualizações de 6 tipos distintos geradas em alta resolução (`dashboards/assets/`), catálogo declarativo (`chart_specs.py`) e notebook interativo | ✅ Concluído |
| 8 | Pipelines | Processar | Pipeline ETL/ML na Dadosfera (módulo de inteligência) | ⏳ Planejado |
| 9 | Data Apps | Consumir | Data App com Streamlit para explorar dados | ⏳ Planejado |
| 10 | Apresentação | — | Vídeo no YouTube: prova de conceito Dadosfera vs arquitetura atual do cliente | ⏳ Planejado |
| Bônus | GenAI + Data Apps | IA Generativa | Gerador de apresentações de produto com DALL-E ou similar | ⏳ Planejado |

---

## 📐 Formato de Entrega (Requisitos Formais)

- **Repositório Github**: `<primeiro_nome>_<ultimo_nome>_DDF_TECH_<mes><ano>` → `PEDRO_SALES_DDF_TECH_082026`
- **Formato**: Markdown com LINKS para ativos na Dadosfera e PRINTS evidenciando datasets, dashboards e data apps.
- **Vídeo**: Unlisted no YouTube, acessível por qualquer usuário com o link.
- **Python/Data Apps/LLMs**: Usar Google Colab. README deve explicar como subir Data App via Streamlit.
- **Regra crítica**: Análises não catalogadas na Dadosfera ou não reprodutíveis pelo repositório NÃO serão avaliadas.

---

## 🏗️ Arquitetura do Cliente (Referência para Item 10)

> Fonte: [`raw (1).md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/agents_prompts_refs/case-internship-files/raw%20(1).md)

### Stack Atual (AWS)
- **Lambda + Kinesis Stream**: Configuração manual de shards.
- **Firehose**: Latência de buffering.
- **S3 Bucket**: Data Lake sem schema enforcement.
- **Redis (ElastiCache)**: Complexidade entre modos standalone/cluster.

### Pain Points Identificados
1. Complexidade de serviços não gerenciados.
2. Headcount crescente proporcional ao volume de dados.
3. Fragilidade em períodos de pico (Black Friday, etc.).
4. Lead time de 3-6 semanas para novos apps.
5. Governança dispersa e difícil de auditar.

### Proposta Dadosfera
A Dadosfera substitui a complexidade da infraestrutura com: ingestão plug & play, transformação centralizada, catálogo e governança automáticos, consumo/analytics integrado, segurança/IAM centralizado, e IA/GenAI nativa.

---

## 🧭 Decisões Estratégicas Consolidadas

> Apenas decisões fundamentais já validadas. Para novas decisões, registrar em `relatorios/decision-making/` como arquivos separados.

### DEC-001: Métricas em % ao invés de R$
- **Decisão**: O pitch se ancora em taxas, ratios e eficiência — não em valores monetários absolutos.
- **Justificativa**: Transferibilidade (funciona para qualquer ticket médio), desacoplamento (o valor é a capacidade, não o R$), credibilidade (dados mock + valores absolutos = "fabricado"), escalabilidade do argumento.
- **Impacto**: Todas as métricas do METRICS.md usam 5 camadas hierárquicas em % (Conversão → Canal → RFM → Operacional → Timing). Valores monetários ficam como contexto secundário.
- **Referência**: [`pitch.txt`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/relatorios/decision-making/pitch/pitch.txt)

### DEC-002: Base sintética ao invés de dataset público
- **Decisão**: Gerar dados mock com geradores Python modulares e declarativos (`data/mock/generators/parquet/`) ao invés de usar AdventureWorks, NYC Taxi, etc.
- **Justificativa**: Controle total sobre métricas realistas (taxa de abandono ~70%, recuperação ~10%, ROI ~31x), dirty data determinístico (cotas mínimas garantidas de e-mails nulos/inválidos, frete negativo, total inconsistente, promoções invertidas, inversões temporais e dados órfãos), aderência exata ao domínio de carrinho abandonado, e parametrização desacoplada via `config/settings.py` e perfis (`standard` ~116k, `rich` ~160k, `dev` ~12k) — garantindo dados significativos e auditáveis para o pitch.
- **Impacto**: 115.777+ registros gerados no perfil padrão (superando o mínimo de 100k), scripts reprodutíveis e extensíveis em `data/mock/generators/parquet/`.
- **Referência**: [`METRICS.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/mock/METRICS.md)

### DEC-003: Insights em Markdown ao invés de formatos específicos
- **Decisão**: Especificar insights e métricas como documentos Markdown estruturados, não como queries SQL ou código.
- **Justificativa**: Documentação mais próxima da linguagem humana, funcionando como blueprint expansivo de dados. Separação entre especificação e implementação — o mesmo insight pode gerar SQL, views na Dadosfera, visualizações no Metabase ou cards num Data App. Reutilizável por diferentes agentes ou formatos.
- **Impacto**: Insights organizados em `insights/` por categoria (01_descriptive, 02_risk, 03_prescriptive, 04_opportunity).
- **Referência**: Skill [`cart-recovery-insights`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/.agents/skills/cart-recovery-insights/SKILL.md)

### DEC-004: Proibição de arquivos .SQL locais — Execução exclusiva na Dadosfera
- **Decisão**: É terminantemente proibido criar novos arquivos `.sql` ou manter lógica de banco localmente. Toda criação de views, pipelines e consultas analíticas deve ser feita exclusivamente dentro da plataforma Dadosfera (módulos de Coleta, Inteligência/Pipelines e Visualizar/Metabase).
- **Justificativa**: O case técnico avalia a implementação dentro da Dadosfera. A regra formal do case é explícita: *"Qualquer outra análise ou trabalho feito que não esteja catalogado na Dadosfera ou reprodutíveis pelo repositório no Github NÃO serão avaliados"*. Os arquivos em `data/database/sql/` foram apenas DDL inicial de prototipação na Etapa 1.
- **Impacto**:
  - Todo o trabalho analítico no repositório limita-se a especificações em Markdown (`insights/`, `dashboards/`, `metrics/`).
  - No relatório final (Item 7), o SQL só aparecerá copiado como texto/snippet da query executada dentro do Metabase da Dadosfera, acompanhado do print do resultado e do link do ativo na plataforma.
  - Nenhum agente ou skill deve criar, sugerir ou modificar arquivos `.sql` locais.
- **Referência**: [`specs-internship.txt`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/agents_prompts_refs/case-internship-files/specs-internship.txt) (Item 7 e Regras de Avaliação)

### DEC-005: Governança na API Dadosfera (Autenticação, Deduplicação e Isolamento de Duplicatas)
- **Decisão**: 
  1. O header HTTP de autenticação contra a API Maestro (`https://maestro.dadosfera.ai`) deve enviar o token JWT diretamente em `Authorization: <token>`, sem o prefixo `Bearer` (que causa `401 Unauthorized`).
  2. O script de catalogação (`catalog_assets.py`) deve sempre verificar previamente a existência dos ativos para realizar `PUT /catalog/data-asset/{id}` e evitar a criação descontrolada de duplicatas via `POST /catalog`.
  3. Diante da restrição de privilégio de exclusão (`DELETE /catalog/data-asset/{id}` retorna `403 Forbidden` na conta de estágio), todas as duplicatas órfãs geradas em testes devem ser isoladas programaticamente via `PUT` renomeando-as para `[DUPLICATA - IGNORAR]` e marcando-as com as tags `duplicata`, `ignorar`, `lixeira` até o expurgo manual definitivo na interface web da Dadosfera.
- **Justificativa**: Descoberta empírica durante a auditoria de permissões do tenant `pedro-sales` (que possui `catalog:create` e `catalog:edit`, mas não `catalog:delete` nem `storage-explorer`).
- **Impacto**:
  - Garantia de integridade do catálogo oficial com 7 ativos únicos e com Dicionário de Dados rico sincronizado.
  - Prevenção de que duplicatas interfiram na catalogação, linhagem e consumo de dados.
- **Referência**: [`03_explorar_catalogacao.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/relatorios/03_explorar_catalogacao.md) (Seção 4) e [`assets_registry.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/agents_prompts_refs/dadosfera-api/output-mappers/assets_registry.md)

### DEC-006: Dual-Artifact Pipeline & Fronteira Plataforma vs. Domínio
- **Decisão**:
  1. O pipeline de qualidade gera dois artefatos na camada Silver: `[entidade]_qualify` (dados validados) e `[entidade]_anomalies` (dead-letter/auditoria de riscos).
  2. A Plataforma de Dados é responsável por detecção, classificação de severidade, captura da evidência bruta (`payload_raw`) e comunicação. A Aplicação/Domínio é responsável pela tomada de decisão e política de resolução (rejeitar, recalcular, alertar, corrigir).
  3. Adoção do blueprint canônico em 4 divisões para todas as entidades lógicas (`data/data-models/logical/entities/blueprint-entities-archive.md`).
- **Justificativa**: Preservação da integridade e auditabilidade dos dados brutos sem assumir mutações operacionais arbitrárias na camada de infraestrutura/plataforma.
- **Impacto**: Modelagem e linhagem padronizadas, com isolamento de desvios que representam risco operacional ou financeiro.
- **Referência**: [`blueprint-entities-archive.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/data-models/logical/entities/blueprint-entities-archive.md) e [`carrinhos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/data-models/logical/entities/carrinhos.md)

### DEC-007: Taxas Quebradas e Distribuições Naturais no Mock Engine
- **Decisão**: Configuração de taxas de dirty data e anomalias com percentuais fracionários e naturais (ex.: 4.87%, 5.73%, 2.15%) ao invés de números inteiros redondos (5.00%, 8.00%).
- **Justificativa**: Verossimilhança estatística de telemetria real de e-commerce e credibilidade durante a apresentação de dashboards (Metabase) e Data Apps (Streamlit) no pitch do Item 10.
- **Impacto**: Datasets sintéticos e pipelines de qualificação operando com distribuições fracionárias auditáveis em Parquet.
- **Referência**: [`dec-007-natural-broken-rates.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/docs/relatorios/decision-making/dec-007-natural-broken-rates.md)


---

## 📂 Materiais-Fonte (Source of Truth)

Prioridade de consulta:

| # | Fonte | Caminho | Conteúdo |
|---|---|---|---|
| 1 | Especificação do case | [`specs-internship.txt`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/agents_prompts_refs/case-internship-files/specs-internship.txt) | Requisitos oficiais dos 11 itens do case |
| 2 | Análise estratégica do cliente | [`raw (1).md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/agents_prompts_refs/case-internship-files/raw%20(1).md) | Pain points da arquitetura AWS do cliente, proposta Dadosfera |
| 3 | Prompt original do case | [`data_domain/1.txt`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/agents_prompts_refs/data_domain/1.txt) | Contexto de modelagem de dados |
| 4 | Referência da API Dadosfera | [`README.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/agents_prompts_refs/dadosfera-api/README.md) / [`endpoints.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/agents_prompts_refs/dadosfera-api/referencia/endpoints.md) | Documentação de endpoints Maestro, fluxos de autenticação e pipelines |
| 5 | Output Mappers & Catálogo de Ativos | [`assets_registry.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/agents_prompts_refs/dadosfera-api/output-mappers/assets_registry.md) / [`assets_registry.json`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/agents_prompts_refs/dadosfera-api/output-mappers/assets_registry.json) | Mapeamento de Data Asset IDs oficiais, URLs da UI Dadosfera e schemas |
| 6 | Decisão de métricas do pitch | [`pitch.txt`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/relatorios/decision-making/pitch/pitch.txt) | Decision record: % vs R$ |
| 7 | Plano inicial (pré-revisão) | [`init.md`](file:///c:/Users/pedro/OneDone/Desktop/wheels/relatorios/decision-making/pitch/init.md) | Versão inicial com métricas em R$ |
| 8 | Plano final (pós-revisão) | [`end.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/relatorios/decision-making/pitch/end.md) | Versão final com métricas em % |
| 9 | Regras de negócio | [`business-rules.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/models/logical/business-rules.md) | Estados do carrinho, RFM, canais de resgate, sequência de comunicação |
| 10 | Métricas do dataset | [`METRICS.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/mock/METRICS.md) | Taxas de conversão, ROI, volumes gerados |
| 11 | Framework analítico | [`data-strategy-analyst SKILL.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/.agents/skills/data-strategy-analyst/SKILL.md) | Template Dadosfera: descritiva, diagnóstica, preditiva, prescritiva |

---

## 🤝 Relação com Outros Agentes e Skills

| Agente/Skill | Responsabilidade | O que precisa deste contexto |
|---|---|---|
| `platform-registry-consultant` | Mapeamento de ativos, IDs e output-mappers | Consultar contexto do case para vincular e documentar Data Assets oficiais em `agents_prompts_refs/dadosfera-api/output-mappers/` |
| `project-context-specialist` | Estado técnico e evolução do repositório | Validar se o progresso técnico está alinhado com os objetivos do case |
| `cart-recovery-insights` | Especificação de insights de negócio | Saber quais análises a empresa espera, quais métricas priorizar |
| `data-pipeline-documentation` | Documentação, catálogo e linhagem de pipelines Medallion | Conhecer arquitetura de dados e requisitos dos itens 4 e 8 para documentar contratos e regras de DQ |
| `data-strategy-analyst` | Framework analítico Dadosfera | Entender o cenário do cliente e o problema de negócio |
| `datamaker` | Modelagem e geração de dados | Garantir que os dados mock refletem o domínio do case |
| `scout` | Mapeamento de estrutura do repo | Contexto sobre o que já existe e onde encontrar |

---

## 📋 Diretrizes para Consulta

1. **Não invente requisitos**: Se não está no material da empresa, não é requisito. Recomendações devem ser claramente marcadas como tal.
2. **Distinga explicitamente** entre: requisito explícito da empresa, inferência razoável do material, e recomendação adicional.
3. **Ao responder, use o formato**:
   - **Contexto**: O que o case está tentando resolver.
   - **Requisito da Empresa**: O que é explicitamente pedido/indicado no material.
   - **Estado Atual**: O que já foi definido ou implementado.
   - **Orientação**: O que deve ser feito considerando o contexto disponível.
   - **Pontos Abertos**: O que ainda precisa ser decidido ou validado.
4. **Quando houver divergência** entre uma decisão técnica do projeto e o material original da empresa, destaque a diferença ao invés de assumir qual está correta.
