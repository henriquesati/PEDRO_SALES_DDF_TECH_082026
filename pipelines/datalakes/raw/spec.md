# 📥 Especificação Imutável: Camada Raw (Bronze / Ingestão Bruta)

> **Doc ID:** `spec_datalake_raw_001`  
> **Camada:** `Raw (Bronze)`  
> **Natureza:** Objeto Imutável de Especificação de Ingestão  
> **Localização Física:** S3 Explorer Dadosfera (`/raw/recuperacao_carrinho/`)  
> **Formato de Carga:** Arquivos binários `Parquet`  
> **Status:** ✅ Homologado & Ativo  

---

## 1. 📌 Objetivo e Princípios da Camada Raw

A camada **Raw (Bronze)** atua como a zona de aterrissagem (*landing zone*) bruta e imutável para todos os dados transacionais, cadastrais e de telemetria do case de Recuperação de Carrinho Abandonado. 

### Princípios Fundamentais:
1. **Preservação Integral ("As-Is"):** Nenhum dado de negócio é alterado, tipado agressivamente ou descartado nesta etapa. Erros, tipos textuais mistos e anomalias de origem são armazenados exatamente como emitidos pelas fontes.
2. **Imutabilidade e Replayability:** Os arquivos gravados nesta camada nunca sofrem `UPDATE` ou `DELETE`. Servem como a fonte primária de verdade histórica para reprocessamento de pipelines downstream a qualquer momento.
3. **Injeção de Metadados Técnicos:** Cada carga bruta recebe metadados de auditoria de ingestão (`_ingested_at`, `_source_file_path`, `_batch_id`) sem interferir no payload original.

---

## 2. 📋 Entidades Integradas na Camada Raw

A camada Raw organiza suas 7 entidades em diretórios dedicados, onde coabitam o dataset bruto e sua especificação de catálogo:

- **`carrinhos_raw`**: Sessões e estados de intenção de compra originados da webstore e app móvel.
- **`pedidos_raw`**: Compras finalizadas e liquidadas extraídas do ERP transacional e checkout.
- **`clientes_raw`**: Base cadastral e de consentimento (opt-ins) do CRM corporativo.
- **`produtos_raw`**: Catálogo de SKUs, categorias e tabela de preços exportados do PIM.
- **`itens_carrinho_raw`**: Detalhamento unitário de mercadorias adicionadas ou removidas de cada carrinho.
- **`eventos_carrinho_raw`**: Telemetria contínua de clickstream e etapas do fluxo de checkout.
- **`eventos_resgate_raw`**: Disparos de réguas de CRM e registros de engajamento do funil de marketing.

---

## 3. 🔍 Validações de Ingestão em Texto Corrido por Entidade

Diferente das camadas analíticas, a validação na camada Raw foca exclusivamente em sanidade de transporte, integridade de arquivo e persistência física. As regras de tipo, obrigatoriedade de campos e integridade de negócio correspondem às **validações declaradas no corpo da entidade**:

- **Entidade `carrinhos_raw`**: A validação assegura a legibilidade do arquivo Parquet e a presença das colunas estruturais básicas de sessão. Eventuais incoerências contábeis são preservadas para roteamento na camada seguinte, conforme as validações declaradas no corpo da entidade.
- **Entidade `pedidos_raw`**: O processo confirma a integridade de compressão e o cabeçalho do lote diário de pedidos, preservando ordens canceladas e estornadas para fins de conciliação financeira.
- **Entidade `clientes_raw`**: Valida a presença dos atributos cadastrais sob criptografia at-rest AES-256 no bucket de landing, resguardando os dados pessoais conforme as diretrizes de governança.
- **Entidade `produtos_raw`**: Confere a codificação UTF-8 do catálogo para preservar a integridade de caracteres e acentuações de nomes de produtos brasileiros.
- **Entidade `itens_carrinho_raw`**: Inspeciona a integridade das tuplas contra perdas de pacotes ou truncamentos de transferência entre microserviços e o storage.
- **Entidade `eventos_carrinho_raw`**: Monitora a sequência cronológica dos blocos de telemetria ingeridos e a padronização dos timestamps brutos.
- **Entidade `eventos_resgate_raw`**: Garante que o lote recebido da plataforma de marketing contém todos os campos necessários para posterior apuração do funil de resgate.

---

## 4. 🔗 Linhagem e Rastreabilidade

```mermaid
flowchart LR
    S1[Webstore / App] --> R2[carrinhos_raw]
    S1 --> R3[itens_carrinho_raw]
    S1 --> R6[eventos_carrinho_raw]
    S2[ERP / Checkout] --> R1[pedidos_raw]
    S3[CRM / Cadastros] --> R4[clientes_raw]
    S4[Catálogo / PIM] --> R5[produtos_raw]
    S5[Marketing Hub] --> R7[eventos_resgate_raw]

    R1 --> Q1[qualify.pedidos]
    R2 --> Q2[qualify.carrinhos]
    R3 --> Q3[qualify.itens_carrinho]
    R4 --> Q4[qualify.clientes]
    R5 --> Q5[qualify.produtos]
    R6 --> Q6[qualify.eventos_carrinho]
    R7 --> Q7[qualify.eventos_resgate]
```

> **Próxima Etapa:** Os dados brutos desta camada são consumidos pelos pipelines de qualidade e bifurcados de acordo com a [Especificação da Camada Qualify](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/datalakes/qualify/spec.md) e a [Especificação da Camada Anomaly](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/datalakes/anomaly/spec.md).
