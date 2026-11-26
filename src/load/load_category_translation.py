from sqlalchemy import text
from src.extract.extract_data import extract_csv
from src.transform.transform_category_translation import transform_category_translation
from src.utils.database import engine

def load_category_translation(df):
    table_name = "stg_category_translation"
    with engine.begin() as connection:
        connection.execute(
            text("TRUNCATE TABLE staging.stg_category_translation")
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
    categories = extract_csv("product_category_name_translation.csv")
    transformed = transform_category_translation(categories)
    load_category_translation(transformed)