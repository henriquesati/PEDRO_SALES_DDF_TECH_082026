# Métricas-Alvo — Case Recuperação de Carrinho Abandonado

> **Propósito**: Documento de referência com as métricas-alvo usadas para gerar os dados mock.
> Todas as métricas são expressas em **taxas, ratios e eficiência** — agnósticas ao ticket médio do cliente.
> Valores monetários existem nos dados como contexto, mas **não são o argumento central do pitch**.

---

## Premissas de Geração

| Parâmetro | Valor |
|---|---|
| Período | Janeiro–Junho 2026 (6 meses) |
| Total de clientes | ~1.200 |
| Total de produtos | ~250 (7 categorias) |
| Total de carrinhos | ~6.000 |
| Total de registros | ~101.000 |
| Taxa de dirty data | 5-10% |
| Seed | 42 (reprodutível) |

---

## Camada 1 — Conversão & Recuperação

> **Pergunta central**: _"Qual o impacto de uma estratégia de recuperação de carrinho?"_

| Métrica | Target | Benchmark |
|---|---|---|
| Taxa de abandono | ~70% | Baymard Institute: 69.8% global |
| **Taxa de recuperação geral** | **~10% dos abandonados** | Klaviyo/Salesforce: 5-15% |
| Taxa de conversão direta (sem resgate) | ~20% | Baseline sem intervenção |
| Lift de conversão com resgate vs sem | **+50%** | Campanhas vs controle |

---

## Camada 2 — Eficiência por Canal

> **Pergunta central**: _"Qual canal entrega melhor resultado?"_

| Canal | Envio→Abertura | Abertura→Clique | Clique→Conversão | Conversão End-to-End |
|---|---|---|---|---|
| Email | ~42% | ~28% | ~15% | ~4.5% |
| WhatsApp | ~68% | ~35% | ~18% | ~2.5% |
| SMS | ~55% | ~22% | ~14% | ~1.8% |
| Push | ~30% | ~18% | ~12% | ~1.2% |

**Leitura**: Email tem maior volume e ROI por custo baixo. WhatsApp tem melhor engajamento unitário mas custo 6x maior.

---

## Camada 3 — Eficiência da Segmentação RFM

> **Pergunta central**: _"Segmentar o resgate por perfil do cliente compensa?"_

| Segmento | Taxa de Recuperação | O que demonstra |
|---|---|---|
| Premium | ~18% | Segmento mais responsivo — retenção prioritária |
| Regular | ~10% | Base sólida — volume de conversões |
| Dormant | ~6% | Menor taxa, mas cada conversão reativa o cliente |
| Novo | ~12% | Cupom de primeira compra funciona |
| **Ratio Premium/Dormant** | **3x** | Segmentar compensa: foco nos segmentos certos |

---

## Camada 4 — Eficiência Operacional

> **Pergunta central**: _"O investimento em campanhas se paga?"_

| Métrica | Target | O que demonstra |
|---|---|---|
| ROI médio por campanha | ~45x custo | R$1 investido → ~R$45 retornados |
| Custo médio por conversão | < 1% do valor | Investimento desprezível |
| % campanhas com abertura | ~55% | Mais da metade engaja |
| % campanhas com conversão | ~10% | 1 em 10 converte |
| Redução na expiração | ~-15% | Menos carrinhos perdidos |

---

## Camada 5 — Timing & Sequência

> **Pergunta central**: _"Quando e quantas vezes comunicar?"_

| Toque | % das Conversões | O que demonstra |
|---|---|---|
| 1º (lembrete_1h) | ~35% | Urgência do primeiro contato |
| 2º (lembrete_24h) | ~30% | Reforço sem desconto funciona |
| 3º (desconto_48h) | ~25% | Desconto como acelerador |
| 4º (urgencia_72h) | ~10% | Última chance — menor volume |
| **Tempo médio abandono→conversão** | **~28h** | Janela de oportunidade |

---

## Contexto Monetário (secundário)

> Os valores abaixo existem nos dados para viabilizar o cálculo de ROI, mas
> **não são apresentados como métrica de valor no pitch**.
> O argumento central é: _"Recuperamos ~10% dos carrinhos com ROI de 45x — insira seu ticket médio para projetar receita."_

| Dado | Valor no Dataset | Propósito |
|---|---|---|
| Ticket médio geral | ~R$150-200 | Cálculo de ROI no dataset |
| Custo por canal | R$0.02-0.30 | Eficiência operacional |
| Faixa de desconto | 5-15% | Desconto é marginal ao valor |

---

## Volumes Gerados

| Entidade | Volume | Arquivo |
|---|---|---|
| `clientes` | ~1.200 | `clientes.parquet` |
| `produtos` | ~250 | `produtos.parquet` |
| `carrinhos` | ~6.000 | `carrinhos.parquet` |
| `itens_carrinho` | ~18.000 | `itens_carrinho.parquet` |
| `eventos_carrinho` | ~70.000 | `eventos_carrinho.parquet` |
| `eventos_resgate` | ~4.200 | `eventos_resgate.parquet` |
| `pedidos` | ~1.800 | `pedidos.parquet` |
| **TOTAL** | **~101.450** | — |

---

## Dirty Data Injetada

| Entidade | Anomalia | Taxa |
|---|---|---|
| `clientes` | Email com casing inconsistente | ~5% |
| `clientes` | Telefone sem máscara | ~5% |
| `produtos` | `preco_atual > preco_original` | ~5% |
| `carrinhos` | Frete negativo | ~3% |
| `carrinhos` | `valor_total ≠ subtotal + frete - desconto` | ~5% |
| `itens_carrinho` | `data_remocao < data_adicao` | ~5% |
| `eventos_resgate` | `data_abertura < data_envio` | ~5% |
