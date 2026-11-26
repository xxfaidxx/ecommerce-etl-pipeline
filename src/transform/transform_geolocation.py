from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "olist"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

CHUNK_SIZE = 100_000


def transform_geolocation(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    df["geolocation_zip_code_prefix"] = (
        df["geolocation_zip_code_prefix"]
        .astype("string")
        .str.strip()
        .str.zfill(5)
    )

    df["geolocation_city"] = (
        df["geolocation_city"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    df["geolocation_state"] = (
        df["geolocation_state"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    df["geolocation_lat"] = pd.to_numeric(
        df["geolocation_lat"], errors="coerce"
    )

    df["geolocation_lng"] = pd.to_numeric(
        df["geolocation_lng"], errors="coerce"
    )

    df["is_outside_brazil"] = ~(
        df["geolocation_lat"].between(-34, 6)
        & df["geolocation_lng"].between(-74, -34)
    )

    return df.reset_index(drop=True)


if __name__ == "__main__":
    input_file = DATA_DIR / "olist_geolocation_dataset.csv"
    output_file = PROCESSED_DIR / "geolocation_transformed.csv"

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    total_rows = 0
    total_outliers = 0

    for chunk_number, chunk in enumerate(
        pd.read_csv(input_file, chunksize=CHUNK_SIZE),
        start=1,
    ):
        transformed = transform_geolocation(chunk)

        transformed.to_csv(
            output_file,
            mode="w" if chunk_number == 1 else "a",
            header=chunk_number == 1,
            index=False,
        )

        total_rows += len(transformed)
        total_outliers += int(transformed["is_outside_brazil"].sum())

        print(
            f"Processed chunk {chunk_number}: "
            f"{len(transformed):,} rows"
        )

    print("\nTransformation Summary")
    print(f"Total rows      : {total_rows:,}")
    print(f"Outside Brazil  : {total_outliers:,}")
    print(f"Output file     : {output_file}")