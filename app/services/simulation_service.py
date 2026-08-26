"""Serviço puro de cálculo financeiro, simulação de resgate, sensibilidade de ROI e rebalanceamento."""

from typing import Sequence, Tuple, Mapping
import pandas as pd

from app.constants.settings import (
    CUSTO_POR_DISPARO,
    DEFAULT_TICKET_MEDIO,
    PRESCRIBED_MIX,
    TAXA_CONVERSAO_POR_CANAL,
)
from app.types.models import (
    ChannelAllocation,
    ChannelSimulationResult,
    SimulationInput,
    SimulationOutput,
)

def calculate_channel_result(
    allocation: ChannelAllocation,
    discount_pct: float,
    elasticity: float,
    average_ticket: float,
) -> ChannelSimulationResult:
    """Calcula a projeção de receita e custos para um único canal (Função Pura)."""
    # Elasticidade de conversão impulsionada pelo cupom
    effective_conversion = min(
        1.0,
        allocation.base_conversion_rate * (1.0 + (elasticity * (discount_pct / 100.0)))
    )
    
    recovered = int(round(allocation.dispatches_count * effective_conversion))
    gross_revenue = recovered * average_ticket
    comm_cost = allocation.dispatches_count * allocation.cost_per_dispatch
    disc_cost = gross_revenue * (discount_pct / 100.0)
    total_cost = comm_cost + disc_cost
    net_revenue = gross_revenue - total_cost
    
    roi = (net_revenue / total_cost) if total_cost > 0 else 0.0
    
    return ChannelSimulationResult(
        channel=allocation.channel,
        dispatches=allocation.dispatches_count,
        recovered_carts=recovered,
        conversion_rate_pct=round(effective_conversion * 100.0, 2),
        gross_recovered_revenue=round(gross_revenue, 2),
        communication_cost=round(comm_cost, 2),
        discount_cost=round(disc_cost, 2),
        net_recovered_revenue=round(net_revenue, 2),
        roi_multiplier=round(roi, 2),
    )

def run_simulation(input_data: SimulationInput) -> SimulationOutput:
    """Executa a simulação orçamentária completa de forma declarativa e pura."""
    channel_results = tuple(
        calculate_channel_result(
            alloc,
            input_data.discount_pct,
            input_data.conversion_elasticity,
            input_data.average_ticket,
        )
        for alloc in input_data.channel_allocations
    )
    
    total_dispatches = sum(r.dispatches for r in channel_results)
    total_recovered = sum(r.recovered_carts for r in channel_results)
    blended_conv = (total_recovered / total_dispatches * 100.0) if total_dispatches > 0 else 0.0
    
    total_gross = sum(r.gross_recovered_revenue for r in channel_results)
    total_comm = sum(r.communication_cost for r in channel_results)
    total_disc = sum(r.discount_cost for r in channel_results)
    total_net = sum(r.net_recovered_revenue for r in channel_results)
    total_investment = total_comm + total_disc
    
    overall_roi = (total_net / total_investment) if total_investment > 0 else 0.0
    
    # Cálculo de Margem Preservada (Baseline comercial 32.0% bruta - desconto - custo)
    base_gross_margin = 0.320
    effective_net_margin = (base_gross_margin * total_gross - total_investment) / (total_gross if total_gross > 0 else 1.0)
    preserved_margin_pct = max(0.0, round(effective_net_margin * 100.0, 1))

    return SimulationOutput(
        total_dispatches=total_dispatches,
        total_recovered_carts=total_recovered,
        blended_conversion_rate_pct=round(blended_conv, 2),
        total_gross_revenue=round(total_gross, 2),
        total_communication_cost=round(total_comm, 2),
        total_discount_cost=round(total_disc, 2),
        total_net_revenue=round(total_net, 2),
        overall_roi_multiplier=round(overall_roi, 2),
        preserved_margin_pct=preserved_margin_pct,
        channel_breakdown=channel_results,
    )

def create_preset_simulation_input(
    total_carrinhos: int = 7500,
    ticket_medio: float = DEFAULT_TICKET_MEDIO,
    discount_pct: float = 0.0,
    elasticity: float = 1.2,
    mix: Mapping[str, float] = PRESCRIBED_MIX,
) -> SimulationInput:
    """Gera o objeto de entrada com preset de canais parametrizado."""
    allocations = (
        ChannelAllocation(
            channel="Email",
            share_pct=mix.get("Email", 0.85),
            dispatches_count=int(total_carrinhos * mix.get("Email", 0.85)),
            cost_per_dispatch=CUSTO_POR_DISPARO["Email"],
            base_conversion_rate=TAXA_CONVERSAO_POR_CANAL["Email"],
        ),
        ChannelAllocation(
            channel="WhatsApp",
            share_pct=mix.get("WhatsApp", 0.12),
            dispatches_count=int(total_carrinhos * mix.get("WhatsApp", 0.12)),
            cost_per_dispatch=CUSTO_POR_DISPARO["WhatsApp"],
            base_conversion_rate=TAXA_CONVERSAO_POR_CANAL["WhatsApp"],
        ),
        ChannelAllocation(
            channel="SMS",
            share_pct=mix.get("SMS", 0.02),
            dispatches_count=int(total_carrinhos * mix.get("SMS", 0.02)),
            cost_per_dispatch=CUSTO_POR_DISPARO["SMS"],
            base_conversion_rate=TAXA_CONVERSAO_POR_CANAL["SMS"],
        ),
        ChannelAllocation(
            channel="Push",
            share_pct=mix.get("Push", 0.01),
            dispatches_count=int(total_carrinhos * mix.get("Push", 0.01)),
            cost_per_dispatch=CUSTO_POR_DISPARO["Push"],
            base_conversion_rate=TAXA_CONVERSAO_POR_CANAL["Push"],
        ),
    )
    
    return SimulationInput(
        total_abandoned_carts=total_carrinhos,
        average_ticket=ticket_medio,
        discount_pct=discount_pct,
        conversion_elasticity=elasticity,
        channel_allocations=allocations,
    )

def generate_discount_sensitivity_curve(
    base_input: SimulationInput,
    discount_steps: Sequence[float] = (0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0)
) -> pd.DataFrame:
    """Gera uma matriz de sensibilidade variando o percentual de desconto."""
    rows: list[dict] = []
    for disc in discount_steps:
        scenario_input = SimulationInput(
            total_abandoned_carts=base_input.total_abandoned_carts,
            average_ticket=base_input.average_ticket,
            discount_pct=disc,
            conversion_elasticity=base_input.conversion_elasticity,
            channel_allocations=base_input.channel_allocations,
        )
        out = run_simulation(scenario_input)
        rows.append({
            "Desconto (%)": disc,
            "Taxa Conversão (%)": out.blended_conversion_rate_pct,
            "Carrinhos Recuperados": out.total_recovered_carts,
            "Receita Bruta (R$)": out.total_gross_revenue,
            "Custo Total (R$)": out.total_communication_cost + out.total_discount_cost,
            "Receita Líquida (R$)": out.total_net_revenue,
            "ROI Multiplicador": out.overall_roi_multiplier,
            "Margem Preservada (%)": out.preserved_margin_pct,
        })
    return pd.DataFrame(rows)
