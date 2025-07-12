from fpdf import FPDF

# Replace this with your full Streamlit code as a string
streamlit_code = """<YOUR FULL STREAMLIT CODE HERE>"""

# Create a PDF object
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=10)
pdf.add_page()
pdf.set_font("Courier", size=8)

# Add the code line by line
for line in streamlit_code.split('\n'):
    pdf.multi_cell(0, 4.5, line)

# Save the PDF
pdf.output("health_dashboard_code.pdf")
print("✅ PDF saved as 'health_dashboard_code.pdf'")
