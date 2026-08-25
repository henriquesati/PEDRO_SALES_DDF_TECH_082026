# Especificação Visual & Técnica: Módulo de Arquitetura (`arquitetura-view`)

> **Momento do Pitch**: Ato 1 — Diagnóstico da Arquitetura Legada (AWS DIY) vs. Solução Unificada Dadosfera  
> **Padrão Visual**: Fundo Branco Puro (`#FFFFFF`), Proporção 16:9 Widescreen (300 DPI), Paleta Semântica Oficial dos 5 Pilares do Ciclo de Vida dos Dados.  
> **Fonte Estratégica**: [`presentation/pitch/roteiro.txt`](../roteiro.txt) e [`presentation/pitch/roteiro/spec.md`](../spec.md).

---

## 🗺️ 1. Governança e Submódulo [`arc-diagram-view/`](arc-diagram-view/)

Seguindo a regra de governança onde **apenas a view de diagramas de arquitetura possui subdiretório `assets/`** devido aos 26 logos e ícones de serviços:

```
presentation/pitch/roteiro/arquitetura-view/
├── arc-diagram-view/                     # 🏛️ Submódulo Canônico da View de Arquitetura L2R
│   ├── assets/
│   │   └── icons/                        # 🖼️ 26 Ícones Transparentes (PNG) da AWS e Dadosfera
│   ├── generate_chart.py                 # 🐍 Script declarativo de renderização em alta resolução
│   ├── download_high_res_icons.py        # 📥 Script utilitário para download dos assets oficiais
│   ├── spec.md                           # 📄 Especificação técnica em texto corrido
│   ├── grafico-legado-l2r.png            # 📊 Diagrama Legado AWS DIY completo
│   ├── grafico-dadosfera-l2r.png         # 📊 Diagrama Dadosfera unificado completo
│   ├── grafico-legado-l2r-vazio.png      # 📊 Template limpo dos 5 blocos
│   └── grafico-legado-l2r-populated.png  # 📊 Guia de referência mapeado
└── spec.md                               # 📄 Esta Especificação Geral do Módulo
```

---

## 🎨 2. Diretrizes Visuais Aprovadas (Os 5 Pilares de Negócio)

O fluxo do ciclo de vida analítico é estruturado sob os 5 pilares:

$$\mathbf{1.\; INGEST\tilde{A}O} \;\longrightarrow\; \mathbf{2.\; VALIDA\Ccedil\tilde{A}O} \;\longrightarrow\; \mathbf{3.\; MODELAGEM} \;\longrightarrow\; \mathbf{4.\; GOVERNAN\Ccedil A} \;\longrightarrow\; \mathbf{5.\; INTELIG\hat{E}NCIA}$$

* 🟦 **Pilar 1 (Ingestão)**: `#1E3A8A` (*Navy Blue*)
* 🔵 **Pilar 2 (Validação)**: `#2563EB` (*Royal Blue*)
* 🟣 **Pilar 3 (Modelagem)**: `#7C3AED` (*Vibrant Purple*)
* 🟠 **Pilar 4 (Governança)**: `#D97706` (*Amber Orange*)
* 🟢 **Pilar 5 (Inteligência)**: `#059669` (*Emerald Green*)

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
