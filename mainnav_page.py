import tkinter as tk
from home_page import HomePage
from donation_page import DonationPage
from bloodinventory_page import InventoryPage

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blood Bank System")
        self.geometry("1000x600")
        self.configure(bg='white')

        self.frames = {}

        container = tk.Frame(self)
        container.pack(fill='both', expand=True)

        for F in (HomePage, DonationPage, InventoryPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
