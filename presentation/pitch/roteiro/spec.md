# 📄 Especificação Master de Governança das Views do Roteiro

> **Objetivo**: Definir o padrão normativo de governança, convenções de estrutura e padrões gráficos para todas as visões analíticas que apoiam a apresentação executiva do case no [`roteiro.txt`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro.txt) e no [`pitch_spec.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/pitch_spec.md).  
> **Arquitetura Completa de Diretórios**: Consulte [`presentation/pitch/roteiro/README.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/README.md).

---

## 🏛️ 1. Padrão Arquitetural de Diretórios de Views

A organização de diretórios visuais do roteiro segue a convenção estruturada:

$$\text{presentation/pitch/roteiro/} \longrightarrow \mathbf{arquitetura\text{-}view/[diretorio\text{-}nomeado\text{-}view]}$$

### 📌 Regras Obrigatórias de Estrutura de Pastas:
1. **Estrutura Padrão (Enxuta / Tríade Canônica)**:
   A estrutura padrão para todas as pastas de views é obrigatoriamente:
   ```text
   pasta/
   ├── generate_chart.py    # 🐍 Script declarativo de renderização a partir do Parquet
   ├── spec.md              # 📄 Especificação técnica em texto corrido
   └── chart_*.png          # 📊 Imagem gerada em alta resolução (300 DPI)
   ```
2. **Exceção Única para Subpasta `assets/`**:
   * **Somente a pasta `arc-diagram-view/`** possui um subdiretório `assets/` (dedicado exclusivamente a armazenar os 26 logos e ícones de serviços da AWS e da Dadosfera) e scripts utilitários adicionais (`download_high_res_icons.py`).
   * **Todas as demais pastas de views devem ser normais e sem pasta `assets/`**, mantendo seus scripts e saídas gráficos diretamente na raiz do diretório.
   * As pastas só podem ter arquivos e scripts adicionais quando estritamente **necessário e aprovado pelo usuário**.
3. **Envelopamento Lógico e Agrupamento de Diretórios**:
   * A arquitetura de diretórios é flexível e **suporta o envelopamento de subdiretórios dentro de outros** para organização lógica de atos ou seções temáticas complexas do roteiro.
   * Envelopes lógicos homologados:
     * `view-03-dado-qualidades/` $\longrightarrow$ envelopa `view-lake-architecture/`, `view-governanca/` e `view-model-kimball/`.
     * `arquitetura-view/` $\longrightarrow$ envelopa `arc-diagram-view/`.
     * `views-04-insights/` $\longrightarrow$ envelopa `descritivos/` (3 views) e `prescritivos/` (4 views).
     * `views-05-insights-ia/` $\longrightarrow$ envelopa `modelos-preditivos-ml/`, `genai-extracao-copies/`, `similaridade-produtos/` e `data-app-simulador-roi/`.
4. **Documento `spec.md` em Texto Corrido**:
   Cada diretório DEVE conter uma `spec.md` explicando em **texto corrido** o que a view representa no roteiro, qual momento da narrativa ela apoia e qual o diagnóstico/insight de negócio transmitido.

---

## 🗺️ 2. Mapeamento dos Módulos de Views do Roteiro

| Diretório da View | Momento / Ato do Roteiro | Estrutura de Arquivos | Artefatos Gerados |
| :--- | :--- | :---: | :--- |
| [`arquitetura-view/arc-diagram-view/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/arquitetura-view/arc-diagram-view/) | **Ato 1: Diagnóstico da Arquitetura Legada (AWS DIY) vs. Solução Dadosfera** | `assets/icons/` + Scripts | • `grafico-legado-l2r.png`<br/>• `grafico-dadosfera-l2r.png`<br/>• `grafico-legado-l2r-vazio.png`<br/>• `grafico-dadosfera-l2r-vazio.png` |
| [`problema-elasticidade/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/problema-elasticidade/) | **Momento 3: Risco de Elasticidade e Downtime em Picos (Black Friday)** | Padrão Enxuto | • `chart_problema_elasticidade.png` (Painel Executivo 16:9) |
| [`staff-pain-point/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/staff-pain-point/) | **Momento 4: Headcount Linear & Escalabilidade de Equipe** | Padrão com 2 Scripts Aprovados | • `chart_staff_pain_point.png`<br/>• `chart_custo_infra_vs_dadosfera_crossover.png` |
| [`view-03-dado-qualidades/view-lake-architecture/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/view-03-dado-qualidades/view-lake-architecture/) | **Seção [3]: Arquitetura Lakehouse Medallion, Pipelines & Data Quality** | Padrão Enxuto | • `chart_lake_architecture.png`<br/>• `chart_powerpoint_medallion.png` |
| [`view-03-dado-qualidades/view-governanca/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/view-03-dado-qualidades/view-governanca/) | **Seção {3.1}: Governança, Dicionário de Dados, RBAC & Blindagem LGPD** | Padrão Enxuto | • `chart_governanca_lgpd.png` |
| [`view-03-dado-qualidades/view-model-kimball/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/view-03-dado-qualidades/view-model-kimball/) | **Seção {3.2}: Modelagem Dimensional Kimball (Star Schema) & Insights** | Padrão Enxuto | • `chart_modelagem_kimball.png` |
| [`views-04-insights/descritivos/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-04-insights/descritivos/) | **Ato 3 / Seção [4.1]: Insights Descritivos — Funil, Causas-Raiz & Eficiência** | Padrão Enxuto (3 Submódulos) | • `chart_insights_descritivos.png`<br/>• `chart_02_motivos_abandono.png`<br/>• `chart_03_custo_recuperacao_roi.png` |
| [`views-04-insights/prescritivos/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-04-insights/prescritivos/) | **Ato 3 / Seção [4.2]: Insights Prescritivos — Decaimento (+1h) & Matriz RFM** | Envelopamento (4 Submódulos) | • `chart_insights_prescritivos.png`<br/>• `chart_05_otimizacao_timing_envio.png`<br/>• `card_destaque_timing_executivo.png`<br/>• `chart_03_produtos_mais_abandonados.png`<br/>• `chart_04_roi_campanhas_resgate.png` |
| [`views-05-insights-ia/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-05-insights-ia/) | **Ato 4 / Seção [5]: Módulo de Inteligência, GenAI & Data Apps** | Envelopamento Master com 5 Submódulos | • `chart_insights_ia_master.png`<br/>• `chart_modelos_preditivos_ml.png`<br/>• `chart_feature_importance_ml.png`<br/>• `chart_genai_extracao_copies.png`<br/>• `chart_similaridade_produtos.png`<br/>• `chart_data_app_simulador_roi.png` |

---

## 🎨 3. Padrão Visual Global (`charts-maker` Standard)

Todos os geradores e saídas gráficas do diretório `roteiro/` devem obrigatoriamente respeitar os seguintes princípios:
* **Fundo Branco Puro**: `#FFFFFF` em 100% dos painéis e canvas.
* **Resolução**: Exportação a **300 DPI** com `bbox_inches="tight"`.
* **Tipografia**: Família sem serifa moderna (`Segoe UI`, `DejaVu Sans`, `Helvetica`, `Arial`).
* **Integridade dos Dados**: Conexão exclusiva aos dados reais em Parquet (`data/mock/output_cleaned/parquet/`).
