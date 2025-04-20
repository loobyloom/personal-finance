import pandas as pd
from pathlib import Path

def load_data(filename):
    if Path(filename).exists():
        return pd.read_csv(filename)
    else:
        return pd.DataFrame(columns=[
            "date", "name", "vendor/target", "price", "currency", "type",
            "category", "subcategory", "details", "payment_method",
            "account", "savings_goal", "month", "savings"
        ])

def add_transaction(entry: dict, filename: str):
    df = load_data(filename)
    df = df.append(entry, ignore_index=True)
    df.to_csv(filename, index=False)
    return df

def get_months(df):
    return sorted(df["month"].unique())