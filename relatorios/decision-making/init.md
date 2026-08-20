# Geração de Dados Mock em Parquet — ~110k Registros
## Versão Inicial (antes da revisão de métricas)

Criar generators Python para o case de recuperação de carrinho abandonado, gerando datasets em **Parquet** com métricas realistas que demonstrem o valor da plataforma Dadosfera para o cliente.

---

## Métricas-Chave Planejadas (anotadas em `data/mock/METRICS.md`)

As métricas são derivadas dos dados gerados e demonstram valor tangível:

| Métrica | Valor Alvo | Justificativa de Mercado |
|---|---|---|
| Taxa de abandono geral | ~70% | Benchmark e-commerce BR (Baymard Institute: 69.8%) |
| Carrinhos recuperados (total) | ~10% dos abandonados | Referência Klaviyo/Salesforce: 5-15% |
| Recuperação via Email | ~4.5% dos abandonados | Canal com maior volume, menor custo |
| Recuperação via WhatsApp | ~2.5% dos abandonados | Alta conversão BR, custo intermediário |
| Recuperação via SMS | ~1.8% dos abandonados | Médio, complementar |
| Recuperação via Push | ~1.2% dos abandonados | Baixo custo, alcance limitado |
| ROI médio geral | ~45x | (receita recuperada - custos) / custos |
| **ROI email** | **~85x** | **Custo R$0.05 vs ticket médio ~R$180** |
| **ROI WhatsApp** | **~28x** | **Custo R$0.30, alta conversão** |
| Taxa de abertura email | ~42% | Benchmark: 40-50% para recovery |
| Taxa de clique email | ~12% | Benchmark: 8-15% |
| **Ticket médio recuperado** | **~R$180** | **Ligeiramente acima do geral (high-value carts)** |
| **Receita incremental (6 meses)** | **~R$120k-150k** | **Demonstra valor mensurável** |
| **Custo total de campanhas** | **~R$1.2k-1.5k** | **Investimento mínimo** |
| Premium recuperados vs Dormant | 2.5x mais | Validação da segmentação RFM |

> **Nota**: As linhas em negrito são as métricas que foram removidas ou rebaixadas na versão final, por estarem ancoradas em valores monetários absolutos.

---

## Volumes de Dados (~110k registros)

| Entidade | Volume | Arquivo Parquet |
|---|---|---|
| `clientes` | ~1.200 | `clientes.parquet` |
| `produtos` | ~250 | `produtos.parquet` |
| `carrinhos` | ~6.000 | `carrinhos.parquet` |
| `itens_carrinho` | ~18.000 | `itens_carrinho.parquet` |
| `eventos_carrinho` | ~70.000 | `eventos_carrinho.parquet` |
| `eventos_resgate` | ~4.200 | `eventos_resgate.parquet` |
| `pedidos` | ~1.800 | `pedidos.parquet` |
| **TOTAL** | **~101.450** | — |

> [!NOTE]
> Volume ajustado de ~76k (plano original) para ~101k aumentando `eventos_carrinho` (de 50k para 70k) e itens_carrinho (de 15k para 18k), aproximando-se do target de 110k. Os eventos de carrinho são o maior volume por natureza (time series com ~12 eventos/carrinho em média).

---

## Proposed Changes

### Arquivo de Métricas Anotadas

#### [NEW] `METRICS.md`
- Documento com todas as métricas-alvo no topo, premissas de geração, e resumo dos dados gerados
- Serve como referência rápida para o pitch e validação pós-geração

---

### Generators Python (`data/mock/generators/`)

Cada generator é um script Python independente que usa `faker`, `random`, `numpy` e `pandas`, exportando para **Parquet** via `pyarrow`.

#### [NEW] `_config.py`
- Constantes compartilhadas: períodos, distribuições, custos por canal, segmentos RFM
- Seeds para reprodutibilidade
- Paths de output

#### [NEW] `clientes.py`
- ~1.200 clientes com distribuição RFM: 15% premium, 40% regular, 30% dormant, 15% novo
- Dirty data: emails com casing variado (~5%), telefones sem máscara, nulos em campos opcionais

#### [NEW] `produtos.py`
- ~250 produtos em 7 categorias (Eletrônicos, Moda, Casa & Decoração, Esportes, Beleza, Livros, Brinquedos)
- Dirty data: `preco_atual > preco_original` (~5% promoção invertida)

#### [NEW] `carrinhos.py`
- ~6.000 carrinhos: 70% abandonados, 15% comprados direto, 10% recuperados→comprados, 5% expirados
- Distribuição temporal Jan-Jun 2026 com sazonalidade (picos em março/maio)
- Dirty data: frete negativo, valor_total inconsistente com itens (~7%)

#### [NEW] `itens_carrinho.py`
- ~18.000 itens (média ~3 por carrinho, range 1-8)
- Snapshot de preço no momento da adição
- Dirty data: `data_remocao < data_adicao` (~5%)

#### [NEW] `eventos_carrinho.py`
- ~70.000 eventos (média ~12 por carrinho)
- Sequência realista de ações: view → add → checkout → pagamento/abandono
- Dados JSONB contextuais por tipo de evento

#### [NEW] `eventos_resgate.py`
- ~4.200 eventos de resgate para carrinhos abandonados
- Sequência de comunicação: lembrete_1h → lembrete_24h → desconto_48h → urgencia_72h
- Taxa de conversão por canal: email 4.5%, WhatsApp 2.5%, SMS 1.8%, push 1.2%
- Dirty data: `data_abertura < data_envio` (~5%)

#### [NEW] `pedidos.py`
- ~1.800 pedidos totais (diretos + recuperados)
- `origem_recuperacao=TRUE` para pedidos gerados via campanha
- Vinculação com `resgate_id` quando aplicável

#### [NEW] `run_all.py`
- Orquestrador que executa todos os generators na ordem correta de dependência
- Garante integridade referencial entre entidades
- Loga volumes e métricas finais

---

### Output

#### [NEW] `data/mock/output/*.parquet`
- 7 arquivos Parquet gerados pelo `run_all.py`

---

## User Review Required

> [!IMPORTANT]
> **Formato de saída**: O plano gera **apenas Parquet** (não CSV/SQL como mencionado no relatório Etapa 1). Confirme se deseja também CSV ou apenas Parquet.

> [!IMPORTANT]
> **Volume total**: Com os ajustes, chegamos a ~101k registros. Para atingir exatamente 110k, posso aumentar `eventos_carrinho` para ~78k. Deseja esse ajuste?

## Open Questions

1. **Dependências Python**: O projeto já possui `requirements.txt` ou `pyproject.toml`? Devo criar um com `faker`, `pandas`, `pyarrow`, `numpy`?

---

## Verification Plan

### Automated Tests
- Executar `python run_all.py` e validar que todos os Parquet são gerados
- Validar volumes por entidade (±5% do target)
- Validar integridade referencial (FKs existem nos datasets pai)
- Validar distribuições (RFM, status carrinho, canais)
- Validar que as métricas calculadas estão dentro dos ranges esperados

### Manual Verification
- Inspecionar `METRICS.md` com métricas calculadas pós-geração
- Carregar Parquets em um notebook para spot-check
