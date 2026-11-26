
from sqlalchemy import text
from src.extract.extract_data import extract_csv
from src.transform.transform_sellers import transform_sellers
from src.utils.database import engine

def load_sellers(df):
    table_name = "stg_sellers"
    with engine.begin() as connection:
        connection.execute(
            text("TRUNCATE TABLE staging.stg_sellers")
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
    sellers = extract_csv("olist_sellers_dataset.csv")
    transformed = transform_sellers(sellers)
    load_sellers(transformed)