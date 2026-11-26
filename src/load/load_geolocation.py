import pandas as pd
from pathlib import Path
from src.utils.database import engine

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
CHUNK_SIZE = 100_000

def load_geolocation():
    input_file = PROCESSED_DIR / "geolocation_transformed.csv"

    if not input_file.exists():
        raise FileNotFoundError(f"File not found: {input_file}")

    total_rows = 0
    total_outliers = 0

    with engine.begin() as connection:
        connection.exec_driver_sql(
            "TRUNCATE TABLE staging.stg_geolocation RESTART IDENTITY"
        )

        for chunk_number, chunk in enumerate(
            pd.read_csv(input_file, chunksize=CHUNK_SIZE),
            start=1,
        ):
            chunk["is_outside_brazil"] = (
                chunk["is_outside_brazil"].astype(bool)
            )

            chunk.to_sql(
                name="stg_geolocation",
                con=connection,
                schema="staging",
                if_exists="append",
                index=False,
                chunksize=5000,
                method="multi",
            )

            total_rows += len(chunk)
            total_outliers += int(chunk["is_outside_brazil"].sum())

            print(
                f"Loaded chunk {chunk_number}: "
                f"{len(chunk):,} rows"
            )

    print("\nGeolocation Load Summary")
    print(f"Total rows     : {total_rows:,}")
    print(f"Outside Brazil : {total_outliers:,}")
    print("Load completed successfully!")


if __name__ == "__main__":
    load_geolocation()
