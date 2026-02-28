import math
import numpy as np


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


def extract_brand_features(brand: str, domain: str) -> np.ndarray:
    brand = brand.lower()
    domain = domain.lower()

    lev_dist = levenshtein_distance(brand, domain)
    similarity = max(0, 1 - (lev_dist / max(len(brand), 1)))
    entropy = shannon_entropy(domain)
    keyword_flag = int(any(k in domain for k in ["login", "secure", "auth", "verify"]))
    length = len(domain)

    return np.array([similarity, entropy, keyword_flag, length])