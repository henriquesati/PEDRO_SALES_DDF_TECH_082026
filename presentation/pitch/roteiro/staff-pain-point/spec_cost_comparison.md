# Especificação Técnica & Visual: Gráficos Conceituais de Custo (Infra Própria vs. Dadosfera)

> **Diretório**: `presentation/pitch/roteiro/staff-pain-point/`  
> **Artefatos Principais**:
> 1. [`chart_custo_infra_vs_dadosfera_stacked.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/staff-pain-point/chart_custo_infra_vs_dadosfera_stacked.png) (2 Gráficos Conceituais Empilhados Verticalmente)
> 2. [`chart_custo_infra_vs_dadosfera_crossover.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/staff-pain-point/chart_custo_infra_vs_dadosfera_crossover.png) (Gráfico Único com Curvas se Cruzando / Divergência de Custo)  
> **Script Gerador**: [`generate_cost_comparison_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/staff-pain-point/generate_cost_comparison_chart.py)  
> **Padrão Visual**: Fundo Branco Puro (`#FFFFFF`), Proporção 16:9 Widescreen (3600x2025 px), 300 DPI, Sem Eixos Numéricos Rígidos (Design Minimalista com Espaço Livre para Títulos e Textos no PowerPoint).

---

## 🎨 1. Identificação Direta das Linhas & Eixos Conceituais

* **Eixo Y (Vertical)**: **`Custo Total de Operação & Sustentação (TCO)`** *(Provisionamento, Headcount, Apps, Dados)*.
* **Eixo X (Horizontal)**: **`Tempo / Volume de Dados & Expansão de Casos de Uso ->`**.
* 🔴 **Linha Vermelha Coral (`#DC2626`)**: **`Custo Infraestrutura Própria (AWS DIY)`**
  * **Comportamento**: Começa baixa no início, mas sofre uma **subida exponencial / acelerada** com o aumento de complexidade em: *Provisionamento, Headcount, Apps, Dados*.
* 🟢 **Linha Verde Esmeralda (`#059669`)**: **`Custo com Dadosfera`**
  * **Comportamento**: Começa em patamar previsível e mantém uma **subida suave e estável**, demonstrando a previsibilidade e elasticidade como *Plataforma Unificada SaaS*.
* ⚪ **Ponto de Cruzamento / Break-even**: **`Ponto de Inflexão (Break-even)`**
  * Marca visualmente o momento em que a infraestrutura própria se torna muito mais cara e complexa do que a Dadosfera.

---

## 📐 2. Estrutura dos 2 Gráficos Gerados

### Opção A: Gráficos Empilhados Verticalmente (`chart_custo_infra_vs_dadosfera_stacked.png`)

```
+---------------------------------------------------------------------------------------------------+
|  [CARD SUPERIOR - ESPAÇO LIVRE PARA ANOTAÇÃO: CUSTO COM INFRA PRÓPRIA AWS DIY]                   |
|                                                                                                   |
|           . - ~ ~ ~                                                        /                      |
|         /           Curva Exponencial (Subida Acentuada)                  /  ▲ (Alta Aceleração)  |
|       /                                                                  /                        |
|  ----+------------------------------------------------------------------+------------------------ |
+---------------------------------------------------------------------------------------------------+
|  [CARD INFERIOR - ESPAÇO LIVRE PARA ANOTAÇÃO: CUSTO PLATAFORMA DADOSFERA]                         |
|                                                                                                   |
|                                                      Curva Linear       /   ▲ (Subida Suave)      |
|  ----------------------------------------------------------------------/------------------------- |
+---------------------------------------------------------------------------------------------------+
```

---

### Opção B: Gráfico Único de Cruzamento / Crossover (`chart_custo_infra_vs_dadosfera_crossover.png`)

```
+---------------------------------------------------------------------------------------------------+
|  [ESPAÇO SUPERIOR LIVRE PARA TÍTULO / BULLETS NO SLIDE DO POWERPOINT]                             |
|                                                                                                   |
|                                                       [🔴 Custo Infra Própria AWS DIY]            |
|                                                                         /  ▲ (Escalada de Custos) |
|                                                                        /                          |
|                                              ● (PONTO DE CRUZAMENTO)  /                           |
|                                                \                     /                            |
|             [🟢 Custo Dadosfera] ----------------\------------------/-------> ▲ (Custo Estável)   |
|                                                    \               /                              |
|  ------------------------------------------------------------------------------------------------ |
+---------------------------------------------------------------------------------------------------+
```

---

## 🖥️ 3. Como Utilizar no PowerPoint

1. **Inserção Direta**:
   * Copie o arquivo [`chart_custo_infra_vs_dadosfera_stacked.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/staff-pain-point/chart_custo_infra_vs_dadosfera_stacked.png) ou [`chart_custo_infra_vs_dadosfera_crossover.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/staff-pain-point/chart_custo_infra_vs_dadosfera_crossover.png) e cole no slide desejado.
2. **Textos Personalizados**:
   * O topo e os interiores dos cards foram intencionalmente deixados limpos e sem rótulos de eixos para que você possa inserir caixas de texto com a sua tipografia preferida no PowerPoint (ex: *"Custo com Infra Própria (AWS DIY)"* e *"Custo Previsível (Plataforma Dadosfera)"*).
3. **Animação**:
   * No PowerPoint, você pode adicionar a animação de entrada nas caixas de texto sincronizando a sua fala com a curva do gráfico.
