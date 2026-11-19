from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "olist"

def extract_csv(filename: str) -> pd.DataFrame:
    file_path = DATA_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    df = pd.read_csv(file_path)
    print(f"Extracted: {filename}")
    print(f"Rows     : {len(df):,}")
    print(f"Columns  : {len(df.columns)}")
    return df

if __name__ == "__main__":
    customers = extract_csv("olist_customers_dataset.csv")
    print(customers.head())
