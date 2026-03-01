import pandas as pd
from pathlib import Path

SYNTH_PATH = Path("data/processed/brand_synthetic_dataset.csv")
TRANC0_PATH = Path("data/processed/brand_legitimate_domains.csv")
OUTPUT_PATH = Path("data/processed/brand_full_dataset.csv")

def main():

    synth_df = pd.read_csv(SYNTH_PATH)
    legit_pool = pd.read_csv(TRANC0_PATH)

    legit_sample = legit_pool.sample(n=2000, random_state=42)

    legit_rows = []

    brands = synth_df["brand"].unique()

    for domain in legit_sample["domain"]:
        random_brand = pd.Series(brands).sample(1).values[0]
        legit_rows.append([random_brand, domain, 0])

    legit_df = pd.DataFrame(
        legit_rows,
        columns=["brand", "domain", "label"]
    )

    final_df = pd.concat([synth_df, legit_df])
    final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)

    final_df.to_csv(OUTPUT_PATH, index=False)

    print("Final dataset distribution:")
    print(final_df["label"].value_counts())


if __name__ == "__main__":
    main()