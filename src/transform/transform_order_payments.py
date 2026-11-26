import pandas as pd

def transform_order_payments(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna(
        subset=["order_id", "payment_sequential"]
    )
    df = df.drop_duplicates(
        subset=["order_id", "payment_sequential"]
    )
    df["payment_sequential"] = pd.to_numeric(
        df["payment_sequential"], errors="coerce"
    )
    df["payment_installments"] = pd.to_numeric(
        df["payment_installments"], errors="coerce"
    )
    df["payment_value"] = pd.to_numeric(
        df["payment_value"], errors="coerce"
    )
    df["payment_type"] = (
        df["payment_type"].astype("string").str.strip().str.lower()
    )
    df = df.dropna(
        subset=[
            "payment_sequential",
            "payment_installments",
            "payment_value",
        ]
    )

    df["payment_sequential"] = df["payment_sequential"].astype("int64")
    df["payment_installments"] = df["payment_installments"].astype("int64")

    return df.reset_index(drop=True)
if __name__ == "__main__":
    from src.extract.extract_data import extract_csv

    payments = extract_csv("olist_order_payments_dataset.csv")
    transformed = transform_order_payments(payments)
    print("\nTransformation Summary")
    print(f"Rows before : {len(payments):,}")
    print(f"Rows after  : {len(transformed):,}")
    print(
        "Duplicate composite keys:",
        payments.duplicated(
            subset=["order_id", "payment_sequential"]
        ).sum()
    )
    print("Null order_id:", payments["order_id"].isna().sum())
    print(
        "Null payment_sequential:",
        payments["payment_sequential"].isna().sum()
    )
    print("\nTransformed Data:")
    print(transformed.head())