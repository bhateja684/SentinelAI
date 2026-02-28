import joblib
import numpy as np
from app.features.brand_features import extract_brand_features

class BrandRiskService:

    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)

    def risk_tier(self, score: float) -> str:
        if score > 0.8:
            return "HIGH"
        elif score > 0.5:
            return "MEDIUM"
        return "LOW"

    def evaluate(self, brand: str, domain: str):
        features = extract_brand_features(brand, domain)
        risk = float(self.model.predict_proba([features])[0][1])

        return {
            "risk_score": round(risk, 3),
            "risk_level": self.risk_tier(risk),
            "explanation": {
                "high_similarity": bool(features[0] > 0.7),
                "high_entropy": bool(features[1] > 3.5),
                "suspicious_keyword": bool(features[2])
            }
        }