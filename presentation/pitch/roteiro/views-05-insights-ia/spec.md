# 🧠 Módulo Master de Views: Inteligência, GenAI & Data Apps (`views-05-insights-ia`)

> **Momento do Roteiro**: **Ato 4 / Seção [5] — Módulo de Inteligência, GenAI e Data Apps**  
> **Diretório Envelope**: `presentation/pitch/roteiro/views-05-insights-ia/`  
> **Artefato Master**: [`chart_insights_ia_master.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-05-insights-ia/chart_insights_ia_master.png)  
> **Arquitetura Master**: [`presentation/pitch/roteiro/README.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/README.md)  
> **Fontes Estratégicas**: [`presentation/pitch/roteiro.txt`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro.txt), [`presentation/pitch/pitch_spec.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/pitch_spec.md), [`pipelines/case-item-08/specs.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-08/specs.md), [`pipelines/case-item-05/specs.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-05/specs.md), [`pipelines/case-item-09/specs.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-09/specs.md) e [`metrics/metricas_ml_genai.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/metrics/metricas_ml_genai.md).

---

## 🎯 1. Visão Geral da Seção [5] do Roteiro

A seção `[5]` do roteiro narrativo de pitch aborda o **Módulo de Inteligência da Plataforma Dadosfera**, demonstrando como empresas médias e grandes conseguem criar, treinar, governar e consumir modelos avançados de **Machine Learning**, **Inteligência Artificial Generativa (GenAI/LLMs)** e **Data Apps interativos** sem o atrito operacional e os custos proibitivos de manter uma infraestrutura em nuvem fragmentada (AWS DIY).

### 🥊 O Contraste Arquitetural Fundamental:
* **Antes (AWS DIY / Serviços Desconectados):** Para rodar pipelines de ML e LLMs, a equipe de TI precisa subir instâncias EC2 manuais, configurar clusters pesados de AWS Glue ou EMR (PySpark) que sofrem com *cold-start* de 1 a 4 minutos apenas para alocar DPUs antes de processar qualquer dado, orquestrar dependências frágeis via MWAA / Airflow, gerenciar Dockerfiles e registros ECR, e construir integrações ad-hoc com APIs de LLMs sem governança de schema ou garantias contratuais. Esse modelo gera um custo marginal crescente de headcount e semanas de Lead Time para qualquer novo modelo entrar em produção.
* **Agora (Plataforma Dadosfera):** Um ambiente único e integrado com suporte nativo a **Jupyter Notebooks**, orquestração declarativa via **Stepsfera** e execução elástica *in-database* (**Snowpark / Snowflake Cortex**). A plataforma fornece o ecossistema pronto para treinar modelos do negócio (**Scikit-Learn, XGBoost, LightGBM**), validar saídas de GenAI com **Pydantic / JSON Schema (100% de conformidade)** e disponibilizar aplicações operacionais em **Streamlit** com 1 clique para as áreas de Marketing e CRM, entregando resultados de baixíssima latência e alta disponibilidade.

---

## 📊 2. Resumo dos Submódulos e Métricas Canônicas

| Submódulo da View | Momento no Roteiro | Pergunta de Negócio & Foco Técnico | Artefatos & Métricas de Impacto |
| :--- | :--- | :--- | :--- |
| **`views-05-insights-ia/` (Master)** | **Ato 4 / Seção [5] — Visão Geral de Inteligência** | *Como a Dadosfera unifica IA, GenAI e Consumo sem overhead de infraestrutura?* | • `chart_insights_ia_master.png`<br/>• Comparativo Antes x Agora: Eliminação de cold-start de Glue e orquestração integrada via Stepsfera.<br/>• Scorecard: ROC-AUC 0.9478, Pydantic 100%, +18% CTR, 45x ROI. |
| [`modelos-preditivos-ml/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-05-insights-ia/modelos-preditivos-ml/) | **Ato 4 / Seção [5.1] — Machine Learning no Negócio** | *Como predizer e priorizar os carrinhos com maior chance de recuperação?* | • `chart_modelos_preditivos_ml.png`<br/>• **ROC-AUC: 0.9478** e **Acurácia: 99.53%** (F1-Score 0.995).<br/>• Treinamento in-database em **111.7 ms** sobre 5.142 amostras.<br/>• Top Drivers: Ticket (+38.4%), RFM VIP (+26.2%), Frete (+18.5%). |
| [`feature-importance-ml/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-05-insights-ia/feature-importance-ml/) | **Ato 4 / Seção [5.1.1] — Pesos e Interpretabilidade (XAI)** | *Quais fatores matemáticos explicam a propensão de resgate calculada pelo modelo?* | • `chart_feature_importance_ml.png`<br/>• Decomposição dimensional de pesos (Ticket +38.4%, RFM VIP +26.2%, Frete +18.5%).<br/>• Regras prescritivas automatizadas de CRM para WhatsApp e E-mail. |
| [`genai-extracao-copies/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-05-insights-ia/genai-extracao-copies/) | **Ato 4 / Seção [5.2] — GenAI & Processamento Desestruturado** | *Como converter textos brutos em features e gerar mensagens altamente persuasivas?* | • `chart_genai_extracao_copies.png`<br/>• **100.0% de aderência Pydantic** (Zero alucinação).<br/>• **+18.0% de lift no CTR** (de 8.2% para 26.2% de cliques).<br/>• Custo ultrabaixo: < R$ 0,0008 por inferência (latência 4.0 ms). |
| [`similaridade-produtos/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-05-insights-ia/similaridade-produtos/) | **Ato 4 / Seção [5.3] — Busca Semântica & Catálogo Inteligente** | *O que fazer quando o cliente abandona por preço ou estoque indisponível?* | • `chart_similaridade_produtos.png`<br/>• Projeção vetorial 2D (t-SNE/PCA) de 300 SKUs em 7 categorias.<br/>• Motor de Similaridade de Cosseno no Lakehouse (< 2.5 ms).<br/>• **+12.4% de recuperação incremental** recomendando produtos substitutos. |
| [`data-app-simulador-roi/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-05-insights-ia/data-app-simulador-roi/) | **Ato 4 / Seção [5.4] — Consumo, Data Apps & Simulação de ROI** | *Como permitir que gestores simulem e aprovem réguas em tempo real?* | • `chart_data_app_simulador_roi.png`<br/>• Deploy nativo em Streamlit no módulo Consumir com 1 clique.<br/>• **45.0x ROI Consolidado** sobre custos de envio.<br/>• Waterfall Contábil: **+R$ 167.900,00 de Ganho Líquido Incremental**. |

---

## 🎨 3. Padrões Gráficos Compartilhados (`charts-maker` Standard)

* **Fundo Branco Puro (`#FFFFFF`)**: 100% dos painéis, gráficos e eixos.
* **Proporção & Resolução**: **16:9 Widescreen** exportado em **300 DPI** com `bbox_inches="tight"`.
* **Tipografia**: Família sem serifa moderna (`Segoe UI`, `DejaVu Sans`, `Arial`).
* **Integridade Absoluta (Ground Truth)**: Todos os dados plotados carregam diretamente dos arquivos Parquet em `data/mock/output_cleaned/parquet/` e relatórios auditados de execução em `pipelines/`.
* **Ausência de Pasta `assets/`**: Estrutura plana, limpa e modular.
