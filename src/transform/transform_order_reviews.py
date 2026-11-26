import pandas as pd

TIMESTAMP_COLUMNS = [
    "review_creation_date",
    "review_answer_timestamp",
]

def transform_order_reviews(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna(subset=["order_id", "review_id"])
    df = df.drop_duplicates(subset=["order_id", "review_id"])
    df["review_score"] = pd.to_numeric(
        df["review_score"], errors="coerce"
    )
    text_columns = [
        "review_comment_title",
        "review_comment_message",
    ]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()
    for column in TIMESTAMP_COLUMNS:
        df[column] = pd.to_datetime(df[column], errors="coerce")
    df = df.dropna(subset=["review_score"])
    df = df[df["review_score"].between(1, 5)]
    df["review_score"] = df["review_score"].astype("int64")
    return df.reset_index(drop=True)

if __name__ == "__main__":
    from src.extract.extract_data import extract_csv
    reviews = extract_csv("olist_order_reviews_dataset.csv")
    transformed = transform_order_reviews(reviews)
    print("\nTransformation Summary")
    print(f"Rows before : {len(reviews):,}")
    print(f"Rows after  : {len(transformed):,}")
    print(
        "Duplicate composite keys:",
        reviews.duplicated(
            subset=["order_id", "review_id"]
        ).sum()
    )
    print("Null order_id:", reviews["order_id"].isna().sum())
    print("Null review_id:", reviews["review_id"].isna().sum())
    print("\nTimestamp Null Summary:")
    print(transformed[TIMESTAMP_COLUMNS].isna().sum())
    print("\nTransformed Data:")
    print(transformed.head())