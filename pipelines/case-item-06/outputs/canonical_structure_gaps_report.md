# Relatório de Diagnóstico & Mapeamento de Estruturas Canônicas (Gap Analysis)

**Módulo:** `pipelines/case-item-06/outputs/`  
**Item do Case:** Item 6 — Sobre Modelagem de Dados (Kimball Star Schema)  
**Objetivo:** Inspecionar e auditar a transição de estruturas canônicas entre as camadas Bronze (RAW), Silver (Qualify) e Gold (Curated/Dimensional), identificando eventuais lacunas conceituais e garantindo que nenhuma estrutura seja inventada.

---

## 🔍 1. Inspeção das Entidades Canônicas (`data/data-models/logical/entities/`)

Foram inspecionados os 7 documentos de entidades lógicas canônicas no padrão de 4 divisões:

| # | Entidade Canônica | Arquivo Fonte | Camadas Cobertas no Arquivo | Papel no Domínio de Recuperação |
|---|---|---|:---:|---|
| **1** | `clientes` | [`clientes.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/data-models/logical/entities/clientes.md) | Bronze & Silver | Cadastro mestre de clientes, opt-ins LGPD e métricas de LTV/RFM. |
| **2** | `produtos` | [`produtos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/data-models/logical/entities/produtos.md) | Bronze & Silver | Catálogo de SKUs, precificação, categorias e disponibilidade em estoque. |
| **3** | `carrinhos` | [`carrinhos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/data-models/logical/entities/carrinhos.md) | Bronze & Silver | Transacional central de sessões de checkout, estados e motivos de abandono. |
| **4** | `itens_carrinho` | [`itens_carrinho.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/data-models/logical/entities/itens_carrinho.md) | Bronze & Silver | Itens adicionados aos carrinhos com snapshot de preços e subtotais. |
| **5** | `eventos_carrinho` | [`eventos_carrinho.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/data-models/logical/entities/eventos_carrinho.md) | Bronze & Silver | Telemetria comportamental de funil de navegação (alta volumetria). |
| **6** | `eventos_resgate` | [`eventos_resgate.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/data-models/logical/entities/eventos_resgate.md) | Bronze & Silver | Disparos de mensageria multicanal (E-mail, SMS, Push, WhatsApp) e ROI. |
| **7** | `pedidos` | [`pedidos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/data-models/logical/entities/pedidos.md) | Bronze & Silver | Fechamento financeiro da conversão pós-resgate (relação 1:1 estrita com carrinho). |

---

## 📊 2. Diagnóstico de Transição para a Camada Gold (Curated / Dimensional)

### 2.1 Observação de Arquitetura & Diagnóstico de Lacunas
- **Constatação**: Os arquivos em `data/data-models/logical/entities/*.md` documentam a modelagem lógica relacional (3NF / transacional) das camadas **Bronze (RAW)** e **Silver (Qualify/Anomalies)**. Eles não definem diretamente as tabelas dimensionais desnormalizadas da camada Gold (`dim_*` e `fato_*`).
- **Resolução Normativa**: A especificação formal da camada **Gold (Kimball Star Schema)** foi desenhada e estabelecida especificamente no **Item 6** ([`pipelines/case-item-06/specs.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-06/specs.md)), derivando as dimensões conformadas e fatos diretamente dos datasets qualificados da camada Silver.

### 2.2 Mapeamento de Linhagem: Silver Qualify $\rightarrow$ Gold Dimensional

```text
┌──────────────────────────────────────┐       ┌──────────────────────────────────────┐
│        SILVER QUALIFY (Origem)       │       │       GOLD DIMENSIONAL (Destino)     │
├──────────────────────────────────────┤       ├──────────────────────────────────────┤
│ clientes (1.386 registros limpos)    │ ────► │ dim_clientes (Enriquecida com RFM)   │
│ clientes.segmento_rfm                │ ────► │ dim_segmento_rfm (Lookup de 4 clusters)│
│ carrinhos.dispositivo                │ ────► │ dim_dispositivo (Lookup de fricção)  │
│ carrinhos.motivo_abandono            │ ────► │ dim_motivo_abandono (Taxonomia de 5) │
│ eventos_resgate.canal                │ ────► │ dim_canal_resgate (Custos & benchmarks)│
│ [Geração de Calendário ISO]          │ ────► │ dim_tempo (731 dias - 2023/2024)     │
│ carrinhos + itens_carrinho           │ ────► │ fato_abandono (6.525 linhas granulares)│
│ eventos_resgate + pedidos            │ ────► │ fato_resgate (6.289 linhas granulares) │
└──────────────────────────────────────┘       └──────────────────────────────────────┘
```

---

## 🛠️ 3. Recomendações e Diretrizes de Governança

1. **Preservação de Integridade**: Nenhuma entidade ou dimensão foi inventada fora do escopo estrito de negócio da Recuperação de Carrinho Abandonado.
2. **Consistência de Nomes**: Todas as 6 dimensões (`dim_clientes`, `dim_tempo`, `dim_dispositivo`, `dim_motivo_abandono`, `dim_canal_resgate`, `dim_segmento_rfm`), 2 fatos (`fato_abandono`, `fato_resgate`) e 2 views analíticas (`v_abandonment_summary`, `v_recovery_roi_by_segment`) mantêm 100% de consistência semântica e tipagem com os schemas canônicos.
3. **Observabilidade de Data Quality**: Os registros em quarentena (`data/mock/output/anomalies/*.parquet` - 5.8% de desvios detectados pelo Item 4) permanecem isolados na camada Silver, alimentando a observabilidade sem distorcer as métricas Gold.
