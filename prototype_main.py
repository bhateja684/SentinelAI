# prototype_main.py

from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import math
import uvicorn

app = FastAPI(title="Digital Risk Intelligence Prototype")
 
def shannon_entropy(string: str) -> float:
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    return -sum([p * math.log2(p) for p in prob])


def levenshtein_distance(a: str, b: str) -> int:
    if len(a) < len(b):
        return levenshtein_distance(b, a)
    if len(b) == 0:
        return len(a)

    previous_row = range(len(b) + 1)
    for i, c1 in enumerate(a):
        current_row = [i + 1]
        for j, c2 in enumerate(b):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def extract_brand_features(brand, domain):
    brand = brand.lower()
    domain = domain.lower()

    lev_dist = levenshtein_distance(brand, domain)
    similarity = 1 - (lev_dist / max(len(brand), 1))
    entropy = shannon_entropy(domain)
    keyword_flag = int(any(k in domain for k in ["login", "secure", "auth", "verify"]))

    return np.array([similarity, entropy, keyword_flag, len(domain)])

def extract_signup_features(email, username):
    domain = email.split("@")[-1]

    entropy = shannon_entropy(username)
    digit_ratio = sum(c.isdigit() for c in username) / len(username)
    disposable_domains = ["tempmail.xyz", "mailinator.com", "10minutemail.com"]
    disposable_flag = int(domain in disposable_domains)

    return np.array([entropy, digit_ratio, disposable_flag, len(username)])

def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def hybrid_model(features):
    weights = np.array([0.6, 0.4, 0.8, 0.2])
    score = np.dot(weights, features)
    return sigmoid(score)


class BrandRequest(BaseModel):
    brand_name: str
    domain: str

class SignupRequest(BaseModel):
    email: str
    username: str


 
@app.post("/brand-risk")
def brand_risk(request: BrandRequest):
    features = extract_brand_features(request.brand_name, request.domain)
    risk = hybrid_model(features)

    def risk_tier(score):
        if score > 0.8:
            return "HIGH"
        elif score > 0.5:
            return "MEDIUM"
        else:
            return "LOW"

    return {
        "risk_score": round(float(risk), 3),
        "risk_level": risk_tier(risk),
        "explanation": {
            "high_similarity": bool(features[0] > 0.7),
            "high_entropy": bool(features[1] > 3.5),
            "suspicious_keyword": bool(features[2])
        }
    }

# def brand_risk(request: BrandRequest):
#     features = extract_brand_features(request.brand_name, request.domain)
#     risk = hybrid_model(features)

#     def risk_tier(score):
#     if score > 0.8:
#         return "HIGH"
#     elif score > 0.5:
#         return "MEDIUM"
#     else:
#         return "LOW"

#     return {
#         "risk_score": round(float(risk), 3),
#         "risk_level": risk_tier(risk),
#         "explanation": {
#             "high_similarity": features[0] > 0.7,
#             "high_entropy": features[1] > 3.5,
#             "suspicious_keyword": bool(features[2])
#         }
#     }




@app.post("/signup-risk")
def signup_risk(request: SignupRequest):
    features = extract_signup_features(request.email, request.username)
    risk = hybrid_model(features)

    return {
        "fraud_score": round(float(risk), 3),
        "features": features.tolist()
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)