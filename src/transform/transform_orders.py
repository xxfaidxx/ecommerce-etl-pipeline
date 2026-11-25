import pandas as pd

TIMESTAMP_COLUMNS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna(subset=["order_id"])
    df = df.drop_duplicates(subset=["order_id"])
    df["order_status"] = (
        df["order_status"]
        .astype("string")
        .str.strip()
        .str.lower()
    )
    for column in TIMESTAMP_COLUMNS:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )
    df = df.reset_index(drop=True)
    return df

if __name__ == "__main__":
    from src.extract.extract_data import extract_csv
    orders = extract_csv("olist_orders_dataset.csv")
    transformed = transform_orders(orders)
    print("\nTransformation Summary")
    print(f"Rows before : {len(orders):,}")
    print(f"Rows after  : {len(transformed):,}")
    print(f"Duplicate IDs: {orders['order_id'].duplicated().sum():,}")
    print(f"Null order IDs: {orders['order_id'].isna().sum():,}")
    print("\nTimestamp Null Summary:")
    print(transformed[TIMESTAMP_COLUMNS].isna().sum())
    print("\nTransformed Data:")
    print(transformed.head())