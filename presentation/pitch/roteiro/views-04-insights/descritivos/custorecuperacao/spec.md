# Especificação Visual & Técnica: Custo de Recuperação & ROI por Canal (`custorecuperacao`)

> **Momento do Roteiro**: **Ato 3 / Seção [4.1] — Diagnóstico da Operação: Eficiência Unitária & Retorno por Canal**  
> **Caminho da View**: `presentation/pitch/roteiro/views-04-insights/descritivos/custorecuperacao/`  
> **Artefato Principal**: [`chart_03_custo_recuperacao_roi.png`](chart_03_custo_recuperacao_roi.png) (300 DPI, 16:9 Widescreen)  
> **Script Gerador**: [`generate_chart.py`](generate_chart.py)  
> **Padrão Visual**: Fundo Branco Puro (`#FFFFFF`), Tipografia Sem Serifa Moderna, Paleta Semântica Executiva (`charts-maker` standard).  
> **Base de Dados**: `data/mock/output_cleaned/parquet/eventos_resgate.parquet` e `pedidos.parquet` (Ground Truth 100% Auditável).

---

## 🎯 1. Objetivo & Mensagem Estratégica no Pitch

Apresentar a **eficiência financeira unitária (CAC de Resgate)**, o **Investimento Total em Disparos** e a distribuição de **Lucro Líquido por canal de comunicação**, comprovando a assimetria positiva entre o investimento em infraestrutura de disparos (`R$ 373,06`) e o retorno financeiro líquido gerado (`+R$ 160,8k` com `431x ROI`).

### 📌 Principais Métricas Consolidadas:
* **Investimento Total em Disparos**: `R$ 373,06` (6.427 disparos omnichannel realizados).
* **Lucro Líquido Recuperado**: `+R$ 160.817,35` (498 pedidos resgatados com ticket médio de R$ 337).
* **Multiplicador de ROI Consolidado**: `431x ROI` sobre o custo total de infraestrutura e envios.
* **CAC Médio Global**: `R$ 0,75 / pedido resgatado` (apenas 0,22% do Ticket Médio).
* **Demonstrativo (DRE de Resgate)**: Receita Bruta `R$ 167,9k` - Cupons (4%) `R$ 6,7k` - Disparos `R$ 373,06` = `+R$ 160,8k Líquido`.

---

## 📂 2. Artefatos do Módulo

| Arquivo | Descrição |
| :--- | :--- |
| [`chart_03_custo_recuperacao_roi.png`](chart_03_custo_recuperacao_roi.png) | Painel visual executivo renderizado em alta resolução (300 DPI). |
| [`generate_chart.py`](generate_chart.py) | Script declarativo e funcional em Python para reprodução imediata. |
| [`spec.md`](spec.md) | Especificação técnica e guia de narrativa para o apresentador. |
