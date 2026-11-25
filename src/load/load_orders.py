from sqlalchemy import text
from src.extract.extract_data import extract_csv
from src.transform.transform_orders import transform_orders
from src.utils.database import engine

def load_orders(df):
    table_name = "stg_orders"
    with engine.begin() as connection:
        connection.execute(
            text("TRUNCATE TABLE staging.stg_orders")
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
    orders = extract_csv("olist_orders_dataset.csv")
    transformed = transform_orders(orders)
    load_orders(transformed)