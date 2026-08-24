# Blueprint: Modelo de Dicionário de Dados & Catálogo

Este é o modelo padronizado (blueprint) adotado para documentação de ativos de dados e dicionários de dados do case de **Recuperação de Carrinho Abandonado**. Toda documentação do catálogo de dados deve seguir rigorosamente esta estrutura.

---

## 📌 Identificação do Ativo de Dados

- **Nome Físico:** `[nome_tabela_ou_arquivo]`
- **Nome de Exibição (Display Name):** `[Nome Amigável do Ativo]`
- **Data Asset ID (Dadosfera):** `[UUID da Dadosfera]`
- **URL Direta no Catálogo:** `[https://app.dadosfera.ai/.../uuid]`

---

## 💼 Visão de Negócio

### Descrição de Negócio
`[Explicar em linguagem humana simples para que serve este ativo do ponto de vista de negócio. Qual processo operacional ou decisão estratégica ele apoia?]`

### Principais Casos de Uso
- `[Caso de uso 1: ex. Identificar clientes em potencial para resgate]`
- `[Caso de uso 2: ex. Calcular taxa de conversão por categoria de produto]`

---

## ⚙️ Visão Técnica

### Especificações Gerais
- **Zona do Data Lakehouse:** `[Raw (Bronze) / Qualify (Silver) / Curated (Gold)]`
- **Formato Físico:** `[CSV / Snowflake Table / Parquet / View]`
- **Localização Física:** `[Caminho no Storage ou Schema.Tabela no Snowflake]`
- **Granularidade:** `[O que cada linha representa, ex: Um item adicionado por carrinho]`
- **Frequência de Atualização:** `[Batch diário / Near Real-Time / Event-driven / Estático]`
- **Volume de Registros:** `[Ex: 15.000 registros (~1.6 MB)]`

### Integridade e Relacionamentos (Linhagem)
- **Origem (Lineage Upstream):** `[De qual arquivo ou processo este ativo é gerado]`
- **Destino (Lineage Downstream):** `[Para quais tabelas, views ou dashboards este ativo envia dados]`
- **Chave Primária (PK):** `[Coluna(s) que identificam unicamente a linha]`
- **Chaves Estrangeiras (FK):**
  - `[coluna_fk]` ➔ `[tabela_destino].[coluna_destino]`

---

## 🛡️ Governança & Sensibilidade

- **Proprietário do Dado (Owner):** `[Área / E-mail]`
- **Classificação de Sensibilidade:** `[Público / Interno / Confidencial / Sensível (LGPD)]`
- **Tags de Governança:** `[carrinho_abandonado, tag_categoria, zone_name]`

---

## 📊 Dicionário de Atributos (Colunas)

| Campo Físico | Tipo de Dado | Chave | Nullable | Descrição de Negócio (A é um B que C) | Valores Válidos / Regras | Exemplo de Valor | PII? |
|:---|:---:|:---:|:---:|:---|:---|:---|:---:|
| `[nome_coluna_1]` | `[TIPO]` | `[PK/FK]` | `[S/N]` | `[A coluna_1 é um(a)... que...]` | `[Lista de valores ou limites]` | `[Exemplo]` | `[S/N]` |
| `[nome_coluna_2]` | `[TIPO]` | `[-]` | `[S/N]` | `[A coluna_2 é um(a)... que...]` | `[Regra ou Formato]` | `[Exemplo]` | `[S/N]` |

---

## 🧪 Regras de Qualidade de Dados (Data Quality)

As seguintes validações do Great Expectations/Soda Core são aplicadas a este ativo:
- **Unicidade:** `[Regra de unicidade na chave primária]`
- **Não-Nulidade:** `[Campos que obrigatoriamente devem ser preenchidos]`
- **Valores Permitidos:** `[Intervalos numéricos ou lista de categorias permitidas]`

---

## 📦 7. Formato de Saída Estruturado (JSON Output Specification — Dadosfera API Standard)

Para integração automatizada com o módulo **Explorar**, API Maestro (`https://maestro.dadosfera.ai`) e pipelines de CI/CD, todo ativo de dados e camada do Lakehouse Medallion **DEVE obrigatoriamente** gerar e manter um arquivo `metadata.json` estruturado no seguinte padrão:

```json
{
  "doc_id": "meta_[camada]_[entidade]_[versao]",
  "entity_name": "[nome_entidade]",
  "dadosfera_asset_id": "[UUID_oficial_na_dadosfera]",
  "direct_url": "https://app.dadosfera.ai/pt-BR/catalog/data-assets/[UUID]",
  "snowflake_table": "[DATABASE].[SCHEMA].[TABELA]",
  "format": "parquet | snowflake_table | view | csv",
  "storage_path": "[caminho_no_datalake_ou_storage]",
  "layer": "raw | qualify | anomaly | curated",
  "classification": "Público | Interno | Confidencial (PII)",
  "owner": "[Area_Responsavel]",
  "records_count": 0,
  "size_bytes": 0,
  "upstream": {
    "source": "[sistema_ou_tabela_de_origem]",
    "protocol": "[Batch S3 | API Maestro | Step N]",
    "process": "[Descricao_do_processamento]"
  },
  "downstream": [
    {
      "layer": "[camada_destino]",
      "target": "[tabela_ou_dashboard_destino]",
      "purpose": "[Finalidade_analitica_ou_consumo]"
    }
  ],
  "tags": [
    "carrinho_abandonado",
    "[nome_entidade]",
    "[camada]",
    "[tag_especifica]"
  ],
  "schema": {
    "[nome_coluna]": {
      "type": "VARCHAR | INT | FLOAT | TIMESTAMP | BOOLEAN",
      "nullable": true,
      "null_count": 0,
      "null_percentage": 0.0,
      "cardinality": 0,
      "business_role": "PK Natural | Surrogate Key | Medida / Métrica | Dimensão / Categoria | Atributo Temporal | Atributo Descritivo",
      "is_pii": false,
      "description": "[A coluna é um(a) B que C]",
      "sample_value": "[Exemplo]"
    }
  }
}
```
