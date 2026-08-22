# Dadosfera API — Referência Técnica

Documentação de referência dos endpoints da API Maestro da Dadosfera utilizados no pipeline de integração e catalogação do case de Recuperação de Carrinho Abandonado.

## Base URL

```
https://maestro.dadosfera.ai
```

## Autenticação

> **IMPORTANTE:** O header `Authorization` deve conter **apenas o token JWT**, sem prefixo `Bearer`.
> ```
> Authorization: eyJhbGciOiJFUzUxMiIs...
> ```

O token é obtido via `POST /auth/sign-in` (campo `username`, não `email`) e pode ser renovado via `POST /auth/refresh-access-token`.

## Documentação

| Recurso | Localização |
|:---|:---|
| **Referência completa de endpoints** | [referencia/endpoints.md](referencia/endpoints.md) |
| **Erros conhecidos e soluções** | [referencia/solved-errors.md](referencia/solved-errors.md) |
| **Registro de ativos e IDs** | [output-mappers/assets_registry.md](output-mappers/assets_registry.md) |
| **Registro programático (JSON)** | [output-mappers/assets_registry.json](output-mappers/assets_registry.json) |

## Referência Cruzada: Fase → Endpoint → Script

```
FASE 1  →  POST /auth/sign-in                              →  01_auth/authenticate.py
FASE 2  →  POST /storage-explorer/storage/upload/batch      →  02_integrar/upload_raw_files.py
FASE 3  →  POST /storage-explorer/tables                    →  03_criar_tabelas/create_snowflake_tables.py
FASE 4  →  POST /storage-explorer/tables/{id}/datasets      →  04_vincular/link_datasets_to_tables.py
FASE 5  →  POST /catalog + GET /catalog                     →  05_catalogar/catalog_assets.py
```

## Permissões Conhecidas (Tenant `pedro-sales`)

| Permissão | Disponível |
|:---|:---:|
| `GET /catalog` | ✅ |
| `catalog:create` | ✅ |
| `catalog:edit` | ✅ |
| `catalog:delete` | ❌ |
| `import-file:view` | ✅ |
| `GET /metabase` | ✅ |
| `storage-explorer (tables)` | ❌ (403) |

---

*Documentação de referência — Case Pedro Sales / Dadosfera Internship 2026*
