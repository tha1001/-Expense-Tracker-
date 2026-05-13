import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib import colors

from database import connect


# ---------------- EXCEL ----------------
def export_to_excel():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM expenses")
    data = cur.fetchall()
    conn.close()

    df = pd.DataFrame(
        data,
        columns=["ID", "Title", "Amount", "Category", "Date"]
    )

    df.to_excel("expenses.xlsx", index=False)

    print("✅ Excel exported!")


# ---------------- PDF ----------------
def export_to_pdf():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM expenses")
    data = cur.fetchall()
    conn.close()

    pdf = SimpleDocTemplate("expenses.pdf")

    table = Table([["ID", "Title", "Amount", "Category", "Date"]] + data)

    table.setStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ])

    pdf.build([table])

    print("📄 PDF exported!")