import os
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

class FakeNewsClassifier:

    def __init__(self, model_path="models/fake_news_model.pkl"):
        self.model_path = model_path

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model file not found: {self.model_path}\n"
                "➡ Train first by running: python src/classifier.py"
            )

        # Load trained model
        with open(self.model_path, "rb") as f:
            saved = pickle.load(f)

        self.vectorizer = saved["vectorizer"]
        self.classifier = saved["classifier"]

        print("✓ Loaded trained ML classifier")

    def _extract_features(self, text):
        text_lower = text.lower()
        features = {}

        sensational_words = [
            'shocking','unbelievable','breaking','urgent','exposed',
            'secret','truth','conspiracy','hidden','revealed'
        ]
        features['sensational_count'] = sum(w in text_lower for w in sensational_words)

        import re
        patterns = [
            r"you won'?t believe", r"this will \w+ your \w+", r"one simple trick",
            r"doctors hate", r"click to find out", r"what happened next"
        ]
        features['clickbait_count'] = sum(bool(re.search(p, text_lower)) for p in patterns)

        words = text.split()
        caps_words = [w for w in words if w.isupper() and len(w) > 2]
        features['caps_ratio'] = len(caps_words) / len(words) if words else 0

        features['exclamation_count'] = text.count('!')
        emotional_words = ['fear','panic','crisis','disaster','dangerous','deadly']
        features['emotional_count'] = sum(w in text_lower for w in emotional_words)

        manual_score = (
            features['sensational_count'] * 0.15 +
            features['clickbait_count'] * 0.25 +
            features['caps_ratio'] * 0.20 +
            min(features['exclamation_count'], 3) * 0.10 +
            features['emotional_count'] * 0.10
        )

        features["manual_score"] = min(manual_score, 1.0)
        return features

    def analyze_style(self, text):
        features = self._extract_features(text)

        try:
            X_vec = self.vectorizer.transform([text])
            decision = self.classifier.decision_function(X_vec)[0]
            style_score = 1 / (1 + np.exp(-decision))
        except:
            style_score = features["manual_score"]

        return {
            "style_score": float(style_score),
            "confidence": 0.7,
            "features": features
        }


# TRAINING MODE
if __name__ == "__main__":
    # Only used to train once
    print("Training classifier...")

    data_fake = pd.read_csv("data/Fake.csv")
    data_true = pd.read_csv("data/True.csv")

    X = data_fake["text"].tolist() + data_true["text"].tolist()
    y = [1] * len(data_fake) + [0] * len(data_true)

    vectorizer = TfidfVectorizer(max_features=5000, stop_words="english", ngram_range=(1,3))
    X_vec = vectorizer.fit_transform(X)

    clf = LinearSVC(class_weight="balanced", max_iter=10000)
    clf.fit(X_vec, y)

    os.makedirs("models", exist_ok=True)
    with open("models/fake_news_model.pkl", "wb") as f:
        pickle.dump({"vectorizer": vectorizer, "classifier": clf}, f)

    print("✓ Model trained and saved!")
