"""Serviço puro de cálculo de similaridade semântica por cosseno e projeção 2D (PCA/t-SNE)."""

from typing import Callable, Final, List, Sequence, Tuple
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

from app.types.models import ProductSimilarityMatch, RecommendationStrategy

def _extract_text_corpus(df: pd.DataFrame) -> pd.Series:
    """Extrai corpus textual normalizado de forma pura e determinística."""
    name_s = df["nome_bruto"].fillna("") if "nome_bruto" in df.columns else df.get("nome", pd.Series([""] * len(df))).fillna("")
    mat_s = df.get("material_construcao", pd.Series([""] * len(df))).fillna("")
    dif_s = df.get("diferencial_tecnico", pd.Series([""] * len(df))).fillna("")
    return name_s + " " + mat_s + " " + dif_s

def _extract_categories(df: pd.DataFrame) -> Tuple[np.ndarray, List[str]]:
    """Extrai matriz one-hot categorizada de atributos de catálogo."""
    cat_cols = ["categoria_normalizada", "categoria", "faixa_posicionamento", "sensibilidade_preco", "nivel_urgencia"]
    available_cat_cols = [c for c in cat_cols if c in df.columns]
    
    if available_cat_cols:
        ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
        cat_vectors = ohe.fit_transform(df[available_cat_cols].fillna("Outro"))
        feature_names = list(ohe.get_feature_names_out())
    else:
        cat_vectors = np.zeros((len(df), 1))
        feature_names = ["dummy_cat"]
        
    return cat_vectors, feature_names

def _extract_price_vector(df: pd.DataFrame) -> np.ndarray:
    """Extrai e normaliza vetor contínuo de preços."""
    scaler = MinMaxScaler()
    price_col = df[["preco_atual"]] if "preco_atual" in df.columns else pd.DataFrame({"preco_atual": [100.0] * len(df)})
    return scaler.fit_transform(price_col.fillna(0.0))

def build_product_feature_matrix(df_products: pd.DataFrame) -> Tuple[np.ndarray, List[str]]:
    """Gera a matriz vetorial multidimensional combinando texto, categorias e preço (Função Pura)."""
    # 1. Vetorização textual
    text_corpus = _extract_text_corpus(df_products)
    tfidf = TfidfVectorizer(max_features=25, stop_words=None)
    text_vectors = tfidf.fit_transform(text_corpus).toarray()
    text_feature_names = [f"tfidf_{i}" for i in range(text_vectors.shape[1])]
    
    # 2. One-hot encoding
    cat_vectors, cat_feature_names = _extract_categories(df_products)
    
    # 3. Normalização de preço
    price_vector = _extract_price_vector(df_products)
    
    # 4. Combinação ponderada de vetores
    feature_matrix = np.hstack([text_vectors * 1.5, cat_vectors * 1.0, price_vector * 0.8])
    all_names = text_feature_names + cat_feature_names + ["norm_price"]
    
    return feature_matrix, all_names

def classify_strategy(anchor_price: float, anchor_cat: str, item_price: float, item_cat: str) -> RecommendationStrategy:
    """Função pura de classificação da estratégia de resgate comercial."""
    if item_cat == anchor_cat and item_price <= anchor_price:
        return "Substituto"
    if item_price > anchor_price:
        return "Cross-sell"
    return "Acessório"

def compute_2d_projection(
    df_products: pd.DataFrame,
    method: str = "pca"
) -> pd.DataFrame:
    """Calcula projeção 2D (PCA ou t-SNE) para renderização no mapa semântico Plotly."""
    if df_products.empty:
        return df_products

    feature_matrix, _ = build_product_feature_matrix(df_products)
    
    if method.lower() == "tsne" and len(df_products) > 5:
        perplexity = min(30, max(5, len(df_products) // 3))
        reducer = TSNE(n_components=2, perplexity=perplexity, random_state=42, init="random")
        coords = reducer.fit_transform(feature_matrix)
    else:
        reducer = PCA(n_components=2, random_state=42)
        coords = reducer.fit_transform(feature_matrix)
        
    df_projected = df_products.copy()
    df_projected["dim_x"] = coords[:, 0]
    df_projected["dim_y"] = coords[:, 1]
    if "nome_bruto" not in df_projected.columns and "nome" in df_projected.columns:
        df_projected["nome_bruto"] = df_projected["nome"]
    if "categoria_normalizada" not in df_projected.columns and "categoria" in df_projected.columns:
        df_projected["categoria_normalizada"] = df_projected["categoria"]
        
    return df_projected

def find_similar_products(
    target_product_id: int | str,
    df_products: pd.DataFrame,
    top_k: int = 5
) -> List[ProductSimilarityMatch]:
    """Retorna os top-K produtos mais similares com classificação de estratégia e delta de preço."""
    if df_products.empty:
        return []

    feature_matrix, _ = build_product_feature_matrix(df_products)
    sim_matrix = cosine_similarity(feature_matrix)
    
    try:
        idx = int(df_products[df_products["produto_id"].astype(str) == str(target_product_id)].index[0])
    except (IndexError, KeyError, ValueError):
        return []
        
    anchor_row = df_products.iloc[idx]
    anchor_price = float(anchor_row.get("preco_atual", 100.0))
    anchor_cat = str(anchor_row.get("categoria_normalizada", anchor_row.get("categoria", "Geral")))

    sim_scores = list(enumerate(sim_matrix[idx]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    filtered_scores = [s for s in sorted_scores if s[0] != idx][:top_k]
    
    results: List[ProductSimilarityMatch] = []
    for rank_i, (item_idx, score) in enumerate(filtered_scores):
        row = df_products.iloc[item_idx]
        item_price = float(row.get("preco_atual", 0.0))
        item_cat = str(row.get("categoria_normalizada", row.get("categoria", "Geral")))
        item_name = str(row.get("nome_bruto", row.get("nome", "N/A")))
        
        # Delta de Preço
        delta_pct = ((item_price - anchor_price) / anchor_price) * 100.0 if anchor_price > 0 else 0.0
        
        # Classificação Funcional da Estratégia
        strategy = classify_strategy(anchor_price, anchor_cat, item_price, item_cat)

        results.append(
            ProductSimilarityMatch(
                product_id=str(row["produto_id"]),
                title=item_name,
                category=item_cat if item_cat else "Catálogo",
                price=item_price,
                price_delta_pct=round(delta_pct, 1),
                similarity_score=round(float(score) * 100.0, 1),
                strategy_badge=strategy,
                price_sensitivity=str(row.get("sensibilidade_preco", "Média")),
                urgency_level=str(row.get("nivel_urgencia", "Médio")),
                friction_risk=str(row.get("motivo_raiz", "N/A")),
            )
        )
    return results
