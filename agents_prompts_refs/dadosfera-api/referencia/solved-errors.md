# Erros Conhecidos e Soluções — API Dadosfera

Registro resumido dos erros técnicos identificados durante a integração com a API Maestro e suas respectivas soluções.

---

### 1. Header de Autenticação

- **Endpoint:** Todos os endpoints autenticados
- **Erro:** `401 Unauthorized`
- **Causa:** Envio do prefixo `Bearer ` no cabeçalho HTTP (`Authorization: Bearer <token>`).
- **Solução:** Enviar apenas o token JWT puro: `Authorization: <token>`.

---

### 2. Payload e Resposta de Sign-In

- **Endpoint:** `POST /auth/sign-in`
- **Erro:** `400 Bad Request` ou `KeyError: 'accessToken'`
- **Causa:** Envio de chave `email` em vez de `username` no body, e tentativa de ler `data["accessToken"]` diretamente (o token vem aninhado em `data["tokens"]["accessToken"]`).
- **Solução:** Usar `{"username": ...}` no body e extrair via `data.get("tokens", {}).get("accessToken") or data.get("accessToken")`.

---

### 3. Upload Direto no Storage

- **Endpoint:** `POST /storage-explorer/storage/upload/batch`
- **Erro:** `403 Forbidden` (`AUTH.FORBIDDEN`)
- **Causa:** Role `Candidatos` no tenant de treinamento não possui privilégio para upload de infraestrutura direta via API.
- **Solução:** Realizar a ingestão dos arquivos CSV via interface web no módulo **Coletar / Importar Arquivos** (`app.dadosfera.ai`).

---

### 4. Criação e Vinculação de Tabelas Snowflake

- **Endpoint:** `POST /storage-explorer/tables` e `POST /storage-explorer/tables/{id}/datasets`
- **Erro:** `403 Forbidden`
- **Causa:** Permissão restrita na conta de estágio para manipulação direta de DDL e links de tabelas no banco de dados via API.
- **Solução:** Criação e vínculo de tabelas operados automaticamente pela UI da Dadosfera durante a importação no módulo de Coleta.

---

### 5. Duplicação de Ativos no Catálogo

- **Endpoint:** `POST /catalog`
- **Erro:** Criação de múltiplos Data Assets com o mesmo nome na UI (duplicatas visuais).
- **Causa:** A API não valida unicidade por `display_name` e gera um novo UUID a cada chamada `POST`.
- **Solução:** Consultar ativos existentes via `GET /catalog` antes e usar `PUT /catalog/data-asset/{id}` para atualizar se o ativo já existir.

---

### 6. Exclusão de Ativos via API

- **Endpoint:** `DELETE /catalog/data-asset/{id}`
- **Erro:** `403 Forbidden`
- **Causa:** A conta de estágio não possui a permissão `catalog:delete` ativa.
- **Solução:** Isolar duplicatas via `PUT` renomeando para `[DUPLICATA - IGNORAR]` com tag `lixeira` e excluir/arquivar manualmente pela UI.

---

### 7. Codificação no Terminal Windows

- **Endpoint:** Execução local dos scripts Python (`01_auth`, `run_pipeline.py`, etc.)
- **Erro:** `UnicodeEncodeError: 'charmap' codec can't encode character '\u2713'`
- **Causa:** Console Windows em `cp1252` falha ao imprimir símbolos Unicode (`✓`, `✗`).
- **Solução:** Substituir caracteres especiais por texto ASCII-safe (`[OK]`, `[ERRO]`, `[AVISO]`).
