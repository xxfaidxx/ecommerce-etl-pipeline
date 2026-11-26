import pandas as pd

def transform_order_items(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna(subset=["order_id", "order_item_id"])
    df = df.drop_duplicates(
        subset=["order_id", "order_item_id"]
    )
    df["order_item_id"] = pd.to_numeric(
        df["order_item_id"], errors="coerce"
    )
    df["price"] = pd.to_numeric(
        df["price"], errors="coerce"
    )
    df["freight_value"] = pd.to_numeric(
        df["freight_value"], errors="coerce"
    )
    df["shipping_limit_date"] = pd.to_datetime(
        df["shipping_limit_date"], errors="coerce"
    )
    df = df.dropna(
        subset=["order_item_id", "price", "freight_value"]
    )
    df["order_item_id"] = df["order_item_id"].astype("int64")
    df = df.reset_index(drop=True)
    return df

if __name__ == "__main__":
    from src.extract.extract_data import extract_csv
    order_items = extract_csv("olist_order_items_dataset.csv")
    transformed = transform_order_items(order_items)
    print("\nTransformation Summary")
    print(f"Rows before : {len(order_items):,}")
    print(f"Rows after  : {len(transformed):,}")

    print(
        "Duplicate composite keys:",
        order_items.duplicated(
            subset=["order_id", "order_item_id"]
        ).sum()
    )

    print(
        "Null order_id:",
        order_items["order_id"].isna().sum()
    )

    print(
        "Null order_item_id:",
        order_items["order_item_id"].isna().sum()
    )

    print("\nTransformed Data:")
    print(transformed.head())