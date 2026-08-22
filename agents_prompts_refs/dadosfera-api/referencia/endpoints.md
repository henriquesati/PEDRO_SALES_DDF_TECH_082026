# Referência Completa da API Dadosfera (Maestro)

Documentação técnica consolidada de todos os endpoints utilizados no pipeline de integração e catalogação do case de **Recuperação de Carrinho Abandonado**.

> **Base URL:** `https://maestro.dadosfera.ai`  
> **Tenant:** Dadosfera Treinamentos (`pedro-sales`)  
> **Última Atualização:** 2026-08-22

---

## Autenticação

> [!IMPORTANT]
> O header `Authorization` deve conter **apenas o token**, sem o prefixo `Bearer`.
> ```
> Authorization: eyJhbGciOiJFUzUxMiIs...
> ```
> Usar `Bearer <token>` causa `401 Unauthorized` em todos os endpoints.

### POST `/auth/sign-in`

Realiza login e retorna tokens de acesso.

**Content-Type:** `application/json`  
**Autenticação:** Nenhuma (credenciais no body)

#### Request Body

```json
{
  "username": "email@exemplo.com",
  "password": "senha-do-usuario",
  "customerName": "nome-do-customer"
}
```

| Campo | Tipo | Obrigatório | Descrição |
|:---|:---|:---:|:---|
| `username` | string | ✓ | Email de login na Dadosfera |
| `password` | string | ✓ | Senha da conta |
| `customerName` | string | ✓ | Identificador do tenant (ex: `pedro-sales`) |

#### Response — 200

```json
{
  "permissions": ["GET /catalog", "POST /pipelines", "catalog:create", "catalog:edit", ...],
  "tokens": {
    "idToken": "",
    "accessToken": "eyJ...",
    "refreshToken": "eyJ..."
  },
  "mfaStatus": "none",
  "termsOfUse": { "status": "ok", ... }
}
```

| Campo | Tipo | Descrição |
|:---|:---|:---|
| `permissions` | array[string] | Lista de permissões do usuário |
| `tokens.accessToken` | string (JWT) | Token de acesso. Validade ~1h |
| `tokens.refreshToken` | string (JWT) | Token de renovação. Validade ~24h |
| `tokens.idToken` | string | Token de identidade (pode vir vazio) |
| `mfaStatus` | string | Status do MFA (`none`, `enabled`) |

#### Erros

| Código | Causa | Solução |
|:---|:---|:---|
| `401` | Credenciais inválidas | Verificar email/senha/customerName |
| `403` | Conta desativada | Contatar administrador |
| `429` | Rate limit | Aguardar e re-tentar |
| `500` | Erro interno | Tentar novamente; pode ser instabilidade temporária |

---

### POST `/auth/refresh-access-token`

Renova o accessToken sem re-login.

**Content-Type:** `application/json`  
**Autenticação:** Nenhuma (refreshToken no body)

#### Request Body

```json
{
  "refreshToken": "eyJ..."
}
```

#### Response — 200

```json
{
  "tokens": {
    "accessToken": "eyJ...(novo)..."
  }
}
```

> **Nota:** A resposta pode conter o token dentro de `tokens.accessToken` ou diretamente como `accessToken` na raiz.

#### Erros

| Código | Causa | Solução |
|:---|:---|:---|
| `401` | refreshToken expirado/inválido | Fazer login completo (`POST /auth/sign-in`) |

---

## Catálogo de Ativos

### GET `/catalog`

Lista todos os data assets catalogados.

**Autenticação:** `Authorization: <accessToken>` (sem Bearer)

#### Query Parameters

| Parâmetro | Tipo | Default | Descrição |
|:---|:---|:---|:---|
| `search` | string | `""` | Busca textual em nome e descrição |

> **Nota:** Não usar os parâmetros `page`, `pageSize`, `limit`, `offset` ou `skip` — eles podem zerar o resultado. A API retorna paginação fixa de 10 por chamada sem parâmetros, mas ao adicionar esses params pode retornar 0 itens.

#### Response — 200

```json
{
  "data_assets": [
    {
      "id": "uuid-do-ativo",
      "user_id": "uuid-do-usuario",
      "created_at": "2026-08-22T19:24:08.485Z",
      "createdAt": "2026-08-22T19:24:08.485Z",
      "users": [{"id": "uuid", "email": "user@example.com"}],
      "owner": "user@example.com",
      "tags": [],
      "roles": [],
      "comments": [],
      "manually": 1,
      "is_renamed": false,
      "display_name": "produtos",
      "description": "Catalogo de produtos...",
      "data_asset_type": "dataset"
    }
  ],
  "total": 21
}
```

| Campo | Tipo | Descrição |
|:---|:---|:---|
| `data_assets` | array | Lista de ativos (máx 10 por página) |
| `data_assets[].id` | string (UUID) | ID único do ativo no catálogo |
| `data_assets[].display_name` | string | Nome de exibição |
| `data_assets[].description` | string | Descrição textual |
| `data_assets[].data_asset_type` | string | Tipo: `dataset`, `table`, etc. |
| `data_assets[].tags` | array | Tags (strings ou objetos com `name`) |
| `data_assets[].owner` | string | Email do proprietário |
| `data_assets[].created_at` | string (ISO) | Data de criação |
| `data_assets[].manually` | integer | `1` se criado manualmente (API/UI) |
| `total` | integer | Total de ativos no catálogo |

> **Atenção:** O campo de retorno é `data_assets` (não `items` como em outras APIs). O campo de tags pode retornar array vazio `[]` mesmo quando tags foram definidas na criação.

---

### POST `/catalog`

Registra um novo data asset no catálogo.

**Content-Type:** `application/json`  
**Autenticação:** `Authorization: <accessToken>`

#### Request Body

```json
{
  "display_name": "clientes",
  "description": "Tabela cadastral de clientes - 2.000 registros",
  "data_asset_type": "dataset",
  "tags": ["carrinho_abandonado", "clientes", "raw"]
}
```

| Campo | Tipo | Obrigatório | Descrição |
|:---|:---|:---:|:---|
| `display_name` | string | ✓ | Nome de exibição do ativo |
| `description` | string | ✓ | Descrição do ativo |
| `data_asset_type` | string | ✓ | Tipo: `dataset`, `table` |
| `tags` | array[string] | — | Tags como strings simples |

> [!WARNING]
> A API **não faz deduplicação**. Chamar POST múltiplas vezes com o mesmo `display_name` cria assets duplicados. Verifique antes se já existe.

#### Response — 201

```json
{
  "data_asset": {
    "id": "uuid-gerado",
    "user_id": "uuid-do-usuario",
    "created_at": "2026-08-22T...",
    "display_name": "clientes",
    "description": "...",
    "data_asset_type": "dataset",
    "tags": [],
    "manually": 1,
    "is_renamed": false
  }
}
```

> **Nota:** O response vem dentro de `data_asset` (singular). As tags podem não ser retornadas imediatamente no response.

---

### PUT `/catalog/data-asset/{id}`

Atualiza um data asset existente.

**Content-Type:** `application/json`  
**Autenticação:** `Authorization: <accessToken>`

#### Path Parameters

| Parâmetro | Tipo | Descrição |
|:---|:---|:---|
| `id` | string (UUID) | ID do data asset a atualizar |

#### Request Body

```json
{
  "display_name": "nome-atualizado",
  "description": "descricao-atualizada",
  "data_asset_type": "dataset",
  "tags": ["tag1", "tag2"]
}
```

> [!IMPORTANT]
> Tags devem ser enviadas como **strings simples**, não como objetos `{"name": "tag"}`. Enviar objetos causa `500 Internal Server Error`.

#### Response — 200

Retorna o asset atualizado no mesmo formato de `POST /catalog`.

---

### DELETE `/catalog/data-asset/{id}`

Tenta deletar um data asset.

**Autenticação:** `Authorization: <accessToken>`

> [!CAUTION]
> Requer permissão `catalog:delete` que normalmente não está disponível em contas de treinamento. Retorna `403 Forbidden` sem a permissão.

---

## Storage Explorer

### POST `/storage-explorer/storage/upload/batch`

Upload de arquivos para o Data Lake.

**Content-Type:** `multipart/form-data`  
**Autenticação:** `Authorization: <accessToken>` (sem Bearer)

#### Query Parameters

| Parâmetro | Tipo | Obrigatório | Descrição |
|:---|:---|:---:|:---|
| `folderPath` | string | ✓ | Caminho destino no Data Lake (ex: `/raw/recuperacao_carrinho`) |

#### Form Data

| Campo | Tipo | Obrigatório | Descrição |
|:---|:---|:---:|:---|
| `file` | binary | ✓ | Arquivo (CSV, Parquet, JSON) |

#### Exemplo cURL

```bash
curl -X POST \
  "https://maestro.dadosfera.ai/storage-explorer/storage/upload/batch?folderPath=/raw/recuperacao_carrinho" \
  -H "Authorization: eyJ..." \
  -F "file=@clientes.csv;type=text/csv"
```

#### Response — 200/201

```json
{
  "datasetId": "uuid-do-dataset",
  "fileName": "clientes.csv",
  "folderPath": "/raw/recuperacao_carrinho",
  "status": "success",
  "size": 223983
}
```

| Campo | Tipo | Descrição |
|:---|:---|:---|
| `datasetId` | string (UUID) | ID do dataset criado (pode variar: `dataset_id`, `id`, `fileId`) |
| `fileName` | string | Nome do arquivo enviado |
| `folderPath` | string | Caminho de destino |

#### Limites

- Timeout recomendado: **120s** (para arquivos grandes como `eventos_carrinho.csv` ~11MB)
- Pausa entre uploads: **1s** (evitar rate limiting)

---

### POST `/storage-explorer/tables`

Cria tabela no Snowflake com schema tipado.

**Content-Type:** `application/json`  
**Autenticação:** `Authorization: <accessToken>`

> [!WARNING]
> Requer permissão de storage-explorer. Em contas de treinamento, pode retornar `403 Forbidden`. Caso `403`, as tabelas devem ser criadas pela UI da Dadosfera.

#### Request Body

```json
{
  "name": "clientes",
  "description": "Dados cadastrais dos clientes",
  "schema": "CART_RECOVERY",
  "columns": [
    {"name": "cliente_id", "type": "VARCHAR", "description": "ID do cliente"},
    {"name": "nome", "type": "VARCHAR", "description": "Nome completo"}
  ]
}
```

| Campo | Tipo | Obrigatório | Descrição |
|:---|:---|:---:|:---|
| `name` | string | ✓ | Nome da tabela |
| `description` | string | ✓ | Descrição da tabela |
| `schema` | string | ✓ | Schema Snowflake (ex: `CART_RECOVERY`) |
| `columns` | array | ✓ | Definições de colunas |
| `columns[].name` | string | ✓ | Nome da coluna |
| `columns[].type` | string | ✓ | Tipo Snowflake |
| `columns[].description` | string | — | Descrição da coluna |

#### Tipos Snowflake suportados

| Tipo | Uso no Case |
|:---|:---|
| `VARCHAR` | IDs, nomes, categorias, status |
| `INTEGER` | Contagens, quantidades |
| `FLOAT` | Valores monetários, percentuais |
| `BOOLEAN` | Flags (ativo, convertido) |
| `TIMESTAMP` | Datas e horários de eventos |
| `VARIANT` | Dados JSON semi-estruturados |

---

### GET `/storage-explorer/tables`

Lista tabelas existentes no Snowflake.

**Autenticação:** `Authorization: <accessToken>`

> Pode retornar `403` em contas de treinamento sem permissão de storage-explorer.

---

### POST `/storage-explorer/tables/{tableId}/datasets`

Vincula um dataset (arquivo no Storage) a uma tabela Snowflake.

**Content-Type:** `application/json`  
**Autenticação:** `Authorization: <accessToken>`

#### Path Parameters

| Parâmetro | Tipo | Descrição |
|:---|:---|:---|
| `tableId` | string (UUID) | ID da tabela destino |

#### Request Body

```json
{
  "datasetId": "uuid-do-dataset"
}
```

#### Response — 200/201/204

Vinculação bem-sucedida. O `204 No Content` é possível.

#### Conceito: Materialização

A vinculação carrega os dados do CSV (zona raw) para a tabela Snowflake (zona qualify):

```
CSV no Storage (/raw/)  ──vincular──►  Tabela Snowflake (qualify)
      ↓                                        ↓
  dataset_id                              table_id
      └────────────────link─────────────────┘
```

---

## Códigos de Resposta

| Código | Significado | Ação |
|:---|:---|:---|
| `200` | Sucesso | Processar resposta |
| `201` | Criado com sucesso | Processar resposta |
| `204` | Sucesso sem conteúdo | Considerar sucesso |
| `401` | Token inválido/expirado | Refresh ou re-autenticar |
| `403` | Sem permissão | Verificar permissões da conta |
| `409` | Conflito (recurso existe) | Considerar idempotente |
| `429` | Rate limit | Aguardar e re-tentar |
| `500` | Erro interno | Re-tentar; verificar payload |

---

## Permissões do Usuário (Tenant `pedro-sales`)

```
PUT /pipelines
GET /pipelines
GET /catalog
POST /pipelines
import-file:view
process:open
GET /metabase
catalog:create
catalog:edit
connection:create
network_config:create
```

> **Nota:** A conta possui `catalog:create` e `catalog:edit`, mas **não** possui `catalog:delete` nem permissões explícitas de `storage-explorer`. Isso explica os erros `403` ao tentar criar tabelas ou deletar assets via API.

---

## Referência Cruzada: Fase → Endpoint → Script

| Fase | Endpoint | Script |
|:---|:---|:---|
| 1 - Autenticar | `POST /auth/sign-in` | `01_auth/authenticate.py` |
| 2 - Upload | `POST /storage-explorer/storage/upload/batch` | `02_integrar/upload_raw_files.py` |
| 3 - Criar Tabelas | `POST /storage-explorer/tables` | `03_criar_tabelas/create_snowflake_tables.py` |
| 4 - Vincular | `POST /storage-explorer/tables/{id}/datasets` | `04_vincular/link_datasets_to_tables.py` |
| 5 - Catalogar | `POST /catalog` + `GET /catalog` | `05_catalogar/catalog_assets.py` |

---

*Referência técnica — Case Pedro Sales / Dadosfera Internship 2026*
