"""
Transformações Funcionais: Silver (Qualify) -> Gold (Kimball Star Schema & Analytical Views)
Implementa a decisão DEC-008 e DEC-001 (Ratios em Execução).
"""

from typing import Final, Mapping
from types import MappingProxyType
import pandas as pd
import numpy as np


# =============================================================================
# 🏛️ Construção das Dimensões Conformadas (Pure Dimension Builders)
# =============================================================================

def build_dim_clientes(df_clientes_qualify: pd.DataFrame) -> pd.DataFrame:
    """Gera a dimensão conformada dim_clientes com surrogate key e atributos analíticos."""
    df = df_clientes_qualify.copy().reset_index(drop=True)
    df["cliente_sk"] = df.index + 1
    
    # Padronização de nomes e cálculo de recência
    if "data_ultima_compra" in df.columns:
        dt_last = pd.to_datetime(df["data_ultima_compra"], errors="coerce")
        ref_date = dt_last.max() if dt_last.notna().any() else pd.Timestamp.now()
        df["recencia_dias"] = (ref_date - dt_last).dt.days.fillna(30.0).astype(float)
    else:
        df["recencia_dias"] = 30.0

    if "total_compras" in df.columns:
        df["frequencia_compras"] = df["total_compras"].fillna(1.0).astype(float)
    else:
        df["frequencia_compras"] = 1.0

    if "lifetime_value" in df.columns:
        df["valor_monetario_ltv"] = df["lifetime_value"].fillna(100.0).astype(float)
    else:
        df["valor_monetario_ltv"] = 100.0

    if "churn_risk_score" not in df.columns:
        # Score de risco calibrado a partir de recência e frequência
        rec_factor = np.clip(df["recencia_dias"] / 90.0, 0.0, 1.0)
        freq_factor = np.clip(1.0 / np.maximum(df["frequencia_compras"], 1.0), 0.0, 1.0)
        df["churn_risk_score"] = np.round((rec_factor * 60.0 + freq_factor * 40.0), 2)

    cols_order = [
        "cliente_sk",
        "cliente_id",
        "email",
        "segmento_rfm",
        "status_ativo",
        "permite_email",
        "permite_sms",
        "permite_push",
        "recencia_dias",
        "frequencia_compras",
        "valor_monetario_ltv",
        "churn_risk_score",
    ]
    available_cols = [c for c in cols_order if c in df.columns]
    return df[available_cols].copy()


def build_dim_tempo(df_carrinhos: pd.DataFrame) -> pd.DataFrame:
    """Gera a dimensão de tempo padronizada a partir dos timestamps de carrinho."""
    dates = pd.to_datetime(df_carrinhos["data_criacao"]).dropna().dt.floor("D").unique()
    dates_series = pd.Series(dates).sort_values().reset_index(drop=True)
    
    df_tempo = pd.DataFrame({
        "data_sk": dates_series.dt.strftime("%Y%m%d").astype(int),
        "data": dates_series.dt.date,
        "ano": dates_series.dt.year,
        "mes": dates_series.dt.month,
        "trimestre": dates_series.dt.quarter,
        "ano_mes": dates_series.dt.strftime("%Y-%m"),
        "dia_semana_nome": dates_series.dt.day_name(),
        "eh_fim_semana": dates_series.dt.dayofweek.isin([5, 6]),
    })
    return df_tempo


def build_dim_dispositivo(df_carrinhos: pd.DataFrame) -> pd.DataFrame:
    """Gera a dimensão conformada de dispositivos de acesso."""
    devices = ["mobile", "desktop", "tablet"]
    return pd.DataFrame({
        "dispositivo_sk": [1, 2, 3],
        "dispositivo": devices,
        "fator_friccao_checkout": [1.35, 1.00, 1.15],
        "complexidade_checkout": ["Alta", "Baixa", "Media"],
    })


def build_dim_canal_resgate(df_resgates: pd.DataFrame) -> pd.DataFrame:
    """Gera a dimensão de canais de régua de comunicação com benchmarks."""
    canais = ["email", "sms", "whatsapp", "push_app"]
    return pd.DataFrame({
        "canal_sk": [1, 2, 3, 4],
        "canal": canais,
        "custo_unitario_envio": [0.05, 0.15, 0.40, 0.02],
        "taxa_abertura_benchmark": [0.22, 0.85, 0.90, 0.45],
        "taxa_conversao_benchmark": [0.03, 0.08, 0.12, 0.04],
    })


# =============================================================================
# 📊 Construção das Tabelas de Fatos Granulares (Pure Fact Builders)
# =============================================================================

def build_fato_abandono(
    df_carrinhos_qualify: pd.DataFrame,
    df_dim_clientes: pd.DataFrame,
    df_dim_dispositivo: pd.DataFrame,
) -> pd.DataFrame:
    """Gera a tabela fato granular de sessões de abandono (1 linha por carrinho abandonado)."""
    df_abandono = df_carrinhos_qualify[
        df_carrinhos_qualify["status"].isin(["abandonado", "expirado"])
    ].copy().reset_index(drop=True)
    
    df_abandono["fato_abandono_sk"] = df_abandono.index + 1
    
    # JOINs funcionais com chaves surrogate
    if "cliente_id" in df_dim_clientes.columns and "cliente_sk" in df_dim_clientes.columns:
        cli_map = df_dim_clientes.set_index("cliente_id")["cliente_sk"].to_dict()
        df_abandono["cliente_sk"] = df_abandono["cliente_id"].map(cli_map).fillna(0).astype(int)
    else:
        df_abandono["cliente_sk"] = 0

    disp_map = df_dim_dispositivo.set_index("dispositivo")["dispositivo_sk"].to_dict()
    df_abandono["dispositivo_sk"] = df_abandono["dispositivo"].map(disp_map).fillna(1).astype(int)
    
    if "data_criacao" in df_abandono.columns:
        df_abandono["data_sk"] = pd.to_datetime(df_abandono["data_criacao"]).dt.strftime("%Y%m%d").fillna(0).astype(int)
    else:
        df_abandono["data_sk"] = 0

    # Medidas analíticas
    df_abandono["valor_total_em_risco"] = df_abandono["valor_total"]
    
    cols = [
        "fato_abandono_sk",
        "carrinho_id",
        "cliente_sk",
        "dispositivo_sk",
        "data_sk",
        "status",
        "motivo_abandono",
        "valor_subtotal",
        "valor_frete",
        "valor_desconto",
        "valor_total_em_risco",
        "duracao_sessao_minutos",
    ]
    available_cols = [c for c in cols if c in df_abandono.columns]
    return df_abandono[available_cols].copy()


def build_fato_resgate(
    df_resgates_qualify: pd.DataFrame,
    df_carrinhos_qualify: pd.DataFrame,
    df_dim_canal: pd.DataFrame,
) -> pd.DataFrame:
    """Gera a tabela fato granular de disparos e recuperação de CRM."""
    df_resgate = df_resgates_qualify.copy().reset_index(drop=True)
    df_resgate["fato_resgate_sk"] = df_resgate.index + 1
    
    canal_map = df_dim_canal.set_index("canal")["canal_sk"].to_dict()
    df_resgate["canal_sk"] = df_resgate["canal"].map(canal_map).fillna(1).astype(int)
    
    if "data_envio" in df_resgate.columns:
        df_resgate["data_sk"] = pd.to_datetime(df_resgate["data_envio"]).dt.strftime("%Y%m%d").fillna(0).astype(int)
    else:
        df_resgate["data_sk"] = 0

    # Flags de funil
    if "sucesso" in df_resgate.columns:
        df_resgate["flag_convertido"] = df_resgate["sucesso"].astype(int)
    else:
        df_resgate["flag_convertido"] = df_resgate["data_conversao"].notna().astype(int)

    df_resgate["flag_aberto"] = df_resgate["data_abertura"].notna().astype(int)
    
    if "data_primeiro_clique" in df_resgate.columns:
        df_resgate["flag_clicado"] = df_resgate["data_primeiro_clique"].notna().astype(int)
    elif "data_clique" in df_resgate.columns:
        df_resgate["flag_clicado"] = df_resgate["data_clique"].notna().astype(int)
    else:
        df_resgate["flag_clicado"] = 0

    # Cruzamento com valor do carrinho para atribuição de receita
    if "carrinho_id" in df_carrinhos_qualify.columns and "valor_total" in df_carrinhos_qualify.columns:
        val_map = df_carrinhos_qualify.set_index("carrinho_id")["valor_total"].to_dict()
        df_resgate["valor_carrinho_atribuido"] = df_resgate["carrinho_id"].map(val_map).fillna(0.0)
    else:
        df_resgate["valor_carrinho_atribuido"] = 0.0

    desconto_col = "desconto_oferecido" if "desconto_oferecido" in df_resgate.columns else "taxa_cupom_desconto"
    if desconto_col in df_resgate.columns:
        desconto_vals = df_resgate[desconto_col].fillna(0.0)
        desconto_rate = np.where(desconto_vals > 1.0, desconto_vals / 100.0, desconto_vals)
    else:
        desconto_rate = 0.0

    if "valor_pedido_final" in df_resgate.columns and df_resgate["valor_pedido_final"].notna().any():
        df_resgate["receita_recuperada"] = df_resgate["valor_pedido_final"].fillna(0.0)
    else:
        df_resgate["receita_recuperada"] = np.where(
            df_resgate["flag_convertido"] == 1,
            df_resgate["valor_carrinho_atribuido"] * (1.0 - desconto_rate),
            0.0,
        )

    df_resgate["custo_envio"] = df_resgate["custo_envio"].fillna(0.05)
    df_resgate["roi_liquido_disparo"] = df_resgate["receita_recuperada"] - df_resgate["custo_envio"]

    cols = [
        "fato_resgate_sk",
        "resgate_id",
        "carrinho_id",
        "cliente_id",
        "canal_sk",
        "data_sk",
        "canal",
        "flag_aberto",
        "flag_clicado",
        "flag_convertido",
        "custo_envio",
        "valor_carrinho_atribuido",
        "receita_recuperada",
        "roi_liquido_disparo",
    ]
    available_cols = [c for c in cols if c in df_resgate.columns]
    return df_resgate[available_cols].copy()


# =============================================================================
# 🎯 Construção das 2 Visões Analíticas Gold (Data Views)
# =============================================================================

def build_view_abandonment_summary(
    df_fato_abandono: pd.DataFrame,
    df_dim_clientes: pd.DataFrame,
) -> pd.DataFrame:
    """
    Visão 1 (Executiva): v_abandonment_summary
    Consolida volume em risco, ticket médio e perfil RFM por motivo de desistência.
    """
    cols_cli = ["cliente_sk"]
    if "segmento_rfm" in df_dim_clientes.columns:
        cols_cli.append("segmento_rfm")
    if "churn_risk_score" in df_dim_clientes.columns:
        cols_cli.append("churn_risk_score")

    df_merged = df_fato_abandono.merge(
        df_dim_clientes[cols_cli],
        on="cliente_sk",
        how="left",
    )
    
    group_cols = ["motivo_abandono"]
    if "segmento_rfm" in df_merged.columns:
        group_cols.append("segmento_rfm")

    agg_dict = {
        "total_carrinhos_abandonados": ("fato_abandono_sk", "count"),
        "gmv_total_em_risco": ("valor_total_em_risco", "sum"),
        "ticket_medio_em_risco": ("valor_total_em_risco", "mean"),
    }
    if "churn_risk_score" in df_merged.columns:
        agg_dict["churn_risk_medio"] = ("churn_risk_score", "mean")

    view = df_merged.groupby(group_cols).agg(**agg_dict).reset_index()
    
    total_gmv = view["gmv_total_em_risco"].sum()
    view["representatividade_gmv_pct"] = np.round((view["gmv_total_em_risco"] / max(total_gmv, 1.0)) * 100, 2)
    return view.sort_values(by="gmv_total_em_risco", ascending=False).reset_index(drop=True)


def build_view_recovery_roi_by_channel(
    df_fato_resgate: pd.DataFrame,
) -> pd.DataFrame:
    """
    Visão 2 (Tática): v_recovery_roi_by_channel
    Calcula o funil e ROI de resgate por canal de disparo.
    """
    view = df_fato_resgate.groupby("canal").agg(
        total_disparos=("fato_resgate_sk", "count"),
        total_aberturas=("flag_aberto", "sum"),
        total_cliques=("flag_clicado", "sum"),
        total_conversoes=("flag_convertido", "sum"),
        custo_total_campanha=("custo_envio", "sum"),
        receita_total_recuperada=("receita_recuperada", "sum"),
        roi_liquido_total=("roi_liquido_disparo", "sum"),
    ).reset_index()
    
    view["taxa_abertura_pct"] = np.round((view["total_aberturas"] / view["total_disparos"]) * 100, 2)
    view["taxa_conversao_pct"] = np.round((view["total_conversoes"] / view["total_disparos"]) * 100, 2)
    view["roi_multiplicador"] = np.round(view["receita_total_recuperada"] / np.maximum(view["custo_total_campanha"], 0.01), 2)
    
    return view.sort_values(by="receita_total_recuperada", ascending=False).reset_index(drop=True)
