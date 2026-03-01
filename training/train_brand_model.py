import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from xgboost import XGBClassifier

from app.features.brand_features import extract_brand_features


DATA_PATH = Path("data/processed/brand_full_dataset.csv")
MODEL_PATH = Path("app/models/brand_model.pkl")


def build_feature_matrix(df):
    X = []
    y = []

    for _, row in df.iterrows():
        features = extract_brand_features(row["brand"], row["domain"])
        X.append(features)
        y.append(row["label"])

    return np.array(X), np.array(y)


def main():

    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)

    print("Dataset size:", len(df))
    print(df["label"].value_counts())

    # print("Building feature matrix...")
    # X, y = build_feature_matrix(df)

    # print("Splitting dataset...")
    # X_train, X_test, y_train, y_test = train_test_split(
    #     X, y,
    #     test_size=0.2,
    #     random_state=42,
    #     stratify=y
    # )


    print("Splitting dataset by brand (zero-day simulation)...")
    brands = df["brand"].unique()
    np.random.seed(42)
    np.random.shuffle(brands)

    split_index = int(len(brands) * 0.8)

    train_brands = brands[:split_index]
    test_brands = brands[split_index:]

    train_df = df[df["brand"].isin(train_brands)]
    test_df = df[df["brand"].isin(test_brands)]

    print(f"Train brands: {len(train_brands)}")
    print(f"Test brands: {len(test_brands)}")

    X_train, y_train = build_feature_matrix(train_df)
    X_test, y_test = build_feature_matrix(test_df)



    print("Training XGBoost model...")
    model = XGBClassifier(
        n_estimators=400,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="logloss"
    )

    model.fit(X_train, y_train)
    
    print("\nFeature Importance:")
    for i, score in enumerate(model.feature_importances_):
        print(f"Feature {i}: {score}")

    print("Evaluating...")
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]

    print("\nClassification Report:")
    print(classification_report(y_test, preds))

    print("ROC-AUC:", roc_auc_score(y_test, probs))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"\nModel saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()