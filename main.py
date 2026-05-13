import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database import create_table, connect
from tracker import add_expense, get_all_expenses
from chart import plot_expenses
from export import export_to_excel, export_to_pdf


# ---------------- PASSWORD ----------------
PASSWORD = "1234"


# ---------------- APP START ----------------
def start_app():
    create_table()

    root = tk.Tk()
    root.title("💰 Expense Tracker PRO ULTRA")
    root.geometry("800x550")
    root.configure(bg="#1e1e2e")

    selected_id = tk.StringVar()

    # ---------------- FUNCTIONS ----------------
    def refresh():
        for row in table.get_children():
            table.delete(row)

        for r in get_all_expenses():
            table.insert("", "end", values=r)


    def on_select(event):
        item = table.focus()
        if not item:
            return

        values = table.item(item, "values")
        selected_id.set(values[0])

        title_entry.delete(0, tk.END)
        title_entry.insert(0, values[1])

        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, values[2])

        category_entry.delete(0, tk.END)
        category_entry.insert(0, values[3])


    def add():
        add_expense(
            title_entry.get(),
            float(amount_entry.get()),
            category_entry.get(),
            datetime.now().strftime("%Y-%m-%d")
        )
        refresh()


    def delete():
        if not selected_id.get():
            messagebox.showerror("Error", "Select item first!")
            return

        conn = connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM expenses WHERE id=?", (selected_id.get(),))
        conn.commit()
        conn.close()

        refresh()


    def update():
        if not selected_id.get():
            messagebox.showerror("Error", "Select item first!")
            return

        conn = connect()
        cur = conn.cursor()

        cur.execute("""
            UPDATE expenses
            SET title=?, amount=?, category=?
            WHERE id=?
        """, (
            title_entry.get(),
            float(amount_entry.get()),
            category_entry.get(),
            selected_id.get()
        ))

        conn.commit()
        conn.close()
        refresh()


    def search():
        keyword = search_entry.get()

        conn = connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT * FROM expenses
            WHERE title LIKE ? OR category LIKE ?
        """, (f"%{keyword}%", f"%{keyword}%"))

        rows = cur.fetchall()
        conn.close()

        for row in table.get_children():
            table.delete(row)

        for r in rows:
            table.insert("", "end", values=r)


    # ---------------- INPUTS ----------------
    top = tk.Frame(root, bg="#1e1e2e")
    top.pack(pady=10)

    tk.Label(top, text="Title", bg="#1e1e2e", fg="white").grid(row=0, column=0)
    title_entry = ttk.Entry(top)
    title_entry.grid(row=0, column=1)

    tk.Label(top, text="Amount", bg="#1e1e2e", fg="white").grid(row=1, column=0)
    amount_entry = ttk.Entry(top)
    amount_entry.grid(row=1, column=1)

    tk.Label(top, text="Category", bg="#1e1e2e", fg="white").grid(row=2, column=0)
    category_entry = ttk.Entry(top)
    category_entry.grid(row=2, column=1)


    # ---------------- SEARCH ----------------
    search_entry = ttk.Entry(root)
    search_entry.pack(pady=5)

    ttk.Button(root, text="🔍 Search", command=search).pack()


    # ---------------- BUTTONS ----------------
    btns = tk.Frame(root, bg="#1e1e2e")
    btns.pack(pady=10)

    ttk.Button(btns, text="➕ Add", command=add).grid(row=0, column=0, padx=5)
    ttk.Button(btns, text="🗑 Delete", command=delete).grid(row=0, column=1, padx=5)
    ttk.Button(btns, text="✏ Update", command=update).grid(row=0, column=2, padx=5)
    ttk.Button(btns, text="📊 Chart", command=plot_expenses).grid(row=0, column=3, padx=5)
    ttk.Button(btns, text="📁 Excel", command=export_to_excel).grid(row=0, column=4, padx=5)
    ttk.Button(btns, text="📄 PDF", command=export_to_pdf).grid(row=0, column=5, padx=5)
    ttk.Button(btns, text="🔄 Refresh", command=refresh).grid(row=0, column=6, padx=5)


    # ---------------- TABLE ----------------
    cols = ("ID", "Title", "Amount", "Category", "Date")

    table = ttk.Treeview(root, columns=cols, show="headings")

    for c in cols:
        table.heading(c, text=c)
        table.column(c, width=140)

    table.pack(fill="both", expand=True, pady=10)

    table.bind("<<TreeviewSelect>>", on_select)

    refresh()

    root.mainloop()


# ---------------- LOGIN ----------------
login = tk.Tk()
login.title("Login")
login.geometry("300x150")

tk.Label(login, text="Enter Password").pack(pady=10)

pass_entry = tk.Entry(login, show="*")
pass_entry.pack()


def check():
    if pass_entry.get() == PASSWORD:
        login.destroy()
        start_app()
    else:
        messagebox.showerror("Error", "Wrong password!")


tk.Button(login, text="Login", command=check).pack(pady=10)

login.mainloop()