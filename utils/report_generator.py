import pandas as pd
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from datetime import datetime
from pathlib import Path

def generate_report(df: pd.DataFrame, month: str, template_dir: str, output_dir: str):
    monthly_data = df[df["month"] == month].copy()
    income = monthly_data[monthly_data["type"] == "income"]["price"].sum()
    spending = monthly_data[monthly_data["type"] == "spending"]["price"].sum()
    savings = income - spending

    monthly_data_sorted = monthly_data.sort_values("date")

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("report_template.html")

    html_content = template.render(
        month=month,
        income=income,
        spending=spending,
        savings=savings,
        transactions=monthly_data_sorted.to_dict(orient="records"),
        generated_on=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    html_path = Path(output_dir) / f"report_{month}.html"
    pdf_path = Path(output_dir) / f"report_{month}.pdf"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    HTML(string=html_content).write_pdf(pdf_path)

    return str(pdf_path)