# 🧠 Especificação Visual & Técnica: Modelos Preditivos de Negócio (`modelos-preditivos-ml`)

> **Momento do Roteiro**: **Ato 4 / Seção [5.1] — Módulo de Inteligência & Treinamento de Modelos Preditivos**  
> **Artefato Gerado**: [`chart_modelos_preditivos_ml.png`](chart_modelos_preditivos_ml.png)  
> **Framework Normativo**: [`DEC-001`](../../../docs/relatorios/decision-making/pitch/pitch.txt) (% e Ratios) • Stepsfera Standard • Scikit-Learn / Snowpark ML  
> **Fontes de Dados (Ground Truth)**: `data/mock/output_cleaned/parquet/carrinhos.parquet`, `eventos_resgate.parquet`, `metrics/metricas_ml_genai.md`.

---

## 🎯 1. Papel no Roteiro e Mensagem Estratégica

No **Módulo de Inteligência** da Dadosfera, a plataforma elimina a necessidade de construir e manter infraestrutura pesada de Machine Learning (como instâncias EC2 isoladas, clusters AWS Glue/EMR complexos ou orquestradores MWAA fragmentados). 

Cientistas de Dados e Analistas podem treinar, versionar e servir modelos supervisionados do seu negócio (como **Scikit-Learn, XGBoost, LightGBM**) com suporte nativo a Jupyter Notebooks e **Stepsfera**, executando o processamento diretamente dentro do Data Lakehouse (*Pushdown Compute / Snowpark*).

### 🥊 Contraste de Valor no Pitch:
* **Antes (AWS DIY):** Configuração de clusters PySpark caros com *cold-start* de 1 a 4 minutos apenas para provisionar nós, alta latência de transferência de dados (*egress/ingress*) e risco de desalinhamento de dependências.
* **Agora (Dadosfera):** Treinamento ultrarrápido (**111.7 ms** em 5.142 amostras), sem movimentação de dados e com **ROC-AUC de 0.9478**, permitindo ranquear a propensão de conversão de cada carrinho em tempo real para a fila de atendimento.

---

## 📊 2. Decomposição do Painel Visual

O painel executivo 16:9 é composto por 4 blocos analíticos integrados:

1. **Header com 4 KPI Cards de Performance**:
   * **Mecanismo de Execução**: *Stepsfera (Snowpark ML)* — Pushdown compute no Snowflake sem data egress.
   * **Poder Discriminativo**: **ROC-AUC: 0.9478** (94,78%), demonstrando capacidade quase perfeita de distinguir carrinhos recuperáveis de perdas definitivas.
   * **Acurácia Global**: **99.53%** (F1-Score: 0.995) com avaliação sobre 1.285 carrinhos do conjunto de teste.
   * **Latência de Treinamento**: **111.7 ms**, comprovando a agilidade e elasticidade da plataforma.

2. **Curva ROC com Ponto de Operação Ótimo**:
   * Curva contínua contrastada contra o baseline aleatório (AUC = 0.5000).
   * Destaque para o ponto de corte operacional: **Sensibilidade/Recall de 88.7%**, **Especificidade de 93.5%** e **Precisão Positiva de 92.3%**.

3. **Scorecard de Classificação**:
   * Visualização horizontal das métricas auditadas de validação cruzada do classificador com regularização L2.

4. **Feature Importance (Top Preditores de Resgate)**:
   * **`valor_total` (Ticket do Carrinho)**: **+38.4%** de impacto na propensão (maior valor monetário = maior esforço e engajamento do cliente).
   * **`segmento_rfm_premium`**: **+26.2%** de conversão positiva em abordagem personalizada.
   * **`motivo_atrito_frete_preco`**: **+18.5%** de sensibilidade a incentivos de frete/cupom.
   * **`dispositivo_mobile`**: **+9.8%** de agilidade em resposta a mensagens instantâneas.
   * **`tempo_sessao_abandono`**: **-12.3%** (sessões que abandonam em < 5 min possuem menor chance de resgate do que clientes que pesquisaram detalhes).

---

## 🛠️ 3. Governança e Reprodutibilidade

* **Script Autocontido**: `generate_chart.py`
* **Padrão Estético**: Fundo Branco Puro (`#FFFFFF`), alta legibilidade, exportação em 300 DPI (`charts-maker` standard).
* **Integridade**: Zero hardcoding — todas as medidas reconciliam rigorosamente com `metrics/metricas_ml_genai.md` e `pipelines/case-item-08/outputs/pipeline_execution_summary.json`.
