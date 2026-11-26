from sqlalchemy import text
from src.extract.extract_data import extract_csv
from src.transform.transform_order_reviews import transform_order_reviews
from src.utils.database import engine

def load_order_reviews(df):
    table_name = "stg_order_reviews"
    with engine.begin() as connection:
        connection.execute(
            text("TRUNCATE TABLE staging.stg_order_reviews")
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
    reviews = extract_csv("olist_order_reviews_dataset.csv")
    transformed = transform_order_reviews(reviews)
    load_order_reviews(transformed)