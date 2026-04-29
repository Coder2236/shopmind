import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder
import os

class RecommendationEngine:
    def __init__(self):
        self.products_df = None
        self.interactions_df = None
        self.user_item_matrix = None
        self.item_similarity_matrix = None
        self.user_encoder = LabelEncoder()
        self.product_encoder = LabelEncoder()

    def load_data(self):
        base = os.path.dirname(__file__)
        self.products_df = pd.read_csv(os.path.join(base, "data/products.csv"))
        self.interactions_df = pd.read_csv(os.path.join(base, "data/interactions.csv"))
        self._build_matrices()

    def _build_matrices(self):
        df = self.interactions_df.copy()

        # Weight: purchase = 5, browse = 1
        df["weight"] = df.apply(
            lambda r: r["rating"] * 2 if r["interaction"] == "purchase" else r["rating"], axis=1
        )

        # Pivot table: users x products
        pivot = df.pivot_table(
            index="user_id", columns="product_id", values="weight", aggfunc="max", fill_value=0
        )
        self.user_item_matrix = pivot
        self.item_similarity_matrix = cosine_similarity(pivot.T)

    def get_collaborative_recommendations(self, user_id, top_n=5):
        """User-based collaborative filtering."""
        if user_id not in self.user_item_matrix.index:
            return self.get_popular_products(top_n)

        user_vector = self.user_item_matrix.loc[user_id].values.reshape(1, -1)
        all_users = self.user_item_matrix.values
        similarities = cosine_similarity(user_vector, all_users)[0]

        similar_users_idx = similarities.argsort()[::-1][1:6]
        similar_users = self.user_item_matrix.index[similar_users_idx]

        # Products the user hasn't interacted with
        user_products = set(self.user_item_matrix.columns[self.user_item_matrix.loc[user_id] > 0])
        scores = {}

        for su in similar_users:
            su_vector = self.user_item_matrix.loc[su]
            for pid, score in su_vector.items():
                if score > 0 and pid not in user_products:
                    scores[pid] = scores.get(pid, 0) + score

        top_ids = sorted(scores, key=scores.get, reverse=True)[:top_n]
        return self._get_product_details(top_ids)

    def get_item_based_recommendations(self, product_id, top_n=5):
        """Item-based collaborative filtering."""
        if product_id not in self.user_item_matrix.columns:
            return self.get_popular_products(top_n)

        col_idx = list(self.user_item_matrix.columns).index(product_id)
        sim_scores = self.item_similarity_matrix[col_idx]
        similar_idx = sim_scores.argsort()[::-1][1:top_n+1]
        similar_ids = [self.user_item_matrix.columns[i] for i in similar_idx]
        return self._get_product_details(similar_ids)

    def get_category_recommendations(self, category, top_n=5):
        """Recommend products from the same category."""
        cat_products = self.products_df[self.products_df["category"] == category]
        ids = cat_products["id"].tolist()[:top_n]
        return self._get_product_details(ids)

    def get_popular_products(self, top_n=5):
        """Fallback: most interacted products."""
        counts = self.interactions_df.groupby("product_id")["rating"].sum().sort_values(ascending=False)
        top_ids = counts.index[:top_n].tolist()
        return self._get_product_details(top_ids)

    def _get_product_details(self, product_ids):
        results = []
        for pid in product_ids:
            row = self.products_df[self.products_df["id"] == pid]
            if not row.empty:
                results.append(row.iloc[0].to_dict())
        return results

    def get_all_products(self):
        return self.products_df.to_dict(orient="records")

    def get_all_users(self):
        return sorted(self.interactions_df["user_id"].unique().tolist())

    def get_all_categories(self):
        return sorted(self.products_df["category"].unique().tolist())

    def get_stats(self):
        return {
            "total_products": len(self.products_df),
            "total_users": self.interactions_df["user_id"].nunique(),
            "total_interactions": len(self.interactions_df),
            "categories": len(self.products_df["category"].unique())
        }
