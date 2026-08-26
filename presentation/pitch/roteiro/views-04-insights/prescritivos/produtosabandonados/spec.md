# Especificação Visual & Técnica: Produtos e Categorias Mais Abandonados (`produtosabandonados`)

> **Momento do Roteiro**: **Ato 3 / Seção [4.2] — Tomada de Decisão: Atrito por Catálogo & Intervenções Prescritivas de UX**  
> **Caminho da View**: `presentation/pitch/roteiro/views-04-insights/prescritivos/produtosabandonados/`  
> **Artefato Principal**: [`chart_03_produtos_mais_abandonados.png`](chart_03_produtos_mais_abandonados.png) (300 DPI, 16:9 Widescreen)  
> **Script Gerador**: [`generate_chart.py`](generate_chart.py)  
> **Script Raiz Canônico**: [`presentation/insights/03_prescriptive/03_produtos_mais_abandonados/generate_chart.py`](../../../../../insights/03_prescriptive/03_produtos_mais_abandonados/generate_chart.py)  
> **Padrão Visual**: Fundo Branco Puro (`#FFFFFF`), Tipografia Sem Serifa Moderna, Paleta Semântica Executiva (`charts-maker` standard).  
> **Base de Dados**: `data/mock/output_cleaned/parquet/itens_carrinho.parquet`, `produtos.parquet`, `carrinhos.parquet` (Ground Truth 100% Auditável).

---

## 🎯 1. Objetivo & Mensagem Estratégica no Pitch

Demonstrar que **o abandono de carrinho não possui uma causa única e homogênea no catálogo**:
1. **Em vez de réguas genéricas de resgate com o mesmo e-mail e desconto fixo**, a Dadosfera permite segmentar a abordagem prescritiva conforme a barreira psicológica e operacional de cada categoria de produto.
2. **Eletrônicos & Casa & Decoração concentram 78,8% (R$ 7,34M) de toda a receita represada**, exigindo tratamento VIP focado em segurança, parcelamento e garantia estendida (sem queimar margem bruta com cupons desnecessários).
3. **Categorias de Menor Ticket (Moda, Esportes, Beleza, Livros)** sofrem com barreiras de caimento (tamanho) ou frete desproporcional, onde intervenções de baixo custo ("1ª Troca Grátis", "Barra de Frete Grátis Progressiva") destravam de **+14% a +35% de lift de conversão**.

---

## 📊 2. Arquitetura do Dashboard Executivo (16:9 Widescreen)

O painel visual [`chart_03_produtos_mais_abandonados.png`](chart_03_produtos_mais_abandonados.png) está estruturado em **3 seções estratégicas**:

### 2.1 Top 4 KPI Cards
* **1. Concentração no Top 2**: `R$ 7,34M (78,8%)` — Eletrônicos e Decoração lideram o valor represado.
* **2. Disparidade de Ticket**: `R$ 2.109 vs R$ 74` — Hesitação Financeira (Tech) vs. Frete Relativo (Livros).
* **3. Top 5 SKUs Críticos**: `R$ 872,8k Represados` — Sony Headset, Tab SPrime, IdeaPad, MacBook, iPhone Classic.
* **4. Lift Prescritivo**: `+18% a +35% Conversão` — Campanhas customizadas pela dor de cada categoria.

### 2.2 Subplot 1A — Matriz de Posicionamento de Catálogo (Scatter Quadrants)
* **Eixo X**: Volume de Itens Abandonados (unidades de demanda represada).
* **Eixo Y (Escala Logarítmica)**: Ticket Médio do Item (`R$ 50` a `R$ 2.500`).
* **Tamanho da Bolha**: Proporcional à Receita Represada em Risco (`R$`).
* **Quadrantes de Decisão**:
  * **Q1 (Alto Impacto / Risco Financeiro)**: Eletrônicos (WhatsApp VIP + Garantia Estendida + 12x Sem Juros).
  * **Q2 (Frete Volumoso / Medidas)**: Casa & Decoração (Simulador 3D + Subsídio de Frete > R$ 150).
  * **Q3 (Hesitação de Caimento / Tamanho)**: Moda & Vestuário (1ª Troca Grátis + Provador Virtual).
  * **Q4 (Frete Desproporcional)**: Beleza, Brinquedos & Livros (Barra de Frete Grátis + Cross-Sell).

### 2.3 Subplot 1B — Ranking Top 5 SKUs Críticos (Eletrônicos)
* Exibe os 5 produtos com maior perda acumulada:
  1. `Sony Headset Neo`: R$ 233,2k (35 abandonos • Ticket R$ 4.751).
  2. `Samsung Tab SPrime`: R$ 170,7k (34 abandonos • Ticket R$ 3.788).
  3. `LG IdeaPad Sport`: R$ 163,0k (27 abandonos • Ticket R$ 4.393).
  4. `Apple MacBook Max`: R$ 154,1k (27 abandonos • Ticket R$ 4.525).
  5. `Samsung iPhone Classic`: R$ 151,8k (24 abandonos • Ticket R$ 4.458).

### 2.4 Subplot 2 — Matriz Prescritiva de Intervenções (Executive Action Cards)
5 Cards de Ação Visual estruturados com identificação da categoria, ticket médio, canal de acionamento Dadosfera, barreira crítica de conversão, ação prescritiva recomendada e impacto estimado de conversão.

---

## 🎙️ 3. Roteiro de Fala Sugerido para o Apresentador

> *"Se olharmos para o catálogo do e-commerce através da Dadosfera, vemos que enviar um e-mail com cupom genérico de 10% é o pior erro de uma operação.*  
> 
> *Eletrônicos representam quase 60% de todo o faturamento abandonado. O cliente que deixa um notebook ou headset de R$ 4.000 no carrinho não está esperando R$ 50 de desconto — ele está inseguro quanto à garantia e condições de parcelamento. Ao acioná-lo via WhatsApp VIP oferecendo garantia estendida e 12x sem juros, convertemos 22% sem queimar margem.*  
> 
> *Já em Moda e Decoração, o atrito é caimento e frete volumoso. Com '1ª Troca Grátis' e simulador 3D no e-mail, destravamos até +35% de conversão com custo real operacional mínimo.*  
> 
> *Essa granularidade analítica e prescritiva só é viável porque a Dadosfera unifica dados de catálogo, navegação e sessões em tempo real."*

---

## 📂 4. Artefatos do Módulo

| Arquivo | Descrição |
| :--- | :--- |
| [`chart_03_produtos_mais_abandonados.png`](chart_03_produtos_mais_abandonados.png) | Painel visual executivo renderizado em alta resolução (300 DPI, 16:9). |
| [`generate_chart.py`](generate_chart.py) | Script declarativo e funcional em Python para reprodução local. |
| [`spec.md`](spec.md) | Especificação técnica e guia de narrativa para o apresentador. |
