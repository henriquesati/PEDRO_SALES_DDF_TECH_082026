# Especificação Visual & BI: Motivos de Abandono de Carrinho

## 📌 Contexto & Pergunta de Negócio
- **Pergunta Central**: Qual razão de abandono causa a maior perda de receita na plataforma e como esses motivos se distribuem entre diferentes dispositivos (Mobile, Desktop, Tablet) e faixas de valor de carrinho?
- **Insight de Negócio**: A análise descritiva dos 5.231 carrinhos abandonados revela que **Preço Alto (1.307 un / 25,0% / R$ 498,8k)** e **Frete Caro (1.207 un / 23,1% / R$ 434,6k)** são as duas principais causas-raiz de atrito no marketplace, somando mais de 48% do volume e ~R$ 933,4k em receita represada. **Indecisão (1.045 un / 20,0% / R$ 379,5k)** e **Problemas no Pagamento (961 un / 18,4% / R$ 365,3k)** concentram-se com maior intensidade no dispositivo móvel devido a atritos de preenchimento e etapas de checkout.

---

## 📊 Métricas & Fórmulas (Ground Truth)

- **Distribuição Percentual por Motivo (%)**: $\frac{\text{Carrinhos com Motivo } M}{\text{Total de Carrinhos Abandonados (5.231)}} \times 100$.
- **Receita Represada por Motivo (R$)**: Soma de `valor_total` dos carrinhos abandonados por `motivo_abandono`.
- **Ticket Médio por Motivo (R$)**: $\frac{\text{Receita Represada do Motivo } M}{\text{Volume de Carrinhos do Motivo } M}$.
- **Participação por Dispositivo (%)**: Distribuição relativa de cada causa de abandono entre Mobile, Desktop e Tablet.

---

## 🎨 Diretrizes Visuais de Design

1. **Estrutura em Painel Duplo (Multi-Panel Executive Layout)**:
   - **Painel Esquerdo (Distribuição & Dispositivo)**: Gráfico de barras horizontais empilhadas/agrupadas exibindo o volume absoluto e percentual de cada motivo decomposto por dispositivo (Mobile `#2563EB`, Desktop `#059669`, Tablet `#F59E0B`).
   - **Painel Direito (Impacto Financeiro)**: Gráfico de barras com a Receita Represada Total em R$ por motivo e o respectivo ticket médio destacado.
2. **Estilo Executivo**:
   - Fundo branco puro (`#FFFFFF`), grid sutil em cinza claro (`#CBD5E1`, linestyle `--`).
   - Tipografia limpa (`Segoe UI`, `DejaVu Sans`, `Arial`).
   - Exportação em 300 DPI com `bbox_inches="tight"`.

---

## 📍 Mapeamento dos Dados Parquet
- **Entidades Utilizadas**:
  - `data/mock/output_cleaned/parquet/carrinhos.parquet` (`motivo_abandono`, `dispositivo`, `valor_total`, `status`)
  - `data/mock/output_cleaned/parquet/clientes.parquet` (`segmento_rfm`, `cliente_id`)
- **Filtro de Escopo**: `status IN ('abandonado', 'recuperado', 'expirado')` com `motivo_abandono IS NOT NULL`.

---

## 🖼️ Artefato Visual Gerado
- **Arquivo**: [`chart_02_motivos_abandono.png`](chart_02_motivos_abandono.png)
- **Script Gerador**: [`generate_chart.py`](generate_chart.py)
