import csv
from datetime import datetime

def write_closing_log(Geld, reisen, log_file="logs.txt"):
    with open(log_file, "a+") as logs:
        zeit = datetime.now()
        ts = zeit.strftime("%d.%m;%H:%M")
        writetext = (
            "BEENDEN\n"
            "TS: " + ts + "\n" +
            "Geld: " + str(Geld) + ", Reisen: " + str(reisen) +
            "\n---------------\n"
        )
        logs.write(writetext)

def upload_score(score, username, score_file="score.csv"):
    daten = []
    kategorien = ["Benutzername", "Score"]
    try:
        with open(score_file, "r") as p:
            reader = csv.reader(p)
            kategorien = next(reader)
            for row in reader:
                daten.append(row)
    except FileNotFoundError:
        pass
    daten.append([username, score])
    with open(score_file, "w", newline='') as p:
        writer = csv.writer(p)
        writer.writerow(kategorien)
        writer.writerows(daten)