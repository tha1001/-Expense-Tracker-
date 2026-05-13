from database import connect

def add_expense(title, amount, category, date):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO expenses (title, amount, category, date)
        VALUES (?, ?, ?, ?)
    """, (title, amount, category, date))

    conn.commit()
    conn.close()


def get_all_expenses():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM expenses")
    rows = cur.fetchall()

    conn.close()
    return rows