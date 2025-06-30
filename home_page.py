import tkinter as tk
from PIL import Image, ImageTk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')

        # --- Navbar ---
        nav_bar = tk.Frame(self, bg='white')
        nav_bar.pack(fill='x')

        logo_img = Image.open("C:/Users/Lenovo Thinkpad T460/PycharmProjects/VIVIYS/LogoBBIS.png").resize((30, 30))
        logo_photo = ImageTk.PhotoImage(logo_img)

        logo_label = tk.Label(nav_bar, image=logo_photo, bg='white')
        logo_label.image = logo_photo
        logo_label.pack(side='left', padx=(15, 5), pady=10)

        tk.Label(nav_bar, text="Sintang Duguan", fg="maroon", font=("Arial", 12, "bold"), bg='white').pack(side='left')

        # Navigation
        tk.Label(nav_bar, text="Home", font=("Arial", 10, "underline"), fg='red', bg='white').pack(side='left', padx=25)
        tk.Label(nav_bar, text="Donations", font=("Arial", 10), bg='white', cursor="hand2").pack(side='left', padx=5)
        tk.Label(nav_bar, text="Blood Inventory", font=("Arial", 10), bg='white', cursor="hand2").pack(side='left', padx=25)

        nav_bar.winfo_children()[3].bind("<Button-1>", lambda e: controller.show_frame("DonationPage"))
        nav_bar.winfo_children()[4].bind("<Button-1>", lambda e: controller.show_frame("InventoryPage"))

        tk.Label(nav_bar, text="👤", font=("Arial", 12), bg='white').pack(side='right', padx=20)
        tk.Frame(self, bg='lightgray', height=1).pack(fill='x')

        # --- Dashboard Content ---
        content = tk.Frame(self, bg='white')
        content.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(content, text="Blood Bank Admin Dashboard", font=("Arial", 18, "bold"), bg='white', fg='red').pack(anchor='w')
        tk.Label(content, text="Overview of current blood trends and inventory status.", font=("Arial", 11), bg='white').pack(anchor='w', pady=(0, 20))

        card_frame = tk.Frame(content, bg='white')
        card_frame.pack(fill='x', pady=(0, 10))

        def create_card(title, content_text, icon="🩸"):
            card = tk.Frame(card_frame, bg='#ffe5e5', padx=15, pady=10, relief='ridge', bd=1)
            card.pack(side='left', padx=10, fill='both', expand=True)
            tk.Label(card, text=f"{icon} {title}", font=("Arial", 11, "bold"), bg='#ffe5e5', fg='red').pack(anchor='w')
            tk.Label(card, text=content_text, font=("Arial", 10), bg='#ffe5e5').pack(anchor='w', pady=(5, 0))

        create_card("Most Available Blood", "O+ (120 units)")
        create_card("Least Available Blood", "AB- (5 units)")
        create_card("Recent Donations", "15 donations this week")
        create_card("Expiring Soon", "12 units in next 3 days")

        graph_frame = tk.Frame(content, bg='white')
        graph_frame.pack(fill='both', expand=True, pady=10)
        tk.Label(graph_frame, text="📊 Blood Inventory Trends", font=("Arial", 12, "bold"), bg='white', fg='red').pack(anchor='w')
        graph_placeholder = tk.Frame(graph_frame, height=200, bg='#f5f5f5', bd=1, relief='sunken')
        graph_placeholder.pack(fill='x')
        tk.Label(graph_placeholder, text="(Graph Placeholder)", font=("Arial", 10, "italic"), bg='#f5f5f5').place(relx=0.5, rely=0.5, anchor='center')
