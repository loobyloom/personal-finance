import pandas as pd
from datetime import datetime

def forecast_savings(df: pd.DataFrame, selected_month: str):
    monthly_df = df[df["month"] == selected_month]
    today = datetime.today().day
    
    total_income = monthly_df[monthly_df["type"] == "income"]["price"].sum()
    total_expense = monthly_df[monthly_df["type"] == "spending"]["price"].sum()
    net_savings = total_income - total_expense

    avg_daily_savings = net_savings / today if today > 0 else 0
    
    # Estimate end of month savings
    now = datetime.now()
    _, last_day = pd.Period(f'{now.year}-{now.month}').days_in_month, pd.Period(f'{now.year}-{now.month}').days_in_month
    projected_savings = avg_daily_savings * last_day

    status = "on track" if projected_savings >= df["savings_goal"].astype(float).mean() else "below goal"

    return {
        "net_savings": net_savings,
        "avg_daily_savings": avg_daily_savings,
        "projected_savings": projected_savings,
        "status": status
    }