
import pandas as pd


def transform_customers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    text_columns = ["customer_city", "customer_state"]
    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()
    df = df.dropna(subset=["customer_id"])
    df = df.drop_duplicates(subset=["customer_id"])
    df["customer_zip_code_prefix"] = (
        df["customer_zip_code_prefix"]
        .astype("string")
        .str.zfill(5)
    )
    df["customer_state"] = df["customer_state"].str.upper()
    df = df.reset_index(drop=True)
    return df

if __name__ == "__main__":
    from src.extract.extract_data import extract_csv
    customers = extract_csv("olist_customers_dataset.csv")
    transformed = transform_customers(customers)
    print("\nTransformation Summary")
    print(f"Rows before : {len(customers):,}")
    print(f"Rows after  : {len(transformed):,}")
    print(f"Duplicates  : {customers['customer_id'].duplicated().sum():,}")
    print(f"Null IDs    : {customers['customer_id'].isna().sum():,}")
    print("\nTransformed Data:")
    print(transformed.head())
