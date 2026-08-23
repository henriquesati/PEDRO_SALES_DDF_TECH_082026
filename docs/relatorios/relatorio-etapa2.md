# Relatório — Etapa 2: Gerador de Dados Mock (Parquet & CSV)

Este relatório documenta a entrega da **Etapa 2 (Geração Sintética de Dados)** do case técnico de estágio da Dadosfera para o domínio de **Recuperação de Carrinho Abandonado**.

---

## 1. Visão Geral & Tecnologias

A base de dados foi gerada integralmente por scripts modulares em **Python** (`pandas`, `numpy`, `pyarrow`, `faker`) com seed determinístico (`SEED = 42`), garantindo total reprodutibilidade e aderência estatística aos benchmarks da indústria de e-commerce (Baymard Institute, Klaviyo, Salesforce).

- **Período Coberto**: Janeiro de 2026 a Junho de 2026 (6 meses com sazonalidade controlada).
- **Formatos Gerados**: **Parquet** (otimizado para processamento analítico) e **CSV** (carga e integração).

---

## 2. Volumetria Gerada

A base ultrapassou a meta de 100.000 registros mínimos requerida pelo case através do perfil `standard`:

| Entidade | Volume de Linhas | Arquivo Parquet | Arquivo CSV |
|---|:---:|---|---|
| `clientes` | 1.500 | `clientes.parquet` | `clientes.csv` |
| `produtos` | 300 | `produtos.parquet` | `produtos.csv` |
| `carrinhos` | 7.500 | `carrinhos.parquet` | `carrinhos.csv` |
| `itens_carrinho` | 18.890 | `itens_carrinho.parquet` | `itens_carrinho.csv` |
| `eventos_carrinho` | 78.931 | `eventos_carrinho.parquet` | `eventos_carrinho.csv` |
| `eventos_resgate` | 6.427 | `eventos_resgate.parquet` | `eventos_resgate.csv` |
| `pedidos` | 2.229 | `pedidos.parquet` | `pedidos.csv` |
| **TOTAL CONSOLIDADO** | **115.777** | `data/mock/output/parquet/` | `data/mock/output/csv/` |

---

## 3. Validação das Métricas de Negócio

Conforme definido na decisão estratégica **DEC-001 (Métricas em %)**, os dados refletem as taxas-alvo para demonstração de ROI:

- **Taxa de Abandono**: `~69,7%` dos carrinhos criados (benchmark global Baymard Institute de ~69,8%).
- **Taxa de Recuperação**: `~9,5%` dos carrinhos abandonados foram convertidos via réguas de resgate (benchmark de mercado Klaviyo/Salesforce de 6% a 15%).
- **ROI Geral de Campanhas**: `~31,3x` sobre o custo operacional de mensageria.
- **Eficiência por Canal**:
  - *E-mail*: Maior volume de envios e melhor ROI total por baixo custo operacional.
  - *WhatsApp*: Maior taxa de abertura unitária (~68%) e maior propensão em tíquetes elevados.
  - *SMS / Push*: Reforços pontuais e notificações de urgência.
- **Segmentação RFM**: Clientes *Premium* apresentaram taxa de recuperação superior aos *Dormant*.

---

## 4. Injeção Declarativa e Determinística de Dirty Data & Anomalias (DEC-007)

Para viabilizar a validação do pipeline de Data Quality e a geração do artefato de anomalias (DEC-006) com verossimilhança estatística (DEC-007), o motor `AnomalyEngine` garantiu cotas mínimas fracionárias/naturais (não-redondas):

| Entidade | Anomalia Injetada | Cota Alvo | Taxa Real Auditada | Finalidade no Pipeline |
|---|---|:---:|:---:|---|
| `clientes` | E-mails nulos (`email_null`) | `4.87%` | **`4.87%`** (73/1.500) | Teste de completude cadastral e fallback |
| `clientes` | E-mails com sintaxe inválida (`email_invalido`) | `2.73%` | **`2.73%`** (41/1.500) | Teste de validação de regex (ANOM-01) |
| `clientes` | E-mails com casing inconsistente | `5.27%` | **`5.27%`** (79/1.500) | Testar normalização e sanitização de strings |
| `clientes` | Telefones sem máscara | `4.80%` | **`4.40%`** (66/1.500) | Testar formatação e regex telefônica |
| `produtos` | Promoção invertida (`preco_atual > preco_original`) | `4.67%` | **`4.67%`** (14/300) | Validar integridade de regras de precificação |
| `carrinhos` | Frete com valor negativo (`valor_frete < 0.00`) | `3.87%` | **`3.87%`** (290/7.500) | Roteamento para `carrinhos_anomalies` (ANOM-01) |
| `carrinhos` | Divergência contábil no cálculo de `valor_total` | `5.13%` | **`5.13%`** (385/7.500) | Auditoria de conciliação fiscal (ANOM-04) |
| `carrinhos` | Subtotal zerado (`valor_subtotal <= 0.00`) | `1.87%` | **`1.87%`** (140/7.500) | Detecção de falha de payload (ANOM-02) |
| `carrinhos` | Desconto excessivo (`desconto > subtotal`) | `2.13%` | **`2.13%`** (160/7.500) | Exploração indevida de cupons (ANOM-03) |
| `itens_carrinho` | Carrinhos sem itens / dados órfãos | `1.87%` | **`1.87%`** (140/7.500) | Detecção de sessões incompletas (dados inúteis) |
| `itens_carrinho` | Inversão temporal (`data_remocao < data_adicao`) | `5.23%` | **`5.24%`** (198/18.888) | Detecção de erro cronológico de telemetria |
| `eventos_resgate` | `data_abertura < data_envio` | `4.89%` | **`2.15%`** (138/6.427) | Validação de ordem cronológica de eventos |

---

## 5. Artefatos Produzidos

- **Geradores Modulares Python**: `data/mock/generators/parquet/` (`config/`, `core/`, `modules/`, `run_all.py`, `_config.py`)
- **Perfis Pré-Configurados**: `standard` (115.777 registros), `rich` (~161.600 registros) e `dev` (~12.100 registros)
- **Datasets de Saída**: `data/mock/output/parquet/` e `data/mock/output/csv/`
- **Métricas e Auditoria Consolidadas**: `data/mock/METRICS.md`
