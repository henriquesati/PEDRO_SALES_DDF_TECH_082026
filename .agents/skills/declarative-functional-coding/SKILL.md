---
name: declarative-functional-coding
description: "Skill para orientar a geração de código sob o paradigma funcional e declarativo, com tipagem estrita (Type Annotations), pipelines modelados como sequências de funções puras de validação/transformação, alta modularidade e constantes centralizadas para fácil alternância de configurações e perfis."
---

# 🧠 Skill: Declarative & Functional Coding Standards

## 🎯 Objetivo da Skill
Padronizar a escrita de código em Python e pipelines de engenharia de dados sob os princípios do **paradigma funcional declarativo**, garantindo:
1. **Imutabilidade e Funções Puras:** Código determinístico, sem efeitos colaterais ocultos e fácil de testar.
2. **Pipelines Declarativos:** Pipelines compostos por listas/tuplas de funções tipadas (`Callable`), explicitando cada estágio de transformação e validação.
3. **Tipagem Estrita (Type Annotations):** Uso abrangente de `typing` (`Callable`, `TypeAlias`, `NamedTuple`, `TypedDict`, `Literal`, `Protocol`, `dataclass(frozen=True)`).
4. **Configuração Desacoplada & Constantes:** Centralização de constantes e parâmetros em módulos de settings imutáveis (`Final`), permitindo troca instantânea de perfis (`dev`, `standard`, `rich`).
5. **Modularidade e Pattern Matching:** Separação estrita de responsabilidades em módulos coesos e uso de dispatch tables declarativas em vez de `if/else` imperativos aninhados.

---

## 🏛️ Diretrizes e Regras de Ouro

### 1. 🛡️ Imutabilidade e Pureza
- **Funções Puras:** Devem receber dados de entrada e retornar um novo dado transformado, sem modificar as entradas originais.
- **Proibição de Efeitos Colaterais em Lógica de Negócio:** Mutações *in-place* (ex.: `df.drop(..., inplace=True)`, `list.sort()`) **MUST NOT** ser utilizadas.
- **Modelos de Dados Imutáveis:** Usar `@dataclass(frozen=True)` ou `NamedTuple` para contratos de dados.

### 2. 🧩 Pipelines como Sequências de Funções (Array of Callables)
- Trate pipelines como fluxos de dados direcionados compostos por funções puras encadeadas:
  $$\text{Output} = f_n(\dots(f_2(f_1(\text{Input}))))$$
- Um pipeline de validação ou transformação **MUST** ser declarado como uma lista/tupla de funções tipadas:

```python
PipelineStep: TypeAlias = Callable[[pd.DataFrame], pd.DataFrame]
ValidationRule: TypeAlias = Callable[[pd.DataFrame], ValidationResult]

CLEANING_PIPELINE: tuple[PipelineStep, ...] = (
    remove_null_keys,
    sanitize_negative_shipping,
    standardize_status_column,
    recalculate_totals
)
```

### 3. ⚙️ Constantes e Fácil Switch de Configuração
- Valores literais (strings mágicas, números mágicos, percentuais) **MUST NOT** estar espalhados no código executável.
- Centralize parâmetros em `config/settings.py` com tipos `Final` e dicionários de perfis.
- A alternância de comportamento (ex.: modo `dev` vs `standard`, taxas de erro, volumetria) deve ser feita alterando apenas a constante de perfil ativo.

---

## 📐 Padrões Canônicos de Implementação

### 1. Centralização Declarativa de Configurações & Perfis

```python
from typing import Final, Literal, TypedDict, Mapping
from types import MappingProxyType

ProfileName: TypeAlias = Literal["dev", "standard", "rich"]

class ProfileConfig(TypedDict):
    row_count: int
    anomaly_rate: float
    batch_size: int
    enable_profiling: bool

PROFILES: Final[Mapping[ProfileName, ProfileConfig]] = MappingProxyType({
    "dev": {
        "row_count": 10_000,
        "anomaly_rate": 0.02,
        "batch_size": 1_000,
        "enable_profiling": False,
    },
    "standard": {
        "row_count": 100_000,
        "anomaly_rate": 0.05,
        "batch_size": 10_000,
        "enable_profiling": True,
    },
    "rich": {
        "row_count": 250_000,
        "anomaly_rate": 0.08,
        "batch_size": 25_000,
        "enable_profiling": True,
    }
})

# Switch central instantâneo:
ACTIVE_PROFILE: Final[ProfileName] = "standard"
CURRENT_CONFIG: Final[ProfileConfig] = PROFILES[ACTIVE_PROFILE]
```

---

### 2. Estruturas de Dados de Validação e Resultados (Result Pattern)

```python
from dataclasses import dataclass
from typing import NamedTuple, Literal, TypeAlias, Sequence, Callable
import pandas as pd

Severity: TypeAlias = Literal["INFO", "WARNING", "CRITICAL"]

@dataclass(frozen=True)
class ValidationResult:
    rule_name: str
    dimension: str
    passed: bool
    affected_count: int
    severity: Severity
    description: str

ValidationRule: TypeAlias = Callable[[pd.DataFrame], ValidationResult]

# Exemplo de Regras de Validação Puras
def validate_no_null_pks(df: pd.DataFrame) -> ValidationResult:
    nulls = int(df["carrinho_id"].isna().sum())
    return ValidationResult(
        rule_name="PK_NOT_NULL",
        dimension="Completeness",
        passed=(nulls == 0),
        affected_count=nulls,
        severity="CRITICAL",
        description="Identificadores de carrinho não podem ser nulos."
    )

def validate_positive_shipping(df: pd.DataFrame) -> ValidationResult:
    negatives = int((df["valor_frete"] < 0).sum())
    return ValidationResult(
        rule_name="NON_NEGATIVE_SHIPPING",
        dimension="Validity",
        passed=(negatives == 0),
        affected_count=negatives,
        severity="WARNING",
        description="Valores de frete não podem ser negativos."
    )

# Matriz Declarativa de Validação
DATA_QUALITY_SUITE: Final[tuple[ValidationRule, ...]] = (
    validate_no_null_pks,
    validate_positive_shipping,
)

def run_validation_suite(
    df: pd.DataFrame, 
    rules: Sequence[ValidationRule] = DATA_QUALITY_SUITE
) -> tuple[ValidationResult, ...]:
    return tuple(rule(df) for rule in rules)
```

---

### 3. Composição de Pipelines Funcionais (Pipe / Compose)

```python
from functools import reduce
from typing import Callable, TypeAlias, Sequence
import pandas as pd

TransformFn: TypeAlias = Callable[[pd.DataFrame], pd.DataFrame]

def sanitize_shipping(df: pd.DataFrame) -> pd.DataFrame:
    """Função pura que retorna novo DataFrame com frete sanitizado."""
    return df.assign(valor_frete=df["valor_frete"].abs())

def recalculate_totals(df: pd.DataFrame) -> pd.DataFrame:
    """Recalcula total financeiro de forma determinística e contábil."""
    return df.assign(
        valor_total=df["valor_subtotal"] + df["valor_frete"] - df["valor_desconto"]
    )

def apply_status_normalization(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza strings de status para maiúsculo sem espaços."""
    return df.assign(status=df["status"].str.strip().str.upper())

# Lista Declarativa de Transformações (Pipeline)
SILVER_TRANSFORMATION_STEPS: Final[tuple[TransformFn, ...]] = (
    sanitize_shipping,
    recalculate_totals,
    apply_status_normalization,
)

def pipe(data: pd.DataFrame, *steps: TransformFn) -> pd.DataFrame:
    """Executa a composição funcional sequencial: f_n(...f_2(f_1(data)))."""
    return reduce(lambda current_df, step_fn: step_fn(current_df), steps, data)

def execute_silver_pipeline(
    raw_df: pd.DataFrame, 
    steps: Sequence[TransformFn] = SILVER_TRANSFORMATION_STEPS
) -> pd.DataFrame:
    return pipe(raw_df, *steps)
```

---

### 4. Dispatch Declarativo em Substituição a `if/elif/else`

```python
from typing import Callable, Mapping, Final
from types import MappingProxyType

ActionHandler: TypeAlias = Callable[[pd.DataFrame, str], pd.DataFrame]

def handle_sanitize(df: pd.DataFrame, col: str) -> pd.DataFrame:
    return df.assign(**{col: df[col].abs()})

def handle_quarantine(df: pd.DataFrame, col: str) -> pd.DataFrame:
    return df[df[col].notna()].copy()

def handle_default(df: pd.DataFrame, col: str) -> pd.DataFrame:
    return df

# Tabela de despacho funcional imutável
DISPATCH_TABLE: Final[Mapping[str, ActionHandler]] = MappingProxyType({
    "SANITIZE_NUMERIC": handle_sanitize,
    "ISOLATE_RECORDS": handle_quarantine,
    "PASSTHROUGH": handle_default,
})

def route_action(action_key: str, df: pd.DataFrame, target_column: str) -> pd.DataFrame:
    handler = DISPATCH_TABLE.get(action_key, handle_default)
    return handler(df, target_column)
```

---

## 🚫 Anti-Patterns a Evitar

| Anti-Pattern Imperativo | Padrão Funcional Declarativo Recomendado |
|---|---|
| Mutações *in-place* (`df['x'] = y`, `df.drop(inplace=True)`) | Métodos funcionais encadeados ou `.assign()`, retornando cópias explícitas |
| Cadeias de 10 `if/elif` aninhadas para decidir transformações | Tabela de despacho (*dispatch dict*) `Mapping[Key, Callable]` |
| Classes monolíticas acumulando estado interno mutável | Módulos desacoplados contendo funções puras e tipos imutáveis |
| Hardcoded de regras e valores no corpo das funções | Constantes declarativas em `settings.py` e argumentos com defaults tipados |
| Código não tipado (`def func(data):`) | Tipagem explícita (`def func(data: pd.DataFrame) -> ProcessedBatch:`) |

---

## ✅ Checklist de Revisão de Código Funcional

- [ ] Todas as funções possuem **Type Annotations** completas de entrada e retorno.
- [ ] Não há mutações diretas em argumentos de funções.
- [ ] Constantes, limites e perfis estão centralizados em arquivo de configurações.
- [ ] Pipelines de dados estão modelados como tuplas/listas de funções de transformação (`tuple[Callable, ...]`).
- [ ] Validações retornam objetos de resultado tipados (`ValidationResult`) em vez de simples prints ou booleanos opacos.
- [ ] O código é determinístico: para a mesma entrada, sempre produz a mesma saída.
