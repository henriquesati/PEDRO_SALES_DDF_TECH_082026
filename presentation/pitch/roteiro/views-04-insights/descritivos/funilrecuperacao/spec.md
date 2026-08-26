# Especificação Visual & Técnica: Funil de Recuperação de Carrinhos (`funilrecuperacao`)

> **Momento do Roteiro**: **Ato 3 / Seção [4.1] — Diagnóstico da Operação: Funil de Conversão & Série Semestral**  
> **Caminho da View**: `presentation/pitch/roteiro/views-04-insights/descritivos/funilrecuperacao/`  
> **Artefato Principal**: [`chart_insights_descritivos.png`](chart_insights_descritivos.png) (300 DPI, 16:9 Widescreen)  
> **Script Gerador**: [`generate_chart.py`](generate_chart.py)  
> **Padrão Visual**: Fundo Branco Puro (`#FFFFFF`), Tipografia Sem Serifa Moderna, Paleta Semântica Executiva (`charts-maker` standard).  
> **Base de Dados**: `data/mock/output_cleaned/parquet/carrinhos.parquet` e `pedidos.parquet` (Ground Truth 100% Auditável).

---

## 🎯 1. Objetivo & Mensagem Estratégica no Pitch

Apresentar o **diagnóstico quantitativo da operação de e-commerce**, demonstrando a evolução acumulada dos 7.500 carrinhos semestrais (Jan–Jun 2026), a taxa basal de abandono de 69,7% e o impacto de resgate ativo da Dadosfera (+10,1% sobre os abandonos / lift de +28,6% na conversão total).

### 📌 Principais Métricas:
* **Volume Semestral**: 7.500 carrinhos (R$ 2,80M GMV criado).
* **Abandono no Checkout**: 69,7% (5.231 carrinhos / R$ 1,58M represados).
* **Resgate Dadosfera**: + 498 pedidos faturados (+R$ 167,9k recuperados).
* **Eficiência Financeira**: CAC E-mail R$ 1,02 por pedido e ROI consolidado de 45x.

---

## 📂 2. Artefatos do Módulo

| Arquivo | Descrição |
| :--- | :--- |
| [`chart_insights_descritivos.png`](chart_insights_descritivos.png) | Painel visual executivo renderizado em alta resolução (300 DPI). |
| [`generate_chart.py`](generate_chart.py) | Script declarativo e funcional em Python para reprodução imediata. |
| [`spec.md`](spec.md) | Especificação técnica e guia de narrativa para o apresentador. |
