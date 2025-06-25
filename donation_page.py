import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime

class DonationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')

        def add_donation():
            donor_id = donor_id_entry.get()
            date = date_entry.get()
            blood_type = blood_type_combobox.get()
            component = component_combobox.get()
            volume = volume_entry.get()
            donation_table.insert('', 'end', values=(donor_id, date, component, volume, "Pending"))

        # Navbar
        nav_bar = tk.Frame(self, bg='white')
        nav_bar.pack(fill='x')

        logo_img = Image.open("C:/Users/Megan Nazareth/Downloads/bbis_logo.png").resize((30, 30))
        logo_photo = ImageTk.PhotoImage(logo_img)

        logo_label = tk.Label(nav_bar, image=logo_photo, bg='white')
        logo_label.image = logo_photo
        logo_label.pack(side='left', padx=(15, 5), pady=10)

        tk.Label(nav_bar, text="Sintang Duguan", fg="maroon", font=("Arial", 12, "bold"), bg='white').pack(side='left')

        tk.Label(nav_bar, text="Home", font=("Arial", 10), bg='white', cursor="hand2").pack(side='left', padx=25)
        tk.Label(nav_bar, text="Donations", font=("Arial", 10, "underline"), fg='red', bg='white').pack(side='left')
        tk.Label(nav_bar, text="Blood Inventory", font=("Arial", 10), bg='white', cursor="hand2").pack(side='left', padx=25)

        nav_bar.winfo_children()[2].bind("<Button-1>", lambda e: controller.show_frame("HomePage"))
        nav_bar.winfo_children()[4].bind("<Button-1>", lambda e: controller.show_frame("InventoryPage"))

        tk.Label(nav_bar, text="👤", font=("Arial", 12), bg='white').pack(side='right', padx=20)
        tk.Frame(self, bg='lightgray', height=1).pack(fill='x')

        # Content
        main_frame = tk.Frame(self, bg='white')
        main_frame.pack(fill='both', expand=True, pady=10, padx=10)

        input_frame = tk.Frame(main_frame, bg='white')
        input_frame.pack(side='left', padx=10)

        tk.Label(input_frame, text="+ ADD DONATION", fg='red', font=("Arial", 10, "bold"), bg='white').pack(anchor='w', pady=5)

        form_frame = tk.Frame(input_frame, bg='red', padx=10, pady=10)
        form_frame.pack()

        tk.Label(form_frame, text="Donor ID:", bg='red', fg='white', font=("Arial", 9)).pack(anchor='w')
        donor_id_entry = tk.Entry(form_frame, width=30)
        donor_id_entry.pack(pady=2)

        current_date = datetime.now().strftime("%m/%d/%Y")
        tk.Label(form_frame, text="Date:", bg='red', fg='white', font=("Arial", 9)).pack(anchor='w')
        date_entry = tk.Entry(form_frame, width=30)
        date_entry.insert(0, current_date)
        date_entry.configure(state='readonly')
        date_entry.pack(pady=2)

        tk.Label(form_frame, text="Blood Type:", bg='red', fg='white', font=("Arial", 9)).pack(anchor='w')
        blood_type_combobox = ttk.Combobox(form_frame, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], width=27)
        blood_type_combobox.pack(pady=2)

        tk.Label(form_frame, text="Component:", bg='red', fg='white', font=("Arial", 9)).pack(anchor='w')
        component_combobox = ttk.Combobox(form_frame, values=["Whole Blood", "Plasma", "Platelets", "RBC", "WBC", "Cryo"], width=27)
        component_combobox.pack(pady=2)

        tk.Label(form_frame, text="Volume:", bg='red', fg='white', font=("Arial", 9)).pack(anchor='w')
        volume_entry = tk.Entry(form_frame, width=30)
        volume_entry.pack(pady=2)

        tk.Button(form_frame, text="ADD", bg='white', fg='red', font=("Arial", 10, "bold"), width=20, command=add_donation).pack(pady=10)

        # Table section
        table_frame = tk.Frame(main_frame, bg='white')
        table_frame.pack(side='right', fill='both', expand=True, padx=10)

        columns = ('Donor ID', 'Date', 'Component', 'Volume', 'Status')
        donation_table = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white", bordercolor='black', borderwidth=1)
        style.map('Treeview', background=[('selected', 'lightgray')])
        style.configure("Treeview.Heading", font=("Arial", 9, "bold"), background='red', foreground='white', relief="ridge")

        for col in columns:
            donation_table.heading(col, text=col)
            donation_table.column(col, anchor='center', width=140, stretch=False)

        donation_table.pack(fill='both', expand=True)
