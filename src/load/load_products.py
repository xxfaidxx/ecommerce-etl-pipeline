from sqlalchemy import text
from src.extract.extract_data import extract_csv
from src.transform.transform_products import transform_products
from src.utils.database import engine

def load_products(df):
    table_name = "stg_products"
    with engine.begin() as connection:
        connection.execute(
            text("TRUNCATE TABLE staging.stg_products")
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
    products = extract_csv("olist_products_dataset.csv")
    transformed = transform_products(products)
    load_products(transformed)