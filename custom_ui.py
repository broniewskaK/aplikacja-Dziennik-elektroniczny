import tkinter as tk
from tkinter import ttk
#ustalenie wygladu aplikacji
def style_window(window): # funkcja ustawia wymiar i kolor okna
    window.configure(bg="#E8EAF6")
    window.geometry("800x750")  #  wymiar okna

def create_header(parent, text): # funkcja tworzy nagłówek i odpowienio go stylizuje w oknie logowania
    header = tk.Label(parent, text=text, font=("Helvetica", 24, "bold"), bg="#283593", fg="white")
    header.pack(pady=20, padx=20, fill="x")

def create_label(parent, text): # funkcja tworzy etykiete i ją stylizuje
    label = tk.Label(parent, text=text, font=("Helvetica", 14), bg="#E8EAF6")
    label.pack(pady=5, padx=10)
    return label

def create_entry(parent, show=None): # funkcja tworzy pole tekstowe do hasła i je stylizuje
    entry = tk.Entry(parent, font=("Helvetica", 14), show=show)
    entry.pack(pady=5, padx=10)
    return entry

def create_button(parent, text, command, bg_color="#3F51B5", fg_color="white"): # funkcja tworzy przyciski zaloguj się, wyjście wyślij  i je stylizuje
    button = tk.Button(parent, text=text, font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color, command=command)
    button.pack(pady=10, padx=20)
    return button

def create_tab_control(parent): # funkcja tworzy kontrolkę zakladek Notebook w panelu rodzica w funkcji create_parent_panel, umożliwia przełączenie się miedzy ocenami, frekwencja, planem lekcji i wiadomościami
    tab_control = ttk.Notebook(parent)
    tab_control.pack(expand=1, fill="both")
    return tab_control

def create_tab(parent, tab_control, text): # funkcja tworzy nową zakladke Frame w danej kontrolce zakladek, tworzy zakładki oceny, frekwencja, plan lekcji, wiadomosci
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text=text)
    return tab

def create_text(parent, height, width): # funkcja tworzy pole tekstowe i je stylizuje, użyta do wpisywania wiadomosci w zakladce wiadomosci
    text = tk.Text(parent, height=height, width=width, font=("Helvetica", 12))
    text.pack(pady=5)
    return text

def create_treeview(parent, columns, height=5): # funkcja tworzy drzewo z kolumnami i wysokościa, użyta do tworzenia widuku drzewa doa Odebranych i Wysłanych wiadomości
    treeview = ttk.Treeview(parent, columns=columns, show="headings", height=height)
    for col in columns:
        treeview.heading(col, text=col)
    treeview.pack(fill="both", expand=True, pady=5)
    return treeview


