# Especificação Visual & BI: Estratégia de Resgate por Segmento

## 📌 Contexto & Pergunta de Negócio
- **Pergunta Central**: Qual é a política ótima de resgate (timing, canal e incentivo financeiro) para cada segmento RFM (`Premium`, `Regular`, `Dormant`, `Novo`) que maximiza a receita recuperada líquida e impede o desperdício de margem com descontos desnecessários?
- **Insight de Negócio**: Clientes **Premium** possuem ticket médio elevado (~R$ 800) e alta responsividade, o que gera uma **Viabilidade Líquida Unitária fortemente positiva** mesmo utilizando canais nobres de maior custo (WhatsApp a R$ 0,30 / atendimento VIP), sem necessidade de desconto. Por outro lado, para clientes **Novos** e **Dormant**, o uso de canais caros ou frete grátis irrestrito resulta em viabilidade negativa; a prescrição correta exige automação de custo quase zero (Email a R$ 0,05 / Push a R$ 0,02) e foco em *Social Proof* ou descontos progressivos condicionados ao valor da cesta.

> [!NOTE]
> **Foco do Projeto em Proporções (%)**: A modelagem de viabilidade baseia-se em multiplicadores de ROI e taxas relativas de conversão. O cliente pode plugar o seu próprio Ticket Médio por segmento para projetar seu ganho líquido. Os valores monetários apresentados refletem os tickets médios da *Entidade Exemplo de Baseline* (Premium R$ 800, Regular R$ 360, Novo R$ 250, Dormant R$ 200).


---

## 📊 Métricas & Fórmulas (Ground Truth & Prescritiva)

- **Viabilidade Líquida Unitária por Resgate (R$)**:
  $$\text{Viabilidade Líquida} = (\text{Taxa de Conversão Esperada} \times \text{Ticket Médio}) - (\text{Custo de Comunicação} + \text{Custo do Desconto})$$
- **Custos Unitários por Canal**:
  - `WhatsApp`: R$ 0,30
  - `SMS`: R$ 0,15
  - `Email`: R$ 0,05
  - `Push App`: R$ 0,02
- **Múltiplo de Retorno sobre Custo (ROI)**: $\frac{\text{Receita Líquida Recuperada}}{\text{Custo Total de Disparos}}$.

---

## 🎨 Diretrizes Visuais de Design

1. **Painel Integrado: Simulação de Viabilidade Líquida + Alocação Estratégica**:
   - **Painel Esquerdo (Retorno Financeiro Líquido por Canal e Segmento)**: Gráfico de barras agrupadas comparando o ganho líquido esperado (R$) por resgate entre os canais WhatsApp, SMS, Email e Push para cada cluster RFM.
   - **Painel Direito (Matriz Prescritiva de Ações Recomendadas)**: Visualização matricial executiva das regras ótimas de alocação de canais, timigns de primeiro toque e políticas de desconto.
2. **Estilo Executivo**:
   - Fundo branco puro (`#FFFFFF`), grid sutil em cinza claro (`#CBD5E1`).
   - Exportação em 300 DPI com `bbox_inches="tight"`.

---

## 📍 Mapeamento dos Dados Parquet
- **Entidades Utilizadas**:
  - `data/mock/output_cleaned/parquet/clientes.parquet`
  - `data/mock/output_cleaned/parquet/carrinhos.parquet`
  - `data/mock/output_cleaned/parquet/eventos_resgate.parquet`
  - `data/mock/output_cleaned/parquet/pedidos.parquet`

---

## 🖼️ Artefato Visual Gerado
- **Arquivo**: [`chart_04_estrategia_resgate_segmento.png`](chart_04_estrategia_resgate_segmento.png)
- **Script Gerador**: [`generate_chart.py`](generate_chart.py)
