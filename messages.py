import csv

def load_teachers(): # funkcja ładuje dane nauczycieli z pliku i zwraca je w formie listy
    teachers = []
    with open("teachers.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # pomija nagłówki
        for row in reader:
            teachers.append(row)
    return teachers

def send_message(sender, recipient, content): # funkcja zapisuje wiadomosci do pliku messages
    with open("messages.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([sender, recipient, content])

def load_received_messages(login): # funkcja ładuje wszystkie wiadomosci otrzymane przez użytkownika z pliku messages ( funkcjonalnosc do rozszerzenia przy dalszej pracy nad aplikacją)
    received_messages = []
    with open("messages.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == login:
                received_messages.append(row)
    return received_messages

def load_sent_messages(login): # funkcja ładuje wiadomosci wyslane przez użytkownika
    sent_messages = []
    with open("messages.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == login:
                sent_messages.append(row)
    return sent_messages
