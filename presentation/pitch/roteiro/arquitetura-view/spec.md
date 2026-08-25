# Especificação Visual & Técnica: View de Arquitetura (`arquitetura-view`)

> **Momento do Pitch**: Ato 1 — Diagnóstico da Arquitetura Legada (AWS DIY) vs. Solução Unificada Dadosfera  
> **Padrão Visual**: Fundo Branco Puro (`#FFFFFF`), Proporção 16:9 Widescreen (300 DPI), Paleta Semântica Oficial do Treemap (`chart_02_motivos_abandono.png`), Estilo Geométrico Reto (90°).  
> **Fonte Estratégica**: [`presentation/pitch/roteiro.txt`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro.txt) e [`docs/specifications/data-platform-specification.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/docs/specifications/data-platform-specification.md).

---

## 🗺️ 1. Governança e Estrutura de Diretórios (`assets/` vs. `assets/icons/`)

```
presentation/pitch/roteiro/arquitetura-view/
├── assets/                               # 📊 Gráficos Gerados em Alta Resolução (PNG 300 DPI)
│   ├── grafico-legado-l2r-vazio.png      # ⭐ [TEMPLATE OFICIAL APROVADO] Blocos limpos para colar os ícones no PPT
│   ├── grafico-legado-l2r-populated.png  # 🗺️ [GUIA DE MONTAGEM] Mapa visual com todos os ícones e nomes mapeados
│   ├── grafico-legado-l2r.png            # Diagrama Legado AWS completo
│   ├── grafico-dadosfera-l2r-vazio.png   # Template Dadosfera vazio
│   ├── grafico-dadosfera-l2r.png         # Diagrama Dadosfera unificado completo
│   └── icons/                            # 🖼️ 26 Ícones Transparentes (PNG)
│       ├── kinesis.png, lambda.png, redshift.png, redis.png, s3.png, snowflake.png, metabase.png, etc.
├── powerpoint/                           # 📑 Apresentação PPTX
│   ├── arquitetura_dadosfera.pptx        # Apresentação PowerPoint
│   └── generate_architecture_deck.py     # Script Python compilador
├── generate_l2r_charts.py                # 🐍 Script declarativo de renderização
└── spec.md                               # 📄 Esta Especificação Técnica
```

---

## 🎨 2. Diretrizes Visuais Aprovadas (Negócio & Ciclo de Vida dos Dados)

O fluxo foi estruturado sob os **5 Pilares Canônicos de Negócio**:

```
[ 1. INGESTÃO ] ➔ [ 2. VALIDAÇÃO ] ➔ [ 3. MODELAGEM ] ➔ [ 4. GOVERNANÇA ] ➔ [ 5. INTELIGÊNCIA ]
```

1. **Blocos Quadrados Estritamente Retos (90°)**:
   - **Borda branca grossa (`edgecolor = "#FFFFFF"`, `linewidth = 3.5pt`)** idêntica ao acabamento do Treemap.
   - **Cores sólidas oficiais do Treemap (sem tons de cinza)**:
     - 🟦 **Pilar 1 (Ingestão)**: `#1E3A8A` (*Navy Blue*)
     - 🔵 **Pilar 2 (Validação)**: `#2563EB` (*Royal Blue*)
     - 🟣 **Pilar 3 (Modelagem)**: `#7C3AED` (*Vibrant Purple*)
     - 🟠 **Pilar 4 (Governança)**: `#D97706` (*Amber Orange*)
     - 🟢 **Pilar 5 (Inteligência)**: `#059669` (*Emerald Green*)
2. **Minimalismo Interno dos Quadrados**:
   - Contém apenas o número (**`1`**, **`2`**, **`3`**, **`4`**, **`5`**) em tipografia discreta (`11.5pt`, bold white) no topo central.
   - Espaço amplo e liso para posicionar e animar os ícones no PowerPoint.
3. **Seta Contínua Espessa e Translúcida**:
   - Fundo em **Âmbar (`#D97706`)** com **opacidade suave (`alpha = 0.72`)** e borda marcante (`#B45309`, `linewidth = 2.0pt`).
   - Tópicos limpos sem prefixo numérico:  
     `INGESTÃO  ➔  VALIDAÇÃO  ➔  MODELAGEM  ➔  GOVERNANÇA  ➔  INTELIGÊNCIA`
4. **String Externa**:
   - `FLUXO CONTÍNUO DO CICLO DE VIDA ANALÍTICO` em badge centralizado abaixo da seta.

---

## 🗺️ 3. Guia de Montagem no PowerPoint (Qual Ícone Colar em Qual Bloco)

Consulte o gráfico [`grafico-legado-l2r-populated.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/arquitetura-view/assets/grafico-legado-l2r-populated.png) como gabarito visual:

| Bloco | Pilar de Negócio | Cor | Ícones para Colar (de `assets/icons/`) | Papel no Pitch / Dores Abordadas |
| :---: | :--- | :---: | :--- | :--- |
| **1** | **INGESTÃO** | `#1E3A8A` | • `kinesis.png` (Kinesis Stream)<br>• `firehose.png` (Kinesis Firehose)<br>• `s3.png` (S3 Raw Data Lake) | Ingestão contínua de eventos brutos de navegação e carrinhos. Dores: Sharding manual e latência de buffering. |
| **2** | **VALIDAÇÃO** | `#2563EB` | • `lambda.png` (AWS Lambda)<br>• `sqs.png` (Amazon SQS DLQ)<br>• `dynamodb.png` (DynamoDB Quarentena)<br>• `datadog.png` (CloudWatch/SNS Alertas) | Data Quality e Quarentena ativa (94.2% conformidade). Dores: Falta de schema enforcement rígido no S3 e scripts soltos. |
| **3** | **MODELAGEM** | `#7C3AED` | • `glue.png` (AWS Glue PySpark)<br>• `redshift.png` (Redshift DW)<br>• `airflow.png` (MWAA Airflow)<br>• `redis.png` (ElastiCache Redis)<br>• `docker.png` (Docker / ECR)<br>• `terraform.png` (Terraform / IaC)<br>• `github-actions.png` (GitHub CI/CD)<br>• `secrets-manager.png` (Secrets Manager) | Star Schema Kimball (6 Dim / 2 Fatos) e a complexidade de sustentação. Dores: Cold start de DPUs Spark, Redis downtime na Black Friday (R$ 50k-100k/min) e sobrecarga de DevOps. |
| **4** | **GOVERNANÇA** | `#D97706` | • `lake-formation.png` (Lake Formation)<br>• `datahub.png` (DataHub / Catálogo) | Catálogo de dados, linhagem ponta a ponta e conformidade regulatória. Dores: Políticas IAM em JSON complexas e governança dispersa. |
| **5** | **INTELIGÊNCIA** | `#059669` | • `powerbi.png` (PowerBI / Tableau)<br>• `streamlit.png` (Streamlit Data App)<br>• `genai.png` (Copilot GenAI)<br>• `eventbridge.png` (Alertas de Resgate) | Consumo analítico e ações de negócio (10.1% de resgate / 45x ROI). Dores: Semanas para criar réguas e observabilidade desconectada do negócio. |

---

## 🎬 4. Roteiro Passo a Passo para o Slide de Animação

1. **Inserir Background**: Insira [`grafico-legado-l2r-vazio.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/arquitetura-view/assets/grafico-legado-l2r-vazio.png) como imagem principal do Slide 1.
2. **Posicionar Ícones**: Arraste os PNGs de [`assets/icons/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/arquitetura-view/assets/icons/) para dentro de cada bloco conforme a tabela acima (ou usando o gabarito [`grafico-legado-l2r-populated.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/arquitetura-view/assets/grafico-legado-l2r-populated.png)).
3. **Configurar Animações**: No PowerPoint, aplique a animação **Fade (Esmaecer) ou Appear (Aparecer)** em sequência para cada grupo de ícones conforme você narra as dores de cada etapa no pitch.
4. **Slide de Fechamento**: No Slide 2, apresente [`grafico-dadosfera-l2r.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/arquitetura-view/assets/grafico-dadosfera-l2r.png) mostrando todos os 5 pilares consolidados em uma única plataforma SaaS All-in-One.
