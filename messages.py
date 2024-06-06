import csv

def load_teachers():
    teachers = []
    with open("teachers.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # Pomija nagłówki
        for row in reader:
            teachers.append(row)
    return teachers

def send_message(sender, recipient, content):
    with open("messages.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([sender, recipient, content])

def load_received_messages(login):
    received_messages = []
    with open("messages.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == login:
                received_messages.append(row)
    return received_messages

def load_sent_messages(login):
    sent_messages = []
    with open("messages.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == login:
                sent_messages.append(row)
    return sent_messages
