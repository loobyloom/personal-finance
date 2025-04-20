import pandas as pd

def summarize_by_category(df: pd.DataFrame, selected_month: str):
    monthly_df = df[df["month"] == selected_month]
    grouped = monthly_df.groupby(["type", "category"])["price"].sum().reset_index()
    
    income_cats = grouped[grouped["type"] == "income"][["category", "price"]].rename(columns={"price": "amount"})
    spending_cats = grouped[grouped["type"] == "spending"][["category", "price"]].rename(columns={"price": "amount"})

    return {
        "income_by_category": income_cats,
        "spending_by_category": spending_cats
    }
