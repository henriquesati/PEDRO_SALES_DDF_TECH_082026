# Especificação Visual & BI: Visão Acumulada de Recuperação de Carrinhos

## 📌 Contexto & Pergunta de Negócio
- **Pergunta Central**: Qual é a evolução acumulada do volume total de carrinhos no marketplace ao longo do semestre (partindo de zero até a amplitude máxima), qual a proporção de conversão direta orgânica e qual o impacto visual da faixa intermediária de carrinhos recuperados e reengajados pela Dadosfera?
- **Insight de Negócio**: A visualização de curvas acumuladas evidencia o funil macro: o total de carrinhos inicia em zero e cresce continuamente até 7.500 unidades. A camada basal de compras orgânicas atende ~2.229 carrinhos, enquanto a faixa intermediária de resgate ativo expande a conversão para ~4.100 carrinhos, preenchendo a lacuna entre o abandono puro e a conversão final.

---

## 📊 Métricas & Variáveis no Gráfico

[1] **Linha Superior (Teto / Total de Carrinhos)**:
- **Métrica**: Volume Acumulado de *Carrinhos Criados*.
- **Representação Visual**: Curva suave vermelha/rose (`#E11D48`) iniciando em (0,0) e subindo continuamente até o topo (7.500 unidades).

[2] **Linha Intermediária (Carrinhos Recuperados & Reengajados)**:
- **Métrica**: Volume Acumulado de *Compras Diretas + Carrinhos Resgatados*.
- **Representação Visual**: Curva suave verde esmeralda (`#059669`) no meio (~4.100 unidades), criando uma faixa generosa e claramente visível.

[3] **Linha Inferior (Volume de Conversão Direta Orgânica)**:
- **Métrica**: Volume Acumulado de *Carrinhos Comprados Diretamente*.
- **Representação Visual**: Curva suave azul royal (`#2563EB`) na base (2.229 unidades).

---

## 🎨 Diretrizes Visuais de Design

[1] **Fundo & Grid**:
- Fundo branco puro (`#FFFFFF`) para alto contraste e clareza de leitura executiva.
- Grid sutil e elegante em cinza claro (`#CBD5E1`) com linhas tracejadas.

[2] **Zonas de Cores com Preenchimento (`fill_between`)**:
- **Zona Superior (Abandono Puro / Atrito)**: Preenchimento translúcido entre o Total e a Linha de Resgate em tom rose suave (`#FEE2E2`, alpha 0.60).
- **Zona Intermediária (Recuperação & Reengajamento Dadosfera)**: Preenchimento destacado entre a Linha de Resgate e a Linha de Comprados em tom verde esmeralda suave (`#D1FAE5`, alpha 0.85).
- **Zona Inferior (Conversão Direta Orgânica)**: Preenchimento translúcido entre a Linha de Comprados e o eixo zero em tom azul suave (`#DBEAFE`, alpha 0.60).

[3] **Curvatura das Linhas & Vértices**:
- Interpolação matemática spline cúbica (`scipy.interpolate.make_interp_spline`) com 350 pontos contínuos para gerar curvatura orgânica e transições fluidas.
- Marcadores pontuais circulares (`o`) destacados em cada vértice semanal para marcar os dados reais auditáveis.

---

## 📍 Mapeamento dos Dados Parquet
- **Entidades Utilizadas**:
  - `data/mock/output/parquet/carrinhos.parquet` (`status`, `data_criacao`, `carrinho_id`)
  - `data/mock/output/parquet/eventos_resgate.parquet` (`sucesso`, `data_conversao`)
- **Granularidade**: Semanal contínua acumulada (Semanas de Jan/2026 a Jun/2026).
- **Escala Y**: Escala acumulada completa (0 a 7.500 unidades) com span balanceado entre as 3 curvas.

---

## 🖼️ Artefatos Visuais Gerados

### 1. Visão Canônica Acumulada (Macro Semestre)
- **Script**: [`generate_chart.py`](generate_chart.py)
- **Imagem**: [`chart_bi_recuperacao_carrinhos.png`](chart_bi_recuperacao_carrinhos.png)
- **Características**: Curva acumulada iniciando em (0,0) até 7.500 unidades, linha basal de comprados (2.229 un) e linha intermediária de resgate & reengajamento (~4.100 un) com span balanceado e zonas amplas.

### 2. Visão Sinuosa com Janela Curta (Recorte de 1 Semana)
- **Script**: [`generate_chart_sinuous_1week.py`](generate_chart_sinuous_1week.py)
- **Imagem**: [`chart_bi_recuperacao_carrinhos_sinuous_1week.png`](chart_bi_recuperacao_carrinhos_sinuous_1week.png)
- **Características**: Recorte temporal diário de 7 dias (09/Fev a 15/Fev/2026), linhas com curvatura sinuosa hiper-suave, vértices auditáveis com valores anotados e visualização da dinâmica diária de conversão direta vs atrito de abandono.

