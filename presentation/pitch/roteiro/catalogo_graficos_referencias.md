# 📊 Catálogo Mestre Completo: Todos os Gráficos do Ecossistema

> **Status da Execução**: `20/20 Scripts Executados com Sucesso` | `100% dos Artefatos Gerados em Alta Resolução (300 DPI)`  
> **Padrão Visual**: Fundo Branco Puro (`#FFFFFF`), Tipografia Sem Serifa Moderna, Paleta Semântica Executiva (`charts-maker` standard).  
> **Fonte Canônica de Dados**: `data/mock/output_cleaned/parquet/` e `pitch_spec.md` (Ground Truth 100% Auditável).

---

## 📑 Sumário das Galerias

- [🏛️ 1. View de Arquitetura & Roteiro (`presentation/pitch/roteiro/arquitetura-view/`)](#1-view-de-arquitetura--roteiro)
- [🎯 2. Apresentação Pitch Executivo (`presentation/pitch/`)](#2-apresentação-pitch-executivo)
- [📈 3. Galeria Descritiva (`presentation/insights/01_descriptive/`)](#3-galeria-descritiva)
- [⚠️ 4. Galeria de Risco & Diagnóstico (`presentation/insights/02_risk/`)](#4-galeria-de-risco--diagnóstico)
- [💡 5. Galeria Prescritiva & Otimização (`presentation/insights/03_prescriptive/`)](#5-galeria-prescritiva--otimização)
- [⚙️ 6. Pipelines Técnicos dos Case Items (`pipelines/`)](#6-pipelines-técnicos-dos-case-items)

---

## 🏛️ 1. View de Arquitetura & Roteiro

Diretório: [`presentation/pitch/roteiro/arquitetura-view/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/arquitetura-view/)

| Artefato Visual | Link Direto para o Arquivo | Finalidade & Papel na Apresentação |
| :--- | :--- | :--- |
| **⭐ Template Oficial de Animação (Blocos Retos + Seta Leve)** | [`grafico-legado-l2r-vazio.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/arquitetura-view/assets/grafico-legado-l2r-vazio.png) | **Slide 1 no PowerPoint**: 5 blocos retos com fundo suave colorido, sem textos, colados à seta contínua em tom leve com tópicos internos, pronta para inserção de ícones animados. |
| **Diagrama Legado Preenchido (Referência Técnica)** | [`grafico-legado-l2r.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/arquitetura-view/assets/grafico-legado-l2r.png) | Mapeamento completo dos mais de 20 serviços AWS DIY (Kinesis, Lambda, Redshift, Redis, Airflow, etc.). |
| **Solução Dadosfera (Template Vazio)** | [`grafico-dadosfera-l2r-vazio.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/arquitetura-view/assets/grafico-dadosfera-l2r-vazio.png) | Base para apresentação progressiva dos módulos integrados da Dadosfera. |
| **Solução Dadosfera Unificada** | [`grafico-dadosfera-l2r.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/arquitetura-view/assets/grafico-dadosfera-l2r.png) | **Slide 2 no PowerPoint**: Container único da Plataforma Dadosfera absorvendo as 5 etapas. |
| **Deck PowerPoint Formatado** | [`arquitetura_dadosfera.pptx`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/arquitetura-view/powerpoint/arquitetura_dadosfera.pptx) | Apresentação 16:9 widescreen pronta para apresentação executiva. |
| **Biblioteca de 26 Ícones Oficiais (PNG)** | [`assets/icons/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/arquitetura-view/assets/icons/) | Pacote com ícones transparentes (`kinesis.png`, `lambda.png`, `redshift.png`, `redis.png`, `s3.png`, `snowflake.png`, `metabase.png`, etc.). |
| **🔥 View: Risco de Elasticidade em Picos** | [`chart_problema_elasticidade.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/problema-elasticidade/chart_problema_elasticidade.png) | **Slide de Transição Roteiro/Pitch**: Painel executivo demonstrando o custo de R$ 50k–100k/min de downtime em picos de Black Friday e a resposta elástica da Dadosfera. |
| **👥 View: Pain Point de Staff & Escalabilidade** | [`chart_staff_pain_point.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/staff-pain-point/chart_staff_pain_point.png) | **Momento 4 do Roteiro**: Gráfico executivo de projeção de headcount técnico (2020 a 2030) comparando a escalabilidade linear na AWS DIY (de 3 para até 8 staff com custo de R$ 1,0M/ano) vs. equipe enxuta e estável na Dadosfera (2-3 staff com 80% do tempo focado em gerar receita e economia de R$ 400k-750k/ano). |
| **📉 View: Comparativo Conceitual de Custos (Empilhado)** | [`chart_custo_infra_vs_dadosfera_stacked.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/staff-pain-point/chart_custo_infra_vs_dadosfera_stacked.png) | **Layout Minimalista para PowerPoint**: 2 gráficos conceituais empilhados verticalmente sem eixos numéricos rígidos (superior: curva de custo exponencial/subida rápida na AWS DIY vs. inferior: curva de custo linear/suave na Dadosfera). |
| **✂️ View: Comparativo Conceitual de Custos (Crossover / Cruzamento)** | [`chart_custo_infra_vs_dadosfera_crossover.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/staff-pain-point/chart_custo_infra_vs_dadosfera_crossover.png) | **Layout Comparativo Único para PowerPoint**: Gráfico conceitual com a curva vermelha (Infra Própria) cruzando e divergindo da curva verde (Dadosfera), marcando o ponto de break-even. |

---

## 🎯 2. Apresentação Pitch Executivo

Diretório: [`presentation/pitch/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/)

| Módulo do Pitch | Link Direto para o Arquivo | Conteúdo & Métricas Canônicas |
| :--- | :--- | :--- |
| **Item 6: Modelagem Kimball (Star Schema)** | [`chart_caseitem06_kimball_model.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/views/caseitem06/chart_caseitem06_kimball_model.png) | Arquitetura dimensional Gold: 6 dimensões conformadas + 2 tabelas fato (`fato_abandono` e `fato_resgate`) com JOINs 1-Hop otimizados. |
| **Item 4: Data Quality & Quarentena** | [`chart_06_scorecard_data_quality.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/06_data_quality_e_quarentena/chart_06_scorecard_data_quality.png) | Scorecard executivo: **94.2% de conformidade** (18 regras Great Expectations) e quarentena automatizada de 5.8% de anomalias. |
| **Item 10: Comparativo AWS vs Dadosfera** | [`chart_07_arquitetura_dadosfera_vs_aws.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/07_arquitetura_dadosfera_vs_aws/chart_07_arquitetura_dadosfera_vs_aws.png) | Painel comparativo de eficiência: Redução de Lead Time de 6 semanas para < 3 dias (**-86%**) e zero risco de sharding. |
| **Itens 9 e Bônus: Data App & GenAI** | [`chart_08_simulador_roi_data_app.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/08_data_app_simulador_prescritivo_genai/chart_08_simulador_roi_data_app.png) | Simulador interativo de sensibilidade de ROI no Streamlit e motor GenAI com LLMs elevando CTR em +18%. |

---

## 📈 3. Galeria Descritiva

Diretório: [`presentation/insights/01_descriptive/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/01_descriptive/)

| Visualização / Gráfico | Link Direto para o Arquivo | Destaques Técnicos |
| :--- | :--- | :--- |
| **BI: Funil de Recuperação de Carrinhos** | [`chart_bi_recuperacao_carrinhos.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/01_descriptive/01_bi_recuperacao_carrinhos/chart_bi_recuperacao_carrinhos.png) | Série temporal com 70% de abandono basal e **10.1% de taxa de recuperação** com réguas Dadosfera (+50% de lift). |
| **BI: Série Sinuosa 1 Semana** | [`chart_bi_recuperacao_carrinhos_sinuous_1week.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/01_descriptive/01_bi_recuperacao_carrinhos/chart_bi_recuperacao_carrinhos_sinuous_1week.png) | Detalhamento intra-semanal com variação horária de criação, abandono e resgate. |
| **Mini Card: Zonas Acumulado Reto** | [`mini_card_zonas_acumulado_reto.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/01_descriptive/01_bi_recuperacao_carrinhos/mini_card_zonas_acumulado_reto.png) | Mini card executivo consolidando os 7.500 carrinhos semestrais. |
| **Mini Card: Zonas Dupla** | [`mini_card_zonas_dupla.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/01_descriptive/01_bi_recuperacao_carrinhos/mini_card_zonas_dupla.png) | Card duplo comparativo de conversão orgânica vs. resgatados. |
| **Mini Card: Zonas Sinuoso 1 Semana** | [`mini_card_zonas_sinuoso_1semana.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/01_descriptive/01_bi_recuperacao_carrinhos/mini_card_zonas_sinuoso_1semana.png) | Mini card de telemetria semanal. |
| **Motivos de Abandono (Barras)** | [`chart_02_motivos_abandono.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/01_descriptive/02_motivos_abandono/chart_02_motivos_abandono.png) | Decomposição percentual de causas de abandono (Frete 38%, Indecisão 24%, Cadastro 18%, etc.). |
| **Treemap de Motivos de Abandono** | [`chart_02_treemap_motivos_abandono.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/01_descriptive/02_motivos_abandono/chart_02_treemap_motivos_abandono.png) | Visualização hierárquica por representatividade de abandono. |
| **Perda Financeira por Motivo & Ticket** | [`chart_02_perda_financeira_motivos.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/01_descriptive/02_motivos_abandono/chart_02_perda_financeira_motivos.png) | Cruzamento do motivo de abandono com faixas de ticket médio. |
| **Custo de Recuperação & ROI de Disparos** | [`chart_03_custo_recuperacao_roi.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/01_descriptive/03_custo_recuperacao_roi/chart_03_custo_recuperacao_roi.png) | Eficiência financeira por canal e **ROI consolidado de 45x multiplicador** sobre custos de envio. |

---

## ⚠️ 4. Galeria de Risco & Diagnóstico

Diretório: [`presentation/insights/02_risk/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/02_risk/)

| Visualização / Gráfico | Link Direto para o Arquivo | Destaques Técnicos |
| :--- | :--- | :--- |
| **Painel de Segmentação de Risco** | [`chart_03_segmentacao_risco.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/02_risk/01_segmentacao_risco/chart_03_segmentacao_risco.png) | Matriz consolidada de risco baseada em inatividade, histórico do cliente e valor da cesta. |
| **Dashboard 01: Visão Geral de Risco (KPIs)** | [`chart_03_dashboard_01_risk_overview.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/02_risk/01_segmentacao_risco/chart_03_dashboard_01_risk_overview.png) | Métricas agregadas de exposição financeira e volume sob risco. |
| **Dashboard 02: Drivers de Risco** | [`chart_03_dashboard_02_risk_drivers.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/02_risk/01_segmentacao_risco/chart_03_dashboard_02_risk_drivers.png) | Decomposição das variáveis preditivas de risco de abandono. |
| **Dashboard 03a: Fila de Priorização de Resgate** | [`chart_03_dashboard_03a_fila_acionamento.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/02_risk/01_segmentacao_risco/chart_03_dashboard_03a_fila_acionamento.png) | Fila que prioriza os **20% de carrinhos com mais de 65% do faturamento recuperável**. |
| **Dashboard 03b: Matriz Risco x ROI** | [`chart_03_dashboard_03b_matriz_risk_roi.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/02_risk/01_segmentacao_risco/chart_03_dashboard_03b_matriz_risk_roi.png) | Matriz cruzando probabilidade de conversão vs. retorno financeiro esperado. |
| **Dashboard 03: Matriz de Intervenção Combinada** | [`chart_03_dashboard_03_intervention_matrix.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/02_risk/01_segmentacao_risco/chart_03_dashboard_03_intervention_matrix.png) | Painel completo combinando fila de acionamento e matriz de calor. |
| **LTV Histórico vs Abandono** | [`chart_02_ltv_vs_abandono.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/02_risk/02_ltv_vs_abandono/chart_02_ltv_vs_abandono.png) | Correlação entre o valor vitalício do cliente (LTV) e a propensão a responder réguas de resgate. |
| **Matriz Prescritiva de Viabilidade** | [`chart_03_viabilidade_recuperacao_carrinho.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/02_risk/03_viabilidade_recuperacao_carrinho/chart_03_viabilidade_recuperacao_carrinho.png) | Gráfico de dispersão classificando carrinhos por viabilidade econômica dentro da janela de 28h. |

---

## 💡 5. Galeria Prescritiva & Otimização

Diretório: [`presentation/insights/03_prescriptive/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/03_prescriptive/)

| Visualização / Gráfico | Link Direto para o Arquivo | Destaques Técnicos |
| :--- | :--- | :--- |
| **Estratégia de Resgate por Segmento RFM** | [`chart_04_estrategia_resgate_segmento.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/03_prescriptive/01_estrategia_resgate_segmento/chart_04_estrategia_resgate_segmento.png) | **Preservação de Margem**: Clientes Premium convertem 18% com WhatsApp humanizado *sem desconto*, enquanto Novos recebem cupom para frete. |
| **Otimização de Timing & Curva de Decaimento** | [`chart_05_otimizacao_timing_envio.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/03_prescriptive/02_otimizacao_timing_envio/chart_05_otimizacao_timing_envio.png) | Curva de decaimento temporal: a janela de **+1h concentrou 86,4% das conversões observadas** na amostra. |
| **Categorias e Produtos Mais Abandonados** | [`chart_03_produtos_mais_abandonados.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/03_prescriptive/03_produtos_mais_abandonados/chart_03_produtos_mais_abandonados.png) | Análise de atrito: Eletrônicos (alto ticket/dúvidas técnicas) vs Moda (sensibilidade a frete). |
| **ROI e Eficiência de Campanhas de Resgate** | [`chart_04_roi_campanhas_resgate.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/03_prescriptive/04_roi_campanhas_resgate/chart_04_roi_campanhas_resgate.png) | Matriz de sensibilidade comparando canais (Email R$ 0,05 vs SMS R$ 0,15 vs WhatsApp R$ 0,30). |

---

## ⚙️ 6. Pipelines Técnicos dos Case Items

Diretório: [`pipelines/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/)

| Entregável do Case | Link Direto para o Arquivo | Descrição Técnica |
| :--- | :--- | :--- |
| **Item 6: Kimball Data Warehouse Model** | [`chart_caseitem06_kimball_model.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-06/outputs/assets/chart_caseitem06_kimball_model.png) | Diagrama do Star Schema Gold (dimensões e fatos). |
| **Item 6: Arquitetura DW Snowflake** | [`data_warehouse_architecture.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-06/outputs/assets/data_warehouse_architecture.png) | Fluxo de camadas Medallion Bronze $\rightarrow$ Silver $\rightarrow$ Gold no Snowflake. |
| **Item 7: Série Temporal de Abandono** | [`chart_01_serie_temporal_abandono_resgate.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_01_serie_temporal_abandono_resgate.png) | Telemetria contínua de criação e abandono. |
| **Item 7: Performance de Categorias** | [`chart_02_performance_categorias.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_02_performance_categorias.png) | Volumetria e receita represada por categoria de produto. |
| **Item 7: Rentabilidade & ROI por Canal** | [`chart_03_roi_eficiencia_canais.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_03_roi_eficiencia_canais.png) | Funil de telemetria multicanal (envio, abertura, clique, conversão). |
| **Item 7: Matriz de Atrito RFM (Heatmap)** | [`chart_04_matriz_motivos_rfm_heatmap.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_04_matriz_motivos_rfm_heatmap.png) | Mapa de calor cruzando causas de abandono com segmentos de clientes. |
| **Item 7: Dispersão de Viabilidade** | [`chart_05_dispersao_viabilidade_recuperacao.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_05_dispersao_viabilidade_recuperacao.png) | Análise bidimensional de valor recuperável vs. probabilidade. |
| **Item 7: Resumo de Data Quality & Quarentena** | [`chart_06_data_quality_anomalies_summary.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_06_data_quality_anomalies_summary.png) | Resumo de anomalias interceptadas na camada Silver. |
| **Item 8: Feature Importance (Machine Learning)** | [`ml_feature_importance.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-08/outputs/assets/ml_feature_importance.png) | Pesos das variáveis preditivas de propensão de conversão. |
| **Item 9: Mapa de Similaridade de Produtos** | [`data_app_product_similarity_map.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-09/outputs/assets/data_app_product_similarity_map.png) | Clusterização e espaço vetorial de SKUs recomendados. |
| **Item 9: Simulação Interativa de ROI** | [`data_app_roi_simulation.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-09/outputs/assets/data_app_roi_simulation.png) | Projeção em tempo real com calibração de parâmetros no Streamlit. |
