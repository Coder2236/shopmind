# 🛍️ ShopMind AI — Product Recommendation Engine

## Tech Stack
- **Backend:** Python, Flask
- **ML:** Scikit-learn (Cosine Similarity), Pandas, NumPy
- **Frontend:** HTML5, CSS3, Vanilla JS (Dark themed, animated)

## Algorithms Used
1. **User-Based Collaborative Filtering** — finds similar users and suggests what they liked
2. **Item-Based Collaborative Filtering** — cosine similarity between product vectors
3. **Category-Based Filtering** — top products from the same category
4. **Popularity-Based** — fallback using most-interacted products

---

## ⚙️ Setup Instructions

### 1. Install Python (if not installed)
Download from https://python.org — choose Python 3.10+

### 2. Create a virtual environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate sample data
```bash
python generate_data.py
```

### 5. Run the Flask app
```bash
python app.py
```

### 6. Open in browser
Go to: http://127.0.0.1:5000

---

## 📁 Project Structure
```
recommendation_engine/
├── app.py               ← Flask server & API routes
├── recommender.py       ← ML recommendation engine
├── generate_data.py     ← Generates sample data CSV files
├── requirements.txt     ← Python dependencies
├── data/
│   ├── products.csv     ← Product catalog (auto-generated)
│   └── interactions.csv ← User browsing & purchase data (auto-generated)
└── templates/
    └── index.html       ← Frontend UI
```

## 🔗 API Endpoints
| Endpoint | Description |
|---|---|
| `GET /` | Main UI |
| `GET /api/recommend/user/<user_id>` | User-based collaborative filtering |
| `GET /api/recommend/item/<product_id>` | Item-based similarity |
| `GET /api/recommend/category/<category>` | Category-based filter |
| `GET /api/popular` | Trending / popular products |
| `GET /api/stats` | Dataset statistics |
