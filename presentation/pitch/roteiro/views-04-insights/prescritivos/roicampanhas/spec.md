# Especificação Visual & Técnica: ROI e Eficiência de Campanhas de Resgate (`roicampanhas`)

> **Momento do Roteiro**: **Ato 3 / Seção [4.2] — Tomada de Decisão: Funil por Canal & Rebalanceamento Orçamentário**  
> **Caminho da View**: `presentation/pitch/roteiro/views-04-insights/prescritivos/roicampanhas/`  
> **Artefato Principal**: [`chart_04_roi_campanhas_resgate.png`](chart_04_roi_campanhas_resgate.png) (300 DPI, 16:9 Widescreen)  
> **Script Gerador**: [`generate_chart.py`](generate_chart.py)  
> **Padrão Visual**: Fundo Branco Puro (`#FFFFFF`), Tipografia Sem Serifa Moderna, Paleta Semântica Executiva (`charts-maker` standard).  
> **Base de Dados**: `data/mock/output_cleaned/parquet/eventos_resgate.parquet`, `pedidos.parquet` (Ground Truth 100% Auditável).

---

## 🎯 1. Objetivo & Mensagem Estratégica no Pitch

Apresentar a **eficiência comparativa do funil de conversão por canal de disparo** (Abertura, Clique e Conversão) e a **prescrição de rebalanceamento orçamentário** para maximização do ROI (alocando 85% do budget em E-mail + WhatsApp VIP e reduzindo dispersão em SMS/Push).

### 📌 Principais Métricas:
* **E-mail Transacional**: 85% do budget recomendado | R$ 1,02/resgate | 68% do volume de conversões.
* **WhatsApp VIP**: 12% do budget recomendado | 18% de conversão em clientes Premium.
* **SMS Marketing**: 2% do budget | canal de apoio pontual.
* **Push Notification**: 1% do budget | retenção de usuários ativos com app instalado.

---

## 📂 2. Artefatos do Módulo

| Arquivo | Descrição |
| :--- | :--- |
| [`chart_04_roi_campanhas_resgate.png`](chart_04_roi_campanhas_resgate.png) | Painel visual executivo renderizado em alta resolução (300 DPI). |
| [`generate_chart.py`](generate_chart.py) | Script declarativo e funcional em Python para reprodução imediata. |
| [`spec.md`](spec.md) | Especificação técnica e guia de narrativa para o apresentador. |
