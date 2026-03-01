import tldextract
import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/openphish_feed.txt")
OUTPUT_PATH = Path("data/processed/brand_phishing_domains.csv")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def extract_domain(url: str) -> str:
    ext = tldextract.extract(url)
    if ext.domain and ext.suffix:
        return f"{ext.domain}.{ext.suffix}"
    return None


def main():
    domains = []

    with open(RAW_PATH, "r", encoding="utf-8") as f:
        for line in f:
            url = line.strip()
            if not url:
                continue

            domain = extract_domain(url)
            if domain:
                domains.append(domain.lower())

    
    unique_domains = list(set(domains))

    df = pd.DataFrame({
        "domain": unique_domains,
        "label": 1  
    })

    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved {len(df)} phishing domains to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()