import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from messages import load_teachers, send_message, load_received_messages, load_sent_messages
from data_loader import load_grades, load_attendance, load_timetable
from charts import generate_chart  # Import funkcji generującej wykresy


def create_login_ui(root, parents, show_parent_panel):
    # Nagłówek
    header = tk.Label(root, text="Dziennik elektroniczny", font=("Helvetica", 24))
    header.grid(row=0, column=0, columnspan=2, pady=20)

    # Formularz logowania
    tk.Label(root, text="Login").grid(row=1, column=0, padx=10, pady=10)
    tk.Label(root, text="Hasło").grid(row=2, column=0, padx=10, pady=10)

    entry_login = tk.Entry(root)
    entry_password = tk.Entry(root, show="*")

    entry_login.grid(row=1, column=1, padx=10, pady=10)
    entry_password.grid(row=2, column=1, padx=10, pady=10)

    from auth import login
    tk.Button(root, text="Zaloguj się",
              command=lambda: login(entry_login, entry_password, parents, root, show_parent_panel)).grid(row=3,
                                                                                                         column=1,
                                                                                                         pady=20)

    # Przycisk Wyjście
    tk.Button(root, text="Wyjście", command=root.quit).grid(row=4, column=1, pady=10)


def create_parent_panel(login, root, parents_data, students):
    parent_panel = tk.Toplevel()
    parent_panel.title("Panel Rodzica")

    # Pobierz id rodzica na podstawie loginu
    parent_id = next((row[0] for row in parents_data if row[3] == login), None)

    # Znajdź dzieci tego rodzica
    children = [student for student in students if student[3] == parent_id]

    if not children:
        tk.messagebox.showerror("Błąd", "Nie znaleziono dzieci dla tego rodzica.")
        root.deiconify()  # Przywróć główne okno
        parent_panel.destroy()
        return

    # Dodaj zakładki
    tab_control = ttk.Notebook(parent_panel)

    grades_tab = ttk.Frame(tab_control)
    attendance_tab = ttk.Frame(tab_control)
    timetable_tab = ttk.Frame(tab_control)
    messages_tab = ttk.Frame(tab_control)

    tab_control.add(grades_tab, text="Oceny")
    tab_control.add(attendance_tab, text="Frekwencja")
    tab_control.add(timetable_tab, text="Plan Lekcji")
    tab_control.add(messages_tab, text="Wiadomości")

    tab_control.pack(expand=1, fill="both")

    # Wyświetl oceny dla każdego dziecka
    ttk.Label(grades_tab, text="Oceny").pack()
    grades_tree = ttk.Treeview(grades_tab, columns=("klasa", "imię", "nazwisko", "przedmiot", "ocena"), show="headings")
    for col in grades_tree["columns"]:
        grades_tree.heading(col, text=col)
    grades = load_grades()
    for child in children:
        child_grades = [grade for grade in grades if grade[1] == child[1] and grade[2] == child[2]]
        for row in child_grades:
            grades_tree.insert("", tk.END, values=row)
    grades_tree.pack(fill="both", expand=True)

    # Dodaj przycisk generowania wykresu
    generate_chart_button = tk.Button(grades_tab, text="Wygeneruj wykres",
                                      command=lambda: generate_chart(login, grades, students, parents_data))
    generate_chart_button.pack(pady=10)

    # Wyświetl frekwencję dla każdego dziecka
    ttk.Label(attendance_tab, text="Frekwencja").pack()
    attendance_tree = ttk.Treeview(attendance_tab,
                                   columns=("klasa", "imię", "nazwisko", "przedmiot", "data", "obecność"),
                                   show="headings")
    for col in attendance_tree["columns"]:
        attendance_tree.heading(col, text=col)
    attendance = load_attendance()
    for child in children:
        child_attendance = [att for att in attendance if att[1] == child[1] and att[2] == child[2]]
        for row in child_attendance:
            attendance_tree.insert("", tk.END, values=row)
    attendance_tree.pack(fill="both", expand=True)

    # Wyświetl plan lekcji dla klasy dziecka (zakładamy, że wszystkie dzieci są w tej samej klasie)
    class_name = children[0][0]
    ttk.Label(timetable_tab, text=f"Plan Lekcji dla klasy {class_name}").pack()

    # Przygotowanie tabeli planu lekcji
    timetable_frame = ttk.Frame(timetable_tab)
    timetable_frame.pack(fill="both", expand=True)

    timetable = load_timetable()
    class_timetable = [row for row in timetable if row[0] == class_name]

    # Przygotowanie kolumn i wierszy
    days = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"]
    hours = sorted(set(row[2] for row in class_timetable), key=lambda x: int(x.split(':')[0]))  # Sortowanie godzin

    # Utworzenie nagłówków kolumn
    for col_num, day in enumerate(["Godzina"] + days):
        ttk.Label(timetable_frame, text=day, borderwidth=1, relief="solid").grid(row=0, column=col_num, sticky="nsew")

    # Wypełnianie tabeli planu lekcji
    for row_num, hour in enumerate(hours, start=1):
        ttk.Label(timetable_frame, text=hour, borderwidth=1, relief="solid").grid(row=row_num, column=0, sticky="nsew")
        for col_num, day in enumerate(days, start=1):
            subject = next((row[3] for row in class_timetable if row[1] == day and row[2] == hour), "")
            teacher = next((row[4] for row in class_timetable if row[1] == day and row[2] == hour), "")
            text = f"{subject}\n{teacher}" if subject else ""
            ttk.Label(timetable_frame, text=text, borderwidth=1, relief="solid").grid(row=row_num, column=col_num,
                                                                                      sticky="nsew")

    # Zakładka Wiadomości
    ttk.Label(messages_tab, text="Wyślij wiadomość do nauczyciela").pack()

    teachers = load_teachers()
    teacher_names = [f"{teacher[1]} {teacher[2]}" for teacher in teachers]

    ttk.Label(messages_tab, text="Nauczyciel:").pack()
    teacher_combobox = ttk.Combobox(messages_tab, values=teacher_names)
    teacher_combobox.pack()

    ttk.Label(messages_tab, text="Treść wiadomości:").pack()
    message_text = tk.Text(messages_tab, height=5, width=40)
    message_text.pack()

    # Zakładka Wiadomości (Odebrane i Wysłane)
    ttk.Label(messages_tab, text="Odebrane wiadomości").pack()
    received_tree = ttk.Treeview(messages_tab, columns=("Od", "Treść"), show="headings")
    received_tree.heading("Od", text="Od")
    received_tree.heading("Treść", text="Treść")

    received_messages = load_received_messages(login)
    for msg in received_messages:
        received_tree.insert("", tk.END, values=(msg[0], msg[2]))
    received_tree.pack(fill="both", expand=True)

    ttk.Label(messages_tab, text="Wysłane wiadomości").pack()
    sent_tree = ttk.Treeview(messages_tab, columns=("Do", "Treść"), show="headings")
    sent_tree.heading("Do", text="Do")
    sent_tree.heading("Treść", text="Treść")

    sent_messages = load_sent_messages(login)
    for msg in sent_messages:
        sent_tree.insert("", tk.END, values=(msg[1], msg[2]))
    sent_tree.pack(fill="both", expand=True)

    def send_message_to_teacher():
        selected_teacher = teacher_combobox.get()
        message_content = message_text.get("1.0", tk.END).strip()
        if selected_teacher and message_content:
            send_message(login, selected_teacher, message_content)
            message_text.delete("1.0", tk.END)
            parent_panel.lift()  # Przywróć panel rodzica na pierwszy plan
            tk.messagebox.showinfo("Sukces", "Wiadomość została wysłana pomyślnie!")
            # Odświeżenie listy wysłanych wiadomości
            sent_tree.delete(*sent_tree.get_children())
            sent_messages = load_sent_messages(login)
            for msg in sent_messages:
                sent_tree.insert("", tk.END, values=(msg[1], msg[2]))
        else:
            tk.messagebox.showerror("Błąd", "Musisz wybrać nauczyciela i napisać wiadomość.")

    send_button = ttk.Button(messages_tab, text="Wyślij", command=send_message_to_teacher)
    send_button.pack()

    def on_closing():
        root.deiconify()  # Przywróć główne okno
        parent_panel.destroy()

    parent_panel.protocol("WM_DELETE_WINDOW", on_closing)

    # Przycisk Wyjście w panelu rodzica
    exit_button = ttk.Button(parent_panel, text="Wyjście", command=root.quit)
    exit_button.pack(side=tk.RIGHT, padx=10, pady=10)
