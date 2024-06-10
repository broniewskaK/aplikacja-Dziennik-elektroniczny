import csv
# plik odpowiedzialny za ładowanie danych z csv do aplikacji
def load_parents():  # ładuje dane rodzicow jako slownik, klucz to login, wartosc haslo
    parents = {}
    with open("parents.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # pomija nagłówki
        for row in reader:
            if len(row) >= 5:
                id, imię, nazwisko, login, hasło = row
                parents[login] = hasło
    return parents

def load_parents_data(): # ładuje dane rodziców i zwraca je w firmie listy
    parents_data = []
    with open("parents.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # pomija nagłówki
        for row in reader:
            if len(row) >= 5:
                parents_data.append(row)
    return parents_data

def load_students():
    students = []
    with open("students.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if len(row) >= 4:
                students.append(row)
    return students

def load_grades():
    grades = []
    with open("grades.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if len(row) >= 5:
                grades.append(row)
    return grades

def load_attendance():
    attendance = []
    with open("attendance.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if len(row) >= 6:
                attendance.append(row)
    return attendance

def load_timetable():
    timetable = []
    with open("timetable.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if len(row) >= 5:
                timetable.append(row)
    return timetable
