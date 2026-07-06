import sqlite3

DB_NAME = "app.db"


def skapa_databas():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            namn TEXT NOT NULL,
            alder INTEGER
        )
    """)

    conn.commit()
    conn.close()


def lagg_till_person():
    namn = input("Namn: ")
    alder = int(input("Ålder: "))

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO personer (namn, alder) VALUES (?, ?)",
        (namn, alder)
    )

    conn.commit()
    conn.close()

    print("Person sparad!")


def visa_personer():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM personer")
    personer = cursor.fetchall()

    if personer:
        print("\nPersoner:")
        for person in personer:
            print(f"ID: {person[0]}, Namn: {person[1]}, Ålder: {person[2]}")
    else:
        print("Inga personer hittades.")

    conn.close()


def ta_bort_person():
    person_id = int(input("Ange ID att ta bort: "))

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM personer WHERE id = ?", (person_id,))

    conn.commit()
    conn.close()

    print("Person borttagen.")


def meny():
    while True:
        print("\n=== SQLite Demo ===")
        print("1. Lägg till person")
        print("2. Visa personer")
        print("3. Ta bort person")
        print("4. Avsluta")

        val = input("Välj: ")

        if val == "1":
            lagg_till_person()
        elif val == "2":
            visa_personer()
        elif val == "3":
            ta_bort_person()
        elif val == "4":
            print("Hej då!")
            break
        else:
            print("Ogiltigt val.")


if __name__ == "__main__":
    skapa_databas()
    meny()