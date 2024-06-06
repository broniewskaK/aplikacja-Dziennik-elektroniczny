import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from auth import login
from charts import generate_chart, generate_attendance_pie_chart, generate_attendance_comparison_chart
from messages import load_teachers, send_message, load_received_messages, load_sent_messages
from data_loader import load_grades, load_attendance, load_timetable
from custom_ui import style_window, create_header, create_label, create_entry, create_button, create_tab_control, \
    create_tab, create_text, create_treeview, add_scrollbar


def style_window(window):
    window.configure(bg="#E8EAF6")
    window.geometry("800x750")  # Zwiększony wymiar okna


def create_login_ui(root, parents, show_parent_panel):
    # Stylizacja okna
    style_window(root)

    # Nagłówek
    create_header(root, "Dziennik elektroniczny")

    # Formularz logowania
    create_label(root, "Login:")
    entry_login = create_entry(root)

    create_label(root, "Hasło:")
    entry_password = create_entry(root, show="*")

    # Przycisk logowania
    create_button(root, "Zaloguj się", lambda: login(entry_login, entry_password, parents, root, show_parent_panel))

    # Przycisk Wyjście
    create_button(root, "Wyjście", root.quit, bg_color="#D32F2F")


def create_parent_panel(login, root, parents_data, students):
    parent_panel = tk.Toplevel()
    parent_panel.title("Panel Rodzica")
    style_window(parent_panel)

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
    tab_control = create_tab_control(parent_panel)

    grades_tab = create_tab(parent_panel, tab_control, "Oceny")
    attendance_tab = create_tab(parent_panel, tab_control, "Frekwencja")
    timetable_tab = create_tab(parent_panel, tab_control, "Plan Lekcji")
    messages_tab = create_tab(parent_panel, tab_control, "Wiadomości")

    # Wyświetl oceny dla każdego dziecka w formie tekstowej
    grades = load_grades()
    for child in children:
        create_label(grades_tab, f"Oceny dla {child[1]} {child[2]}")
        child_grades = [grade for grade in grades if grade[1] == child[1] and grade[2] == child[2]]

        subjects = list(set(grade[3] for grade in child_grades))
        for subject in subjects:
            subject_grades = [grade[4] for grade in child_grades if grade[3] == subject]
            create_label(grades_tab, f"{subject}: {', '.join(subject_grades)}")

    # Dodaj przycisk generowania wykresu
    create_button(grades_tab, "Wygeneruj wykres", lambda: generate_chart(login, grades, students, parents_data))

    # Wyświetl frekwencję dla każdego dziecka w formie tabeli
    attendance = load_attendance()

    def show_attendance(child_attendance):
        for widget in attendance_tab.winfo_children():
            widget.destroy()

        create_label(attendance_tab, f"Frekwencja dla {child[1]} {child[2]}")

        # Utworzenie tabeli
        columns = ["Data"]
        tree = ttk.Treeview(attendance_tab, columns=columns, show="headings")
        tree.pack(fill="both", expand=True)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        # Grupowanie obecności według daty, sortowanie od najnowszej do najstarszej
        dates = sorted(list(set(att[4] for att in child_attendance)), reverse=True)
        for date in dates:
            date_attendance = [att for att in child_attendance if att[4] == date]
            absent_subjects = [att for att in date_attendance if att[5] == "nieobecny"]
            if absent_subjects:
                tree.insert("", tk.END, values=(date,), tags=("date",))
                tree.insert("", tk.END, values=("Nieobecny",), tags=("absent", date))
            else:
                tree.insert("", tk.END, values=(date,), tags=("date",))
                tree.insert("", tk.END, values=("Obecny",), tags=("present", date))

        tree.tag_configure("date", font=("Helvetica", 12, "bold"))
        tree.tag_configure("absent", font=("Helvetica", 12))
        tree.tag_configure("present", font=("Helvetica", 12))

        # Event kliknięcia na "Nieobecny" lub "Obecny"
        def on_click(event):
            item = tree.selection()[0]
            tags = tree.item(item, "tags")
            if len(tags) == 2:
                date = tags[1]
                show_details(date, child_attendance)

        tree.bind("<Double-1>", on_click)

    def show_details(date, child_attendance):
        details_window = tk.Toplevel(attendance_tab)
        details_window.title(f"Frekwencja - {date}")
        style_window(details_window)

        details = [att for att in child_attendance if att[4] == date]
        for att in details:
            create_label(details_window, f"{att[3]}: {att[5]}")

    for child in children:
        child_attendance = [att for att in attendance if att[1] == child[1] and att[2] == child[2]]
        show_attendance(child_attendance)

    # Wyświetl plan lekcji dla klasy dziecka (zakładamy, że wszystkie dzieci są w tej samej klasie)
    class_name = children[0][0]
    create_label(timetable_tab, f"Plan Lekcji dla klasy {class_name}")

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
        tk.Label(timetable_frame, text=day, font=("Helvetica", 12, "bold"), borderwidth=1, relief="solid").grid(row=0,
                                                                                                                column=col_num,
                                                                                                                sticky="nsew")

    # Wypełnianie tabeli planu lekcji
    for row_num, hour in enumerate(hours, start=1):
        tk.Label(timetable_frame, text=hour, font=("Helvetica", 12), borderwidth=1, relief="solid").grid(row=row_num,
                                                                                                         column=0,
                                                                                                         sticky="nsew")
        for col_num, day in enumerate(days, start=1):
            subject = next((row[3] for row in class_timetable if row[1] == day and row[2] == hour), "")
            teacher = next((row[4] for row in class_timetable if row[1] == day and row[2] == hour), "")
            text = f"{subject}\n{teacher}" if subject else ""
            tk.Label(timetable_frame, text=text, font=("Helvetica", 12), borderwidth=1, relief="solid").grid(
                row=row_num, column=col_num, sticky="nsew")

    # Zakładka Wiadomości
    create_label(messages_tab, "Wyślij wiadomość do nauczyciela")

    teachers = load_teachers()
    teacher_names = [f"{teacher[1]} {teacher[2]}" for teacher in teachers]

    create_label(messages_tab, "Nauczyciel:")
    teacher_combobox = ttk.Combobox(messages_tab, values=teacher_names, font=("Helvetica", 12))
    teacher_combobox.pack(pady=5)

    create_label(messages_tab, "Treść wiadomości:")
    message_text = create_text(messages_tab, height=3, width=40)

    create_button(messages_tab, "Wyślij", lambda: send_message_to_teacher())

    # Zakładka Wiadomości (Odebrane i Wysłane)
    create_label(messages_tab, "Odebrane wiadomości")
    received_tree = create_treeview(messages_tab, columns=("Od", "Treść"), height=3)

    received_messages = load_received_messages(login)
    for msg in received_messages:
        received_tree.insert("", tk.END, values=(msg[0], msg[2]))

    create_label(messages_tab, "Wysłane wiadomości")
    sent_tree = create_treeview(messages_tab, columns=("Do", "Treść"), height=5)

    sent_messages = load_sent_messages(login)
    for msg in sent_messages:
        sent_tree.insert("", tk.END, values=(msg[1], msg[2]))

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

    def on_closing():
        root.deiconify()  # Przywróć główne okno
        parent_panel.destroy()

    parent_panel.protocol("WM_DELETE_WINDOW", on_closing)

    # Przycisk Wyjście w panelu rodzica
    create_button(parent_panel, "Wyjście", root.quit, bg_color="#D32F2F").pack(side=tk.BOTTOM, padx=10, pady=10)
