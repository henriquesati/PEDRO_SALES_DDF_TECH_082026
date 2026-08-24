"""
Registro Central e Dispatcher Declarativo de Validações (Item 8 - Dadosfera)
Mapeia cada entidade para sua tupla de validações puras.
"""

from types import MappingProxyType
from typing import Final, Mapping
import pandas as pd

from core.types import ValidationResult, ValidationRule
from validators.carrinhos import VALIDATION_CARRINHOS
from validators.clientes import VALIDATION_CLIENTES
from validators.produtos import VALIDATION_PRODUTOS
from validators.itens_carrinho import VALIDATION_ITENS_CARRINHO
from validators.eventos_resgate import VALIDATION_EVENTOS_RESGATE

# =============================================================================
# 🏛️ Dispatcher Central Imutável (Mapping of Callable Arrays)
# =============================================================================

ENTITY_VALIDATION_REGISTRY: Final[Mapping[str, tuple[ValidationRule, ...]]] = MappingProxyType(
    {
        "carrinhos": VALIDATION_CARRINHOS,
        "clientes": VALIDATION_CLIENTES,
        "produtos": VALIDATION_PRODUTOS,
        "itens_carrinho": VALIDATION_ITENS_CARRINHO,
        "eventos_resgate": VALIDATION_EVENTOS_RESGATE,
        "eventos_carrinho": (),  # Telemetria bruta
        "pedidos": (),           # Faturamento direto
    }
)


def get_validators_for_entity(entity_name: str) -> tuple[ValidationRule, ...]:
    """Retorna de forma declarativa o array de funções de validação da entidade."""
    return ENTITY_VALIDATION_REGISTRY.get(entity_name, ())


def evaluate_entity_rules(entity_name: str, df: pd.DataFrame) -> tuple[ValidationResult, ...]:
    """Executa de forma pura todas as funções de validação registradas para uma entidade."""
    validators = get_validators_for_entity(entity_name)
    return tuple(validator_fn(df) for validator_fn in validators)
