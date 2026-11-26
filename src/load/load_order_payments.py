from sqlalchemy import text
from src.extract.extract_data import extract_csv
from src.transform.transform_order_payments import transform_order_payments
from src.utils.database import engine

def load_order_payments(df):
    table_name = "stg_order_payments"
    with engine.begin() as connection:
        connection.execute(
            text("TRUNCATE TABLE staging.stg_order_payments")
        )
        df.to_sql(
            name=table_name,
            con=connection,
            schema="staging",
            if_exists="append",
            index=False,
            chunksize=5000,
            method="multi",
        )

    print(
        f"Successfully loaded {len(df):,} rows "
        f"into staging.{table_name}"
    )

if __name__ == "__main__":
    payments = extract_csv("olist_order_payments_dataset.csv")
    transformed = transform_order_payments(payments)
    load_order_payments(transformed)