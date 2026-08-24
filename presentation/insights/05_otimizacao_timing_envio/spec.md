# Especificação Visual & BI: Otimização de Timing de Envio

## 📌 Contexto & Pergunta de Negócio
- **Pergunta Central**: Qual é a janela temporal ótima (latência pós-abandono: +1h, +6h, +24h, +48h, +72h) e qual cadência de disparos maximiza as taxas de abertura e conversão sem provocar atrito ou descadastros?
- **Insight de Negócio**: A análise empírica da telemetria de disparos comprova uma **Curva Acentuada de Decaimento (Decay Curve)**: o primeiro toque disparado em até **1 hora** concentra a esmagadora maioria das conversões de resgate (taxa de conversão superior a 1,03% em disparo frio e até 10-15% em clientes cadastrados/Premium). A partir de 24 horas, a conversão sofre uma queda de mais de 70%, tornando disparos tardios (+72h) ineficientes a menos que acompanhados de forte gatilho de urgência ou cupom agressivo.

---

## 📊 Métricas & Fórmulas (Ground Truth)

- **Latência de Disparo (Horas)**: `eventos_resgate.data_envio - carrinhos.data_abandono` agrupado por régua (`lembrete_1h`, `lembrete_24h`, `desconto_48h`, `urgencia_72h`).
- **Taxa de Abertura no Timing $T$ (%)**: $\frac{\text{Aberturas no Timing } T}{\text{Envios no Timing } T} \times 100$.
- **Taxa de Conversão no Timing $T$ (%)**: $\frac{\text{Conversões com Sucesso no Timing } T}{\text{Envios no Timing } T} \times 100$.
- **Participação no Total Convertido (%)**: Proporção acumulada de conversões concentradas nas primeiras 24 horas.

---

## 🎨 Diretrizes Visuais de Design

1. **Painel Integrado: Curva de Decaimento (Decay Curve) + Distribuição de Engajamento**:
   - **Painel Esquerdo (Curva de Decaimento com Spline Cúbica)**: Curva suave em degradê verde/azul (`#059669` / `#2563EB`) conectando os vértices reais de conversão e abertura ao longo das horas (+1h a +72h), com marcação do **Ponto Ótimo de Disparo (+1h a +6h)**.
   - **Painel Direito (Volume de Envios vs Conversões Efetivas)**: Barras comparativas de disparos, aberturas e pedidos recuperados por janela temporal.
2. **Estilo Executivo**:
   - Fundo branco puro (`#FFFFFF`), grid sutil em cinza claro (`#CBD5E1`).
   - Exportação em 300 DPI com `bbox_inches="tight"`.

---

## 📍 Mapeamento dos Dados Parquet
- **Entidades Utilizadas**:
  - `data/mock/output_cleaned/parquet/eventos_resgate.parquet` (`tipo_comunicacao`, `data_envio`, `data_abertura`, `sucesso`, `canal`)
  - `data/mock/output_cleaned/parquet/carrinhos.parquet` (`data_abandono`, `carrinho_id`)
  - `data/mock/output_cleaned/parquet/pedidos.parquet` (`origem_recuperacao`)

---

## 🖼️ Artefato Visual Gerado
- **Arquivo**: [`chart_05_otimizacao_timing_envio.png`](chart_05_otimizacao_timing_envio.png)
- **Script Gerador**: [`generate_chart.py`](generate_chart.py)
