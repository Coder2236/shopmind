import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

products = [
    {"id": 1, "name": "Wireless Headphones", "category": "Electronics", "price": 2999, "image": "🎧"},
    {"id": 2, "name": "Running Shoes", "category": "Sports", "price": 3499, "image": "👟"},
    {"id": 3, "name": "Python Programming Book", "category": "Books", "price": 599, "image": "📘"},
    {"id": 4, "name": "Yoga Mat", "category": "Sports", "price": 899, "image": "🧘"},
    {"id": 5, "name": "Smartwatch", "category": "Electronics", "price": 8999, "image": "⌚"},
    {"id": 6, "name": "Coffee Maker", "category": "Kitchen", "price": 2499, "image": "☕"},
    {"id": 7, "name": "Data Science Book", "category": "Books", "price": 799, "image": "📗"},
    {"id": 8, "name": "Bluetooth Speaker", "category": "Electronics", "price": 1999, "image": "🔊"},
    {"id": 9, "name": "Gym Gloves", "category": "Sports", "price": 399, "image": "🥊"},
    {"id": 10, "name": "Air Fryer", "category": "Kitchen", "price": 3999, "image": "🍳"},
    {"id": 11, "name": "Machine Learning Book", "category": "Books", "price": 899, "image": "📙"},
    {"id": 12, "name": "Laptop Stand", "category": "Electronics", "price": 1299, "image": "💻"},
    {"id": 13, "name": "Protein Powder", "category": "Sports", "price": 1499, "image": "💪"},
    {"id": 14, "name": "Instant Pot", "category": "Kitchen", "price": 5999, "image": "🥘"},
    {"id": 15, "name": "Noise Cancelling Earbuds", "category": "Electronics", "price": 4499, "image": "🎵"},
]

pd.DataFrame(products).to_csv("data/products.csv", index=False)

# Generate user browsing and purchase data
users = [f"user_{i}" for i in range(1, 101)]
interactions = []

for user in users:
    category_pref = random.choice(["Electronics", "Sports", "Books", "Kitchen"])
    preferred = [p for p in products if p["category"] == category_pref]
    others = [p for p in products if p["category"] != category_pref]

    browsed = random.sample(preferred, min(3, len(preferred))) + random.sample(others, random.randint(1, 3))
    purchased = random.sample(preferred, min(2, len(preferred)))

    for p in browsed:
        interactions.append({"user_id": user, "product_id": p["id"], "interaction": "browse", "rating": random.randint(1, 3)})
    for p in purchased:
        interactions.append({"user_id": user, "product_id": p["id"], "interaction": "purchase", "rating": random.randint(4, 5)})

df = pd.DataFrame(interactions)
df.to_csv("data/interactions.csv", index=False)
print("✅ Data generated: data/products.csv and data/interactions.csv")
