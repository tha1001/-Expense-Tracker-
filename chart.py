import matplotlib.pyplot as plt
from database import connect

def plot_expenses():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    data = cur.fetchall()
    conn.close()

    if not data:
        print("No data for chart!")
        return

    categories = [d[0] for d in data]
    values = [d[1] for d in data]

    plt.figure()
    plt.bar(categories, values)
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.show()