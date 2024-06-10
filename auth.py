import tkinter as tk
from tkinter import messagebox # import modułu odpowiedzialnego za wyświetlanie komunikatów

def login(entry_login, entry_password, parents, root, show_parent_panel): # funkcja odpowiedzialna za sprawdzenie poprawnosci danych logowania
    login = entry_login.get()
    password = entry_password.get()
    if login in parents and parents[login] == password:
        messagebox.showinfo("Sukces", "Zalogowano !")
        root.iconify()  # minimalizacja głównego okno
        show_parent_panel(login)  # funkcja wywołana po poprawnym zalogowaniu ktora tworzy panel rodzica
    else:
        messagebox.showerror("Błąd", "Nieprawidłowy login lub hasło")
