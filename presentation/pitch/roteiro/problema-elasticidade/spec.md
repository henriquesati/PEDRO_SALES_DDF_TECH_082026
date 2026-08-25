# Especificação Visual & Técnica: Imagem `chart_problema_elasticidade.png`

> **Diretório**: `presentation/pitch/roteiro/problema-elasticidade/`  
> **Artefato Principal**: [`chart_problema_elasticidade.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/problema-elasticidade/chart_problema_elasticidade.png)  
> **Script Gerador**: [`generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/problema-elasticidade/generate_chart.py)  
> **Padrão Gráfico**: Fundo Branco Puro (`#FFFFFF`), 16:9 Widescreen (3600x2025 px), 300 DPI, Sem Título/Subtítulo (Espaço 100% livre para títulos e textos no PowerPoint).

---

## 📐 1. Estrutura e Composição da Imagem

```
+---------------------------------------------------------------------------------------------------+
|  [ESPAÇO SUPERIOR LIVRE PARA TÍTULO / BULLETS NO POWERPOINT]                                      |
+---------------------------------------------------------------------------------------------------+
|  [CARD 1]                             [CARD 2]                             [CARD 3]               |
|  Vendas Perdidas por Minuto            Tempo de Parada do Checkout          Faturamento Total     |
|  R$ 50k a 100k                         5 a 15 min                           R$ 250k a 1,5M        |
|  Faturamento Checkout Mercado Livre    Reconfiguração Cache Redis           Vendas Não Concluídas |
+---------------------------------------------------------------------------------------------------+
|  [GRÁFICO PRINCIPAL EXPANDIDO]                                                                    |
|  Projeção de Faturamento Perdido em Vendas por Minutos de Indisponibilidade no Checkout           |
|  - Faixa Sombreada: R$ 50k a R$ 100k por minuto em vendas perdidas                                |
|  - Marco 5 min: -R$ 500k em vendas                                                                |
|  - Marco 10 min: -R$ 1,0 Milhão em vendas                                                         |
|  - Marco 15 min: -R$ 1,5 Milhão em vendas                                                         |
+---------------------------------------------------------------------------------------------------+
|  [RODAPÉ] Fonte: Relatório Anual Mercado Livre 2025 | GMV = Volume Bruto Total de Vendas           |
+---------------------------------------------------------------------------------------------------+
```

---

## 📊 2. Especificação dos Dados Contidos na Imagem

| Elemento Visual | Valor Representado | Cor Semântica | Significado no Negócio |
|---|:---:|:---:|---|
| **Card 1: Vendas Perdidas/min** | `R$ 50.000 a 100.000` | `#EF4444` (Coral/Alerta) | Faturamento bruto por minuto que deixa de ser faturado no checkout. |
| **Card 2: Tempo de Parada** | `5 a 15 minutos` | `#F59E0B` (Âmbar/Atenção) | Janela típica de failover e upgrade de clusters de cache (Redis). |
| **Card 3: Faturamento Total Perdido** | `R$ 250k a 1.500.000` | `#991B1B` (Vermelho Escuro) | Receita total de vendas perdidas durante o evento de pico. |
| **Curva de Decaimento** | `y = 50x a 100x` | `#EF4444` com `alpha=0.18` | Projeção linear do faturamento de vendas perdido minuto a minuto. |
| **Marcos Notáveis** | `5m (-500k), 10m (-1M), 15m (-1.5M)` | `#991B1B` com setas | Volume financeiro de vendas não concluídas em 5, 10 e 15 minutos. |

---

## 🖥️ 3. Diretrizes de Inserção no PowerPoint

1. **Inserção**: Copiar `chart_problema_elasticidade.png` e colar diretamente no slide do PowerPoint.
2. **Customização Total**: O topo da imagem possui espaçamento livre para você adicionar a caixa de título e os bullets textuais da narrativa diretamente no PowerPoint.
3. **Formatação**: Formato 16:9 nativo com fundo branco puro (`#FFFFFF`).
