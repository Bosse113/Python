import sqlite3
import os

def initiera_databas():
    """Skapar databasen och tabellen om de inte finns."""
    conn = sqlite3.connect("uppgifter.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titel TEXT NOT NULL,
            klar INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def lagg_till_uppgift(titel):
    if not titel.strip():
        print(" Uppgiften kan inte vara tom!")
        return
    conn = sqlite3.connect("uppgifter.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (titel) VALUES (?)", (titel,))
    conn.commit()
    conn.close()
    print(f"\n Lagt till: '{titel}'")

def visa_uppgifter():
    conn = sqlite3.connect("uppgifter.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, titel, klar FROM todos")
    rader = cursor.fetchall()
    conn.close()
    
    print("\n================ DETTA SKA GÖRAS ================")
    if not rader:
        print("\n   Listan är tom! Njut av din lediga tid.")
    else:
        for rad in rader:
            status = "🟢 Klar" if rad[2] == 1 else "🔴 Ej klar"
            print(f"  [{rad[0]}] {rad[1]:<30} | {status}")
    print("=================================================\n")

def markera_som_klar(uppgift_id):
    conn = sqlite3.connect("uppgifter.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET klar = 1 WHERE id = ?", (uppgift_id,))
    conn.commit()
    
    if cursor.rowcount == 0:
        print(f"\n Hittade ingen uppgift med ID {uppgift_id}.")
    else:
        print(f"\n Uppgift {uppgift_id} markerad som klar!")
    conn.close()

def ta_bort_uppgift(uppgift_id):
    conn = sqlite3.connect("uppgifter.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ?", (uppgift_id,))
    conn.commit()
    
    if cursor.rowcount == 0:
        print(f"\n Hittade ingen uppgift med ID {uppgift_id}.")
    else:
        print(f"\n Uppgift {uppgift_id} har tagits bort!")
    conn.close()

# --- Huvudprogram med meny ---
def meny():
    initiera_databas()
    
    while True:
        print("--- MENY ---")
        print("1. Visa alla uppgifter")
        print("2. Lägg till en uppgift")
        print("3. Markera en uppgift som klar")
        print("4. Ta bort en uppgift")
        print("5. Avsluta")
        
        val = input("Välj ett alternativ (1-5): ").strip()
        
        if val == "1":
            visa_uppgifter()
        
        elif val == "2":
            ny_uppgift = input("Skriv vad du vill lägga till: ")
            lagg_till_uppgift(ny_uppgift)
            
        elif val == "3":
            visa_uppgifter()
            try:
                valda_id = int(input("Ange ID på uppgiften som är klar: "))
                markera_som_klar(valda_id)
            except ValueError:
                print(" Du måste mata in ett nummer!")
                
        elif val == "4":
            visa_uppgifter()
            try:
                valda_id = int(input("Ange ID på uppgiften du vill ta bort: "))
                ta_bort_uppgift(valda_id)
            except ValueError:
                print(" Du måste mata in ett nummer!")
                
        elif val == "5":
            print("\n Hejdå! Lycka till med dina uppgifter.")
            break
            
        else:
            print(" Ogiltigt val, försök igen.\n")

if __name__ == "__main__":
    meny()