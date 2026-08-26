# Especificação Visual & Técnica: Motivos de Abandono de Carrinho (`motivosabandono`)

> **Momento do Roteiro**: **Ato 3 / Seção [4.1] — Diagnóstico da Operação: Concentração por Ticket & Decomposição Causal**  
> **Caminho da View**: `presentation/pitch/roteiro/views-04-insights/descritivos/motivosabandono/`  
> **Artefato Principal**: [`chart_02_motivos_abandono.png`](chart_02_motivos_abandono.png) (300 DPI, 16:9 Widescreen)  
> **Script Gerador**: [`generate_chart.py`](generate_chart.py)  
> **Padrão Visual**: Fundo Branco Puro (`#FFFFFF`), Tipografia Sem Serifa Moderna, Paleta Semântica Executiva (`charts-maker` standard).  
> **Base de Dados**: `data/mock/output_cleaned/parquet/carrinhos.parquet` (Ground Truth 100% Auditável).

---

## 🎯 1. Objetivo & Mensagem Estratégica no Pitch

Apresentar a análise detalhada do universo de **5.231 carrinhos que sofreram abandono no checkout** (R$ 1,96M represados), dividida em dois eixos complementares:
1. **Painel Esquerdo — Concentração Financeira por Faixa de Ticket**: Evidencia que a perda financeira se concentra desproporcionalmente em cestas de médio e alto valor (tickets acima de R$ 250 concentram mais de 83% de todo o dinheiro parado na mesa).
2. **Painel Direito — Decomposição das 6 Causas-Raiz de Abandono**: Detalha a distribuição percentual e volumétrica das causas (Frete Caro e Indecisão somam mais de 62% dos motivos observados).

### 📌 Universo da Amostra Analisada:
* **Base Analisada**: Exclusiva dos **5.231 carrinhos com atrito no checkout** (não inclui compras diretas sem abandono).
* **Volume Financeiro Represado**: **R$ 1,96M** (ou R$ 1,58M no saldo residual após resgates).
* **Concentração por Ticket**:
  * **Ticket Alto (> R$ 500)**: R$ 833,4k (52,8% da perda / 1.144 carrinhos).
  * **Ticket Médio-Alto (R$ 250–500)**: R$ 490,6k (31,1% da perda / 1.339 carrinhos).
  * **Ticket Médio-Baixo (R$ 100–250)**: R$ 221,6k (14,0% da perda / 1.276 carrinhos).
  * **Ticket Baixo (< R$ 100)**: R$ 31,8k (2,0% da perda / 442 carrinhos).
* **Causas-Raiz**:
  * **Frete Caro**: 38,2% dos motivos.
  * **Indecisão / Dúvidas**: 24,1% dos motivos.
  * **Erro no Pagamento**: 18,3% dos motivos.
  * **Preço Alto / Comparação**: 11,5% dos motivos.
  * **Não Informado & Estoque**: 7,9% dos motivos.

---

## 📂 2. Artefatos do Módulo

| Arquivo | Descrição |
| :--- | :--- |
| [`chart_02_motivos_abandono.png`](chart_02_motivos_abandono.png) | Painel visual executivo renderizado em alta resolução (300 DPI, Concentração à Esquerda e Causas à Direita). |
| [`generate_chart.py`](generate_chart.py) | Script declarativo e funcional em Python para reprodução imediata. |
| [`spec.md`](spec.md) | Especificação técnica e guia de narrativa para o apresentador. |
