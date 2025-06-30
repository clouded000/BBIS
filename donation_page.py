import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from datetime import datetime, timedelta
from db import get_connection

class DonationPage(tk.Frame):
    def __init__(self, parent, controller, admin_id):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.admin_id = admin_id

        def add_donation():
            fn = first_name.get().strip()
            ln = last_name.get().strip()
            bd = birthday.get_date().strftime("%Y-%m-%d")
            gen = gender.get()
            cn = contact.get().strip()
            em = email.get().strip()
            bt = blood_type.get()
            vol = volume.get().strip()
            dt = date_field.get()
            comp = component.get()

            if not all([fn, ln, bd, gen, cn, bt, vol, comp]):
                return messagebox.showerror("Error", "Please fill out every field.")
            if not vol.isdigit() or int(vol) <= 0:
                return messagebox.showerror("Error", "Volume must be a positive number.")

            try:
                conn = get_connection()
                c = conn.cursor()

                # Check if donor exists
                c.execute("""
                    SELECT donor_id FROM Donor
                    WHERE first_name=? AND last_name=? AND date_of_birth=?
                      AND gender=? AND contact_number=? AND IFNULL(email_address,'')=IFNULL(?, '')
                      AND blood_type=?
                """, (fn, ln, bd, gen, cn, em, bt))
                dup = c.fetchone()

                if dup:
                    donor_id = dup[0]
                    return messagebox.showerror("Duplicate", f"Donor already exists with ID {donor_id}")
                else:
                    c.execute("""
                        INSERT INTO Donor (first_name, last_name, date_of_birth,
                                           gender, contact_number, email_address, blood_type)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (fn, ln, bd, gen, cn, em, bt))
                    donor_id = c.lastrowid

                # Component lookup
                c.execute("SELECT component_id, shelf_life_days FROM Blood_Component WHERE component_type=?", (comp,))
                row = c.fetchone()
                if not row:
                    conn.close()
                    return messagebox.showerror("Error", f"Component '{comp}' not found.")
                comp_id, shelf = row

                # Insert Donation
                now = datetime.now()
                c.execute("""
                    INSERT INTO Donation (donor_id, admin_id, donation_date, donation_time, volume_ml, notes)
                    VALUES (?, ?, ?, ?, ?, 'Walk-in donor')
                """, (donor_id, self.admin_id, dt, now.strftime("%H:%M"), vol))
                donation_id = c.lastrowid

                # Insert into Blood Inventory
                expiration = (now + timedelta(days=shelf)).strftime("%Y-%m-%d")
                c.execute("""
                    INSERT INTO Blood_Inventory (donation_id, component_id, quantity_units, expiration_date, status)
                    VALUES (?, ?, 1, ?, 'Available')
                """, (donation_id, comp_id, expiration))

                conn.commit()
                conn.close()

                self.load_donations()
                messagebox.showinfo("Success", "Donation recorded successfully.")

                for var in (first_name, last_name, contact, email, volume):
                    var.delete(0, 'end')
                birthday.set_date(datetime.today())
                gender.set('')
                blood_type.set('')
                component.set('')

            except Exception as e:
                messagebox.showerror("Database Error", str(e))

        # — NAVBAR —
        nav = tk.Frame(self, bg='white'); nav.pack(fill='x')
        logo_img = ImageTk.PhotoImage(Image.open("LogoBBIS.png").resize((30, 30)))
        tk.Label(nav, image=logo_img, bg='white').pack(side='left', padx=10)
        tk.Label(nav, text="Sintang Duguan", fg="maroon", font=("Arial", 12, "bold"), bg='white').pack(side='left')
        for txt, page in [("Home", "HomePage"), ("Donations", "DonationPage"), ("Blood Inventory", "InventoryPage")]:
            lbl = tk.Label(nav, text=txt, font=("Arial", 10), bg='white', cursor="hand2")
            lbl.pack(side='left', padx=20)
            lbl.bind("<Button-1>", lambda e, p=page: controller.show_frame(p))
        tk.Frame(self, bg='lightgray', height=1).pack(fill='x')

        # — FORM —
        mf = tk.Frame(self, bg='white'); mf.pack(fill='both', expand=True, pady=10, padx=10)
        lf = tk.Frame(mf, bg='white'); lf.pack(side='left', padx=10)
        tk.Label(lf, text="+ ADD DONATION", fg='red', font=("Arial", 10, "bold"), bg='white').pack(anchor='w')
        ff = tk.Frame(lf, bg='red', padx=10, pady=10); ff.pack(pady=5)

        def make_field(label, parent=ff):
            tk.Label(parent, text=label, bg='red', fg='white').pack(anchor='w')
            e = tk.Entry(parent, width=30); e.pack(pady=2)
            return e

        first_name = make_field("First Name:")
        last_name  = make_field("Last Name:")
        contact    = make_field("Contact Number:")
        email      = make_field("Email:")
        volume     = make_field("Volume (ml):")

        tk.Label(ff, text="Birthday:", bg='red', fg='white').pack(anchor='w')
        birthday = DateEntry(ff, width=28, date_pattern='yyyy-mm-dd', maxdate=datetime.today())
        birthday.pack(pady=2)

        tk.Label(ff, text="Sex:", bg='red', fg='white').pack(anchor='w')
        gender = ttk.Combobox(ff, values=["Male", "Female", "Other"], width=28); gender.pack(pady=2)

        tk.Label(ff, text="Date:", bg='red', fg='white').pack(anchor='w')
        date_field = tk.Entry(ff, width=30)
        date_field.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_field.configure(state='readonly'); date_field.pack(pady=2)

        tk.Label(ff, text="Blood Type:", bg='red', fg='white').pack(anchor='w')
        blood_type = ttk.Combobox(ff, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], width=28)
        blood_type.pack(pady=2)

        tk.Label(ff, text="Component:", bg='red', fg='white').pack(anchor='w')
        component = ttk.Combobox(ff, values=[
            "Whole Blood", "Plasma", "Platelets", "Red Blood Cells",
            "White Blood Cells", "Cryoprecipitate"
        ], width=28)
        component.pack(pady=2)

        tk.Button(ff, text="ADD", bg='white', fg='red',
                  font=("Arial", 10, "bold"), width=20, command=add_donation).pack(pady=10)

        # — TABLE —
        tf = tk.Frame(mf, bg='white'); tf.pack(side='right', fill='both', expand=True, padx=10)
        cols = ('Date', 'Component', 'Volume', 'Status')
        self.donation_table = ttk.Treeview(tf, columns=cols, show='headings', height=15)
        for c in cols:
            self.donation_table.heading(c, text=c)
            self.donation_table.column(c, anchor='center', width=120)
        self.donation_table.pack(fill='both', expand=True)
        tk.Button(tf, text="🔄 Refresh", command=self.load_donations, bg='red', fg='white').pack(pady=5)

        self.load_donations()
        self._logo = logo_img  # Image reference

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
            self.donation_table.delete(*self.donation_table.get_children())
            for r in rows:
                self.donation_table.insert('', 'end', values=r)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
