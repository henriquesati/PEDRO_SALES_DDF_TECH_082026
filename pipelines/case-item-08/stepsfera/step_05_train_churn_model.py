"""
Step 5: Pipeline de Treinamento de Modelo de Machine Learning (Padrão Stepsfera / Dadosfera)
Treina um modelo preditivo de Propensão de Recuperação de Carrinho / Risco de Churn.
Implementação funcional e pura em NumPy.
"""

import time
from typing import Final
import numpy as np
import pandas as pd

from core.types import MLModelMetrics, StepExecutionResult, StepMetadata

STEP_METADATA = StepMetadata(
    step_id="step_05_train_churn_model",
    step_name="Pipeline de Treinamento de Modelo ML (Propensão/Churn)",
    category="ML",
    layer_source="gold_curated",
    layer_target="gold_curated",
    description="Treina modelo de Machine Learning para prever probabilidade de conversão de resgate.",
    snowpark_compatible=True,
)


def _sigmoid(z: np.ndarray) -> np.ndarray:
    """Função de ativação sigmoide pura."""
    return 1.0 / (1.0 + np.exp(-np.clip(z, -25.0, 25.0)))


def _compute_roc_auc(y_true: np.ndarray, y_score: np.ndarray) -> float:
    """Calcula a métrica ROC-AUC de forma analítica via ordenação e rank-sum."""
    pos_mask = (y_true == 1)
    n_pos = int(np.sum(pos_mask))
    n_neg = len(y_true) - n_pos
    if n_pos == 0 or n_neg == 0:
        return 0.5
    
    ranks = pd.Series(y_score).rank(method="average").values
    sum_ranks_pos = float(np.sum(ranks[pos_mask]))
    auc = (sum_ranks_pos - (n_pos * (n_pos + 1)) / 2.0) / (n_pos * n_neg)
    return float(np.clip(auc, 0.0, 1.0))


def _fit_logistic_regression(
    X: np.ndarray,
    y: np.ndarray,
    epochs: int = 400,
    lr: float = 0.05,
    l2_reg: float = 0.01,
) -> tuple[np.ndarray, float]:
    """Treinamento supervisionado puro via gradiente descendente com regularização L2."""
    n_samples, n_features = X.shape
    weights = np.zeros(n_features)
    bias = 0.0

    for _ in range(epochs):
        linear_model = np.dot(X, weights) + bias
        y_predicted = _sigmoid(linear_model)

        dw = (1 / n_samples) * (np.dot(X.T, (y_predicted - y)) + l2_reg * weights)
        db = (1 / n_samples) * np.sum(y_predicted - y)

        weights -= lr * dw
        bias -= lr * db

    return weights, bias


def run_step(
    gold_models: dict[str, pd.DataFrame],
    random_state: int = 42,
    test_size: float = 0.20,
) -> tuple[MLModelMetrics, StepExecutionResult]:
    """Executa o pipeline de engenharia de features e treinamento supervisionado de ML."""
    start_time = time.perf_counter()
    
    df_fato_resgate = gold_models["fato_resgate"].copy()
    df_dim_clientes = gold_models["dim_clientes"].copy()
    
    # 1. Feature Engineering & Dataset Assembly
    join_key = "cliente_id" if "cliente_id" in df_fato_resgate.columns else "carrinho_id"
    df_features = df_fato_resgate.merge(
        df_dim_clientes,
        left_on=join_key,
        right_on="cliente_id" if "cliente_id" in df_dim_clientes.columns else "cliente_sk",
        how="left",
    )
    
    for col in ["recencia_dias", "frequencia_compras", "valor_monetario_ltv", "churn_risk_score"]:
        if col not in df_features.columns:
            df_features[col] = 50.0
        else:
            df_features[col] = df_features[col].fillna(50.0)

    for col in ["custo_envio", "valor_carrinho_atribuido", "flag_aberto", "flag_clicado"]:
        if col not in df_features.columns:
            df_features[col] = 0.0
        else:
            df_features[col] = df_features[col].fillna(0.0)

    feature_cols = [
        "valor_carrinho_atribuido",
        "custo_envio",
        "flag_aberto",
        "flag_clicado",
        "recencia_dias",
        "frequencia_compras",
        "valor_monetario_ltv",
        "churn_risk_score",
    ]
    
    X_raw = df_features[feature_cols].values.astype(float)
    y_raw = df_features["flag_convertido"].values.astype(int)

    # 2. Padronização Funcional (Z-Score Standard Scaler)
    mean = np.mean(X_raw, axis=0)
    std = np.std(X_raw, axis=0)
    std[std == 0] = 1.0
    X_scaled = (X_raw - mean) / std

    # 3. Divisão Treino / Teste Estratificada Pura
    np.random.seed(random_state)
    n_samples = len(X_scaled)
    n_test = int(n_samples * test_size)
    indices = np.arange(n_samples)
    np.random.shuffle(indices)

    test_indices = indices[:n_test]
    train_indices = indices[n_test:]

    X_train, y_train = X_scaled[train_indices], y_raw[train_indices]
    X_test, y_test = X_scaled[test_indices], y_raw[test_indices]

    # 4. Treinamento do Modelo (Logistic Regression com regularização L2)
    weights, bias = _fit_logistic_regression(X_train, y_train, epochs=400, lr=0.08)

    # 5. Avaliação e Métricas
    y_proba = _sigmoid(np.dot(X_test, weights) + bias)
    y_pred = (y_proba >= 0.50).astype(int)

    acc = float(np.mean(y_pred == y_test))
    auc = _compute_roc_auc(y_test, y_proba)
    
    tp = float(np.sum((y_pred == 1) & (y_test == 1)))
    fp = float(np.sum((y_pred == 1) & (y_test == 0)))
    fn = float(np.sum((y_pred == 0) & (y_test == 1)))

    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

    abs_weights = np.abs(weights)
    sum_weights = np.sum(abs_weights)
    normalized_importances = abs_weights / (sum_weights if sum_weights > 0 else 1.0)

    importances = tuple(
        (col, float(imp))
        for col, imp in sorted(zip(feature_cols, normalized_importances), key=lambda x: x[1], reverse=True)
    )

    metrics = MLModelMetrics(
        model_name="Regularized Logistic Regression (Cart Recovery Propensity)",
        target_variable="flag_convertido",
        train_records=len(X_train),
        test_records=len(X_test),
        accuracy=round(acc, 4),
        roc_auc=round(auc, 4),
        f1_score=round(f1, 4),
        precision=round(prec, 4),
        recall=round(rec, 4),
        feature_importances=importances,
    )

    duration_ms = (time.perf_counter() - start_time) * 1000

    result = StepExecutionResult(
        step_id=STEP_METADATA.step_id,
        step_name=STEP_METADATA.step_name,
        status="SUCCESS",
        records_in=len(X_train),
        records_out=len(X_test),
        duration_ms=round(duration_ms, 2),
        message=f"Modelo treinado com sucesso: ROC-AUC={auc:.4f} | Acurácia={acc*100:.2f}% | F1={f1:.4f}.",
        details=(
            f"Top 1 Feature: {importances[0][0]} ({importances[0][1]*100:.1f}%)",
            f"Top 2 Feature: {importances[1][0]} ({importances[1][1]*100:.1f}%)",
            f"Top 3 Feature: {importances[2][0]} ({importances[2][1]*100:.1f}%)",
        ),
    )

    return metrics, result
