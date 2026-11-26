import pandas as pd

def transform_sellers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna(subset=["seller_id"])
    df = df.drop_duplicates(subset=["seller_id"])
    df["seller_city"] = (
        df["seller_city"].astype("string").str.strip().str.lower()
    )
    df["seller_state"] = (
        df["seller_state"].astype("string").str.strip().str.upper()
    )
    df["seller_zip_code_prefix"] = (
        df["seller_zip_code_prefix"]
        .astype("string")
        .str.strip()
        .str.zfill(5)
    )
    return df.reset_index(drop=True)

if __name__ == "__main__":
    from src.extract.extract_data import extract_csv
    sellers = extract_csv("olist_sellers_dataset.csv")
    transformed = transform_sellers(sellers)
    print("\nTransformation Summary")
    print(f"Rows before : {len(sellers):,}")
    print(f"Rows after  : {len(transformed):,}")
    print("Duplicate seller IDs:", sellers["seller_id"].duplicated().sum())
    print("Null seller IDs:", sellers["seller_id"].isna().sum())
    print("\nTransformed Data:")
    print(transformed.head())