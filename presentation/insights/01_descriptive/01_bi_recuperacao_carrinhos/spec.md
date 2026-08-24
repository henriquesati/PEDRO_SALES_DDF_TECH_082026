# Especificação Visual & BI: Recuperação de Carrinhos

> **Referência Canônica Master**: [`presentation/pitch/pitch_spec.md`](../../../pitch/pitch_spec.md) (Seções 4 e 5)  
> **Base de Dados Unificada**: `data/mock/output_cleaned/parquet/*.parquet` (Ground Truth)

## 📌 Contexto & Pergunta de Negócio
- **Pergunta Central**: Qual é a evolução acumulada do volume de carrinhos no marketplace ao longo do primeiro semestre, qual a proporção de conversão direta no checkout e qual a contribuição do resgate de carrinhos abandonados?
- **Insight de Negócio**: A visualização em camadas evidencia a dinâmica operacional do funil: o total atinge 7.500 carrinhos criados no semestre. A conversão direta orgânica atende **1.731 carrinhos (23,1%)**, enquanto as ações de recuperação Dadosfera resgatam **498 compras adicionais (6,64% do total / 10,60% sobre carrinhos abandonados)**, elevando o total comprado para **2.229 carrinhos (29,7%)**. Adicionalmente, há 153 carrinhos reengajados em andamento (2,04%), totalizando 651 carrinhos impactados por campanhas (8,68% / 13,85% de resgate). O atrito residual não convertido delimita 5.118 a 5.271 carrinhos (~68% a 70%).

> [!NOTE]
> **Foco do Projeto em Proporções (%) & Referência Pitch Spec**: O núcleo desta análise é baseado em taxas percentuais e dinâmicas relativas do funil (DEC-001). O cliente pode adequar o seu próprio Ticket Médio e volumetria sem alterar as proporções analíticas. Os valores monetários absolutos (R$) apresentados utilizam a *Entidade Exemplo de Baseline* declarada em [`presentation/pitch/pitch_spec.md`](../../../pitch/pitch_spec.md#42-entidade-exemplo-de-negócio-baseline-mock-para-simulações-monetárias) (Ticket Médio Global = R$ 375,00) para ilustrar simulações financeiras quando necessário.

---

## 📊 Métricas & Séries Temporais

[1] **Linha Superior (Total de Carrinhos Criados)**:
- **Métrica**: Volume de *Carrinhos Criados* (7.500 un).
- **Representação Visual**: Curva suave vermelha (`#E11D48`).

[2] **Linha Intermediária (Total Convertido: Compras Diretas + Resgate Dadosfera)**:
- **Métrica**: Volume de *Compras Diretas (1.731 un) + Carrinhos Recuperados Convertidos (498 un)* = 2.229 un (29,7%).
- **Representação Visual**: Curva tracejada verde esmeralda (`#059669`).

[3] **Linha Inferior (Conversão Direta Orgânica no Checkout)**:
- **Métrica**: Volume de *Carrinhos Comprados Diretamente sem Resgate* (1.731 un / 23,1%).
- **Representação Visual**: Curva suave azul royal (`#2563EB`).

---

## 🎨 Diretrizes Visuais de Design

[1] **Fundo & Grid**:
- Fundo branco puro (`#FFFFFF`) para alto contraste e clareza executiva.
- Grid sutil em cinza claro (`#CBD5E1`) com linhas tracejadas.

[2] **Zonas de Cores com Preenchimento Leve (`fill_between`)**:
- **Zona Superior (Atrito / Abandono Não Convertido)**: Preenchimento translúcido em tom vermelho suave (`#E11D48`, alpha 0.14).
- **Zona Intermediária (Recuperação Dadosfera)**: Preenchimento em tom verde esmeralda suave (`#059669`, alpha 0.28) delimitando o ganho de 498 compras resgatadas (+10,6% s/ abandono).
- **Zona Inferior (Conversão Direta Orgânica)**: Preenchimento em tom azul suave (`#2563EB`, alpha 0.14).

[3] **Curvatura das Linhas & Vértices**:
- Interpolação matemática spline cúbica conectando os vértices do período.
- Marcadores pontuais circulares (`o`) em cada vértice temporal.

---

## 📍 Mapeamento dos Dados Parquet
- **Entidades Utilizadas**:
  - `data/mock/output_cleaned/parquet/carrinhos.parquet` (`status`, `data_criacao`, `carrinho_id`)
  - `data/mock/output_cleaned/parquet/pedidos.parquet` (`origem_recuperacao`, `carrinho_id`, `valor_total`)
  - `data/mock/output_cleaned/parquet/eventos_resgate.parquet` (`sucesso`, `data_envio`)
- **Granularidade**: Semanal contínua acumulada (Jan a Jun/2026) e diária (09 a 15/Fev/2026).

---

## 🖼️ Pareamento de Artefatos Visuais (1 Gráfico $\leftrightarrow$ 1 Mini Card)

### Par 1: Visão Semestral Acumulada (Janeiro a Junho de 2026)
- **Janela Temporal**: Semestre completo (01/Jan/2026 a 30/Jun/2026 - 7.500 carrinhos).
- **Gráfico Principal**: [`chart_bi_recuperacao_carrinhos.png`](chart_bi_recuperacao_carrinhos.png) (Gerado por [`generate_chart.py`](generate_chart.py)).
- **Mini Card Correspondente**: [`mini_card_zonas_acumulado_reto.png`](mini_card_zonas_acumulado_reto.png) (Gerado por [`generate_mini_tables.py`](generate_mini_tables.py)).
- **Métricas Chave**: 1.731 compras diretas (23,1%), 498 recuperados convertidos (6,6% total | 10,6% s/ abandono), 153 reengajados pendentes (2,0%), total comprado de 2.229 (29,7%), atrito residual de 5.271 (70,3%).

### Par 2: Visão Semanal Diária (09 a 15 de Fevereiro de 2026)
- **Janela Temporal**: Recorte semanal de 7 dias (09/Fev a 15/Fev/2026 - 288 carrinhos).
- **Gráfico Principal**: [`chart_bi_recuperacao_carrinhos_sinuous_1week.png`](chart_bi_recuperacao_carrinhos_sinuous_1week.png) (Gerado por [`generate_chart_sinuous_1week.py`](generate_chart_sinuous_1week.py)).
- **Mini Card Correspondente**: [`mini_card_zonas_sinuoso_1semana.png`](mini_card_zonas_sinuoso_1semana.png) (Gerado por [`generate_mini_tables.py`](generate_mini_tables.py)).
- **Métricas Chave**: 61 compras diretas (21,2%), 20 recuperados convertidos (6,9% total | 8,9% s/ abandono), 5 reengajados pendentes (1,7%), total comprado de 81 (28,1%), atrito residual de 202 (70,1%).

### Artefato Consolidado para Apresentações (PowerPoint)
- **Imagem Dupla Lado a Lado**: [`mini_card_zonas_dupla.png`](mini_card_zonas_dupla.png) combinando o Mini Card Semestral e o Mini Card Semanal.


