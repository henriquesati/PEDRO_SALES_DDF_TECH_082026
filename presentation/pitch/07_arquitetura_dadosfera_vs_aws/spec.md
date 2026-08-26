# Especificação Visual & Aspecto Técnico: Arquitetura Dadosfera vs Stack Legada AWS

> **Módulo do Pitch**: `presentation/pitch/07_arquitetura_dadosfera_vs_aws/`  
> **Item do Case**: Item 10 — Arquitetura & Prova de Conceito  
> **Master Source of Truth**: [`presentation/pitch/pitch_spec.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/pitch_spec.md#2-comentar-arquitetura-do-cliente-e-iniciar-pitch)  
> **Artefato Visual**: [`chart_07_arquitetura_dadosfera_vs_aws.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/07_arquitetura_dadosfera_vs_aws/chart_07_arquitetura_dadosfera_vs_aws.png)  
> **Script Gerador**: [`generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/07_arquitetura_dadosfera_vs_aws/generate_chart.py)

---

## 📌 Contexto & Aspecto Técnico (Item 10 & Prova de Conceito)
- **Cenário do Cliente**: Grande e-commerce operando sobre serviços AWS fragmentados.
  - *Stack Atual*:
    - **Lambda & Kinesis Stream**: Configuração manual de shards baseada em throughput, elevando custos e complexidade de dimensionamento.
    - **Kinesis Firehose**: Latência de buffering que atrasa o acionamento de telemetria em tempo real.
    - **S3 Bucket**: Atua como Data Lake sem *schema enforcement* rígido, vulnerável a quebras de pipelines por alterações de esquema upstream.
    - **Redis Cluster (ElastiCache)**: Complexidade técnica entre modos standalone vs cluster, escalonamento horizontal vs vertical. Upgrades de plano causam 5 a 15 min de indisponibilidade e reconfigurações manuais em N serviços codependentes.
  - *Riscos e Dores Centrais*:
    - **Vulnerabilidade em Picos (Black Friday)**: Erros de reconfiguração de cache geram lentidão no checkout e perdas estimadas em **R$ 50k a 100k por minuto**.
    - **Crescimento Linear de Headcount**: Necessidade de 1 Platform Engineer + 1 a 2 Data Engineers apenas para criar e sustentar "colas" de integração a cada novo data app.
    - **Lead Time Excessivo**: De 3 a 6 semanas para implementar novos painéis analíticos ou pipelines.
    - **Governança Dispersa**: Complexidade de IAM em nuvem dificultando compliance com a LGPD e compartilhamento seguro entre setores.
- **Proposta de Valor Dadosfera**:
  - Plataforma All-in-One: Ingestão Plug & Play (Maestro API) $\rightarrow$ Catálogo Automático $\rightarrow$ Qualify com Great Expectations $\rightarrow$ DW Snowflake Otimizado $\rightarrow$ Analytics (Metabase) $\rightarrow$ Consumo Interativo (Streamlit & GenAI).

## 📊 Métricas de Eficiência & Comparativo
- **Lead Time para Novos Data Apps/Análises**: De **3–6 semanas** na AWS para **< 3 dias** na Dadosfera (**Redução de ~86%**).
- **Risco em Picos**: Eliminação do risco de R$ 50k–100k/min por desacoplamento elástico sobre o Snowflake.
- **Esforço de Manutenção de Infraestrutura**: Zero provisionamento de servidores/shards (SaaS Totalmente Gerenciado).
- **Governança & Linhagem**: 100% dos ativos mapeados com Data Asset IDs oficiais vs documentação manual e dispersa.

## 🎯 Objetivo no Pitch
Posicionar a Dadosfera como o Sistema Operacional de Dados definitivo que desacopla a equipe de dados da manutenção de infraestrutura, permitindo foco exclusivo em inteligência de negócio e recuperação de faturamento.

## 📍 Mapeamento Plataforma Dadosfera
- **Fases do Ciclo de Vida**: Integrar $\rightarrow$ Explorar $\rightarrow$ Processar $\rightarrow$ Analisar $\rightarrow$ Consumir $\rightarrow$ GenAI.
- **Ativos Oficiais**: Sincronização via API Maestro (`assets_registry.md`).
