import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt

def generate_chart(login, grades, students, parents_data): # funckja generuje wykres porównawczy średnioch ocen dziecka i jego klasy dla przedmiotu
    # pobieranie id rodzica na podstawie loginu
    parent_id = next((row[0] for row in parents_data if row[3] == login), None)
    # znajdowanie dziecka uzytkownika
    children = [student for student in students if student[3] == parent_id]

    if not children:
        messagebox.showerror("Błąd", "Nie znaleziono dzieci dla tego rodzica.")
        return

    child = children[0]  # założenie, że rodzic ma tylko jedno dziecko
    class_name = child[0]
    child_name = f"{child[1]} {child[2]}"

    # filtrowanie ocen dziecka i  uczniów w tej samej klasie
    class_grades = [grade for grade in grades if grade[0] == class_name]
    child_grades = [grade for grade in class_grades if grade[1] == child[1] and grade[2] == child[2]]

    # tworzenie listy przedmiotow
    subjects = list(set(grade[3] for grade in class_grades))

    # okno do wyboru przedmiotu
    def on_select():
        subject = subject_combobox.get()
        if not subject:
            messagebox.showerror("Błąd", "Musisz wybrać przedmiot.")
            return

        # obliczanie średniej ocen dla dziecka i dla klasy
        child_subject_grades = [int(grade[4]) for grade in child_grades if grade[3] == subject]
        class_subject_grades = [int(grade[4]) for grade in class_grades if grade[3] == subject]

        if not child_subject_grades or not class_subject_grades:
            messagebox.showerror("Błąd", "Brak ocen dla wybranego przedmiotu.")
            return

        child_avg = sum(child_subject_grades) / len(child_subject_grades)
        class_avg = sum(class_subject_grades) / len(class_subject_grades)

        # tworzenie wykresu
        plt.figure(figsize=(8, 6))
        bars = plt.bar(["Średnia dziecka", "Średnia klasy"], [child_avg, class_avg], color=['blue', 'green'])

        # dodanie wartości średnich ocen nad słupkami wykresu
        plt.text(bars[0].get_x() + bars[0].get_width() / 2, bars[0].get_height(), f'{child_avg:.2f}', ha='center',
                 va='bottom')
        plt.text(bars[1].get_x() + bars[1].get_width() / 2, bars[1].get_height(), f'{class_avg:.2f}', ha='center',
                 va='bottom')

        plt.xlabel("Średnia ucznia na tle klasy")
        plt.ylabel("Średnia ocen")
        plt.title(f"Średnia ocen z {subject}")
        plt.show()

    # okno do wyboru przedmiotu
    dialog = tk.Toplevel()
    dialog.title("Wybierz przedmiot")

    tk.Label(dialog, text="Wybierz przedmiot:").pack(pady=10)
    subject_combobox = ttk.Combobox(dialog, values=subjects)
    subject_combobox.pack(pady=10)

    tk.Button(dialog, text="OK", command=on_select).pack(pady=10)


def generate_attendance_pie_chart(login, attendance, students, parents_data): # funkcja do generowania wykresu kołowego frekwencji dla danego dziecka, procentowy udział nieobecnosci i obecnosci
    # pobierz id rodzica na podstawie loginu
    parent_id = next((row[0] for row in parents_data if row[3] == login), None)
    # znajdź dzieci tego użytkownika
    children = [student for student in students if student[3] == parent_id]

    if not children:
        messagebox.showerror("Błąd", "Nie znaleziono dzieci dla tego rodzica.")
        return

    child = children[0]
    child_attendance = [att for att in attendance if att[1] == child[1] and att[2] == child[2]] # tworzenie listy która zawiera wszystkie elementy frekwencji dziecka

    present_count = sum(1 for att in child_attendance if att[5] == 'obecny') #liczba dni obecnych zsumowanie wszystkich rekordów gdzie status obecnosci jest obecny
    absent_count = sum(1 for att in child_attendance if att[5] == 'nieobecny') # jw nieobecny

    if present_count + absent_count == 0:
        messagebox.showerror("Błąd", "Brak danych o frekwencji.")
        return

    labels = 'Obecny', 'Nieobecny'
    sizes = [present_count, absent_count]
    colors = ['green', 'red']

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Frekwencja ucznia')
    plt.show()


def generate_attendance_comparison_chart(login, attendance, students, parents_data):
    # pobierz id rodzica na podstawie loginu
    parent_id = next((row[0] for row in parents_data if row[3] == login), None)
    # znajdź dzieci tego użytkownika
    children = [student for student in students if student[3] == parent_id]

    if not children:
        messagebox.showerror("Błąd", "Nie znaleziono dzieci dla tego rodzica.")
        return

    child = children[0]
    class_name = child[0]
    child_name = f"{child[1]} {child[2]}"

    # filtrowanie frekwencji dziecka i wszystkich uczniów w tej samej klasie
    class_attendance = [att for att in attendance if att[0] == class_name]
    child_attendance = [att for att in class_attendance if att[1] == child[1] and att[2] == child[2]]

    child_present_count = sum(1 for att in child_attendance if att[5] == 'obecny')
    child_absent_count = sum(1 for att in child_attendance if att[5] == 'nieobecny')

    class_present_count = sum(1 for att in class_attendance if att[5] == 'obecny')
    class_absent_count = sum(1 for att in class_attendance if att[5] == 'nieobecny')

    if child_present_count + child_absent_count == 0 or class_present_count + class_absent_count == 0:
        messagebox.showerror("Błąd", "Brak danych o frekwencji.")
        return

    child_attendance_rate = child_present_count / (child_present_count + child_absent_count)
    class_attendance_rate = class_present_count / (class_present_count + class_absent_count)

    # tworzenie wykresu
    plt.figure(figsize=(8, 6))
    bars = plt.bar(["Frekwencja dziecka", "Frekwencja klasy"], [child_attendance_rate, class_attendance_rate], color=['blue', 'green'])

    # dodanie tekstu z wartościami nad słupkami
    plt.text(bars[0].get_x() + bars[0].get_width() / 2, bars[0].get_height(), f'{child_attendance_rate:.2%}', ha='center', va='bottom')
    plt.text(bars[1].get_x() + bars[1].get_width() / 2, bars[1].get_height(), f'{class_attendance_rate:.2%}', ha='center', va='bottom')

    plt.xlabel("Kategoria")
    plt.ylabel("Frekwencja")
    plt.title(f"Frekwencja ucznia na tle klasy")
    plt.show()
