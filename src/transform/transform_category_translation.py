import pandas as pd

def transform_category_translation(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna(subset=["product_category_name"])
    df = df.drop_duplicates(subset=["product_category_name"])
    df["product_category_name"] = (
        df["product_category_name"].astype("string").str.strip().str.lower()
    )
    df["product_category_name_english"] = (
        df["product_category_name_english"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    df = df.dropna(subset=["product_category_name_english"])
    return df.reset_index(drop=True)

if __name__ == "__main__":
    from src.extract.extract_data import extract_csv
    categories = extract_csv("product_category_name_translation.csv")
    transformed = transform_category_translation(categories)
    print("\nTransformation Summary")
    print(f"Rows before : {len(categories):,}")
    print(f"Rows after  : {len(transformed):,}")
    print(
        "Duplicate category names:",
        categories["product_category_name"].duplicated().sum()
    )
    print(
        "Null category names:",
        categories["product_category_name"].isna().sum()
    )
    print(
        "Null translated names:",
        categories["product_category_name_english"].isna().sum()
    )
    print("\nTransformed Data:")
    print(transformed.head(10))