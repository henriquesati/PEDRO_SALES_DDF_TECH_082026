# Catálogo de Gráficos Executivos (chartsoutput)

Este diretório consolida todos os gráficos analíticos gerados no projeto, organizados por categoria de negócio e versionados para comparação direta entre a **Versão Anterior** e a **Versão Atual Auditada (Ground Truth & Zero Fabrication)**.

---

## Estrutura de Diretórios

- **`versao_atual_auditada/`**: Versão final com cálculos estritamente dinâmicos a partir das camadas Lakehouse/Parquet e 100% aderente à especificação central `presentation/pitch/pitch_spec.md`.
- **`versao_anterior/`**: Versão anterior extraída do commit base para auditoria visual e comparativa.
- **`comparativo_organizado/`**: Diretório unificado contendo os pares `anterior_<nome>.png` e `atual_<nome>.png` lado a lado para inspeção rápida.

---

## Categorias de Gráficos

1. **`01_descriptive/`**: BI e Evolução Acumulada, Causas-Raiz de Abandono (Treemap & Perda Financeira), Custo Unitário por Recuperação & ROI de Canal.
2. **`02_risk/`**: Segmentação de Risco Multidimensional (Overview, Drivers, Fila de Acionamento, Matriz Risk x ROI), LTV vs Abandono, Curva de Viabilidade Prescritiva.
3. **`03_prescriptive/`**: Estratégia de Resgate por Canal, Otimização de Timing & Decaimento Temporal, Categorias/Produtos Mais Abandonados, ROI e Eficiência de Campanhas.
4. **`pitch_views/`**: Scorecard de Data Quality & Quarentena, Arquitetura Comparativa (Dadosfera vs AWS DIY), Simulador Prescritivo Streamlit & GenAI, Modelagem Kimball.
5. **`roteiro_views/`**: Problema de Elasticidade e Queda de Checkout, TCO & Crossover de Custos de Infraestrutura, Visão L2R de Arquitetura.
6. **`pipelines/`**: Visualizações de Data Quality (Item 4), Features GenAI (Item 5), Star Schema DW (Item 6), Hub Analítico de BI (Item 7), Importância de Features ML (Item 8), Simulador Data App (Item 9).
