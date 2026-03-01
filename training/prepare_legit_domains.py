import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/tranco_top.csv")
OUTPUT_PATH = Path("data/processed/brand_legitimate_domains.csv")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(RAW_PATH, header=None, names=["rank", "domain"])

    domains = df["domain"].str.lower()
    
    unique_domains = domains.drop_duplicates()

    legit_df = pd.DataFrame({
        "domain": unique_domains,
        "label": 0
    })

    legit_df.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved {len(legit_df)} legitimate domains to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()