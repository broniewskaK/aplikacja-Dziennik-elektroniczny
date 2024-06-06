import tkinter as tk
from tkinter import messagebox

def login(entry_login, entry_password, parents, root, show_parent_panel):
    login = entry_login.get()
    password = entry_password.get()
    if login in parents and parents[login] == password:
        messagebox.showinfo("Sukces", "Zalogowano pomyślnie!")
        root.iconify()  # Minimalizuj główne okno
        show_parent_panel(login)  # Przekaż login do panelu rodzica
    else:
        messagebox.showerror("Błąd", "Nieprawidłowy login lub hasło")
