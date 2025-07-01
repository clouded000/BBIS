import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def sign_up():
    email = email_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if password != confirm_password:
        messagebox.showerror("Password Mismatch", "Passwords do not match. Please try again.")
    else:
        messagebox.showinfo("Sign Up Info", f"Webmail: {email}\nPassword: {password}")

def forgot_password():
    messagebox.showinfo("Forgot Password", "Password recovery not implemented.")

# --- Main App ---
root = tk.Tk()
root.title("Blood Bank Inventory")
root.geometry("600x450")
root.configure(bg='white')
root.resizable(True, True)

# --- Logo + Title ---
logo_frame = tk.Frame(root, bg='white')
logo_frame.pack(pady=10, anchor='w', padx=20)

logo_image = Image.open("C:/Users/Megan Nazareth/Downloads/bbis_logo.png")  # Update path if needed
logo_image = logo_image.resize((40, 40))
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(logo_frame, image=logo_photo, bg='white')
logo_label.image = logo_photo
logo_label.pack(side='left')

text_frame = tk.Frame(logo_frame, bg='white')
text_frame.pack(side='left', padx=10)

admin_label = tk.Label(text_frame, text="Sintang Duguan", fg="maroon", font=("Arial", 10, "bold"), bg='white')
admin_label.pack(anchor='w')

title_label = tk.Label(text_frame, text="Sign Up", font=("Arial", 14), bg='white')
title_label.pack(anchor='w')

instruction_label = tk.Label(root, text="Let’s Get Started — Become an Admin", font=("Arial", 9), bg='white')
instruction_label.pack()

# --- Email ---
email_frame = tk.Frame(root, bg='white')
email_frame.pack(pady=(20, 5), padx=50, fill='x')

email_label = tk.Label(email_frame, text="Email", font=("Arial", 9), bg='white')
email_label.pack(anchor='w')

email_entry = tk.Entry(email_frame, font=("Arial", 10), width=50)
email_entry.insert(0, "Enter Admin Email")
email_entry.pack(ipady=5)

# --- Password ---
password_frame = tk.Frame(root, bg='white')
password_frame.pack(pady=(10, 5), padx=50, fill='x')

pw_top = tk.Frame(password_frame, bg='white')
pw_top.pack(fill='x')

password_label = tk.Label(pw_top, text="Password", font=("Arial", 9), bg='white')
password_label.pack(side='left')

forgot_btn = tk.Button(pw_top, text="Forgot password?", fg="maroon", font=("Arial", 8, "underline"),
                       bg='white', bd=0, cursor="hand2", command=forgot_password)
forgot_btn.pack(side='right')

password_entry = tk.Entry(password_frame, font=("Arial", 10), width=50, show="*")
password_entry.insert(0, "Enter your password")
password_entry.pack(ipady=5)

# --- Confirm Password ---
confirm_frame = tk.Frame(root, bg='white')
confirm_frame.pack(pady=(10, 5), padx=50, fill='x')

confirm_label = tk.Label(confirm_frame, text="Confirm Password", font=("Arial", 9), bg='white')
confirm_label.pack(anchor='w')

confirm_password_entry = tk.Entry(confirm_frame, font=("Arial", 10), width=50, show="*")
confirm_password_entry.insert(0, "Re-enter your password")
confirm_password_entry.pack(ipady=5)

# --- Sign Up Button ---
signup_btn = tk.Button(root, text="Sign Up", bg="#a00", fg="white", font=("Arial", 10, "bold"),
                      width=40, height=2, command=sign_up)
signup_btn.pack(pady=20)

root.mainloop()
