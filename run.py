import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_handler import load_data, add_transaction, get_months
from utils.forecast import forecast_savings
from utils.comparison import compare_months
from utils.category import summarize_by_category
from utils.report_generator import generate_report

DATA_FILE = "data/transactions.csv"
TEMPLATE_DIR = "templates"
REPORT_DIR = "reports"

st.set_page_config(page_title="Personal Finance Tracker", layout="wide")
st.title("📊 Personal Finance Tracker")

data = load_data(DATA_FILE)

with st.sidebar:
    st.header("➕ Add Transaction")
    with st.form("transaction_form"):
        date = st.date_input("Date", datetime.today())
        name = st.text_input("Name")
        vendor = st.text_input("Vendor/Target")
        price = st.number_input("Price", min_value=0.0, step=0.01)
        currency = st.selectbox("Currency", ["RON", "EUR", "USD"])
        type_ = st.selectbox("Type", ["income", "spending"])
        category = st.text_input("Category")
        subcategory = st.text_input("Subcategory")
        details = st.text_area("Details")
        payment_method = st.selectbox("Payment Method", ["Card", "Cash", "Bank Transfer"])
        account = st.text_input("Account")
        savings_goal = st.number_input("Savings Goal", min_value=0.0, step=0.01)

        submitted = st.form_submit_button("Add Entry")
        if submitted:
            month = f"{date.year}-{date.month:02d}"
            savings = price if type_ == "income" else -price
            entry = {
                "date": date.strftime("%Y-%m-%d"),
                "name": name,
                "vendor/target": vendor,
                "price": price,
                "currency": currency,
                "type": type_,
                "category": category,
                "subcategory": subcategory,
                "details": details,
                "payment_method": payment_method,
                "account": account,
                "savings_goal": savings_goal,
                "month": month,
                "savings": savings,
            }
            data = add_transaction(entry, DATA_FILE)
            st.success("Transaction added!")

months = get_months(data)

st.header("📆 Monthly Overview")
selected_month = st.selectbox("Select Month", months)

if selected_month:
    forecast = forecast_savings(data, selected_month)
    summary = summarize_by_category(data, selected_month)

    col1, col2, col3 = st.columns(3)
    col1.metric("Net Savings", f"{forecast['net_savings']:.2f}")
    col2.metric("Projected Savings", f"{forecast['projected_savings']:.2f}")
    col3.metric("Status", forecast['status'].capitalize())

    st.subheader("💰 Category Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Income by Category**")
        st.dataframe(summary["income_by_category"])
    with col2:
        st.markdown("**Spending by Category**")
        st.dataframe(summary["spending_by_category"])

st.header("📊 Compare Months")
if len(months) >= 2:
    col1, col2 = st.columns(2)
    month1 = col1.selectbox("Month 1", months, index=0, key="m1")
    month2 = col2.selectbox("Month 2", months, index=1, key="m2")
    if month1 != month2:
        comparison = compare_months(data, month1, month2)
        delta = comparison["delta"]

        col1.metric(f"Income Change", f"{delta['income_diff']:.2f}")
        col2.metric(f"Spending Change", f"{delta['spending_diff']:.2f}")
        st.metric(f"Savings Change", f"{delta['savings_diff']:.2f}")

st.header("📄 Generate Monthly Report")
report_month = st.selectbox("Select month for report", months, key="report_month")
if st.button("Generate PDF Report"):
    pdf_path = generate_report(data, report_month, TEMPLATE_DIR, REPORT_DIR)
    st.success(f"Report generated: {pdf_path}")
