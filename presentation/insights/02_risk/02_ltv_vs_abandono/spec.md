# Especificação Visual: LTV vs Abandono de Carrinho & Sensibilidade Financeira

> [!IMPORTANT]
> **REFERÊNCIA CANÔNICA DE BASELINE E VALORES DE NEGÓCIO**:  
> Esta especificação vincula-se diretamente ao insight canônico em [`insights/02_risk/ltv_vs_abandono.md`](../../../insights/02_risk/ltv_vs_abandono.md) e às premissas monetárias de [`presentation/pitch/pitch_spec.md`](../../pitch/pitch_spec.md) (Seções 4 e 5).

---

## 🎯 Objetivo da Visualização

Demonstrar visualmente como o valor histórico do cliente (**Lifetime Value - LTV**) e o **Ticket Médio da Cesta** determinam o orçamento economicamente viável e o canal de resgate ótimo.

O painel evidencia a assimetria de valor entre os segmentos de clientes (**Premium**, **Regular**, **Novo** e **Dormant**), provando que alocar canais de custo unitário mais alto (WhatsApp a R$ 0,30) para clientes de alto valor é altamente rentável (ROI > 400x), enquanto clientes Novos e Dormants exigem canais de custo ultra baixo (Email a R$ 0,05 e Push a R$ 0,02) para preservar a margem operacional.

---

## 📐 Estrutura do Painel (Painel Duplo Integrado)

- **Resolução & Exportação**: `15.0 x 7.0 polegadas`, 300 DPI, fundo `#FFFFFF`, bordas em Slate (`#CBD5E1`).
- **Painel 1 (Gráfico de Bolhas - LTV, Abandono & Ticket)**:
  - **Eixo X**: Taxa de Abandono por Segmento (`%`).
  - **Eixo Y**: Ticket Médio da Cesta Abandonada (`R$`).
  - **Tamanho da Bolha**: Proporcional ao **Valor Total Represado em Risco (`R$`)**.
  - **Segmentos Mapeados**:
    - 🔵 **Premium** (Alto LTV, Baixo Abandono, Alto Retorno Unitário).
    - 🟢 **Regular** (Maior Volume Unitário, Equilíbrio de Margem).
    - 🟡 **Novo** (LTV Inicial Zero, Abandono Elevado, Foco em CAC).
    - 🟣 **Dormant** (Inativos, Margem Sensível, Automação Leve).
- **Painel 2 (Matriz de Decisão Econômica & Canais Ótimos)**:
  - Tabela operacional detalhando LTV Médio, Canal Recomendado, Custo por Disparo, Limite de Desconto Prescrito e Expected ROI por Real Investido.

---

## 🎨 Paleta Semântica & Tipografia

- **Fontes**: `Segoe UI`, `DejaVu Sans`, `Helvetica`, `Arial`, `sans-serif`.
- **Cores por Segmento**:
  - `Premium`: `#059669` (Verde Esmeralda / Rentabilidade Máxima).
  - `Regular`: `#2563EB` (Azul Royal / Volume e Escala).
  - `Novo`: `#F59E0B` (Âmbar / Aquisição & CAC).
  - `Dormant`: `#8B5CF6` (Roxo / Reativação).

---

## 📂 Fontes de Dados (Ground Truth)

- `data/mock/output_cleaned/parquet/carrinhos.parquet`
- `data/mock/output_cleaned/parquet/clientes.parquet`
- `data/mock/output_cleaned/parquet/eventos_resgate.parquet`
