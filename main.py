import tkinter as tk
from data_loader import load_parents, load_parents_data, load_students
from ui import create_login_ui, create_parent_panel

# Inicjalizacja danych
parents = load_parents()
parents_data = load_parents_data()
students = load_students()

# Inicjalizacja głównego okna
root = tk.Tk()
root.title("Dziennik elektroniczny")

# Tworzenie interfejsu logowania
create_login_ui(root, parents, lambda login: create_parent_panel(login, root, parents_data, students))

root.mainloop()
