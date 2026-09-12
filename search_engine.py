"""
search_engine.py
Intent-Aware Semantic Search & Outfit Bundler for Myntra StyleGen.
Bridges classical TF-IDF Inverted Indexing (from DocIndex) with Intent Extraction & Rule-based Bundling.
"""

import re
from typing import List, Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class StyleGenSearchEngine:
    def __init__(self, catalog: List[Dict[str, Any]]):
        self.catalog = catalog
        self.vectorizer = TfidfVectorizer(stop_words='english', token_pattern=r'(?u)\b\w+\b')
        self._build_index()

    def _build_index(self):
        """Constructs the search index combining title, brand, category, tags, and occasion."""
        self.corpus = []
        for item in self.catalog:
            content = f"{item['title']} {item['brand']} {item['category']} {item['gender']} {item['occasion']} {item['color']} {' '.join(item.get('tags', []))}"
            self.corpus.append(content.lower())
        self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)

    def extract_intent(self, query: str) -> Dict[str, Any]:
        """
        Parses intent components from natural language queries:
        - Budget cap (e.g. 'under 2500', 'below 3000', '< 2k')
        - Gender (men, women, unisex)
        - Occasion (Casual, Formal, Festive/Wedding, Party, Athleisure, Vacation/Brunch)
        - Colors
        """
        q_lower = query.lower()
        intent = {
            "budget": None,
            "gender": None,
            "occasion": None,
            "color": None,
            "clean_query": query
        }

        # Extract budget
        budget_match = re.search(r'(?:under|below|<|within)\s*(?:₹|rs\.?|inr)?\s*(\d+(?:k|\d{2,5}))', q_lower)
        if budget_match:
            val = budget_match.group(1)
            if 'k' in val:
                intent["budget"] = int(float(val.replace('k', '')) * 1000)
            else:
                intent["budget"] = int(val)

        # Extract gender
        if any(w in q_lower for w in ["men", "man", "male", "guy", "boy"]):
            intent["gender"] = "Men"
        elif any(w in q_lower for w in ["women", "woman", "female", "girl", "lady"]):
            intent["gender"] = "Women"

        # Extract occasion
        occasions = {
            "Festive/Wedding": ["wedding", "sangeet", "diwali", "festive", "ethnic", "haldi", "traditional"],
            "Formal": ["formal", "office", "presentation", "interview", "corporate", "meeting"],
            "Vacation/Brunch": ["brunch", "sundowner", "vacation", "beach", "resort", "boho", "summer"],
            "Party": ["party", "clubbing", "cocktail", "night out", "evening"],
            "Athleisure": ["gym", "workout", "running", "sports", "activewear"],
            "Casual": ["casual", "everyday", "college", "outing", "hangout"]
        }
        for occ, keywords in occasions.items():
            if any(kw in q_lower for kw in keywords):
                intent["occasion"] = occ
                break

        # Extract color
        colors = ["olive", "beige", "blue", "white", "maroon", "peach", "pink", "gold", "tan", "black", "green"]
        for c in colors:
            if c in q_lower:
                intent["color"] = c
                break

        return intent

    def search(self, query: str, top_k: int = 10) -> List[Tuple[Dict[str, Any], float]]:
        """
        Executes hybrid scoring: Cosine similarity on TF-IDF + Intent match boost + Budget constraint filtering.
        """
        intent = self.extract_intent(query)
        q_vec = self.vectorizer.transform([query.lower()])
        cosine_scores = cosine_similarity(q_vec, self.tfidf_matrix).flatten()

        results = []
        for idx, item in enumerate(self.catalog):
            score = float(cosine_scores[idx])

            # Hard filter on budget if specified
            if intent["budget"] and item["price"] > intent["budget"]:
                continue

            # Soft boost for gender alignment
            if intent["gender"] and (item["gender"] == intent["gender"] or item["gender"] == "Unisex"):
                score += 0.25

            # Soft boost for occasion match
            if intent["occasion"] and item["occasion"] == intent["occasion"]:
                score += 0.35

            # Soft boost for color match
            if intent["color"] and intent["color"] in item["color"].lower():
                score += 0.20

            if score > 0.05:
                results.append((item, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def build_outfit_bundle(self, seed_item: Dict[str, Any], max_bundle_budget: int = 6000) -> Dict[str, Any]:
        """
        Coordinates a complete ensemble around a seed item (Topwear + Bottomwear + Footwear/Accessory).
        """
        target_gender = seed_item["gender"]
        target_occasion = seed_item["occasion"]
        seed_cat = seed_item["category"]

        bundle_items = [seed_item]
        remaining_budget = max_bundle_budget - seed_item["price"]

        # Determine complementary categories needed
        desired_categories = []
        if seed_cat in ["Topwear"]:
            desired_categories = ["Bottomwear", "Footwear", "Accessories"]
        elif seed_cat in ["Bottomwear"]:
            desired_categories = ["Topwear", "Footwear", "Accessories"]
        elif seed_cat in ["Dresses", "Ethnic Sets"]:
            desired_categories = ["Footwear", "Accessories"]
        else:
            desired_categories = ["Topwear", "Bottomwear"]

        for req_cat in desired_categories:
            candidates = [
                it for it in self.catalog
                if it["category"] == req_cat
                and (it["gender"] == target_gender or it["gender"] == "Unisex")
                and it["id"] != seed_item["id"]
                and it["price"] <= remaining_budget
            ]

            if candidates:
                # Pick best occasion match or highest rated
                candidates.sort(
                    key=lambda x: (1 if x["occasion"] == target_occasion else 0, x["rating"]),
                    reverse=True
                )
                chosen = candidates[0]
                bundle_items.append(chosen)
                remaining_budget -= chosen["price"]

        total_price = sum(it["price"] for it in bundle_items)
        combo_discount_pct = 12  # 12% Myntra bundle combo discount
        discounted_price = int(total_price * (1 - combo_discount_pct / 100.0))

        return {
            "seed_item": seed_item,
            "items": bundle_items,
            "total_items": len(bundle_items),
            "original_total": total_price,
            "bundle_price": discounted_price,
            "savings": total_price - discounted_price,
            "bundle_theme": f"{target_occasion} Curated Look"
        }
