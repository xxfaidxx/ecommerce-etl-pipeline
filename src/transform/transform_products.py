import pandas as pd
NUMERIC_COLUMNS = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
]

def transform_products(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna(subset=["product_id"])
    df = df.drop_duplicates(subset=["product_id"])
    df["product_category_name"] = (
        df["product_category_name"].astype("string").str.strip().str.lower()
    )
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    for column in NUMERIC_COLUMNS:
        df[column] = df[column].astype("Int64")
    return df.reset_index(drop=True)

if __name__ == "__main__":
    from src.extract.extract_data import extract_csv
    products = extract_csv("olist_products_dataset.csv")
    transformed = transform_products(products)
    print("\nTransformation Summary")
    print(f"Rows before : {len(products):,}")
    print(f"Rows after  : {len(transformed):,}")
    print("Duplicate product IDs:", products["product_id"].duplicated().sum())
    print("Null product IDs:", products["product_id"].isna().sum())
    print("\nNumeric Null Summary:")
    print(transformed[NUMERIC_COLUMNS].isna().sum())
    print("\nTransformed Data:")
    print(transformed.head())