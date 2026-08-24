# Especificação Visual & BI: Custo por Carrinho Recuperado (CAC de Resgate), ROI & Adjacências

## 📌 Contexto & Pergunta de Negócio
- **Pergunta Central**: Qual é o custo efetivo por carrinho recuperado (CAC de Resgate) em cada canal de comunicação (Email, SMS, WhatsApp, Push) e qual o retorno sobre o investimento (ROI líquido) e margem residual gerados na esteira de recuperação?
- **Insight de Negócio**: A operação multicanal da Dadosfera demonstra que o **Email** atua como o grande motor de escala e rentabilidade (custo de apenas R$ 0,05/envio, gerando CAC de resgate inferior a R$ 1,20 por pedido recuperado). Canais de maior custo unitário como **WhatsApp (R$ 0,30/envio)** e **SMS (R$ 0,15/envio)** devem ser acionados de forma qualificada para tickets médios e altos (> R$ 250), garantindo um **ROI global consolidado superior a 40x** e custo de comunicação **abaixo de 1,5%** do valor resgatado.

> [!NOTE]
> **Foco do Projeto em Proporções (%) & Entidade Exemplo**: As métricas de eficiência são estruturadas em ratios relativos (CAC como % do Ticket Médio e Multiplicador de ROI). A *Entidade Exemplo de Baseline* (TM Geral ~R$ 375,00) exemplifica os ganhos absolutos em R$, permitindo ao cliente plugar sua própria estrutura de custos de mensageria e ticket médio.

---

## 📊 Métricas & Fórmulas (Ground Truth)

- **Custo Unitário de Disparo por Canal**:
  - `push_app`: R$ 0,02 / disparo
  - `email`: R$ 0,05 / disparo
  - `sms`: R$ 0,15 / disparo
  - `whatsapp`: R$ 0,30 / disparo
- **Custo por Carrinho Recuperado (CAC de Resgate)**:
  $$\text{CAC de Resgate} = \frac{\text{Custo Total de Disparos do Canal}}{\text{Total de Pedidos Recuperados pelo Canal}}$$
- **ROI Líquido por Canal (%) & Multiplicador**:
  $$\text{ROI Multiplicador} = \frac{\text{Receita Recuperada} - \text{Descontos} - \text{Custo de Disparo}}{\text{Custo de Disparo}}$$
- **Custo de Resgate sobre o Ticket Médio (%)**:
  $$\text{Custo / Ticket (\%)} = \frac{\text{CAC de Resgate}}{\text{Ticket Médio Recuperado}} \times 100 \quad (\text{Benchmark: } < 2,0\%)$$

---

## 🎨 Diretrizes Visuais de Design (Painel Integrado)

- **Arquivo**: [`chart_03_custo_recuperacao_roi.png`](chart_03_custo_recuperacao_roi.png)
- **Tipo de Gráfico**: **Painel Duplo Executivo Integrado (Lado a Lado - 300 DPI)**
- **Painel 1 (Esquerda) — Eficiência de Custo por Conversão (CAC de Resgate)**:
  - Barras horizontais por Canal (`Email`, `Push App`, `SMS`, `WhatsApp`).
  - Badges com o CAC de Resgate em R$ e o percentual correspondente sobre o Ticket Médio.
  - Linha de benchmark de segurança (< 2,0% do TM).
- **Painel 2 (Direita) — Retorno Líquido & Multiplicador de ROI**:
  - Barras de Receita Líquida Recuperada (R$ Milhares em Verde Esmeralda `#059669`) comparadas ao Custo de Disparos (Rose `#E11D48`).
  - Badges destacados com o **Múltiplo de ROI** de cada canal (`45x`, `38x`, etc.) e ROI consolidado da operação.

---

## 📍 Mapeamento dos Dados Parquet
- **Entidades Utilizadas**:
  - `data/mock/output_cleaned/parquet/eventos_resgate.parquet` (`canal`, `custo_envio`, `desconto_oferecido`, `sucesso`, `valor_pedido_final`, `carrinho_id`)
  - `data/mock/output_cleaned/parquet/pedidos.parquet` (`origem_recuperacao`, `valor_total`, `carrinho_id`)
  - `data/mock/output_cleaned/parquet/carrinhos.parquet` (`valor_total`, `status`)

---

## 🖼️ Artefato Visual Gerado
- **Painel de Custo por Recuperação & ROI**: [`chart_03_custo_recuperacao_roi.png`](chart_03_custo_recuperacao_roi.png)
- **Script Gerador**: [`generate_chart.py`](generate_chart.py)
