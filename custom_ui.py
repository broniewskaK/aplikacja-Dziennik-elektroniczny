import tkinter as tk
from tkinter import ttk

def style_window(window):
    window.configure(bg="#E8EAF6")
    window.geometry("800x600")  # Ustalony wymiar okna

def create_header(parent, text):
    header = tk.Label(parent, text=text, font=("Helvetica", 24, "bold"), bg="#283593", fg="white")
    header.pack(pady=20, padx=20, fill="x")

def create_label(parent, text):
    label = tk.Label(parent, text=text, font=("Helvetica", 14), bg="#E8EAF6")
    label.pack(pady=5, padx=10)
    return label

def create_entry(parent, show=None):
    entry = tk.Entry(parent, font=("Helvetica", 14), show=show)
    entry.pack(pady=5, padx=10)
    return entry

def create_button(parent, text, command, bg_color="#3F51B5", fg_color="white"):
    button = tk.Button(parent, text=text, font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color, command=command)
    button.pack(pady=10, padx=20)
    return button

def create_tab_control(parent):
    tab_control = ttk.Notebook(parent)
    tab_control.pack(expand=1, fill="both")
    return tab_control

def create_tab(parent, tab_control, text):
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text=text)
    return tab

def create_text(parent, height, width):
    text = tk.Text(parent, height=height, width=width, font=("Helvetica", 12))
    text.pack(pady=5)
    return text

def create_treeview(parent, columns, height=5):
    treeview = ttk.Treeview(parent, columns=columns, show="headings", height=height)
    for col in columns:
        treeview.heading(col, text=col)
    treeview.pack(fill="both", expand=True, pady=5)
    return treeview

def add_scrollbar(frame, canvas):
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    return scrollbar
