"""Módulo de validadores funcionais por entidade do Item 8."""
from .registry import ENTITY_VALIDATION_REGISTRY, get_validators_for_entity, evaluate_entity_rules
from .carrinhos import VALIDATION_CARRINHOS
from .clientes import VALIDATION_CLIENTES
from .produtos import VALIDATION_PRODUTOS
from .itens_carrinho import VALIDATION_ITENS_CARRINHO
from .eventos_resgate import VALIDATION_EVENTOS_RESGATE
