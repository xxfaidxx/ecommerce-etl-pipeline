
from sqlalchemy import text
from src.extract.extract_data import extract_csv
from src.transform.transform_customers import transform_customers
from src.utils.database import engine

def load_customers(df):
    table_name = "stg_customers"
    with engine.begin() as connection:
        connection.execute(
            text("TRUNCATE TABLE staging.stg_customers")
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
    print(f"Successfully loaded {len(df):,} rows into staging.{table_name}")

if __name__ == "__main__":
    customers = extract_csv("olist_customers_dataset.csv")
    transformed = transform_customers(customers)
    load_customers(transformed)
