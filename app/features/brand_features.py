import math
import numpy as np
import jellyfish
from collections import Counter
import tldextract
import idna

SUSPICIOUS_TLDS = {"xyz", "top", "club", "click", "gq", "tk"}

def normalize_domain(domain: str) -> str:
    domain = domain.strip().lower()
    domain = domain.replace("http://", "").replace("https://", "")
    domain = domain.split("/")[0]

    try:
        domain = idna.decode(domain)
    except:
        pass

    ext = tldextract.extract(domain)
    if ext.suffix:
        return ext.domain + "." + ext.suffix
    return ext.domain


def shannon_entropy(string: str) -> float:
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    return -sum([p * math.log2(p) for p in prob])


def levenshtein_ratio(a: str, b: str) -> float:
    dist = jellyfish.levenshtein_distance(a, b)
    return max(0, 1 - (dist / max(len(a), 1)))


def jaro_winkler(a: str, b: str) -> float:
    return jellyfish.jaro_winkler_similarity(a, b)


def ngram_cosine(a: str, b: str, n=2) -> float:
    def ngrams(s):
        return [s[i:i+n] for i in range(len(s)-n+1)]

    a_ngrams = Counter(ngrams(a))
    b_ngrams = Counter(ngrams(b))

    intersection = sum((a_ngrams & b_ngrams).values())
    norm_a = sum(v**2 for v in a_ngrams.values()) ** 0.5
    norm_b = sum(v**2 for v in b_ngrams.values()) ** 0.5

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return intersection / (norm_a * norm_b)


def extract_brand_features(brand: str, domain: str) -> np.ndarray:

    brand = brand.lower()
    domain = normalize_domain(domain)
    unicode_flag = contains_unicode(domain)
    tld_flag = tld_risk(domain)
    brand_position = brand_position_feature(brand, domain)

    lev_sim = levenshtein_ratio(brand, domain)
    jw_sim = jaro_winkler(brand, domain)
    ngram_sim = ngram_cosine(brand, domain)

    entropy = shannon_entropy(domain)

    digit_ratio = sum(c.isdigit() for c in domain) / len(domain)
    hyphen_count = domain.count("-")

    keyword_flag = int(any(k in domain for k in ["login", "secure", "verify", "auth"]))
    brand_in_domain = int(brand in domain)

    return np.array([
        lev_sim,
        jw_sim,
        ngram_sim,
        entropy,
        digit_ratio,
        hyphen_count,
        keyword_flag,
        brand_in_domain,
        len(domain),
        unicode_flag,
        tld_flag,
        brand_position
    ])

def contains_unicode(domain: str) -> int:
    return int(any(ord(c) > 127 for c in domain))


def tld_risk(domain: str) -> int:
    tld = domain.split(".")[-1]
    return int(tld in SUSPICIOUS_TLDS)


def brand_position_feature(brand: str, domain: str) -> float:
    if brand not in domain:
        return -1
    return domain.index(brand) / len(domain)