# Registro de Ativos e Mapeamento de Tabelas — Dadosfera

Documento central de referência contendo os identificadores oficiais (`Data Asset IDs`), links diretos para acesso na plataforma Dadosfera, volumetria de dados, dicionários de dados e mapeamento de zonas do Data Lake para o case de **Recuperação de Carrinho Abandonado**.

> **Tenant:** Dadosfera Treinamentos (`pedro-sales`)  
> **Status:** ✅ Ativos Recatalogados com Dicionário de Dados e Tags Atualizadas via API Maestro  
> **Total de Registros:** 116.526 linhas  
> **Última Atualização:** 2026-08-22 (Recatalogação completa com Dicionário de Dados & LGPD)

---

## 1. Tabela Rápida de Identificadores, Links e Dicionários

| Entidade | Data Asset ID | Link Direto na Plataforma | Registros | Tags Semânticas | Dicionário Local |
|:---|:---|:---|:---:|:---|:---:|
| **`clientes`** | `0327fecc-f826-48fb-bb0a-1493fe18a32c` | [Acessar clientes](https://app.dadosfera.ai/pt-BR/catalog/data-assets/0327fecc-f826-48fb-bb0a-1493fe18a32c) | 2.000 | `carrinho_abandonado`, `clientes`, `marketplace`, `qualify`, `dimensao`, `pii_sensivel` | [clientes.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/clientes.md) |
| **`produtos`** | `65fcfa25-a6f3-4cb8-a444-7fd23df3fa84` | [Acessar produtos](https://app.dadosfera.ai/pt-BR/catalog/data-assets/65fcfa25-a6f3-4cb8-a444-7fd23df3fa84) | 500 | `carrinho_abandonado`, `produtos`, `catalogo`, `qualify`, `dimensao` | [produtos.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/produtos.md) |
| **`carrinhos`** | `e2d3b1bb-bf22-456e-bc66-4ac843deec82` | [Acessar carrinhos](https://app.dadosfera.ai/pt-BR/catalog/data-assets/e2d3b1bb-bf22-456e-bc66-4ac843deec82) | 15.000 | `carrinho_abandonado`, `carrinhos`, `transacional`, `qualify`, `fato_central` | [carrinhos.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/carrinhos.md) |
| **`itens_carrinho`** | `7649755a-c6e8-4b56-a092-be9eefde1dab` | [Acessar itens_carrinho](https://app.dadosfera.ai/pt-BR/catalog/data-assets/7649755a-c6e8-4b56-a092-be9eefde1dab) | 22.500 | `carrinho_abandonado`, `itens_carrinho`, `itens`, `qualify`, `fato_detalhe` | [itens_carrinho.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/itens_carrinho.md) |
| **`eventos_carrinho`** | `397c3ebc-15cb-42d2-a717-a3b5d150c3ea` | [Acessar eventos_carrinho](https://app.dadosfera.ai/pt-BR/catalog/data-assets/397c3ebc-15cb-42d2-a717-a3b5d150c3ea) | 72.026 | `carrinho_abandonado`, `eventos_carrinho`, `telemetria`, `qualify`, `timeseries` | [eventos_carrinho.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/eventos_carrinho.md) |
| **`eventos_resgate`** | `04739f6d-e8c3-4d6f-80b7-0f98c12a5798` | [Acessar eventos_resgate](https://app.dadosfera.ai/pt-BR/catalog/data-assets/04739f6d-e8c3-4d6f-80b7-0f98c12a5798) | 2.500 | `carrinho_abandonado`, `eventos_resgate`, `recuperacao`, `qualify`, `crm_marketing` | [eventos_resgate.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/eventos_resgate.md) |
| **`pedidos`** | `7f82a988-8e68-416a-b6fa-5007c4789d1a` | [Acessar pedidos](https://app.dadosfera.ai/pt-BR/catalog/data-assets/7f82a988-8e68-416a-b6fa-5007c4789d1a) | 2.000 | `carrinho_abandonado`, `pedidos`, `conversoes`, `qualify`, `faturamento` | [pedidos.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/pedidos.md) |

---

## 2. Detalhamento por Entidade & Dicionário de Dados

### 👤 `clientes` (Dimensão Cadastral & RFM)
- **ID Dadosfera:** `0327fecc-f826-48fb-bb0a-1493fe18a32c`
- **URL Direta:** `https://app.dadosfera.ai/pt-BR/catalog/data-assets/0327fecc-f826-48fb-bb0a-1493fe18a32c`
- **Tabela Snowflake:** `CART_RECOVERY.CLIENTES`
- **Volume:** 2.000 registros (~224 KB)
- **Sensibilidade:** 🔴 Confidencial (PII / LGPD) — `nome`, `email`, `telefone`.
- **Dicionário Completo:** [`data/catalogo/qualify/clientes.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/clientes.md)

### 📦 `produtos` (Catálogo & Estoque)
- **ID Dadosfera:** `65fcfa25-a6f3-4cb8-a444-7fd23df3fa84`
- **URL Direta:** `https://app.dadosfera.ai/pt-BR/catalog/data-assets/65fcfa25-a6f3-4cb8-a444-7fd23df3fa84`
- **Tabela Snowflake:** `CART_RECOVERY.PRODUTOS`
- **Volume:** 500 registros (~47 KB)
- **Sensibilidade:** 🟢 Interno
- **Dicionário Completo:** [`data/catalogo/qualify/produtos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/produtos.md)

### 🛒 `carrinhos` (Sessões & Lifecycle de Compra)
- **ID Dadosfera:** `e2d3b1bb-bf22-456e-bc66-4ac843deec82`
- **URL Direta:** `https://app.dadosfera.ai/pt-BR/catalog/data-assets/e2d3b1bb-bf22-456e-bc66-4ac843deec82`
- **Tabela Snowflake:** `CART_RECOVERY.CARRINHOS`
- **Volume:** 15.000 registros (~1.6 MB)
- **Sensibilidade:** 🟢 Interno
- **Dicionário Completo:** [`data/catalogo/qualify/carrinhos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/carrinhos.md)

### 🛍️ `itens_carrinho` (Composição do Carrinho)
- **ID Dadosfera:** `7649755a-c6e8-4b56-a092-be9eefde1dab`
- **URL Direta:** `https://app.dadosfera.ai/pt-BR/catalog/data-assets/7649755a-c6e8-4b56-a092-be9eefde1dab`
- **Tabela Snowflake:** `CART_RECOVERY.ITENS_CARRINHO`
- **Volume:** 22.500 registros (~1.2 MB)
- **Sensibilidade:** 🟢 Interno
- **Dicionário Completo:** [`data/catalogo/qualify/itens_carrinho.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/itens_carrinho.md)

### ⚡ `eventos_carrinho` (Telemetria & Funil de Conversão)
- **ID Dadosfera:** `397c3ebc-15cb-42d2-a717-a3b5d150c3ea`
- **URL Direta:** `https://app.dadosfera.ai/pt-BR/catalog/data-assets/397c3ebc-15cb-42d2-a717-a3b5d150c3ea`
- **Tabela Snowflake:** `CART_RECOVERY.EVENTOS_CARRINHO`
- **Volume:** 72.026 registros (~11.4 MB)
- **Sensibilidade:** 🟢 Interno
- **Dicionário Completo:** [`data/catalogo/qualify/eventos_carrinho.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/eventos_carrinho.md)

### 🎯 `eventos_resgate` (Campanhas Multicanal & ROI)
- **ID Dadosfera:** `04739f6d-e8c3-4d6f-80b7-0f98c12a5798`
- **URL Direta:** `https://app.dadosfera.ai/pt-BR/catalog/data-assets/04739f6d-e8c3-4d6f-80b7-0f98c12a5798`
- **Tabela Snowflake:** `CART_RECOVERY.EVENTOS_RESGATE`
- **Volume:** 2.500 registros (~1.3 MB)
- **Sensibilidade:** 🟢 Interno
- **Dicionário Completo:** [`data/catalogo/qualify/eventos_resgate.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/eventos_resgate.md)

### 💳 `pedidos` (Conversões & Faturamento Final)
- **ID Dadosfera:** `7f82a988-8e68-416a-b6fa-5007c4789d1a`
- **URL Direta:** `https://app.dadosfera.ai/pt-BR/catalog/data-assets/7f82a988-8e68-416a-b6fa-5007c4789d1a`
- **Tabela Snowflake:** `CART_RECOVERY.PEDIDOS`
- **Volume:** 2.000 registros (~258 KB)
- **Sensibilidade:** 🟢 Interno
- **Dicionário Completo:** [`data/catalogo/qualify/pedidos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/pedidos.md)

---

## 3. Arquitetura de Zonas e Linhagem

```
[ Mock Data Local ]            [ Dadosfera Storage (RAW) ]               [ Dadosfera Catálogo & Snowflake ]
data/mock/output/csv/          /raw/recuperacao_carrinho/                Schema: CART_RECOVERY

├── clientes.csv       ───►    /raw/recuperacao_carrinho/clientes.csv    ───►  clientes         (0327fecc...)
├── produtos.csv       ───►    /raw/recuperacao_carrinho/produtos.csv    ───►  produtos         (65fcfa25...)
├── carrinhos.csv      ───►    /raw/recuperacao_carrinho/carrinhos.csv   ───►  carrinhos        (e2d3b1bb...)
├── itens_carrinho.csv ───►    /raw/recuperacao_carrinho/itens.csv       ───►  itens_carrinho   (7649755a...)
├── eventos_carrinho.csv ─►    /raw/recuperacao_carrinho/eventos.csv     ───►  eventos_carrinho (397c3ebc...)
├── eventos_resgate.csv ──►    /raw/recuperacao_carrinho/resgate.csv     ───►  eventos_resgate  (04739f6d...)
└── pedidos.csv        ───►    /raw/recuperacao_carrinho/pedidos.csv     ───►  pedidos          (7f82a988...)
```

---

## 4. Notas sobre Duplicatas e Limpeza

Na data de 2026-08-22, foram identificados **8 data assets duplicados** no catálogo (7 entidades + 1 asset de teste). Esses ativos foram marcados com prefixo `[DUPLICATA - IGNORAR]` no display_name e tags `duplicata`, `ignorar`, `lixeira` via `PUT /catalog/data-asset/{id}`.

A API da Dadosfera (tenant de treinamento) não permite `DELETE` em data assets (`403 Forbidden`). A remoção definitiva deve ser feita pela UI da plataforma.

### Duplicatas Marcadas para Exclusão Manual na UI:

| Entidade | ID Duplicado | Status |
|:---|:---|:---|
| clientes | `059360a7-759d-4516-868c-4245d023f24d` | Marcado `[DUPLICATA - IGNORAR]` |
| produtos | `cb5a7a46-48a3-4bc2-8d6c-bf6128d634b1` | Marcado `[DUPLICATA - IGNORAR]` |
| carrinhos | `595f7251-dd76-427f-b590-cc9d820afcde` | Marcado `[DUPLICATA - IGNORAR]` |
| itens_carrinho | `f6000b61-4744-4eef-8a11-8873dbcf3251` | Marcado `[DUPLICATA - IGNORAR]` |
| eventos_carrinho | `7dd16cc4-eab2-4654-b3cb-8f24119ec7bc` | Marcado `[DUPLICATA - IGNORAR]` |
| eventos_resgate | `766174e0-3853-46fa-971d-43d731c4ec9d` | Marcado `[DUPLICATA - IGNORAR]` |
| pedidos | `e88039c6-2b81-4324-a4d6-88e401ccd60a` | Marcado `[DUPLICATA - IGNORAR]` |
| __test_delete_me | `b41be981-36e5-4413-8092-2093374f003f` | Marcado `[DUPLICATA - IGNORAR]` |
