# Especificação da Apresentação: Modelagem Dimensional Kimball (Item 6)

> **Módulo do Pitch**: `presentation/pitch/views/caseitem06/`  
> **Item do Case**: Item 6 — Sobre Modelagem de Dados  
> **Framework Normativo**: Kimball Star Schema (1-Hop) • DEC-001 (% e Ratios) • DEC-006 (Dual-Artifact Silver)  
> **Origem dos Dados (Ground Truth)**: `data/mock/output_cleaned/parquet/*.parquet`  
> **Doc de Referência Central**: [`pipelines/case-item-06/specs.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-06/specs.md)

---

## 1. 🎯 Objetivo Executivo no Pitch

Apresentar a arquitetura da camada **Gold (Curated / Dimensional)** no Snowflake Data Lakehouse da Dadosfera, comprovando por que o **Kimball Star Schema** é a modelagem **mais simples, intuitiva de entender e ágil de implementar** para responder às perguntas de negócio do e-commerce:

1. **Simplicidade Conceitual**: Estrutura 1-Hop com 1 fato no centro e dimensões em estrela, eliminando a sobrecarga de JOINs complexos.
2. **Alta Performance Analítica**: Consultas agregadas ultrarrápidas no Snowflake e renderização nativa de painéis no Metabase (Item 7).
3. **Consumo Unificado Downstream**: Atendimento simultâneo de BI, Data App em Streamlit (Item 9), Modelos de Propensity ML (Item 8) e Copilotos GenAI (Bônus).

---

## 2. ⚖️ Avaliação Metodológica: Por Que Kimball Star Schema é a Mais Simples e Eficiente?

| Abordagem de Modelagem | Simplicidade Conceitual | Facilidade de Implementação | Performance OLAP / Snowflake | Aderência ao Metabase / BI | Veredito no Case |
|---|:---:|:---:|:---:|:---:|:---:|
| **Kimball Star Schema (1-Hop)** | ⭐⭐⭐⭐⭐ **Máxima** (Intuitiva para negócio) | ⭐⭐⭐⭐⭐ **Direta** (Mapeamento limpo da Silver) | ⭐⭐⭐⭐⭐ **Excelente** (1-Hop JOINs) | ⭐⭐⭐⭐⭐ **Nativa e Imediata** | ✅ **ESCOLHA OFICIAL (Simples & Robusta)** |
| **Kimball Snowflake Schema** | ⭐⭐⭐ Média (Sub-dimensões em cadeia) | ⭐⭐⭐ Média (Mais tabelas) | ⭐⭐⭐⭐ Boa | ⭐⭐⭐ Requer navegação em árvore | ⚠️ Overkill para o volume de entidades |
| **Inmon 3NF (Terceira Forma Normal)** | ⭐⭐ Baixa (Voltada a OLTP) | ⭐⭐ Lenta (Múltiplas entidades isoladas) | ⭐⭐ Lenta (10+ JOINs em cascata) | ⭐ Fraca para usuários finais | ❌ Inadequada para Analytics |
| **Data Vault 2.0 (Hubs/Links/Sats)** | ⭐ Muito Complexa (Abstrata) | ⭐ Muito Lenta (Burocrática) | ⭐⭐⭐ Moderada (Multi-Hop) | ⭐⭐ Requer camada de view virtual | ❌ Over-engineering desnecessário |

### Justificativas-Chave para o Pitch:
1. **Compreensão Imediata**: Qualquer stakeholder de negócio (Diretoria, Marketing, Produto) entende um Star Schema em menos de 2 minutos: fatos registram eventos transacionais (`abandono` e `resgate`) e dimensões respondem *Quem* (`dim_clientes`), *Quando* (`dim_tempo`), *Onde/Como* (`dim_dispositivo`, `dim_canal_resgate`) e *Por que* (`dim_motivo_abandono`).
2. **Tempo de Implementação Mínimo**: A criação das tabelas Gold a partir da Silver Qualify ocorre sem a necessidade de criar dezenas de tabelas de junção intermediárias.
3. **Zero Risco de Lock / Conflito**: Desacoplada da ingestão e com chaves substitutas (`_sk`), permitindo histórico SCD Type 2 sem impactos de performance.

---

## 3. 📐 Arquitetura em Camadas Medallion & Linhagem

```text
========================================================================================
                                 LINHAGEM MEDALLION
========================================================================================
[1. ORIGENS]      -->  [2. BRONZE / RAW]   -->  [3. SILVER QUALIFY]  -->  [4. GOLD STAR SCHEMA]
- Sessões Web/App      - 115.777+ linhas        - 94.2% Conformes         - 6 Dimensões
- ERP Catálogo         - Parquet / S3           - Anomalias 5.8%          - 2 Tabelas de Fatos
- CRM Mensageria                                (Quarentena Item 4)       - 2 Views Analíticas
- Gateway Pagamentos
========================================================================================
```

---

## 4. 📊 Estrutura Topológica do Star Schema

### 4.1 Dimensões Conformadas (Lookup & Context)
1. **`dim_clientes`** (`1.386 registros`): `cliente_sk` (PK), `cliente_id`, `email`, `segmento_rfm`, `status_ativo`, `opt_ins`, `recencia_dias`, `frequencia_compras`, `valor_monetario_ltv`, `rfm_score`, `churn_risk_score`.
2. **`dim_tempo`** (`731 dias / 2 anos`): `data_sk` (PK: YYYYMMDD), `data`, `ano`, `mes`, `trimestre`, `ano_mes`, `dia_semana_nome`, `eh_fim_semana`.
3. **`dim_dispositivo`** (`3 registros`): `dispositivo_sk` (PK), `dispositivo` (`mobile`, `desktop`, `tablet`), `complexidade_checkout`, `fator_friccao_checkout`.
4. **`dim_motivo_abandono`** (`5 registros`): `motivo_sk` (PK), `motivo` (`preco`, `frete`, `pagamento`, `indecisao`, `estoque`), `categoria_motivo`, `estrategia_resgate_padrao`.
5. **`dim_canal_resgate`** (`4 registros`): `canal_sk` (PK), `canal` (`email`, `sms`, `push_app`, `whatsapp`), `custo_unitario_envio`, `taxa_abertura_benchmark`, `taxa_conversao_benchmark`.
6. **`dim_segmento_rfm`** (`4 registros`): `segmento_sk` (PK), `segmento` (`premium`, `regular`, `dormant`, `novo`), `prioridade_resgate`, `estrategia_comunicacao`, `expectativa_roi`.

### 4.2 Tabelas de Fatos Granulares
1. **`fato_abandono`** (`6.525 linhas conformes`):
   - **Grão**: 1 linha por sessão de carrinho com abandono.
   - **Chaves**: `fato_abandono_sk` (PK), `cliente_sk` (FK), `data_abandono_sk` (FK), `dispositivo_sk` (FK), `motivo_sk` (FK).
   - **Medidas Aditivas**: `valor_subtotal`, `valor_frete`, `valor_desconto`, `valor_total_em_risco`, `quantidade_itens`.
   - **Medidas Semi-aditivas**: `duracao_sessao_minutos`, `tempo_ate_abandono_segundos`.
2. **`fato_resgate`** (`6.289 linhas conformes`):
   - **Grão**: 1 linha por tentativa de resgate disparada pela régua de CRM.
   - **Chaves**: `fato_resgate_sk` (PK), `cliente_sk` (FK), `data_envio_sk` (FK), `canal_sk` (FK), `fato_abandono_sk` (FK).
   - **Métricas de Funil**: `flag_entregue`, `flag_aberto`, `flag_clicado`, `flag_convertido`.
   - **Métricas Financeiras**: `custo_disparo_envio`, `valor_pedido_recuperado`, `roi_liquido_disparo`.

---

## 5. 🎯 As 2 Visões Analíticas Gold (Metabase & Snowflake Ready)

### 5.1 Visão 1: `v_abandonment_summary` (Visão Executiva & Perfil de Risco)
- **Métricas Chave**: Volume de carrinhos abandonados, % de concentração por motivo/segmento, Churn Risk Score médio e montante financeiro total em risco.
- **Pergunta Respondida**: *"Quais segmentos e motivos concentram a maior perda e risco de churn na operação?"*

### 5.2 Visão 2: `v_recovery_roi_by_segment` (Visão Tática / Eficiência de CRM)
- **Métricas Chave**: Taxa de abertura %, Taxa de conversão %, Custo total de comunicação, Receita recuperada e Multiplicador de ROI líquido por canal de disparo.
- **Pergunta Respondida**: *"Qual canal de resgate entrega a maior rentabilidade líquida para cada perfil de cliente?"*

---

## 6. 🚀 Consumidores Downstream (Camada de Aplicação)

- **Metabase Dashboards (Item 7)**: BI integrado e democratizado para times de marketing e e-commerce.
- **Streamlit Data App (Item 9)**: Simulador interativo em tempo real de ROI e sensibilidade orçamentária.
- **Modelos de ML (Item 8)**: Scoring preditivo de propensão de resgate (`propensity_recovery`).
- **Copilotos GenAI (Bônus)**: Copywriting semântico e geração dinâmica de vitrines de resgate.

---

## 🖼️ Artefato Visual do Módulo

- **Script Gerador**: [`generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/views/caseitem06/generate_chart.py)
- **Artefato de Imagem**: [`chart_caseitem06_kimball_model.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/views/caseitem06/chart_caseitem06_kimball_model.png) (300 DPI, Tema Dadosfera)
