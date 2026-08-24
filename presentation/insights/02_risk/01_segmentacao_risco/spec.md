# Especificação Visual & BI: Segmentação de Risco de Abandono

## 📌 Contexto & Pergunta de Negócio
- **Pergunta Central**: Como identificar carrinhos em risco crítico/alto durante a sessão ativa e como essa vulnerabilidade se distribui entre os segmentos RFM (`Premium`, `Regular`, `Dormant`, `Novo`) e faixas de LTV?
- **Insight de Negócio**: A estratificação de risco demonstra que carrinhos de clientes novos navegando via mobile com tickets elevados apresentam o maior risco de abandono (**Faixa Crítica / Alta**), demandando intervenção em tempo real (ex: modais de checkout ou chat). Por outro lado, clientes **Premium** concentram-se em risco baixo/médio, onde o abandono decorre de interrupção temporária e a recuperação possui alta elasticidade sem necessidade de descontos agressivos.

> [!NOTE]
> **Foco do Projeto em Proporções (%)**: A matriz de calor e a triagem de risco fundamentam-se em proporções de tráfego e taxas relativas de propensão ao abandono. O cliente pode parametrizar o limiar de valor do carrinho da sua própria operação. Os valores em R$ exemplificam a perda financeira usando a *Entidade Exemplo de Baseline*.


---

## 📊 Métricas & Fórmulas (Ground Truth)

- **Score de Risco em Tempo de Sessão (`RISK_SCORE`)**:
  - `Valor do Carrinho > R$ 500`: +2 (senão +1)
  - `Dispositivo Mobile`: +2 (senão +1)
  - `Cliente Novo`: +2 (senão +1)
  - `Duração de Sessão < 5 min`: +2 (senão +1)
  - `Atrito / Erro de Pagamento / Frete Alto`: +3
- **Faixas de Classificação**:
  - `CRÍTICO`: Score $\ge 8$
  - `ALTO`: Score $6 \le \text{Score} < 8$
  - `MÉDIO`: Score $4 \le \text{Score} < 6$
  - `BAIXO`: Score $< 4$
- **Taxa Observada de Abandono por Nível de Risco (%)**: $\frac{\text{Carrinhos Abandonados na Faixa } R}{\text{Total de Carrinhos na Faixa } R} \times 100$.

---

## 🎨 Diretrizes Visuais de Design

1. **Painel Integrado: Matriz de Calor (Heatmap) + Distribuição de Risco**:
   - **Painel Esquerdo (Heatmap 2D)**: Cruzamento de Níveis de Risco (`Crítico`, `Alto`, `Médio`, `Baixo`) $\times$ Segmentos RFM (`Premium`, `Regular`, `Dormant`, `Novo`), com anotações em cada célula contendo o volume de carrinhos e a taxa média de risco.
   - **Painel Direito (Volume & Receita Represada por Faixa)**: Barras com o volume absoluto e receita represada em R$ por faixa de risco.
2. **Estilo Executivo**:
   - Fundo branco puro (`#FFFFFF`), gradiente semântico de calor (tons suaves de azul `#EFF6FF` a vermelho rose `#E11D48`).
   - Exportação em 300 DPI com `bbox_inches="tight"`.

---

## 📍 Mapeamento dos Dados Parquet
- **Entidades Utilizadas**:
  - `data/mock/output_cleaned/parquet/carrinhos.parquet`
  - `data/mock/output_cleaned/parquet/clientes.parquet`
  - `data/mock/output_cleaned/parquet/pedidos.parquet`

---

## 🖼️ Artefato Visual Gerado
- **Arquivo**: [`chart_03_segmentacao_risco.png`](chart_03_segmentacao_risco.png)
- **Script Gerador**: [`generate_chart.py`](generate_chart.py)
