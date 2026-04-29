from flask import Flask, render_template, jsonify, request
from recommender import RecommendationEngine

app = Flask(__name__)
engine = RecommendationEngine()
engine.load_data()

@app.route("/")
def index():
    products = engine.get_all_products()
    users = engine.get_all_users()
    categories = engine.get_all_categories()
    stats = engine.get_stats()
    return render_template("index.html", products=products, users=users, categories=categories, stats=stats)

@app.route("/api/recommend/user/<user_id>")
def recommend_for_user(user_id):
    recs = engine.get_collaborative_recommendations(user_id, top_n=5)
    return jsonify({"recommendations": recs, "type": "Collaborative Filtering", "for": user_id})

@app.route("/api/recommend/item/<int:product_id>")
def recommend_similar(product_id):
    product_id = int(product_id)
    recs = engine.get_item_based_recommendations(product_id, top_n=5)
    return jsonify({"recommendations": recs, "type": "Item-Based Similarity", "for": product_id})

@app.route("/api/recommend/category/<category>")
def recommend_by_category(category):
    recs = engine.get_category_recommendations(category, top_n=5)
    return jsonify({"recommendations": recs, "type": "Category-Based", "for": category})

@app.route("/api/popular")
def popular():
    recs = engine.get_popular_products(top_n=5)
    return jsonify({"recommendations": recs, "type": "Trending / Popular"})

@app.route("/api/stats")
def stats():
    return jsonify(engine.get_stats())

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
