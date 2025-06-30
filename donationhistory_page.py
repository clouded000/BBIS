import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from db import get_connection

class DonationHistoryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')
        self.controller = controller

        # — NAVBAR —
        nav = tk.Frame(self, bg='white'); nav.pack(fill='x')
        logo_img = ImageTk.PhotoImage(Image.open("bbis_logo.png").resize((30, 30)))
        tk.Label(nav, image=logo_img, bg='white').pack(side='left', padx=10)
        tk.Label(nav, text="Sintang Duguan", fg="maroon", font=("Arial", 12, "bold"), bg='white').pack(side='left')
        for txt, page in [("Home", "HomePage"), ("Donations", "DonationPage"), ("Blood Inventory", "InventoryPage"), ("Donation History", "DonationHistoryPage")]:
            lbl = tk.Label(nav, text=txt, font=("Arial", 10), bg='white', cursor="hand2")
            lbl.pack(side='left', padx=20)
            lbl.bind("<Button-1>", lambda e, p=page: controller.show_frame(p))
        tk.Frame(self, bg='lightgray', height=1).pack(fill='x')

        # — TABLE FRAME —
        tf = tk.Frame(self, bg='white'); tf.pack(fill='both', expand=True, padx=20, pady=20)
        cols = ('Date', 'Component', 'Volume', 'Status')
        self.history_table = ttk.Treeview(tf, columns=cols, show='headings', height=20)
        for c in cols:
            self.history_table.heading(c, text=c)
            self.history_table.column(c, anchor='center', width=120)
        self.history_table.pack(fill='both', expand=True)
        tk.Button(tf, text="🔄 Refresh", command=self.load_donations, bg='red', fg='white').pack(pady=10)

        self._logo = logo_img  # prevent garbage collection
        self.load_donations()

    def load_donations(self):
        try:
            conn = get_connection()
            c = conn.cursor()
            c.execute("""
              SELECT d.donation_date,
                     COALESCE(bc.component_type, 'N/A'),
                     d.volume_ml,
                     COALESCE(bi.status, 'Pending')
              FROM Donation d
              LEFT JOIN Blood_Inventory bi ON d.donation_id = bi.donation_id
              LEFT JOIN Blood_Component bc ON bi.component_id = bc.component_id
            """)
            rows = c.fetchall()
            conn.close()
            self.history_table.delete(*self.history_table.get_children())
            for r in rows:
                self.history_table.insert('', 'end', values=r)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
