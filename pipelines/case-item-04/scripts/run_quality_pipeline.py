"""
Script Batch de Execução do Pipeline de Qualificação e Data Quality
Case Dadosfera: Recuperação de Carrinho Abandonado (Item 4)
Gera todos os outputs (relatório markdown, gráficos 300DPI e logs JSON) dentro de pipelines/case-item-04/outputs/
"""

import os
import sys
import json
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import matplotlib.pyplot as plt

CURRENT_DIR = Path(__file__).resolve().parent
ITEM_DIR = CURRENT_DIR.parent
BASE_DIR = ITEM_DIR.parent.parent

RAW_DIR = BASE_DIR / "data" / "mock" / "output" / "parquet"

# Diretórios de Output DENTRO de pipelines/case-item-04/outputs/
OUTPUTS_DIR = ITEM_DIR / "outputs"
OUTPUT_ASSETS_DIR = OUTPUTS_DIR / "assets"
QUALIFY_DIR = OUTPUTS_DIR / "qualify"
ANOMALIES_DIR = OUTPUTS_DIR / "anomalies"
RESULTS_PATH = OUTPUTS_DIR / "validation_results.json"
REPORT_PATH = OUTPUTS_DIR / "data_quality_report.md"

QUALIFY_DIR.mkdir(parents=True, exist_ok=True)
ANOMALIES_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_ASSETS_DIR.mkdir(parents=True, exist_ok=True)

RULES = {
    "clientes": [
        {"type": "not_null", "column": "cliente_id", "code": "ERR_CLI_001", "description": "ID do Cliente nulo/ausente", "severity": "CRITICA"},
        {"type": "not_null", "column": "email", "code": "ERR_CLI_002", "description": "E-mail do cliente ausente", "severity": "ALTA"},
        {"type": "regex", "column": "email", "pattern": r"^[^@]+@[^@]+\.[^@]+$", "code": "ERR_CLI_003", "description": "Formato de e-mail inválido", "severity": "MEDIA"}
    ],
    "produtos": [
        {"type": "not_null", "column": "produto_id", "code": "ERR_PROD_001", "description": "ID do Produto nulo", "severity": "CRITICA"},
        {"type": "gt", "column": "preco_atual", "min_value": 0, "code": "ERR_PROD_002", "description": "Preço menor ou igual a zero", "severity": "ALTA"},
        {"type": "custom_compare", "col_a": "preco_atual", "col_b": "preco_original", "op": "lte", "code": "ERR_PROD_003", "description": "Promoção invertida (preco_atual > original)", "severity": "ALTA"}
    ],
    "carrinhos": [
        {"type": "not_null", "column": "carrinho_id", "code": "ERR_CAR_001", "description": "ID do Carrinho nulo", "severity": "CRITICA"},
        {"type": "not_null", "column": "cliente_id", "code": "ERR_CAR_002", "description": "ID do Cliente ausente", "severity": "CRITICA"},
        {"type": "in_set", "column": "status", "values": ["comprado", "abandonado", "expirado", "ativo", "recuperado"], "code": "ERR_CAR_003", "description": "Status inválido", "severity": "MEDIA"},
        {"type": "gte", "column": "valor_frete", "min_value": 0.0, "code": "ANOM-01", "description": "Frete negativo (ANOM-01)", "severity": "ALTA"},
        {"type": "gt", "column": "valor_subtotal", "min_value": 0.0, "code": "ANOM-02", "description": "Subtotal zerado (ANOM-02)", "severity": "ALTA"},
        {"type": "custom_compare", "col_a": "valor_desconto", "col_b": "valor_subtotal", "op": "lte", "code": "ANOM-03", "description": "Desconto excessivo (ANOM-03)", "severity": "CRITICA"},
        {"type": "accounting_sum", "code": "ANOM-04", "description": "Total contábil inconsistente (ANOM-04)", "severity": "ALTA"},
        {"type": "date_order", "earlier_column": "data_criacao", "later_column": "data_abandono", "code": "ANOM-05", "description": "Inversão temporal", "severity": "ALTA"}
    ],
    "itens_carrinho": [
        {"type": "not_null", "column": "item_id", "code": "ERR_ITM_001", "description": "ID do Item nulo", "severity": "CRITICA"},
        {"type": "not_null", "column": "carrinho_id", "code": "ERR_ITM_002", "description": "ID do Carrinho ausente", "severity": "CRITICA"},
        {"type": "gt", "column": "quantidade", "min_value": 0, "code": "ERR_ITM_003", "description": "Quantidade inválida (<=0)", "severity": "ALTA"},
        {"type": "gt", "column": "preco_unitario", "min_value": 0, "code": "ERR_ITM_004", "description": "Preço unitário inválido (<=0)", "severity": "ALTA"},
        {"type": "date_order", "earlier_column": "data_adicao", "later_column": "data_remocao", "code": "ERR_ITM_005", "description": "Inversão temporal de remoção", "severity": "ALTA"}
    ],
    "eventos_carrinho": [
        {"type": "not_null", "column": "evento_id", "code": "ERR_EVC_001", "description": "ID do Evento nulo", "severity": "CRITICA"},
        {"type": "not_null", "column": "carrinho_id", "code": "ERR_EVC_002", "description": "FK Carrinho ausente", "severity": "CRITICA"}
    ],
    "eventos_resgate": [
        {"type": "not_null", "column": "resgate_id", "code": "ERR_RES_001", "description": "ID de Resgate nulo", "severity": "CRITICA"},
        {"type": "not_null", "column": "carrinho_id", "code": "ERR_RES_002", "description": "FK Carrinho ausente", "severity": "CRITICA"},
        {"type": "date_order", "earlier_column": "data_envio", "later_column": "data_abertura", "code": "ERR_RES_003", "description": "Inversão temporal de abertura", "severity": "ALTA"}
    ],
    "pedidos": [
        {"type": "not_null", "column": "pedido_id", "code": "ERR_PED_001", "description": "ID do Pedido nulo", "severity": "CRITICA"},
        {"type": "not_null", "column": "cliente_id", "code": "ERR_PED_002", "description": "FK Cliente ausente", "severity": "CRITICA"}
    ]
}

def qualify_entity(entity_name: str, df_raw: pd.DataFrame, validation_rules: list) -> tuple:
    anomalous_indices = set()
    anomaly_records = []
    now_iso = datetime.now(timezone.utc).isoformat()
    
    for rule in validation_rules:
        rule_type = rule.get("type")
        col = rule.get("column")
        code = rule.get("code", "VAL_000")
        desc = rule.get("description", "Inconsistência")
        severity = rule.get("severity", "MEDIA")
        
        failed_mask = pd.Series(False, index=df_raw.index)
        
        if rule_type == "not_null":
            failed_mask = df_raw[col].isna()
        elif rule_type == "in_set":
            value_set = rule.get("values", [])
            failed_mask = ~df_raw[col].astype(str).str.lower().isin([v.lower() for v in value_set]) & df_raw[col].notna()
        elif rule_type == "gt":
            failed_mask = (df_raw[col] <= rule.get("min_value", 0)) & df_raw[col].notna()
        elif rule_type == "gte":
            failed_mask = (df_raw[col] < rule.get("min_value", 0)) & df_raw[col].notna()
        elif rule_type == "regex":
            failed_mask = ~df_raw[col].astype(str).str.match(rule.get("pattern"), na=False) & df_raw[col].notna()
        elif rule_type == "date_order":
            t_earlier = pd.to_datetime(df_raw[rule.get("earlier_column")], errors='coerce')
            t_later = pd.to_datetime(df_raw[rule.get("later_column")], errors='coerce')
            failed_mask = (t_later < t_earlier) & t_earlier.notna() & t_later.notna()
            col = f"{rule.get('earlier_column')}_vs_{rule.get('later_column')}"
        elif rule_type == "custom_compare":
            failed_mask = (df_raw[rule.get("col_a")] > df_raw[rule.get("col_b")]) & df_raw[rule.get("col_a")].notna() & df_raw[rule.get("col_b")].notna()
            col = f"{rule.get('col_a')}_vs_{rule.get('col_b')}"
        elif rule_type == "accounting_sum":
            if all(c in df_raw.columns for c in ["valor_subtotal", "valor_frete", "valor_desconto", "valor_total"]):
                exp = (df_raw["valor_subtotal"] + df_raw["valor_frete"] - df_raw["valor_desconto"]).round(2)
                failed_mask = (df_raw["valor_total"].round(2) != exp) & df_raw["valor_total"].notna()
            col = "valor_total_equacao"
            
        failed_rows = df_raw[failed_mask]
        for idx, row in failed_rows.iterrows():
            anomalous_indices.add(idx)
            anomaly_records.append({
                "entity_name": entity_name,
                "record_index": idx,
                "codigo_anomalia": code,
                "campo_afetado": col,
                "descricao_risco": desc,
                "severidade": severity,
                "detected_at": now_iso,
                "payload_raw": json.dumps(row.to_dict(), default=str)
            })
            
    valid_indices = df_raw.index.difference(list(anomalous_indices))
    df_qualify = df_raw.loc[valid_indices].copy().reset_index(drop=True)
    df_anomalies = pd.DataFrame(anomaly_records) if anomaly_records else pd.DataFrame()
    return df_qualify, df_anomalies

def generate_markdown_report(summary_data: list, total_raw: int, total_qualify: int, total_anom: int, pass_rate: float) -> str:
    md = f"""# 📊 Data Quality & Anomaly Report (Outputs Autocontidos)

> **Módulo:** `pipelines/case-item-04/outputs/`  
> **Status:** ✅ Validação Dual-Artifact Executada com Sucesso  
> **Data de Avaliação:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%SZ')}  
> **Conformidade Global:** **{pass_rate}%** dos registros qualificados  

---

## 1. 📌 Executive Summary

- **Total de Registros Avaliados:** `{total_raw:,}`
- **Registros Aprovados (Silver Qualify):** `{total_qualify:,}` (**{pass_rate}%**)
- **Registros Isolados em Quarentena (Silver Anomalies):** `{total_anom:,}` (**{round(100 - pass_rate, 2)}%**)

---

## 2. 📋 Resumo Consolidado por Entidade

| Entidade | Registros RAW | Registros Qualify | Ocorrências de Anomalia | Taxa de Rejeição (%) |
|---|:---:|:---:|:---:|:---:|
"""
    for item in summary_data:
        md += f"| `{item['entidade']}` | {item['registros_raw']:,} | {item['registros_qualify']:,} | {item['ocorrencias_anomalias']:,} | {item['taxa_rejeicao_pct']}% |\n"

    md += f"""
---

## 3. 📈 Galeria de Gráficos de Data Quality & Quarentena

### 3.1 Conformidade Global & Distribuição de Anomalias
![Conformidade Global](assets/chart_01_global_compliance_and_quarantine.png)

### 3.2 Taxa de Rejeição por Entidade
![Taxa de Rejeição](assets/chart_02_rejection_rates_by_entity.png)

### 3.3 Comparativo de Volume: Bronze (RAW) vs Silver (Qualify)
![Antes vs Depois](assets/chart_03_before_vs_after_volume.png)

---

## 4. 🛠️ Roteamento Dual-Artifact

1. **Camada Silver Qualify (`pipelines/case-item-04/outputs/qualify/`):** Registros 100% limpos e aptos para a camada analítica/Gold.
2. **Camada Silver Anomalies (`pipelines/case-item-04/outputs/anomalies/`):** Dead-letter auditável para diagnóstico e prevenção de poluição de métricas.
"""
    return md

def run_all():
    print("\n=== EXECUTANDO PIPELINE DE QUALIFICACAO DUAL-ARTIFACT (SILVER) ===")
    summary = []
    
    for file_path in sorted(list(RAW_DIR.glob("*.parquet"))):
        entity = file_path.stem
        df_raw = pd.read_parquet(file_path)
        total_raw = len(df_raw)
        
        df_qualify, df_anomalies = qualify_entity(entity, df_raw, RULES.get(entity, []))
        total_qualify = len(df_qualify)
        total_anom = len(df_anomalies)
        anom_pct = ((total_raw - total_qualify) / total_raw) * 100 if total_raw > 0 else 0
        
        df_qualify.to_parquet(QUALIFY_DIR / f"{entity}.parquet", index=False, engine='pyarrow')
        df_anomalies.to_parquet(ANOMALIES_DIR / f"{entity}.parquet", index=False, engine='pyarrow')
        
        print(f"  [{entity:<17}] RAW: {total_raw:>7,} | QUALIFY: {total_qualify:>7,} | ANOMALIAS: {total_anom:>5,} ({anom_pct:>5.1f}% rejeitados)")
        summary.append({
            "entidade": entity,
            "registros_raw": total_raw,
            "registros_qualify": total_qualify,
            "ocorrencias_anomalias": total_anom,
            "taxa_rejeicao_pct": round(anom_pct, 2)
        })
        
    df_sum = pd.DataFrame(summary)
    tot_raw = int(df_sum["registros_raw"].sum())
    tot_qualify = int(df_sum["registros_qualify"].sum())
    tot_anom = tot_raw - tot_qualify
    pass_pct = round((tot_qualify / tot_raw) * 100, 2)
    
    # 1. Gerar Conjunto Completo de Gráficos de Qualidade em outputs/assets/
    
    # Gráfico 1: Conformidade Global e Volume em Quarentena
    g1_name = "chart_01_global_compliance_and_quarantine.png"
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    ax1.pie([pass_pct, round(100 - pass_pct, 2)], labels=[f'Qualify\n({pass_pct}%)', f'Anomalias\n({round(100 - pass_pct, 2)}%)'],
            colors=['#2A9D8F', '#E76F51'], autopct='%1.1f%%', startangle=140, pctdistance=0.75, textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax1.add_artist(plt.Circle((0,0), 0.55, fc='white'))
    ax1.set_title('Conformidade Global de Registros (Silver)', fontsize=13, fontweight='bold')

    ax2.barh(df_sum['entidade'], df_sum['ocorrencias_anomalias'], color='#457B9D', alpha=0.85)
    ax2.set_xlabel('Contagem de Ocorrencias Rejeitadas', fontsize=10, fontweight='bold')
    ax2.set_title('Anomalias por Entidade (Quarentena)', fontsize=13, fontweight='bold')
    ax2.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    g1_path = OUTPUT_ASSETS_DIR / g1_name
    fig1.savefig(g1_path, bbox_inches='tight', dpi=300)
    plt.close(fig1)
    print(f"  [+] Grafico 1 salvo em: {g1_path}")

    # Gráfico 2: Taxa de Rejeição Percentual por Entidade
    g2_name = "chart_02_rejection_rates_by_entity.png"
    fig2, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(df_sum['entidade'], df_sum['taxa_rejeicao_pct'], color=['#E63946' if x > 5 else '#F4A261' if x > 0 else '#2A9D8F' for x in df_sum['taxa_rejeicao_pct']], alpha=0.85)
    ax.set_ylabel('Taxa de Rejeicao (%)', fontsize=11, fontweight='bold')
    ax.set_title('Taxa de Rejeicao de Dados por Entidade do Case', fontsize=13, fontweight='bold')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.xticks(rotation=20, ha='right', fontweight='bold')
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.2, f'{yval:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
    plt.tight_layout()
    g2_path = OUTPUT_ASSETS_DIR / g2_name
    fig2.savefig(g2_path, bbox_inches='tight', dpi=300)
    plt.close(fig2)
    print(f"  [+] Grafico 2 salvo em: {g2_path}")

    # Gráfico 3: Comparativo Antes vs Depois (Bronze RAW vs Silver Qualify)
    g3_name = "chart_03_before_vs_after_volume.png"
    fig3, ax = plt.subplots(figsize=(11, 5))
    x = range(len(df_sum))
    width = 0.35
    ax.bar([i - width/2 for i in x], df_sum['registros_raw'], width, label='Bronze (RAW)', color='#A8DADC')
    ax.bar([i + width/2 for i in x], df_sum['registros_qualify'], width, label='Silver (Qualify)', color='#1D3557')
    ax.set_xticks(x)
    ax.set_xticklabels(df_sum['entidade'], rotation=20, ha='right', fontweight='bold')
    ax.set_yscale('log')
    ax.set_ylabel('Total de Registros (Escala Logaritmica)', fontsize=10, fontweight='bold')
    ax.set_title('Volume de Dados: Bronze RAW vs Silver Qualify (Promovidos)', fontsize=13, fontweight='bold')
    ax.legend(frameon=True)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    g3_path = OUTPUT_ASSETS_DIR / g3_name
    fig3.savefig(g3_path, bbox_inches='tight', dpi=300)
    plt.close(fig3)
    print(f"  [+] Grafico 3 salvo em: {g3_path}")

    # 2. Salvar Evidencias JSON em outputs/
    evidence = {
        "evaluation_parameters": {
            "run_id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_batch_eval"),
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
            "total_entities_evaluated": len(df_sum),
            "total_records_evaluated": tot_raw
        },
        "statistics": {
            "records_promoted_to_qualify": tot_qualify,
            "records_isolated_in_anomalies": tot_anom,
            "record_pass_rate_percent": pass_pct
        },
        "entity_breakdown": summary
    }
    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(evidence, f, indent=2, ensure_ascii=False)
    print(f"  [+] Evidencia JSON salva em: {RESULTS_PATH}")

    # 3. Gerar e Salvar Relatorio Markdown em outputs/
    report_md = generate_markdown_report(summary, tot_raw, tot_qualify, tot_anom, pass_pct)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"  [+] Relatorio Markdown salvo em: {REPORT_PATH}")

    print(f"\n[SUCESSO] Pipeline concluido! Todos os outputs gerados em: {OUTPUTS_DIR}")

if __name__ == "__main__":
    run_all()
