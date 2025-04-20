import pandas as pd

def compare_months(df: pd.DataFrame, month1: str, month2: str):
    def summarize(month):
        monthly_df = df[df["month"] == month]
        income = monthly_df[monthly_df["type"] == "income"]["price"].sum()
        spending = monthly_df[monthly_df["type"] == "spending"]["price"].sum()
        savings = income - spending
        return {"income": income, "spending": spending, "savings": savings}

    summary1 = summarize(month1)
    summary2 = summarize(month2)

    delta = {
        "income_diff": summary2["income"] - summary1["income"],
        "spending_diff": summary2["spending"] - summary1["spending"],
        "savings_diff": summary2["savings"] - summary1["savings"]
    }

    return {
        "month1": month1,
        "summary1": summary1,
        "month2": month2,
        "summary2": summary2,
        "delta": delta
    }