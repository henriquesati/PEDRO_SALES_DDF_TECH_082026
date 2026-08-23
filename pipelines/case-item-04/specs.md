# Especificação: Data Quality & Quarentena de Anomalias

**Doc ID**: `spec_data_quality_001`  
**Versão**: 1.1  
**Módulo:** `pipelines/case-item-04/`  
**Case Oficial Dadosfera:** Item 4 — Sobre Data Quality  
**Escopo**: Case Técnico de Estágio em Engenharia de Soluções / Dados (Dadosfera)  
**Status**: Implementado & Validado  

---

## 📋 1. Requisitos Oficiais da Empresa (Dadosfera)

> Fonte: [`specs-internship.txt`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/agents_prompts_refs/case-internship-files/specs-internship.txt)

```text
Item 4 - Sobre Data Quality
Após a integração e exploração dos dados do site de e-commerce, você identificou várias inconsistências e dados faltantes que podem impactar negativamente a performance dos modelos de IA e a experiência de compra dos clientes. Como você abordaria a melhoria da qualidade desses dados utilizando as ferramentas e práticas recomendadas pela Dadosfera?

Gere um relatório de qualidade dos dados usando uma biblioteca apropriada - great-expectations ou soda-core - para identificar inconsistências e dados faltantes.

Bônus: Definir e implementar um Common Data Model para os dados utilizados.
```

### Escala de Avaliação do Case
- **Mínimo:** Relatório básico de inconsistências e nulos.
- **Avançado:** Uso de biblioteca formal (Great Expectations / Soda Core) com regras parametrizadas.
- **Excelente / Outlier:** Arquitetura **Dual-Artifact Pipeline** na camada Silver (Bifurcação entre `Qualify` e `Anomalies` em quarentena dead-letter auditável), suíte de 18 regras de Data Quality (técnicas, contábeis e de negócio), relatório executivo gerado automaticamente em Markdown com gráficos 300DPI, e log de auditoria JSON.

---

## 🎯 2. Arquitetura Dual-Artifact & Roteamento (DEC-006)

Em conformidade com a decisão arquitetural **DEC-006**, os dados da camada Bronze (RAW Parquet) são processados por um pipeline de qualificação que bifurca os registros em dois destinos:
1. **Silver Qualify (`data/mock/output/qualify/`):** Registros 100% íntegros e promovidos para consultas analíticas e consumo no Metabase / Data Apps.
2. **Silver Anomalies (`data/mock/output/anomalies/`):** Dead-letter estruturada com metadados de diagnóstico (`codigo_anomalia`, `campo_afetado`, `descricao_risco`, `severidade`, `detected_at`, `payload_raw`).

```text
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA BRONZE (RAW)                      │
│            115.777+ registros em Parquet (7 entidades)      │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│           PIPELINE DE QUALIFICAÇÃO & DATA QUALITY           │
│        18 regras (Great Expectations + Pandas Validator)     │
└──────────────────────────────┬──────────────────────────────┘
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
┌─────────────────────────────┐ ┌─────────────────────────────┐
│    SILVER QUALIFY (94.2%)   │ │   SILVER ANOMALIES (5.8%)   │
│   Registros conformes para  │ │  Quarentena auditável para  │
│      camada Gold / BI       │ │   mitigação e diagnóstico   │
└─────────────────────────────┘ └─────────────────────────────┘
```

---

## 🔍 3. Catálogo de Regras de Validação (18 Regras)

### 3.1 Entidade `clientes`
- `ERR_CLI_001` (Crítica): `cliente_id` não nulo.
- `ERR_CLI_002` (Alta): `email` não nulo.
- `ERR_CLI_003` (Média): `email` com sintaxe válida via regex.

### 3.2 Entidade `produtos`
- `ERR_PROD_001` (Crítica): `produto_id` não nulo.
- `ERR_PROD_002` (Alta): `preco_atual > 0`.
- `ERR_PROD_003` (Alta): `preco_atual <= preco_original` (sem promoção invertida).

### 3.3 Entidade `carrinhos`
- `ERR_CAR_001` (Crítica): `carrinho_id` não nulo.
- `ERR_CAR_002` (Crítica): `cliente_id` não nulo.
- `ERR_CAR_003` (Média): `status` contido no conjunto de estados válidos (`comprado`, `abandonado`, `expirado`, `ativo`, `recuperado`).
- `ANOM-01` (Alta): `valor_frete >= 0` (detecção de frete negativo).
- `ANOM-02` (Alta): `valor_subtotal > 0` (detecção de subtotal zerado).
- `ANOM-03` (Crítica): `valor_desconto <= valor_subtotal` (desconto abusivo superior a 100%).
- `ANOM-04` (Alta): `valor_total == subtotal + frete - desconto` (equação contábil).
- `ANOM-05` (Alta): `data_abandono >= data_criacao` (consistência temporal).

### 3.4 Entidade `itens_carrinho`
- `ERR_ITM_001` (Crítica): `item_id` não nulo.
- `ERR_ITM_002` (Crítica): `carrinho_id` não nulo.
- `ERR_ITM_003` (Alta): `quantidade > 0`.
- `ERR_ITM_004` (Alta): `preco_unitario > 0`.
- `ERR_ITM_005` (Alta): `data_remocao >= data_adicao` (consistência temporal de remoção).

### 3.5 Entidades Transacionais (`eventos_carrinho`, `eventos_resgate`, `pedidos`)
- Integridade de chaves estrangeiras e sequenciamento temporal de aberturas de e-mail/SMS.

---

## 📁 4. Estrutura do Módulo

```text
pipelines/case-item-04/
├── specs.md                # Esta especificação técnica
├── implementation_plan.md  # Plano de execução e tarefas
├── scripts/
│   └── run_quality_pipeline.py  # Script de execução batch
├── notebooks/
│   └── qualification_raw.ipynb  # Notebook Google Colab executável
├── quality/
│   ├── expectations/
│   │   └── carrinhos_suite.json # Suite Great Expectations
│   └── results/
│       └── validation_results.json # Evidência de execução
└── outputs/
    ├── data_quality_report.md   # Relatório gerado de Data Quality
    ├── validation_results.json  # Log JSON de validação
    └── assets/                  # Gráficos em alta resolução (300 DPI)
```
