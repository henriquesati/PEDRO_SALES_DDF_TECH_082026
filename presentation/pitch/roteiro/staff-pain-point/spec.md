# Especificação Visual & Técnica: Imagem `chart_staff_pain_point.png`

> **Diretório**: `presentation/pitch/roteiro/staff-pain-point/`  
> **Artefato Principal**: [`chart_staff_pain_point.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/staff-pain-point/chart_staff_pain_point.png)  
> **Script Gerador**: [`generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/staff-pain-point/generate_chart.py)  
> **Momento no Roteiro**: Item 4 do Pitch — Sobrecarga de Infraestrutura/DevOps, Inflação de Headcount e Sustentabilidade da Arquitetura (AWS DIY vs. Dadosfera)  
> **Padrão Gráfico**: Fundo Branco Puro (`#FFFFFF`), 16:9 Widescreen (3600x2025 px), 300 DPI, Tipografia Sem Serifa Moderna (`charts-maker` standard).  
> **Padrão de Nomenclatura**: Padronização estrita da métrica em **`Staff`** (Headcount / FTEs) em 100% dos eixos, vértices e anotações para máxima clareza e uniformidade visual.  
> **Estilo Visual**: Multi-line projection chart (Série Histórica 2020-2024 + Bifurcação em Cenários 2025-2030) com direct point labeling e legenda superior executiva.

---

## 📐 1. Estrutura e Composição da Imagem

```
+---------------------------------------------------------------------------------------------------+
|  Projeção de Headcount Técnico & Sobrecarga de Infraestrutura                                    |
|  Demanda de equipe com a expansão de infraestrutura, pipelines, DevOps, governança e casos de uso |
|                                                                                                   |
|  [■] Histórico (AWS DIY)  [■] AWS DIY (Alta Complexidade)  [■] AWS DIY (Moderada)  [■] Dadosfera  |
+---------------------------------------------------------------------------------------------------+
|  Headcount Técnico (Staff)                                                                        |
|   10 |                                                                  8 staff  8 staff (R$ 1.0M)|
|      |                                                         7 staff                            |
|    8 |                                                 6 staff                                    |
|      |                                         5 staff                  5 staff  5 staff (R$ 650k)|
|    6 |                                 4 staff                 4 staff  5 staff                   |
|      |                 3 staff         3 staff                                                    |
|    4 |         2 staff                                                                            |
|      | 2 staff         3 staff (Bifurcação 2024) ------------------------------------------------ |
|    2 |                                 2 staff         2 staff          2-3 staff (R$ 300k/ano)   |
|    0 |                                                                                            |
+---------------------------------------------------------------------------------------------------+
|  Ano: 2020     2021    2022    2023    2024    2025    2026    2027    2028    2029    2030       |
+---------------------------------------------------------------------------------------------------+
|  [RODAPÉ] Fonte: User Case Raw Analyses, Roteiro Estratégico & Benchmarks de Mercado              |
+---------------------------------------------------------------------------------------------------+
```

---

## 📊 2. Diagnóstico Completo dos Pain Points de Arquitetura, DevOps & Staff

A necessidade de expandir a equipe técnica na arquitetura não gerenciada (AWS DIY) decorre da **explosão multidimensional de serviços periféricos, manutenção de infraestrutura e sobrecarga de DevOps**.

### 2.1 As 6 Camadas de Sobrecarga Técnica na AWS DIY (O "Efeito Bola de Neve")

1. **Ingestão & Streaming Não Gerenciados**:
   - Configuração manual e redimensionamento de shards no **Kinesis Data Streams** conforme o throughput varia.
   - Latência de buffering do **Firehose** e ausência de *schema enforcement* nativo no **S3 Bucket (Data Lake)**, gerando corrupção silenciosa de dados.
2. **Engenharia de Qualidade & Quarentena Dispersa**:
   - Manutenção de dezenas de **Lambdas de validação** em Python/Great Expectations.
   - Gerenciamento de **filas Dead-Letter (AWS SQS DLQ)**, tabelas de quarentena no **DynamoDB** e alarmes fragmentados no **CloudWatch / SNS**.
3. **Processamento & Orquestração Pesada**:
   - **AWS Glue Jobs / PySpark**: Cold start de 1 a 4 minutos apenas para alocação de DPUs Spark antes de processar uma única linha. Cobrança de tempo mínimo por micro-job que encarece a fatura ao processar eventos de carrinho contínuos.
   - **AWS MWAA (Apache Airflow)**: Gestão de clusters dedicados, resolução de conflitos de dependências em DAGs, workers e schedulers.
   - **Amazon Redshift**: Manutenção de clusters, tuning de WLM, distribuição de chaves e vacuum de tabelas dimensionais (Star Schema).
4. **Explosão de DevOps, IaC & Infraestrutura Periférica**:
   - **Dockerfiles & AWS ECR**: Registry, segurança e versionamento contínuo de imagens de containers para tarefas analíticas.
   - **Terraform / CloudFormation**: Repositórios complexos de Infraestrutura como Código (IaC) que exigem manutenção a cada nova tabela ou conector.
   - **Esteiras de CI/CD (GitHub Actions / GitLab CI)**: Pipelines frágeis de deploy com múltiplos pontos de falha entre ambientes (dev/staging/prod).
   - **AWS Secrets Manager, VPCs & Gateways**: Gestão descentralizada de credenciais, certificados e rotas de rede seguras.
5. **Fragilidade de Cache & Risco de Downtime em Picos**:
   - **Redis Cluster (ElastiCache)**: Complexidade operacional entre modos standalone e cluster. Upgrades de plano e failovers manuais causam **5 a 15 minutos de indisponibilidade no checkout**, com perdas estimadas de **R$ 50 mil a R$ 100 mil por minuto** em eventos como Black Friday.
6. **Governança Fragmentada & Gargalo de SecOps/LGPD**:
   - Manutenção de centenas de linhas de **Políticas IAM em JSON** para liberação granular de acessos.
   - Configurações isoladas no **AWS Lake Formation**, **Glue Crawlers** e catálogos externos (**DataHub/OpenMetadata**).
   - **Gargalo Operacional**: Qualquer novo dado ou visão analítica para CRM, Marketing ou Produto exige abertura de chamados técnicos com **Lead Time de 3 a 6 semanas**, incentivando o *Shadow IT* (extração de planilhas CSV com dados sensíveis de clientes/PII sem controle ou auditoria LGPD).

---

### 2.2 Balanço Técnico & Perfil do Staff Necessário por Cenário

Abaixo está o balanço detalhado da **composição de perfis do staff** para cada arquitetura:

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               BALANÇO TÉCNICO DE COMPOSIÇÃO DE STAFF (HEADCOUNT TOTAL)                 │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 🔴 CENÁRIO 1: AWS DIY - ALTA COMPLEXIDADE (8 STAFF | ~R$ 1,0M/ano em folha)            │
│    • 2 Platform / DevOps / SRE Engineers (Terraform, CI/CD, Docker/ECR, VPCs, Shards)  │
│    • 3 Data Engineers Seniores (Glue/Spark, Airflow DAGs, Redshift Tuning, DLQs)      │
│    • 1 Cloud Security / SecOps Specialist (Políticas IAM JSON, Lake Formation, LGPD)   │
│    • 2 Analytics Engineers / Data Analysts (Modelagem, SQL e suporte ao negócio)       │
│    👉 80% do tempo gasto em sustentação de infraestrutura e encanamento técnico.      │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 🟡 CENÁRIO 2: AWS DIY - EXPANSÃO MODERADA (5 STAFF | ~R$ 650k/ano em folha)            │
│    • 1 Platform / DevOps Engineer (Containers, CI/CD e infraestrutura básica)          │
│    • 2 Data Engineers (Pipelines de ingestão, Glue Jobs e Redshift)                    │
│    • 2 Analytics Engineers / Data Analysts (Relatórios e dashboards)                   │
│    👉 60-70% do tempo gasto em infraestrutura e chamados técnicos.                     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 🟢 CENÁRIO 3: PLATAFORMA DADOSFERA (2 a 3 STAFF | ~R$ 300k/ano em folha)               │
│    • 0 Platform / DevOps Engineers (Infraestrutura 100% gerenciada e elástica)         │
│    • 0 Data Engineers de Infraestrutura (Pipelines declarativos na Stepsfera)          │
│    • 2 a 3 Analytics Engineers / Data Analysts (Foco total em SQL, Métricas, Negócio)  │
│    👉 80%+ do tempo dedicado à geração direta de receita e inteligência de negócio.   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 2.3 Resumo Comparativo Executivo

| Dimensão | Cenário AWS DIY (Arquitetura Solta) | Solução Plataforma Dadosfera |
|---|---|---|
| **Composição de Staff** | • Platform Engineers / DevOps<br>• Data Engineers de Infraestrutura<br>• Especialistas em IAM/SecOps<br>• Analistas | • **Analytics Engineers & Analistas de Negócio** (foco em SQL, modelagem Kimball e métricas) |
| **Alocação de Esforço** | **80% em "Encanamento" Técnico** (sustentação de clusters, CI/CD, shards, IAM e correções de pipeline) | **80% em Inteligência de Negócio** (modelagem, análises descritivas/prescritivas, conversão e ROI) |
| **Tamanho do Staff** | Salta de 3 para **até 8 staff** | Equipe enxuta e estável de **2 a 3 staff** |
| **Custo Anual de Folha** | **R$ 650 mil a mais de R$ 1,0 Milhão/ano** | **R$ 300 mil/ano** (Economia anual de R$ 400k a R$ 750k+) |
| **Time-to-Value de Novas Demandas** | **3 a 6 semanas** por conector/visão | **Minutos a poucos dias** com módulos nativos e catálogo integrado |

---

### 2.4 Séries de Dados Padronizadas (Unidade Única: Staff)

#### A. Série Histórica (2020 a 2024) — Linha Azul Royal (`#2563EB`)
Evolução real da equipe técnica de dados do e-commerce:
- **2020**: `2 staff` (Início da ingestão básica Kinesis/S3)
- **2021**: `2 staff` (Adição de Lambdas e pipelines Glue)
- **2022**: `3 staff` (Inclusão de Redis Cluster, Airflow e Redshift)
- **2023**: `3 staff` (Estabilização da infraestrutura)
- **2024**: `3 staff` (**Baseline Atual / PoC**: 1 Platform Engineer + 2 Data Engineers consumidos por sustentação)

#### B. Projeções de Headcount (2025 a 2030)

1. **AWS DIY — Alta Complexidade (Múltiplas Fontes, Pipelines, Shards & Casos de Uso) — Linha Vermelha (`#DC2626`)**
   - Expansão contínua com novas fontes (CRM, ERP, logs, checkout), modelos de IA, réguas multicanal e novos data apps.
   - A complexidade de sustentar containers Docker, esteiras CI/CD, shards Kinesis, políticas IAM e tuning de Redshift força a contratação contínua de engenheiros de infraestrutura.
   - **2025**: `4 staff` | **2026**: `5 staff` | **2027**: `6 staff` | **2028**: `7 staff` | **2029**: `8 staff` | **2030**: `8 staff` (**R$ 1,0M/ano | 80% em Infraestrutura**).

2. **AWS DIY — Expansão Moderada — Linha Âmbar / Dourado (`#D97706`)**
   - Expansão contida com menos integrações simultâneas, mas sustentação contínua de servidores e alarmes.
   - **2025**: `3 staff` | **2026**: `4 staff` | **2027**: `4 staff` | **2028**: `5 staff` | **2029**: `5 staff` | **2030**: `5 staff` (**R$ 650k/ano**).

3. **Plataforma Dadosfera — Escala Elástica & Equipe Estável — Linha Verde Esmeralda (`#059669`)**
   - O Sistema Operacional de Dados All-in-One abstrai a infraestrutura: ingestão plug & play, Lakehouse Snowflake automático, catálogo unificado, Data Quality nativo e consumo integrado (Metabase e Streamlit).
   - Elimina 100% da necessidade de engenheiros dedicados exclusivamente a "encanamento" técnico.
   - **2025**: `2 staff` | **2026**: `2 staff` | **2027**: `2 staff` | **2028**: `2 staff` | **2029**: `2-3 staff` | **2030**: `2 a 3 staff` (**R$ 300k/ano | 80% em Inteligência de Negócio**).

---

## 🎙️ 3. Roteiro de Fala Sugerido no Pitch (Momento 4 do Roteiro)

> *"Quando analisamos a sustentabilidade da arquitetura na nuvem, o verdadeiro gargalo da AWS DIY não é o volume de dados — é a sobrecarga operacional e de headcount.*  
> 
> *Para manter uma arquitetura solta funcionando, a empresa não precisa apenas de ferramentas analíticas. Ela é forçada a manter um ecossistema periférico gigante: gerenciar shards de Kinesis, esteiras de CI/CD, repositórios de Terraform, imagens Docker no ECR, cold starts no Glue, clusters de Airflow, políticas IAM em JSON e a fragilidade do Redis em eventos de pico como a Black Friday.*  
> 
> *O resultado prático é que 80% do tempo dos profissionais mais caros da empresa é queimado em encanamento de infraestrutura. Cada nova fonte de dados, modelo preditivo ou relatório exige mais Platform Engineers e DevOps apenas para manter a cola entre os serviços de pé, fazendo o staff saltar de 3 para até 8 pessoas e custando mais de R$ 1 milhão por ano.*  
> 
> *Com a Dadosfera, essa camada inteira de infraestrutura é abstraída. A empresa sustenta qualquer expansão com um staff enxuto de 2 a 3 analistas focados em SQL, inteligência de negócio e conversão, economizando centenas de milhares de reais por ano e reduzindo o lead time de semanas para minutos."*

---

## 📉 4. View Complementar Minimalista: Comparativo de Custo (Crossover / Curvas Cruzadas)

> **Artefato**: [`chart_custo_infra_vs_dadosfera_crossover.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/staff-pain-point/chart_custo_infra_vs_dadosfera_crossover.png)  
> **Script**: [`generate_cost_comparison_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/staff-pain-point/generate_cost_comparison_chart.py)  
> **Finalidade no Slide**: Visualização executiva simplista e limpa com eixos conceituais e rotulagem direta das linhas, ideal para comparar TCO e sustentação no PowerPoint.

```
+---------------------------------------------------------------------------------------------------+
|  ▲ Custo Total de Operação & Sustentação (TCO)                                                    |
|  │ (Provisionamento, Headcount, Apps, Dados)                                                      |
|  │                                                    [🔴 Custo Infraestrutura Própria (AWS DIY)]  |
|  │                                                                      /  ▲ (Escalada Exponencial|
|  │                                           ● Ponto de Inflexão       /     Custos & Complexidade|
|  │                                             \ (Break-even)         /                           |
|  │          [🟢 Custo com Dadosfera] ------------\-------------------/-------> ▲ (Crescimento     |
|  │          (Plataforma SaaS Unificada)            \                /             Suave e Estável)|
|  └──────────────────────────────────────────────────\──────────────/───────────────────────────► |
|                  Tempo / Volume de Dados & Expansão de Casos de Uso ->                            |
+---------------------------------------------------------------------------------------------------+
```

### 🏷️ Identificação dos Elementos no Gráfico:
* **Eixo Y (Vertical)**: **`Custo Total de Operação & Sustentação (TCO)`** *(Provisionamento, Headcount, Apps, Dados)*.
* **Eixo X (Horizontal)**: **`Tempo / Volume de Dados & Expansão de Casos de Uso ->`**.
* **🔴 Linha Vermelha Coral (`#DC2626`)**: **`Custo Infraestrutura Própria (AWS DIY)`** *(Crescimento Exponencial de Custos | Provisionamento, Headcount, Apps, Dados)*.
* **🟢 Linha Verde Esmeralda (`#059669`)**: **`Custo com Dadosfera`** *(Crescimento Suave e Previsível | Plataforma Unificada SaaS)*.
* **Ponto de Cruzamento**: **`Ponto de Inflexão (Break-even)`**, demarcando a virada de ROI onde a infra própria se torna exponencialmente mais cara.
