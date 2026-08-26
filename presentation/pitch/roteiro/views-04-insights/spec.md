# 🏛️ Módulo Master de Views: Insights de Negócio (`views-04-insights`)

> **Momento do Roteiro**: **Ato 3 / Seção [4]-[5] — Prova de Conceito: Insights Descritivos e Prescritivos em Recuperação de Carrinho**  
> **Diretório Envelope**: `presentation/pitch/roteiro/views-04-insights/`  
> **Padrão de Organização**: Envelopamento Lógico de Módulos Analíticos (Consulte a arquitetura completa em [`presentation/pitch/roteiro/README.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/README.md))  
> **Fontes Estratégicas**: [`presentation/pitch/roteiro.txt`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro.txt), [`presentation/pitch/pitch_spec.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/pitch_spec.md), [`insights/README.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/insights/README.md) e [`data/mock/output_cleaned/parquet/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/mock/output_cleaned/parquet/).

---

## 🎯 1. Visão Geral da Seção de Insights do Roteiro

A seção de **Insights de Negócio (`views-04-insights`)** materializa o valor tangível da Plataforma Dadosfera no contexto do e-commerce através da Prova de Conceito (PoC) de **Recuperação de Carrinho Abandonado**. 

Após demonstrar a transição da arquitetura técnica legada para a Dadosfera (Ato 1) e comprovar a confiabilidade dos pipelines, governança LGPD e modelagem Kimball (Ato 2 / Seção [3]), este módulo apresenta as **respostas analíticas às duas perguntas fundamentais de negócio**:

1. **Insights Descritivos** (*O que aconteceu?*): Mapeamento do funil de conversão, série temporal semestral, decomposição das 6 causas-raiz de abandono, taxa de recuperação observada e eficiência de custo por resgate (CAC / ROI).
2. **Insights Prescritivos** (*O que devemos fazer?*): Determinação do timing ótimo de disparo (curva de decaimento temporal +1h), estratégia de abordagem por cluster RFM (preservação de margem de clientes Premium sem desconto vs. cupons para Novos), análise de catálogo por categoria e rebalanceamento orçamentário entre canais.

---

## 📊 2. Resumo dos Submódulos e Métricas Canônicas

| Submódulo da View | Momento no Roteiro | Pergunta de Negócio | Foco da Narrativa & Artefatos |
| :--- | :--- | :---: | :--- |
| [`descritivos/funilrecuperacao/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-04-insights/descritivos/funilrecuperacao/) | **Ato 3 / Seção [4.1] — Diagnóstico da Operação** | *O que aconteceu?* | • **7.500 carrinhos semestrais** com **69,7% de abandono basal**.<br/>• **+10,1% de recuperação** com réguas Dadosfera (+R$ 167,9k recuperados e lift de conversão total de 23,1% para 29,7%).<br/>• Artefato: `chart_insights_descritivos.png`. |
| [`descritivos/motivosabandono/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-04-insights/descritivos/motivosabandono/) | **Ato 3 / Seção [4.1] — Causas de Abandono** | *Por que abandonaram?* | • Decomposição das 6 causas-raiz: Frete Caro (38,2%), Indecisão (24,1%), Erro no Pagamento (18,3%).<br/>• Concentração financeira por faixa de ticket.<br/>• Artefato: `chart_02_motivos_abandono.png`. |
| [`descritivos/custorecuperacao/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-04-insights/descritivos/custorecuperacao/) | **Ato 3 / Seção [4.1] — CAC & ROI** | *Qual foi o custo?* | • CAC Unitário de Resgate: E-mail R$ 1,02/resgate, Push R$ 1,67, SMS R$ 3,00, WhatsApp R$ 12,00.<br/>• Multiplicador de ROI consolidado em 45x.<br/>• Artefato: `chart_03_custo_recuperacao_roi.png`. |
| [`prescritivos/timingenvio/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-04-insights/prescritivos/timingenvio/) | **Ato 3 / Seção [4.2] — Timing de Disparo** | *Quando agir?* | • **Janela de Ouro (+1h)**: A 1ª hora após o abandono concentra **86,4% de todas as conversões observadas** (-70% após 24h).<br/>• Artefatos: `chart_05_otimizacao_timing_envio.png` e `card_destaque_timing_executivo.png`. |
| [`prescritivos/estrategiaresgate/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-04-insights/prescritivos/estrategiaresgate/) | **Ato 3 / Seção [4.2] — Segmentação RFM** | *O que oferecer para quem?* | • **Preservação de Margem**: Clientes Premium convertem 18% via WhatsApp VIP **sem conceder desconto** (100% da margem protegida).<br/>• Artefato: `chart_insights_prescritivos.png`. |
| [`prescritivos/produtosabandonados/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-04-insights/prescritivos/produtosabandonados/) | **Ato 3 / Seção [4.2] — Ações de Catálogo** | *Quais produtos otimizar?* | • Eletrônicos & Decoração (78,8% / R$ 7,34M represados).<br/>• Matriz Multidimensional de Posicionamento (Scatter Log + 4 Quadrantes), Top 5 SKUs Críticos e 5 Cards Prescritivos de Intervenção de Catálogo.<br/>• Artefato: `chart_03_produtos_mais_abandonados.png`. |
| [`prescritivos/roicampanhas/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-04-insights/prescritivos/roicampanhas/) | **Ato 3 / Seção [4.2] — Alocação de Budget** | *Como balancear o orçamento?* | • Rebalanceamento orçamentário: 85% E-mail + 12% WhatsApp VIP (reduzindo dispersão em SMS/Push).<br/>• Artefato: `chart_04_roi_campanhas_resgate.png`. |

---

## 🎨 3. Padrões Gráficos Compartilhados (`charts-maker` Standard)

* **Canvas & Fundo**: `#FFFFFF` (Branco Puro) em 100% dos painéis, eixos e canvas.
* **Proporção & Resolução**: **16:9 Widescreen** exportado a **300 DPI** com `bbox_inches="tight"`.
* **Tipografia**: Família sem serifa moderna (`Segoe UI`, `DejaVu Sans`, `Arial`).
* **Integridade Absoluta (Ground Truth)**: Todos os dados plotados são carregados diretamente dos arquivos Parquet em `data/mock/output_cleaned/parquet/`.
* **Ausência de Pasta `assets/`**: Estrutura de pastas limpa, plana e padronizada.
