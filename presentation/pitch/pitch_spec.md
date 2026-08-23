# Especificação do Pitch — Plataforma Dadosfera

> **Projeto**: Implementação da Plataforma Dadosfera no E-commerce com PoC em Recuperação de Carrinho Abandonado  
> **Autor**: Pedro Sales  
> **Fonte Estratégica**: `agents_prompts_refs/case-internship-files/user-case-raw-analyses.md`

---

## [1] Apresentar Plataforma Dadosfera

### 1.1 O que é a Dadosfera
A Dadosfera é o Sistema Operacional de Dados unificado (SaaS All-in-One) projetado para cobrir ponta a ponta o ciclo de vida analítico de uma empresa: Ingestão, Catálogo, Processamento, Análise, Consumo e Inteligência Artificial.

### 1.2 A Plataforma como Meio
- **Meio vs Fim**: A Dadosfera é o **meio** estruturante (agregação, governança, discovery e disponibilização ágil) para todas as áreas de negócio da empresa, e não uma ferramenta restrita a um único caso de uso.
- **Escalabilidade sem Headcount Linear**: Elimina a necessidade de expandir a equipe de infraestrutura de dados proporcionalmente ao crescimento do volume ou de novas ferramentas.

### 1.3 Capacidades e Módulos Integrados
- **Ingestão Plug & Play**: Conectores nativos e API Maestro que eliminam o desenvolvimento de scripts e pipelines manuais de integração para cada nova fonte.
- **Transformação Centralizada**: Ambiente integrado no Snowflake Data Lakehouse, substituindo scripts dispersos por pipelines estruturados de Data Quality e modelagem dimensional Star Schema (Kimball).
- **Catálogo e Governança Automáticos**: Linhagem de dados nativa, dicionários e mapeamento de Data Asset IDs oficiais para descoberta autônoma de dados entre setores.
- **Segurança e IAM Simplificado**: Controle de acesso granular e conformidade LGPD nativa, permitindo democratizar o acesso e compartilhar views analíticas com marketing e CRM sem colocar a privacidade em risco.
- **Consumo e Analytics Integrado**: Dashboards interativos via Metabase nativo e Data Apps em Streamlit, eliminando o custo e a dispersão de licenças de BI externas.
- **Inteligência com GenAI**: Capacidades nativas de exploração de dados em linguagem natural e automação semântica com modelos LLM.

---

## [2] Comentar Arquitetura do Cliente e Iniciar Pitch

### 2.1 Diagnóstico da Arquitetura Legada (AWS)
A infraestrutura atual do cliente é fragmentada em múltiplos serviços não gerenciados que impõem alto custo de manutenção e risco operacional:

- **Lambda & Kinesis Data Streams**: Exigem configuração e sharding manual baseado em throughput, gerando custos imprevisíveis e complexidade de dimensionamento.
- **Kinesis Firehose**: Introduz latência de buffering que impede ações em tempo real.
- **S3 Bucket**: Atua como Data Lake sem imposição rígida de schema (schema enforcement), deixando os pipelines suscetíveis a quebras frequentes por dados malformados.
- **Redis Cluster (ElastiCache)**: Complexidade técnica de operação entre modos standalone e cluster. Upgrades de plano causam de 5 a 15 minutos de indisponibilidade e qualquer ajuste exige reconfigurações manuais em N serviços codependentes.

### 2.2 Principais Riscos e Gargalos Identificados
1. **Fragilidade em Datas de Pico (Black Friday)**: Erros ou atrasos na reconfiguração manual do cache geram lentidão no checkout e perdas estimadas em **R$ 50 mil a R$ 100 mil por minuto** de indisponibilidade.
2. **Crescimento Linear de Headcount**: Manter a arquitetura atual exige pelo menos 1 Platform Engineer e 1 a 2 Data Engineers dedicados apenas para sustentar "colas" de integração manual a cada nova ferramenta conectada.
3. **Lead Time Excessivo**: Leva de **3 a 6 semanas** para colocar no ar um novo painel analítico ou régua de dados.
4. **Governança Dispersa**: A complexidade do IAM em nuvem torna a auditoria de compliance (LGPD) difícil e trava a democratização dos dados com as áreas de negócio.

### 2.3 Proposta de Valor e Transição para o Pitch
A Dadosfera substitui toda essa complexidade operacional:
- **Redução de Lead Time**: De 6 semanas para **menos de 3 dias (-86%)** para novas análises e aplicações.
- **Zero Risco de Sharding em Picos**: Desacoplamento e elasticidade nativa da nuvem gerenciada.
- **Foco no Negócio**: Desloca o esforço da equipe técnica da manutenção de servidores para a geração direta de receita.

---

## [3] Case Carrinho (Prova de Conceito / PoC)

### 3.1 O Problema e a Escolha da PoC
Para comprovar o valor prático e o ROI imediato da Dadosfera, selecionou-se como Prova de Conceito o maior gargalo de receita do e-commerce: o **abandono de cerca de 70% dos carrinhos de compra**.

### 3.2 Regras de Negócio e Evidências Analíticas

#### Regra 1: Série Temporal e Ciclo de Vida do Carrinho
- Classificação de abandono após 30 minutos de inatividade.
- Taxa média de abandono identificada em ~69.7%.
- Taxa de recuperação com réguas Dadosfera: **10.1% dos carrinhos abandonados** (lift de +50% sobre a conversão basal sem campanha).
- Artefato: `01_abandono_vs_recuperacao_timeline/chart_01_serie_temporal_abandono_resgate.png`

#### Regra 2: Performance de Catálogo e Atrito por Categoria
- Categorias de alto ticket (Eletrônicos) concentram alto valor represado por indecisão e dúvidas técnicas.
- Categorias como Moda sofrem alto abandono por atrito no valor do frete.
- A plataforma permite direcionar réguas específicas para o contexto de cada produto.
- Artefato: `02_performance_categorias_produtos/chart_02_performance_categorias.png`

#### Regra 3: Topologia de Canais e Eficiência Financeira (ROI)
- **Email** (R$ 0,05 por envio): Canal de tração em escala e maior retorno absoluto.
- **WhatsApp** (R$ 0,30 por envio): Maior conversão unitária (18% clique-para-venda), reservado estrategicamente para clientes e carrinhos de alto valor.
- **ROI Médio Consolidado**: **45x multiplicador** sobre o custo total de disparos (custo de campanha < 1% do valor recuperado).
- Artefato: `03_roi_canais_e_comunicacao/chart_03_roi_eficiencia_canais.png`

#### Regra 4: Causa-Raiz vs Segmentação RFM (Preservação de Margem)
- Cruzamento do valor do carrinho com o histórico RFM para proteger a rentabilidade da empresa:
  - **Clientes Premium**: Abandonam por indecisão ou suporte -> recebem atendimento humanizado (WhatsApp) **sem cupom de desconto**, preservando a margem de lucro.
  - **Clientes Novos**: Abandonam por frete -> recebem incentivo/cupom de primeira compra.
- Taxa de conversão do segmento Premium é **3 vezes maior** que a do segmento Dormant (18% vs 6%).
- Artefato: `04_matriz_motivos_segmentos_rfm/chart_04_matriz_motivos_rfm_heatmap.png`

#### Regra 5: Matriz Prescritiva de Viabilidade
- Matriz de dispersão em tempo real combinando valor do carrinho e probabilidade de conversão.
- Fila de acionamento que prioriza os 20% de carrinhos que respondem por mais de 65% do faturamento recuperável dentro da janela de 28 horas de expiração.
- Artefato: `05_matriz_viabilidade_recuperacao/chart_05_dispersao_viabilidade_recuperacao.png`

### 3.3 Governança Ativa e Data Quality (Item 4)
- Arquitetura **Dual-Artifact Silver**:
  - Suíte de 18 regras em Great Expectations alcançando **94.2% de conformidade**.
  - 5.8% de dados corrompidos (fretes negativos, divergências contábeis e e-mails inválidos) são interceptados em quarentena automatizada com captura do payload bruto.
- Blindagem das réguas de marketing contra disparos com dados inconsistentes.
- Artefato: `06_data_quality_e_quarentena/chart_06_scorecard_data_quality.png`

### 3.4 Data App e Inteligência com GenAI (Itens 9 e Bônus)
- **Data App Interativo em Streamlit (Item 9)**: Simulador em tempo real de sensibilidade de ROI, permitindo ao gestor calibrar volume, taxas e custos de canais.
- **Motor de GenAI com LLMs (Case Bônus)**: Geração automatizada de mensagens persuasivas contextualizadas pela causa do abandono (suporte técnico vs prova social), elevando o CTR em mais de 18%.
- Artefato: `08_data_app_simulador_prescritivo_genai/chart_08_simulador_roi_data_app.png`

### 3.5 Conclusão e Próximos Passos
- **Modelo Agnóstico em % (DEC-001)**: Todas as métricas baseiam-se em taxas, ratios e multiplicadores, sendo aplicáveis a qualquer ticket médio ou vertical de marketplace.
- **Resultados Consolidados**:
  - Lead time: -86% (de semanas para dias).
  - Recuperação: 10.1% dos abandonos.
  - ROI de Disparos: 45x.
- **Call to Action**: Proposta de Prova de Conceito (PoC) guiada de 2 semanas em ambiente de homologação/produção do cliente.
