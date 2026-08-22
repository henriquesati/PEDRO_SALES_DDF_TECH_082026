# API Dadosfera — Pipeline de Integração e Catalogação

## Case: Recuperação de Carrinho Abandonado (Marketplace)

Pipeline Python que executa as 5 fases do ciclo de vida do dado na Dadosfera:
upload dos dados mock (116k+ registros), criação de tabelas Snowflake, vinculação e catalogação automática.

---

## Pré-requisitos

- **Python 3.10+**
- **Biblioteca `requests`**: `pip install requests`
- **Credenciais Dadosfera**: configuradas em `dadosfera/00_config.py`
- **Dados mock gerados**: 7 CSVs em `data/mock/output/csv/`

## Estrutura

```
api/dadosfera/
├── 00_config.py                        ← credenciais, URLs, constantes
├── 01_auth/authenticate.py             ← FASE 1: login → token
├── 02_integrar/upload_raw_files.py     ← FASE 2: upload CSV → Storage /raw/
├── 03_criar_tabelas/create_snowflake_tables.py  ← FASE 3: tabelas Snowflake
├── 04_vincular/link_datasets_to_tables.py       ← FASE 4: dataset → tabela
├── 05_catalogar/catalog_assets.py      ← FASE 5: catálogo + relatório
├── run_pipeline.py                     ← orquestrador (todas as fases)
└── .state/                             ← estado persistido (auto-gerado)
    ├── auth_tokens.json
    ├── uploaded_datasets.json
    ├── created_tables.json
    ├── linked_datasets.json
    └── catalog_report.md
```

## Configuração

Edite `dadosfera/00_config.py` com suas credenciais:

```python
DADOSFERA_USERNAME      = "seu-email@exemplo.com"
DADOSFERA_PASSWORD      = "sua-senha"
DADOSFERA_CUSTOMER_NAME = "seu-customer"
```

> ⚠️ **Nunca commite credenciais reais.** O `.gitignore` já protege `.state/`.

## Execução

### Todas as fases de uma vez

```bash
python api/dadosfera/run_pipeline.py
```

### Fase individual

```bash
python api/dadosfera/run_pipeline.py --fase 1    # apenas autenticação
python api/dadosfera/run_pipeline.py --fase 2    # apenas upload
```

### Parar após fase N

```bash
python api/dadosfera/run_pipeline.py --stop-after 3   # fases 1, 2 e 3
```

### Continuar mesmo com erros

```bash
python api/dadosfera/run_pipeline.py --continuar-em-erros
```

### Executar diretamente (sem orquestrador)

```bash
python api/dadosfera/01_auth/authenticate.py
python api/dadosfera/02_integrar/upload_raw_files.py
python api/dadosfera/03_criar_tabelas/create_snowflake_tables.py
python api/dadosfera/04_vincular/link_datasets_to_tables.py
python api/dadosfera/05_catalogar/catalog_assets.py
```

## Fases do Pipeline

| Fase | Script | Endpoint API | Entrada | Saída |
|------|--------|-------------|---------|-------|
| 1 | `authenticate.py` | `POST /auth/sign-in` | Credenciais | `auth_tokens.json` |
| 2 | `upload_raw_files.py` | `POST /storage-explorer/storage/upload/batch` | 7 CSVs | `uploaded_datasets.json` |
| 3 | `create_snowflake_tables.py` | `POST /storage-explorer/tables` | Schemas das entidades | `created_tables.json` |
| 4 | `link_datasets_to_tables.py` | `POST /tables/{id}/datasets` | IDs das fases 2+3 | `linked_datasets.json` |
| 5 | `catalog_assets.py` | `GET /catalog` | Token | `catalog_report.md` |

## Validação Pós-Execução

1. **Fase 1**: Token gerado → `.state/auth_tokens.json` existe
2. **Fase 2**: 7 uploads com `status: success` → verificar no Storage Explorer em `/raw/recuperacao_carrinho/`
3. **Fase 3**: 7 tabelas criadas no schema `CART_RECOVERY`
4. **Fase 4**: 7 vínculos dataset→tabela confirmados
5. **Fase 5**: Relatório em `.state/catalog_report.md` com inventário dos ativos

## Troubleshooting

| Erro | Causa | Solução |
|------|-------|---------|
| `401 Unauthorized` | Token expirado | Re-executar Fase 1 |
| `FileNotFoundError: Token nao encontrado` | Fase 1 não executada | Executar `--fase 1` primeiro |
| `FileNotFoundError: uploaded_datasets` | Fase 2 não executada | Executar fases em ordem |
| `Connection timeout` | API instável | Tentar novamente; aumentar timeout em `00_config.py` |

## Arquitetura Data Lake

```
/raw/recuperacao_carrinho/        ← Zona RAW (dados brutos CSV)
│── clientes.csv
│── produtos.csv
│── carrinhos.csv
│── itens_carrinho.csv
│── eventos_carrinho.csv          ← 72k+ registros
│── eventos_resgate.csv
└── pedidos.csv

Snowflake: CART_RECOVERY          ← Zona QUALIFY (tabelas catalogadas)
│── clientes        (2.000 linhas)
│── produtos        (500 linhas)
│── carrinhos       (15.000 linhas)
│── itens_carrinho  (22.500 linhas)
│── eventos_carrinho(72.026 linhas)
│── eventos_resgate (2.500 linhas)
└── pedidos         (2.000 linhas)
```

---

*Pipeline do case técnico de estágio Dadosfera — Pedro Sales — Agosto 2026*
