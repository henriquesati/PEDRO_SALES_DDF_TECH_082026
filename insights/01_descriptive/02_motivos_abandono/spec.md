# Especificação Visual & BI: Motivos de Abandono de Carrinho

> **Referência Canônica Master**: [`presentation/pitch/pitch_spec.md`](../../../pitch/pitch_spec.md) (Seções 4 e 5)  
> **Base de Dados Unificada**: `data/mock/output_cleaned/parquet/*.parquet` (Ground Truth)

## 📌 Contexto & Pergunta de Negócio
- **Pergunta Central**: Qual razão de abandono causa a maior perda de volume e receita na plataforma e como esses motivos se distribuem entre diferentes causas-raiz e dispositivos?
- **Insight de Negócio**: A análise descritiva dos 5.231 carrinhos abandonados revela que **Preço Alto (1.307 un / 25,0%)** e **Frete Caro (1.207 un / 23,1%)** são as duas principais causas-raiz de atrito no marketplace, somando mais de 48% de todo o volume abandonado. **Indecisão (1.045 un / 20,0%)** e **Problemas no Pagamento (961 un / 18,4%)** concentram-se principalmente em dispositivos móveis.

> [!NOTE]
> **Foco do Projeto em Proporções (%) & Referência Pitch Spec**: O núcleo desta análise é estruturado em proporções e volumes de atrito (DEC-001). O Treemap principal é 100% focado em contagem e participação percentual (%) sem poluição financeira, permitindo ao cliente adequar seu próprio Ticket Médio. A perda financeira em R$ é gerada em gráfico separado como baseline da *Entidade Exemplo* declarada em [`presentation/pitch/pitch_spec.md`](../../../pitch/pitch_spec.md#42-entidade-exemplo-de-negócio-baseline-mock-para-simulações-monetárias) (TM Global = R$ 375,00).

---

## 📊 Métricas & Fórmulas (Ground Truth)

- **Distribuição Percentual por Motivo (%)**: $\frac{\text{Carrinhos com Motivo } M}{\text{Total de Carrinhos Abandonados (5.231)}} \times 100$.
- **Volume de Carrinhos por Causa-Raiz (unidades)**: Contagem exata de carrinhos com status de abandono agrupados por motivo.
- **Receita Represada por Motivo (R$ - Gráfico Separado)**: Soma de `valor_total` dos carrinhos abandonados por `motivo_abandono`.
- **Ticket Médio por Motivo (R$ - Gráfico Separado)**: $\frac{\text{Receita Represada do Motivo } M}{\text{Volume de Carrinhos do Motivo } M}$.

---

## 🎨 Diretrizes Visuais de Design (Artefatos Separados)

### Artefato 1: Treemap Hierárquico de Blocos Proporcionais ao Volume
- **Arquivo**: [`chart_02_treemap_motivos_abandono.png`](chart_02_treemap_motivos_abandono.png) (salvo também como [`chart_02_motivos_abandono.png`](chart_02_motivos_abandono.png))
- **Tipo de Gráfico**: **Treemap Hierárquico Proporcional (Áreas Proporcionais)**
- **Áreas dos Blocos**:
  - `Preço Alto`: 25,0% (1.307 carrinhos abandonados por preços elevados)
  - `Frete Caro`: 23,1% (1.207 carrinhos abandonados por frete muito caro)
  - `Indecisão / Dúvida`: 20,0% (1.045 carrinhos abandonados por indecisão ou dúvida)
  - `Erro no Pagamento`: 18,4% (961 carrinhos abandonados por falhas no pagamento)
  - `Não Informado`: 9,3% (487 carrinhos abandonados sem motivo declarado)
  - `Estoque Indisponível`: 4,3% (224 carrinhos abandonados por falta de estoque)
- **Estrutura de Rótulos**: Título do motivo + `% do abandono` + `X carrinhos abandonados por [motivo]`. Sem poluição de cifras monetárias.

### Artefato 2: Gráfico Separado de Impacto Financeiro por Faixa de Ticket (Lado a Lado)
- **Arquivo**: [`chart_02_perda_financeira_motivos.png`](chart_02_perda_financeira_motivos.png)
- **Tipo de Gráfico**: **Painel Duplo Executivo (Lado a Lado)**
- **Painel 1 (Perda Bruta por Faixa de Ticket - Unicolor Rose `#E11D48`)**:
  - `Ticket Alto (> R$ 500)`: R$ 1.017,1k (52,3% da perda | 1.388 carrinhos)
  - `Ticket Médio-Alto (R$ 250–500)`: R$ 606,5k (31,2% da perda | 1.676 carrinhos)
  - `Ticket Médio-Baixo (R$ 100–250)`: R$ 283,2k (14,6% da perda | 1.606 carrinhos)
  - `Ticket Baixo (< R$ 100)`: R$ 38,2k (2,0% da perda | 561 carrinhos)
- **Painel 2 (Impacto do Resgate Dadosfera - Verde Esmeralda `#059669` vs Residual `#E11D48`)**:
  - `Ticket Alto`: Resgate de **+R$ 82,8k** (8,1% / 116 pedidos convertidos) | Residual R$ 934,2k
  - `Ticket Médio-Alto`: Resgate de **+R$ 57,2k** (9,4% / 158 pedidos convertidos) | Residual R$ 549,4k
  - `Ticket Médio-Baixo`: Resgate de **+R$ 29,5k** (10,4% / 167 pedidos convertidos) | Residual R$ 253,7k
  - `Ticket Baixo`: Resgate de **+R$ 4,2k** (11,1% / 57 pedidos convertidos) | Residual R$ 34,0k
  - **Total Resgatado**: **+R$ 173,7k** (498 pedidos convertidos) de um total de R$ 1.945,0k represados.

---

## 📍 Mapeamento dos Dados Parquet
- **Entidades Utilizadas**:
  - `data/mock/output_cleaned/parquet/carrinhos.parquet` (`motivo_abandono`, `valor_total`, `status`, `carrinho_id`)
  - `data/mock/output_cleaned/parquet/clientes.parquet` (`cliente_id`)
- **Filtro de Escopo**: `status IN ('abandonado', 'recuperado', 'expirado')` com `motivo_abandono IS NOT NULL`.

---

## 🖼️ Artefatos Visuais Gerados
- **Treemap de Volume por Causa-Raiz**: [`chart_02_treemap_motivos_abandono.png`](chart_02_treemap_motivos_abandono.png)
- **Perda Financeira Represada (Separado)**: [`chart_02_perda_financeira_motivos.png`](chart_02_perda_financeira_motivos.png)
- **Script Gerador**: [`generate_chart.py`](generate_chart.py)
