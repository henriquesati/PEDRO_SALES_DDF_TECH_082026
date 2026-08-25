# Especificação do Pitch — Plataforma Dadosfera

> **Projeto**: Implementação da Plataforma Dadosfera no E-commerce com PoC em Recuperação de Carrinho Abandonado  
> **Autor**: Pedro Sales  
> **Fonte Estratégica**: `agents_prompts_refs/case-internship-files/user-case-raw-analyses.md`

---

## [1] Apresentar Plataforma Dadosfera

### [1.1] O que é a Dadosfera
A Dadosfera é o Sistema Operacional de Dados unificado (SaaS All-in-One) projetado para cobrir ponta a ponta o ciclo de vida analítico de uma empresa: Ingestão, Catálogo, Processamento, Análise, Consumo e Inteligência Artificial.

### [1.2] A Plataforma como Meio
[1] **Meio vs Fim**: A Dadosfera é o **meio** estruturante (agregação, governança, discovery e disponibilização ágil) para todas as áreas de negócio da empresa, e não uma ferramenta restrita a um único caso de uso.  
[2] **Escalabilidade sem Headcount Linear**: Elimina a necessidade de expandir a equipe de infraestrutura de dados proporcionalmente ao crescimento do volume ou de novas ferramentas.

### [1.3] Capacidades e Módulos Integrados
[1] **Ingestão Plug & Play**: Conectores nativos e API Maestro que eliminam o desenvolvimento de scripts e pipelines manuais de integração para cada nova fonte.  
[2] **Transformação Centralizada**: Ambiente integrado no Snowflake Data Lakehouse, substituindo scripts dispersos por pipelines estruturados de Data Quality e modelagem dimensional Star Schema (Kimball).  
[3] **Catálogo e Governança Automáticos**: Linhagem de dados nativa, dicionários e mapeamento de Data Asset IDs oficiais para descoberta autônoma de dados entre setores.  
[4] **Segurança e IAM Simplificado**: Controle de acesso granular e conformidade LGPD nativa, permitindo democratizar o acesso e compartilhar views analíticas com marketing e CRM sem colocar a privacidade em risco.  
[5] **Consumo e Analytics Integrado**: Dashboards interativos via Metabase nativo e Data Apps em Streamlit, eliminando o custo e a dispersão de licenças de BI externas.  
[6] **Inteligência com GenAI**: Capacidades nativas de exploração de dados em linguagem natural e automação semântica com modelos LLM.

---

## [2] Comentar Arquitetura do Cliente e Iniciar Pitch

### [2.1] Diagnóstico da Arquitetura Legada (AWS)
A infraestrutura atual do cliente é fragmentada em múltiplos serviços não gerenciados que impõem alto custo de manutenção e risco operacional:

[1] **Lambda & Kinesis Data Streams**: Exigem configuração e sharding manual baseado em throughput, gerando custos imprevisíveis e complexidade de dimensionamento.  
[2] **Kinesis Firehose**: Introduz latência de buffering que impede ações em tempo real.  
[3] **S3 Bucket**: Atua como Data Lake sem imposição rígida de schema (schema enforcement), deixando os pipelines suscetíveis a quebras frequentes por dados malformados.  
[4] **Redis Cluster (ElastiCache)**: Complexidade técnica de operação entre modos standalone e cluster. Upgrades de plano causam de 5 a 15 minutos de indisponibilidade e qualquer ajuste exige reconfigurações manuais em N serviços codependentes.

### [2.2] Principais Riscos e Gargalos Identificados
[1] **Fragilidade em Datas de Pico (Black Friday)**: Erros ou atrasos na reconfiguração manual do cache geram lentidão no checkout e perdas estimadas em **R$ 50 mil a R$ 100 mil por minuto** de indisponibilidade.  
[2] **Crescimento Linear de Headcount**: Manter a arquitetura atual exige pelo menos 1 Platform Engineer e 1 a 2 Data Engineers dedicados apenas para sustentar "colas" de integração manual a cada nova ferramenta conectada.  
[3] **Lead Time Excessivo**: Leva de **3 a 6 semanas** para colocar no ar um novo painel analítico ou régua de dados.  
[4] **Governança Dispersa**: A complexidade do IAM em nuvem torna a auditoria de compliance (LGPD) difícil e trava a democratização dos dados com as áreas de negócio.

### [2.3] Proposta de Valor e Transição para o Pitch
A Dadosfera substitui toda essa complexidade operacional:

[1] **Redução de Lead Time**: De 6 semanas para **menos de 3 dias (-86%)** para novas análises e aplicações.  
[2] **Zero Risco de Sharding em Picos**: Desacoplamento e elasticidade nativa da nuvem gerenciada.  
[3] **Foco no Negócio**: Desloca o esforço da equipe técnica da manutenção de servidores para a geração direta de receita.  
[4] **Artefatos e Views do Roteiro**: 
    - Template Oficial de Animação (Blocos Vazios): [`presentation/pitch/roteiro/arquitetura-view/assets/grafico-legado-l2r-vazio.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/arquitetura-view/assets/grafico-legado-l2r-vazio.png)
    - Diagrama L2R Legado (Referência): [`presentation/pitch/roteiro/arquitetura-view/assets/grafico-legado-l2r.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/arquitetura-view/assets/grafico-legado-l2r.png)
    - Diagrama L2R Dadosfera: [`presentation/pitch/roteiro/arquitetura-view/assets/grafico-dadosfera-l2r.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/arquitetura-view/assets/grafico-dadosfera-l2r.png)
    - Apresentação PPTX: [`presentation/pitch/roteiro/arquitetura-view/powerpoint/arquitetura_dadosfera.pptx`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/arquitetura-view/powerpoint/arquitetura_dadosfera.pptx)
    - Gráfico Comparativo: [`presentation/pitch/07_arquitetura_dadosfera_vs_aws/chart_07_arquitetura_dadosfera_vs_aws.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/07_arquitetura_dadosfera_vs_aws/chart_07_arquitetura_dadosfera_vs_aws.png)

---

## [3] Case Carrinho (Prova de Conceito / PoC)

### [3.1] O Problema e a Escolha da PoC
Para comprovar o valor prático e o ROI imediato da Dadosfera, selecionou-se como Prova de Conceito o maior gargalo de receita do e-commerce: o **abandono de cerca de 70% dos carrinhos de compra**.

### [3.2] Regras de Negócio e Evidências Analíticas

#### [Regra 1] Série Temporal e Ciclo de Vida do Carrinho
[1] Classificação de abandono após 30 minutos de inatividade.  
[2] Taxa média de abandono identificada em ~69.7%.  
[3] Taxa de recuperação com réguas Dadosfera: **10.1% dos carrinhos abandonados** (lift de +50% sobre a conversão basal sem campanha).  
[4] Artefato: `presentation/insights/01_descriptive/01_bi_recuperacao_carrinhos/chart_bi_recuperacao_carrinhos.png`

#### [Regra 2] Performance de Catálogo e Atrito por Categoria
[1] Categorias de alto ticket (Eletrônicos) concentram alto valor represado por indecisão e dúvidas técnicas.  
[2] Categorias como Moda sofrem alto abandono por atrito no valor do frete.  
[3] A plataforma permite direcionar réguas específicas para o contexto de cada produto.  
[4] Artefato: `presentation/insights/03_prescriptive/03_produtos_mais_abandonados/chart_03_produtos_mais_abandonados.png`

#### [Regra 3] Topologia de Canais e Eficiência Financeira (ROI)
[1] **Email** (R$ 0,05 por envio): Canal de tração em escala e maior retorno absoluto.  
[2] **WhatsApp** (R$ 0,30 por envio): Maior conversão unitária (18% clique-para-venda), reservado estrategicamente para clientes e carrinhos de alto valor.  
[3] **ROI Médio Consolidado**: **45x multiplicador** sobre o custo total de disparos (custo de campanha < 1% do valor recuperado).  
[4] Artefato: `presentation/insights/01_descriptive/03_custo_recuperacao_roi/chart_03_custo_recuperacao_roi.png`

#### [Regra 4] Causa-Raiz vs Segmentação RFM (Preservação de Margem)
[1] Cruzamento do valor do carrinho com o histórico RFM para proteger a rentabilidade da empresa.  
[2] **Clientes Premium**: Abandonam por indecisão ou suporte -> recebem atendimento humanizado (WhatsApp) **sem cupom de desconto**, preservando a margem de lucro.  
[3] **Clientes Novos**: Abandonam por frete -> recebem incentivo/cupom de primeira compra.  
[4] Taxa de conversão do segmento Premium é **3 vezes maior** que a do segmento Dormant (18% vs 6%).  
[5] Artefato: `presentation/insights/03_prescriptive/01_estrategia_resgate_segmento/chart_04_estrategia_resgate_segmento.png`

#### [Regra 5] Matriz Prescritiva de Viabilidade
[1] Matriz de dispersão em tempo real combinando valor do carrinho e probabilidade de conversão.  
[2] Fila de acionamento que prioriza os 20% de carrinhos que respondem por mais de 65% do faturamento recuperável dentro da janela de 28 horas de expiração.  
[3] Artefato: `presentation/insights/02_risk/03_viabilidade_recuperacao_carrinho/chart_03_viabilidade_recuperacao_carrinho.png`

#### [Regra 6] Otimização de Timing & Curva de Decaimento (Decay Curve)
[1] **Concentração Temporal de Conversão**: Nos dados simulados e observados, quanto maior o atraso do primeiro contato, menor foi a conversão observada, com a janela de **+1h concentrando 86,4% das conversões**.  
[2] **Rigor Metodológico no Pitch**: Em vez de afirmar dogmaticamente que "o horário ótimo é +1h", a defesa analítica correta é:  
> *"Nos dados observados, +1h apresentou a maior taxa de conversão e concentrou a maior parte das conversões, indicando +1h como a janela inicial candidata prioritária à otimização contínua via experimentação (testes A/B)."* [^nota-timing-review]  
[3] Artefato: `presentation/insights/03_prescriptive/02_otimizacao_timing_envio/chart_05_otimizacao_timing_envio.png`

[^nota-timing-review]: **[FLAG: REVIEW PENDENTE - METODOLOGIA DE TIMING]** A janela de +1h é a candidata inicial de maior performance na amostra histórica observada (86,4% do volume recuperado). Recomenda-se manter esta ressalva metodológica no pitch para evidenciar maturidade estatística perante o cliente, destacando que o pipeline da Dadosfera permite rodar testes A/B contínuos para aferir empiricamente o ponto ótimo para cada cluster de produtos.

### [3.3] Modelagem Dimensional Kimball (Item 6)
[1] **Arquitetura Star Schema (1-Hop)**: Camada Gold no Snowflake com 6 dimensões conformadas e 2 fatos granulares (`fato_abandono` e `fato_resgate`).  
[2] **Simplicidade & Performance**: Modelo mais intuitivo de compreender e rápido de implementar no Metabase e Snowflake (1-Hop JOINs vs cascata de 3NF/Data Vault).  
[3] **2 Visões Analíticas Gold**: `v_abandonment_summary` (Executiva) e `v_recovery_roi_by_segment` (Tática).  
[4] Artefato: `presentation/pitch/views/caseitem06/chart_caseitem06_kimball_model.png`

### [3.4] Governança Ativa e Data Quality (Item 4)
[1] Arquitetura **Dual-Artifact Silver**:  
    - [1.1] Suíte de 18 regras em Great Expectations alcançando **94.2% de conformidade**.  
    - [1.2] 5.8% de dados corrompidos (fretes negativos, divergências contábeis e e-mails inválidos) são interceptados em quarentena automatizada com captura do payload bruto.  
[2] Blindagem das réguas de marketing contra disparos com dados inconsistentes.  
[3] Artefato: `presentation/pitch/06_data_quality_e_quarentena/chart_06_scorecard_data_quality.png`

### [3.5] Data App e Inteligência com GenAI (Itens 9 e Bônus)
[1] **Data App Interativo em Streamlit (Item 9)**: Simulador em tempo real de sensibilidade de ROI, permitindo ao gestor calibrar volume, taxas e custos de canais.  
[2] **Motor de GenAI com LLMs (Case Bônus)**: Geração automatizada de mensagens persuasivas contextualizadas pela causa do abandono (suporte técnico vs prova social), elevando o CTR em mais de 18%.  
[3] Artefato: `presentation/pitch/08_data_app_simulador_prescritivo_genai/chart_08_simulador_roi_data_app.png`

### [3.6] Conclusão e Próximos Passos
[1] **Modelo Agnóstico em % (DEC-001)**: Todas as métricas baseiam-se em taxas, ratios e multiplicadores, sendo aplicáveis a qualquer ticket médio ou vertical de marketplace.  
[2] **Resultados Consolidados**:  
    - [2.1] Lead time: -86% (de semanas para dias).  
    - [2.2] Recuperação: 10.1% dos abandonos.  
    - [2.3] ROI de Disparos: 45x.  
[3] **Call to Action**: Proposta de Prova de Conceito (PoC) guiada de 2 semanas em ambiente de homologação/produção do cliente.

---

## [4] Diretriz Metodológica: Foco em Proporções (%) & Entidade Exemplo de Negócio

### [4.1] Princípio de Universalidade (Foco em % e Taxas Relativas - DEC-001)
> [!IMPORTANT]
> **O foco primordial de todas as especificações e gráficos do projeto é a representação em PORCENTAGENS (%) e TAXAS RELATIVAS.**
> A dinâmica do funil de conversão, curvas de decaimento temporal, distribuição de causas de abandono e matrizes de risco são estruturalmente agnósticas de tíquete. Essa arquitetura permite que qualquer cliente ou prospect conecte sua própria operação e **adeque seu próprio Ticket Médio e volumetria**, recalculando instantaneamente o ganho financeiro sem distorcer as dinâmicas analíticas.

### [4.2] Entidade Exemplo de Negócio (Baseline Mock para Simulações Monetárias)
Quando for estritamente necessário exemplificar cálculos financeiros absolutos (R$) em simulações, pitch executivo ou relatórios de ROI, adota-se a seguinte **Entidade Exemplo de Referência (Varejo Online / Marketplace Padrão)**:

| Dimensão / Parâmetro | Valor de Referência (Baseline Exemplo) | Notas & Aplicação |
|---|:---:|---|
| **Volume Semestral de Carrinhos** | `7.500 carrinhos` (~1.250/mês) | Base total observada no semestre de PoC |
| **Taxa Global de Abandono** | `~70,0% a 70,9%` (~69,7% real) | Benchmark Baymard / E-commerce Brasil |
| **Taxa de Conversão Direta no Checkout** | `23,1%` (1.731 un) | Conversão orgânica direta sem recuperação |
| **Taxa de Recuperação de Carrinho** | `10,1% a 10,6% s/ abandono` | ~6,6% sobre o total de carrinhos criados (498 un) |
| **Reengajados em Andamento** | `2,0% a 2,5%` (153 un) | Carrinhos acionados em janela de conversão |
| **Ticket Médio Global de Carrinho** | `R$ 375,00` | Baseline médio ponderado da cesta |
| **Ticket Médio: Segmento PREMIUM** | `R$ 800,00` | Cestas de alta fidelidade / múltiplos itens |
| **Ticket Médio: Segmento REGULAR** | `R$ 360,00` | Cestas de compras recorrentes |
| **Ticket Médio: Segmento NOVO** | `R$ 250,00` | Primeira compra / itens promocionais |
| **Ticket Médio: Segmento DORMANT** | `R$ 200,00` | Tentativa de reativação |
| **Ticket Médio: Eletrônicos** | `R$ 850,00` | Alto ticket / atrito por indecisão |
| **Ticket Médio: Casa & Decoração** | `R$ 420,00` | Médio ticket / atrito por frete |
| **Ticket Médio: Moda & Vestuário** | `R$ 180,00` | Giro rápido / sensibilidade a frete e tamanho |
| **Ticket Médio: Beleza & Saúde** | `R$ 110,00` | Cesta complementar / reposição |
| **Ticket Médio: Livros & Papelaria** | `R$ 75,00` | Baixo ticket / frete representativo |
| **Custo Unitário de Canal: WhatsApp** | `R$ 0,30 / envio` | Canal VIP / alta conversão unitária |
| **Custo Unitário de Canal: SMS** | `R$ 0,15 / envio` | Canal transacional |
| **Custo Unitário de Canal: Email** | `R$ 0,05 / envio` | Canal de escala / alta margem líquida |
| **Custo Unitário de Canal: Push App** | `R$ 0,02 / envio` | Canal proprietário / custo marginal zero |
| **Margem Bruta Operacional Média** | `35%` | Base para cálculo de preservação de margem |

---

## [5] Governança de Dados, Entidades Canônicas & Fonte Única da Verdade

### [5.1] Base de Dados Física Unificada (Ground Truth)
Todos os geradores de gráficos do pitch (`presentation/pitch/`) e da galeria de insights (`presentation/insights/`) consom **rigorosamente a mesma base de dados persistida** no repositório, garantindo reproducibilidade e ausência de dados fabricados:
- **Diretório Canônico Primário**: `data/mock/output_cleaned/parquet/`
- **Diretório de Fallback**: `data/mock/output/parquet/`

### [5.2] Entidades Canônicas Utilizadas em Todos os Gráficos
| Entidade Parquet | Arquivo Físico | Granularidade / Papel | Utilização nos Gráficos do Pitch & Insights |
|---|---|---|---|
| **Carrinhos** | `carrinhos.parquet` | 1 linha por carrinho criado | Funil temporal, atrito de abandono, motivos, matriz RFM e viabilidade |
| **Pedidos** | `pedidos.parquet` | 1 linha por pedido faturado | Cruzamento de conversão direta vs recuperação Dadosfera (`origem_recuperacao`) |
| **Clientes** | `clientes.parquet` | 1 linha por cliente cadastrado | Segmentação RFM (`premium`, `regular`, `novo`, `dormant`) e LTV |
| **Produtos** | `produtos.parquet` | 1 linha por SKU de catálogo | Categoria de produto, preço unitário e atrito de catálogo |
| **Itens do Carrinho** | `itens_carrinho.parquet` | 1 linha por item adicionado | Composição da cesta e volumetria por categoria |
| **Eventos de Resgate** | `eventos_resgate.parquet` | 1 linha por disparo de campanha | Telemetria multicanal, custos de disparo, timing de abertura e conversão |
| **Eventos do Carrinho** | `eventos_carrinho.parquet` | 1 linha por interação na sessão | Rastreamento comportamental e tempo de sessão |

### [5.3] Declaração de Autoridade Canônica: `pitch_spec.md` como Master Source
> [!IMPORTANT]
> **Este documento (`presentation/pitch/pitch_spec.md`) é a Fonte Canônica da Verdade (Master Source of Truth) para todo o ecossistema de visualizações do projeto.**
> 
> 1. Toda especificação contida em `presentation/insights/` e seus subdiretórios (`01_descriptive/`, `02_risk/`, `03_prescriptive/`) deve obrigatoriamente referenciar e estar em estrita conformidade com os parâmetros, entidades e métricas aqui declarados.
> 2. Qualquer simulação monetária (R$), análise de CAC de resgate, ROI multiplicador ou categorização RFM em qualquer apresentação ou relatório deve reconciliar perfeitamente com a **Entidade Exemplo de Negócio (Seção 4.2)** e os datasets Parquet unificados (Seção 5.1).
> 3. É expressamente proibida a criação de bases de dados paralelas, entidades divergentes ou valores arbitrários de ticket em qualquer artefato visual do projeto.


