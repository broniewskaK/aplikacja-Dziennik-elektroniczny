import tkinter as tk
from data_loader import load_parents, load_parents_data, load_students # importowanie funkcji z data_loader
from ui import create_login_ui, create_parent_panel # importowanie  funkcji z ui

# inicjalizacja danych
parents = load_parents() # ładowanie loginow i haseł z csv i przypisanie do zmiennej parents
parents_data = load_parents_data() # ładowanie danych rodziców: id, imię, nazwisko, login, hasło z csv i przypisanie do zmiennej parents_data
students = load_students() # ładowanie danych uczniow: klasa, imię, nazwisko, id rodzica z csv i przypisanie do zmiennej students

# inicjalizacja głównego okna
root = tk.Tk() # tworzenie głównego okna aplikacji
root.title("Dziennik elektroniczny") #tytuł
root.geometry("800x750")  # ustalony wymiar okna

# tworzenie interfejsu logowania
create_login_ui(root, parents, lambda login: create_parent_panel(login, root, parents_data, students)) # funkcji, która tworzy interfejs logowanie
# funkcja lambda po zalogowaniu tworzy panel rodzica, funckja create_parent_panel przyjmuje login rodzica, dane rodziców i uczniów

root.mainloop() # uruchomienie głównej pętli aplikacji tkinter, która obsluguje GUI, uruchomienie głównej pętli aplikacji Tkinter
