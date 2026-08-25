# 🏛️ Especificação da View de Arquitetura: Diagrama do Ciclo de Vida dos Dados (`arc-diagram-view`)

> **Caminho da View**: `presentation/pitch/roteiro/arquitetura-view/arc-diagram-view/`  
> **Momento do Roteiro**: **Ato 1 — Diagnóstico da Arquitetura Legada (AWS DIY) vs. Solução Unificada Dadosfera**  
> **Arquivos Geradores**: `generate_chart.py` (Wrapper de Importação) $\longrightarrow$ [`../generate_l2r_charts.py`](../generate_l2r_charts.py)  
> **Ícones Utilizados**: [`../assets/icons/`](../assets/icons/) (26 ícones oficiais em alta resolução)

---

## 📌 1. O que Esta View Representa (Texto Corrido Explicativo)

Esta visualização é o **pilar central de transição do Ato 1 do roteiro de vendas**. Ela traduz graficamente o contraste entre o modelo fragmentado de computação em nuvem própria (*AWS DIY — Do It Yourself*) e a abordagem moderna de plataforma unificada (*SaaS All-in-One da Dadosfera*).

O diagrama organiza toda a jornada do dado em **5 Pilares Canônicos de Negócio**:

$$\mathbf{1.\; Ingest\tilde{a}o} \;\longrightarrow\; \mathbf{2.\; Valida\ccedil\tilde{a}o} \;\longrightarrow\; \mathbf{3.\; Modelagem} \;\longrightarrow\; \mathbf{4.\; Governan\ccedil a} \;\longrightarrow\; \mathbf{5.\; Intelig\hat{e}ncia}$$

### 🔍 Narrativa Comparativa Apresentada no Roteiro:
* **No Cenário Legado (AWS DIY - Slide 1)**: Para fazer o ciclo de vida dos dados funcionar, a empresa é obrigada a acoplar e manter mais de 20 serviços periféricos isolados (Kinesis, Lambda de validação, filas DLQ no SQS, Glue Jobs com Spark, Redshift, MWAA Airflow, Dockerfiles no ECR, scripts Terraform, Secrets Manager, Lake Formation e políticas IAM complexas). Isso cria um alto custo oculto de infraestrutura, lentidão de 3 a 6 semanas para novas entregas e dependência excessiva de engenheiros de plataforma dedicados apenas a manter "colas" de integração.
* **Na Solução Dadosfera**: A plataforma Dadosfera unifica essas 5 etapas em uma única interface gerenciada. A ingestão é plug-and-play, a validação com Data Quality é nativa, a modelagem dimensional roda no Snowflake Lakehouse de forma elástica, a governança/catálogo com LGPD é automática e a inteligência (Machine Learning e GenAI) roda integrada sem que o cliente precise gerenciar servidores ou clusters.

---

## 🎨 2. Estrutura dos Artefatos Visuais

| Artefato Gerado | Papel na Apresentação |
| :--- | :--- |
| **`grafico-legado-l2r-vazio.png`** | **Template de Animação**: Os 5 blocos retos coloridos colados à seta contínua de fluxo analítico, sem ícones internos, permitindo a inserção progressiva de cada componente AWS. |
| **`grafico-legado-l2r.png`** | **Diagrama Legado Completo**: Versão com todos os ícones de serviços AWS mapeados e legendados em seus respectivos pilares. |
| **`grafico-dadosfera-l2r.png`** | **Diagrama Dadosfera Unificado**: Demonstração visual do container da Dadosfera absorvendo os 5 pilares com simplicidade e foco no negócio. |
| **`grafico-dadosfera-l2r-vazio.png`** | Template limpo da Dadosfera para suporte a mockups e customizações. |

---

## ⚙️ 3. Mecanismo de Execução & Exceção de Assets

Seguindo a regra de governança onde **esta é a única view com subpasta `assets/`** devido à biblioteca de logos e ícones:
* [`assets/icons/`](assets/icons/): Contém os 26 ícones transparentes em PNG de cada serviço de nuvem e ferramentas da Dadosfera.
* [`generate_chart.py`](generate_chart.py): Script declarativo autônomo que renderiza todos os diagramas em 300 DPI (`matplotlib` + `Pillow`).
* [`download_high_res_icons.py`](download_high_res_icons.py): Script utilitário para atualização automática dos ícones oficiais.
