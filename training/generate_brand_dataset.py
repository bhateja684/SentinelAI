import random
import pandas as pd
from pathlib import Path

BRAND_PATH = Path("data/raw/brands.txt")
OUTPUT_PATH = Path("data/processed/brand_synthetic_dataset.csv")

SUSPICIOUS_TLDS = ["xyz", "top", "info", "ru", "cn"]
KEYWORDS = ["login", "secure", "verify", "auth", "update"]

HOMOGLYPHS = {
    "o": "0",
    "l": "1",
    "e": "3",
    "a": "@",
    "i": "1"
}


def load_brands():
    with open(BRAND_PATH, "r") as f:
        return [b.strip().lower() for b in f.readlines()]


def substitute_char(brand):
    brand_list = list(brand)
    for i, c in enumerate(brand_list):
        if c in HOMOGLYPHS:
            brand_list[i] = HOMOGLYPHS[c]
            break
    return "".join(brand_list)


def insert_random_char(brand):
    pos = random.randint(0, len(brand))
    char = random.choice("abcdefghijklmnopqrstuvwxyz0123456789")
    return brand[:pos] + char + brand[pos:]


def delete_char(brand):
    if len(brand) > 3:
        pos = random.randint(0, len(brand)-1)
        return brand[:pos] + brand[pos+1:]
    return brand


def keyword_injection(brand):
    return f"{brand}-{random.choice(KEYWORDS)}"


def random_tld():
    return random.choice(SUSPICIOUS_TLDS)


def generate_variants(brand):
    variants = set()

    for _ in range(10):
        variants.add(substitute_char(brand))
        variants.add(insert_random_char(brand))
        variants.add(delete_char(brand))
        variants.add(keyword_injection(brand))

    return list(variants)


def main():
    brands = load_brands()

    rows = []

    for brand in brands:
        rows.append([brand, f"{brand}.com", 0])

        
        variants = generate_variants(brand)

        for v in variants:
            domain = f"{v}.{random_tld()}"
            rows.append([brand, domain, 1])

    df = pd.DataFrame(rows, columns=["brand", "domain", "label"])
    df.to_csv(OUTPUT_PATH, index=False)

    print("Dataset created.")
    print(df["label"].value_counts())


if __name__ == "__main__":
    main()