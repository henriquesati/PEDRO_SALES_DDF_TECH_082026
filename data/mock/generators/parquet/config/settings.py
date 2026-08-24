"""
Estruturas de Configuração e Tipagem — Cart Recovery Mock Data.

Define dataclasses fortemente tipadas para volumes de dataset,
cotas mínimas declarativas de dirty data / anomalias e parâmetros de runtime.
Taxas configuradas com valores realistas/quebrados (não-redondos) para verossimilhança estatística.
"""
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
import pytz


@dataclass
class VolumeConfig:
    """Configuração de volumetria das entidades geradas."""
    n_clientes: int = 1_500
    n_produtos: int = 300
    n_carrinhos: int = 7_500
    # Fatores médios multiplicativos para entidades filhas
    itens_por_carrinho_media: float = 3.0
    eventos_por_carrinho_media: float = 12.0
    toques_resgate_por_abandonado_media: float = 1.8


@dataclass
class AnomalyConfig:
    """
    Configuração declarativa de Dirty Data e Anomalias de Negócio.
    Utiliza taxas naturais/quebradas para evitar percentuais redondos artificiais.
    """
    # ── Clientes ──
    min_null_emails_pct: float = 0.0487           # ~4.87% E-mails nulos (missing)
    min_invalid_emails_pct: float = 0.0273        # ~2.73% E-mails com sintaxe inválida
    min_casing_inconsistent_pct: float = 0.0527   # ~5.27% E-mails com casing misto
    min_unmasked_phones_pct: float = 0.0480       # ~4.80% Telefones sem máscara/formato
    min_ltv_inconsistency_pct: float = 0.0287     # ~2.87% LTV > 0 com total_compras = 0

    # ── Produtos ──
    min_inverted_price_pct: float = 0.0467        # ~4.67% Preço promocional atual > preço original
    min_missing_evaluations_pct: float = 0.1473   # ~14.73% Produtos sem avaliação

    # ── Carrinhos ──
    min_negative_freight_pct: float = 0.0387      # ~3.87% ANOM-01: Frete negativo
    min_total_inconsistency_pct: float = 0.0513   # ~5.13% ANOM-04: Total divergente da soma
    min_zero_or_negative_subtotal_pct: float = 0.0187 # ~1.87% ANOM-02: Subtotal zerado/negativo
    min_excessive_discount_pct: float = 0.0213    # ~2.13% ANOM-03: Desconto > Subtotal

    # ── Itens do Carrinho ──
    min_temporal_inversion_itens_pct: float = 0.0523  # ~5.23% data_remocao < data_adicao
    min_empty_or_orphan_carts_pct: float = 0.0187     # ~1.87% Carrinhos sem itens / zerados

    # ── Eventos de Resgate ──
    min_temporal_inversion_resgate_pct: float = 0.0489 # ~4.89% data_abertura < data_envio
    min_click_without_open_pct: float = 0.0217         # ~2.17% clique com data_abertura nula

    def scale_rates(self, multiplier: float) -> 'AnomalyConfig':
        """Retorna uma nova instância com todas as taxas escaladas pelo multiplicador."""
        return AnomalyConfig(
            min_null_emails_pct=min(1.0, self.min_null_emails_pct * multiplier),
            min_invalid_emails_pct=min(1.0, self.min_invalid_emails_pct * multiplier),
            min_casing_inconsistent_pct=min(1.0, self.min_casing_inconsistent_pct * multiplier),
            min_unmasked_phones_pct=min(1.0, self.min_unmasked_phones_pct * multiplier),
            min_ltv_inconsistency_pct=min(1.0, self.min_ltv_inconsistency_pct * multiplier),
            min_inverted_price_pct=min(1.0, self.min_inverted_price_pct * multiplier),
            min_missing_evaluations_pct=min(1.0, self.min_missing_evaluations_pct * multiplier),
            min_negative_freight_pct=min(1.0, self.min_negative_freight_pct * multiplier),
            min_total_inconsistency_pct=min(1.0, self.min_total_inconsistency_pct * multiplier),
            min_zero_or_negative_subtotal_pct=min(1.0, self.min_zero_or_negative_subtotal_pct * multiplier),
            min_excessive_discount_pct=min(1.0, self.min_excessive_discount_pct * multiplier),
            min_temporal_inversion_itens_pct=min(1.0, self.min_temporal_inversion_itens_pct * multiplier),
            min_empty_or_orphan_carts_pct=min(1.0, self.min_empty_or_orphan_carts_pct * multiplier),
            min_temporal_inversion_resgate_pct=min(1.0, self.min_temporal_inversion_resgate_pct * multiplier),
            min_click_without_open_pct=min(1.0, self.min_click_without_open_pct * multiplier),
        )


@dataclass
class GeneratorSettings:
    """Configuração global de execução dos geradores."""
    seed: int = 42
    profile_name: str = "standard"
    volumes: VolumeConfig = field(default_factory=VolumeConfig)
    anomalies: AnomalyConfig = field(default_factory=AnomalyConfig)
    
    # Período temporal
    timezone_str: str = "America/Sao_Paulo"
    data_inicio: datetime = field(default_factory=lambda: datetime(2026, 1, 1))
    data_fim: datetime = field(default_factory=lambda: datetime(2026, 6, 30, 23, 59, 59))
    
    # Diretórios (relativo a data/mock/output/)
    base_dir: Path = field(default_factory=lambda: Path(__file__).resolve().parent.parent.parent.parent.parent) # data/
    output_dir: Path = field(default_factory=lambda: Path(__file__).resolve().parent.parent.parent.parent / "output") # data/mock/output

    @property
    def timezone(self):
        return pytz.timezone(self.timezone_str)

    @property
    def parquet_dir(self) -> Path:
        return self.output_dir / "parquet"

    @property
    def csv_dir(self) -> Path:
        return self.output_dir / "csv"
