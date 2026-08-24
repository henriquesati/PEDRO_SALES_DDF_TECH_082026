# Especificação Visual & BI: Motivos de Abandono de Carrinho

## 📌 Contexto & Pergunta de Negócio
- **Pergunta Central**: Qual razão de abandono causa a maior perda de receita na plataforma e como esses motivos se distribuem entre diferentes dispositivos (Mobile, Desktop, Tablet) e faixas de valor de carrinho?
- **Insight de Negócio**: A análise descritiva dos 5.231 carrinhos abandonados revela que **Preço Alto (1.307 un / 25,0% / R$ 498,8k)** e **Frete Caro (1.207 un / 23,1% / R$ 434,6k)** são as duas principais causas-raiz de atrito no marketplace, somando mais de 48% do volume e ~R$ 933,4k em receita represada. **Indecisão (1.045 un / 20,0% / R$ 379,5k)** e **Problemas no Pagamento (961 un / 18,4% / R$ 365,3k)** concentram-se com maior intensidade no dispositivo móvel devido a atritos de preenchimento e etapas de checkout.

> [!NOTE]
> **Foco do Projeto em Proporções (%)**: O núcleo desta análise é a distribuição percentual das causas de atrito e a quebra relativa por dispositivo. O cliente pode adequar o seu próprio Ticket Médio por categoria/motivo. Os valores em R$ refletem o baseline da *Entidade Exemplo* (TM Geral ~R$ 375,00) apenas para ilustrar a perda financeira correspondente.

---

## 📊 Métricas & Fórmulas (Ground Truth)

- **Distribuição Percentual por Motivo (%)**: $\frac{\text{Carrinhos com Motivo } M}{\text{Total de Carrinhos Abandonados (5.231)}} \times 100$.
- **Receita Represada por Motivo (R$)**: Soma de `valor_total` dos carrinhos abandonados por `motivo_abandono`.
- **Ticket Médio por Motivo (R$)**: $\frac{\text{Receita Represada do Motivo } M}{\text{Volume de Carrinhos do Motivo } M}$.
- **Dispersão de Carrinhos por Causa-Raiz**: Distribuição pontual de cada carrinho individual por faixa de valor (`valor_total`) cruzado com o motivo declarado/inferido e dispositivo utilizado.

---

## 🎨 Diretrizes Visuais de Design (Artefatos Separados)

### Artefato 1: Gráfico de Dispersão de Volume por Causa-Raiz e Valor do Carrinho
- **Arquivo**: [`chart_02_dispersao_motivos_abandono.png`](chart_02_dispersao_motivos_abandono.png)
- **Tipo de Gráfico**: **Gráfico de Dispersão / Strip Plot com Jitter Controlado**
- **Eixo X**: Motivos de Abandono (`Preço Alto`, `Frete Caro`, `Indecisão`, `Erro no Pagamento`, `Não Informado`, `Estoque Indisponível`) ordenados por volume.
- **Eixo Y**: Valor do Carrinho Abandonado (`valor_total` em R$, escala 0 a 1.600).
- **Pontos (Scatter)**: Cada ponto representa um carrinho abandonado real, colorido pelo dispositivo (`Mobile` em Azul `#2563EB`, `Desktop` em Verde `#059669`, `Tablet` em Âmbar `#F59E0B`), com jitter horizontal proporcional à densidade de volume.
- **Anotações**: Badges superiores indicando o volume absoluto (`un`), a participação percentual (`%`) e a linha de valor mediano/médio para cada causa-raiz.

### Artefato 2: Gráfico Separado de Impacto e Perda Financeira Represada (R$)
- **Arquivo**: [`chart_02_perda_financeira_motivos.png`](chart_02_perda_financeira_motivos.png)
- **Tipo de Gráfico**: **Gráfico Executivo de Barras Horizontais com Badges de Ticket Médio**
- **Eixo Y**: Motivo de Abandono.
- **Eixo X**: Receita Total Represada em R$ Milhares.
- **Destaques**: Valor financeiro total represado (R$ 1.845,0k), ticket médio de cada grupo e participação percentual no montante total da perda.

---

## 📍 Mapeamento dos Dados Parquet
- **Entidades Utilizadas**:
  - `data/mock/output_cleaned/parquet/carrinhos.parquet` (`motivo_abandono`, `dispositivo`, `valor_total`, `status`, `carrinho_id`)
  - `data/mock/output_cleaned/parquet/clientes.parquet` (`segmento_rfm`, `cliente_id`)
- **Filtro de Escopo**: `status IN ('abandonado', 'recuperado', 'expirado')` com `motivo_abandono IS NOT NULL`.

---

## 🖼️ Artefatos Visuais Gerados
- **Dispersão por Causa-Raiz**: [`chart_02_dispersao_motivos_abandono.png`](chart_02_dispersao_motivos_abandono.png)
- **Perda Financeira Represada**: [`chart_02_perda_financeira_motivos.png`](chart_02_perda_financeira_motivos.png)
- **Script Gerador Único**: [`generate_chart.py`](generate_chart.py)
