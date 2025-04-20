from fpdf import FPDF

def generate_report(data, month, template_dir, report_dir):
    # Create PDF object
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Set font
    pdf.set_font("Arial", size=12)

    # Add a title
    pdf.cell(200, 10, txt=f"Monthly Report for {month}", ln=True, align='C')

    # Example content (replace with your actual logic)
    total_income = sum(entry['price'] for entry in data if entry['type'] == 'income' and entry['month'] == month)
    total_spending = sum(entry['price'] for entry in data if entry['type'] == 'spending' and entry['month'] == month)

    # Add content
    pdf.ln(10)  # Line break
    pdf.cell(200, 10, txt=f"Total Income: {total_income:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Total Spending: {total_spending:.2f}", ln=True)

    # Save the PDF to a file
    report_path = f"{report_dir}/monthly_report_{month}.pdf"
    pdf.output(report_path)

    return report_path