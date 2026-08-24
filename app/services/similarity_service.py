"""Serviço puro de cálculo de similaridade semântica por cosseno e projeção 2D (PCA/t-SNE)."""

from typing import Sequence
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

from app.types.models import ProductSimilarityMatch

def build_product_feature_matrix(df_products: pd.DataFrame) -> tuple[np.ndarray, list[str]]:
    """Gera a matriz vetorial multidimensional combinando texto, categorias e preço (Função Pura)."""
    # 1. Vetorização textual dos diferenciais e materiais
    text_corpus = (
        df_products["nome_bruto"].fillna("") + " " +
        df_products["material_construcao"].fillna("") + " " +
        df_products["diferencial_tecnico"].fillna("")
    )
    tfidf = TfidfVectorizer(max_features=25, stop_words=None)
    text_vectors = tfidf.fit_transform(text_corpus).toarray()
    
    # 2. One-hot encoding de categorias e perfil de atrito
    cat_cols = ["categoria_normalizada", "faixa_posicionamento", "sensibilidade_preco", "nivel_urgencia"]
    available_cat_cols = [c for c in cat_cols if c in df_products.columns]
    ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    cat_vectors = ohe.fit_transform(df_products[available_cat_cols].fillna("Outro"))
    
    # 3. Normalização de preço
    scaler = MinMaxScaler()
    price_vector = scaler.fit_transform(df_products[["preco_atual"]].fillna(0.0))
    
    # 4. Combinação ponderada de vetores
    feature_matrix = np.hstack([text_vectors * 1.5, cat_vectors * 1.0, price_vector * 0.8])
    feature_names = [f"tfidf_{i}" for i in range(text_vectors.shape[1])] + list(ohe.get_feature_names_out()) + ["norm_price"]
    
    return feature_matrix, feature_names

def compute_2d_projection(
    df_products: pd.DataFrame,
    method: str = "pca"
) -> pd.DataFrame:
    """Calcula projeção 2D (PCA ou t-SNE) para renderização no mapa semântico Plotly."""
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
    return df_projected

def find_similar_products(
    target_product_id: int | str,
    df_products: pd.DataFrame,
    top_k: int = 5
) -> list[ProductSimilarityMatch]:
    """Retorna os top-K produtos mais similares usando distância de Cosseno."""
    feature_matrix, _ = build_product_feature_matrix(df_products)
    sim_matrix = cosine_similarity(feature_matrix)
    
    try:
        idx = int(df_products[df_products["produto_id"].astype(str) == str(target_product_id)].index[0])
    except (IndexError, KeyError, ValueError):
        return []
        
    sim_scores = list(enumerate(sim_matrix[idx]))
    # Ordenar por maior similaridade ignorando o próprio produto
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    filtered_scores = [s for s in sorted_scores if s[0] != idx][:top_k]
    
    results: list[ProductSimilarityMatch] = []
    for item_idx, score in filtered_scores:
        row = df_products.iloc[item_idx]
        results.append(
            ProductSimilarityMatch(
                product_id=str(row["produto_id"]),
                title=str(row.get("nome_bruto", "N/A")),
                category=str(row.get("categoria_normalizada", "N/A")),
                price=float(row.get("preco_atual", 0.0)),
                similarity_score=round(float(score) * 100.0, 1),
                price_sensitivity=str(row.get("sensibilidade_preco", "Média")),
                urgency_level=str(row.get("nivel_urgencia", "Médio")),
                friction_risk=str(row.get("motivo_raiz", "N/A")),
            )
        )
    return results
