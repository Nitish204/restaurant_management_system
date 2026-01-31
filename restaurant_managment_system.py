""" A modern Restaurant-Management-System using Pyhton and Tkinter with enhansed UI and with Stock Tracking and Smart Billing System """
import tkinter as tk
from tkinter import messagebox
import random
import datetime
import sqlite3

# ================= DATABASE =================
conn = sqlite3.connect("restaurant.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT,
    total REAL,
    date TEXT
)
""")
conn.commit()

# ================= INVENTORY =================
MENU = {
    "Idly": {"price": 25, "stock": 50},
    "Dosa": {"price": 35, "stock": 40},
    "Kesari Bath": {"price": 25, "stock": 30},
    "Pulav": {"price": 35, "stock": 25},
    "Kara Bath": {"price": 20, "stock": 30},
    "Drinks": {"price": 20, "stock": 60}
}

# ================= WINDOW =================
root = tk.Tk()
root.title("Advanced Restaurant Management System")
root.geometry("1200x700")
root.config(bg="#ecf0f1")

# ================= HEADER =================
header = tk.Frame(root, bg="#34495e", pady=10)
header.pack(fill=tk.X)

tk.Label(header, text="AMRUTHA RESTAURANT",
         font=("Arial", 28, "bold"),
         fg="white", bg="#34495e").pack()

tk.Label(header, text=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
         font=("Arial", 12),
         fg="lightgray", bg="#34495e").pack()

# ================= VARIABLES =================
order_vars = {}
receipt_text = tk.StringVar()
subtotal_var = tk.StringVar()
total_var = tk.StringVar()
ref_var = tk.StringVar()

# ================= ORDER FRAME =================
order_frame = tk.LabelFrame(root, text="Order Menu", font=("Arial", 14, "bold"), bg="#ecf0f1")
order_frame.pack(side=tk.LEFT, padx=20, pady=20)

tk.Label(order_frame, text="Item", font=("Arial", 12, "bold"), bg="#ecf0f1").grid(row=0, column=0)
tk.Label(order_frame, text="Qty", font=("Arial", 12, "bold"), bg="#ecf0f1").grid(row=0, column=1)
tk.Label(order_frame, text="Stock", font=("Arial", 12, "bold"), bg="#ecf0f1").grid(row=0, column=2)

for i, item in enumerate(MENU):
    tk.Label(order_frame, text=f"{item} (₹{MENU[item]['price']})",
             bg="#ecf0f1").grid(row=i+1, column=0, sticky="w")
    qty = tk.StringVar()
    order_vars[item] = qty
    tk.Entry(order_frame, textvariable=qty, width=8).grid(row=i+1, column=1)
    tk.Label(order_frame, text=str(MENU[item]["stock"]),
             bg="#ecf0f1").grid(row=i+1, column=2)

# ================= RECEIPT =================
receipt_frame = tk.LabelFrame(root, text="Receipt", font=("Arial", 14, "bold"), bg="#ecf0f1")
receipt_frame.pack(side=tk.RIGHT, padx=20, pady=20)

receipt_box = tk.Text(receipt_frame, width=45, height=22)
receipt_box.pack()

# ================= FUNCTIONS =================
def generate_bill():
    receipt_box.delete("1.0", tk.END)
    subtotal = 0
    ref = f"ORD-{random.randint(1000,9999)}"

    receipt_box.insert(tk.END, "AMRUTHA RESTAURANT\n")
    receipt_box.insert(tk.END, f"Order ID: {ref}\n")
    receipt_box.insert(tk.END, "-"*35 + "\n")

    for item, var in order_vars.items():
        if var.get().isdigit():
            qty = int(var.get())
            if qty > MENU[item]["stock"]:
                messagebox.showerror("Stock Error", f"Not enough stock for {item}")
                return
            cost = qty * MENU[item]["price"]
            subtotal += cost
            MENU[item]["stock"] -= qty
            receipt_box.insert(tk.END, f"{item} x{qty} = ₹{cost}\n")

    if subtotal == 0:
        messagebox.showwarning("Empty Order", "No items selected")
        return

    tax = subtotal * 0.05
    service = subtotal * 0.02
    total = subtotal + tax + service

    receipt_box.insert(tk.END, "-"*35 + "\n")
    receipt_box.insert(tk.END, f"Subtotal: ₹{subtotal:.2f}\n")
    receipt_box.insert(tk.END, f"Tax (5%): ₹{tax:.2f}\n")
    receipt_box.insert(tk.END, f"Service: ₹{service:.2f}\n")
    receipt_box.insert(tk.END, f"TOTAL: ₹{total:.2f}\n")

    cur.execute("INSERT INTO orders VALUES (?,?,?)",
                (ref, total, datetime.date.today()))
    conn.commit()

def reset_all():
    for v in order_vars.values():
        v.set("")
    receipt_box.delete("1.0", tk.END)

def view_report():
    cur.execute("SELECT COUNT(*), SUM(total) FROM orders")
    data = cur.fetchone()
    messagebox.showinfo(
        "Daily Report",
        f"Total Orders: {data[0]}\nTotal Revenue: ₹{data[1] if data[1] else 0}"
    )

# ================= BUTTONS =================
btn_frame = tk.Frame(root, bg="#ecf0f1")
btn_frame.pack(fill=tk.X)

tk.Button(btn_frame, text="Generate Bill", bg="#27ae60", fg="white",
          font=("Arial", 12, "bold"), command=generate_bill).pack(side=tk.LEFT, padx=20)

tk.Button(btn_frame, text="Reset", bg="#f39c12", fg="white",
          font=("Arial", 12, "bold"), command=reset_all).pack(side=tk.LEFT, padx=20)

tk.Button(btn_frame, text="Daily Report", bg="#2980b9", fg="white",
          font=("Arial", 12, "bold"), command=view_report).pack(side=tk.LEFT, padx=20)

tk.Button(btn_frame, text="Exit", bg="#c0392b", fg="white",
          font=("Arial", 12, "bold"), command=root.destroy).pack(side=tk.LEFT, padx=20)

root.mainloop()

