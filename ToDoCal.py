import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar


class TodoApp:

    def __init__(self, root):
        # Sparar referensen till huvudfönstret
        self.root = root
        self.root.title("Att-göra-lista med Kalender")
        self.root.geometry("750x450")
        self.root.configure(bg="#f0f0f0")  # Ljusgrå bakgrundsfärg

        # Skapa databasen och tabellen om den inte redan finns
        self.init_db()

        # ==========================================
        # LAYOUT OCH GRÄNSSNITT (GUI)
        # ==========================================

        # Vänster ram (Frame) för kalendern.
        # fill=tk.BOTH gör att den kan ta upp vertikal plats, expand=False gör att den inte breder ut sig i sidled.
        self.left_frame = tk.Frame(root, bg="#f0f0f0")
        self.left_frame.pack(
            side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10, pady=10
        )

        # Höger ram (Frame) för själva att-göra-listan och dess knappar.
        # expand=True gör att den här delen tar upp allt resterande utrymme på skärmen.
        self.right_frame = tk.Frame(root, bg="#f0f0f0")
        self.right_frame.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10
        )

        # --- Kalender (Placeras i vänster ram) ---
        self.cal = Calendar(
            self.left_frame,
            selectmode="day",  # Tillåt att man väljer en specifik dag
            date_pattern="yyyy-mm-dd",  # Standardiserat datumformat (ISO)
            cursor="hand2",  # Muspekaren ändras till en hand när man hovrar över kalendern
        )
        self.cal.pack(pady=10, fill=tk.BOTH, expand=True)

        # Koppla (bind) en händelse: När användaren klickar på ett datum i kalendern,
        # körs funktionen self.load_tasks automatiskt för att hämta det datumets uppgifter.
        self.cal.bind("<<CalendarSelected>>", self.load_tasks)

        # --- Att-göra-gränssnitt (Placeras i höger ram) ---
        # En etikett (Label) som visar vilket datum som är valt just nu
        self.date_label = tk.Label(
            self.right_frame,
            text="",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            fg="#333",
        )
        self.date_label.pack(anchor="w", pady=(0, 10))  # anchor="w" vänsterjusterar texten

        # En mindre ram för att hålla inmatningsfältet och "Lägg till"-knappen på samma rad
        self.entry_frame = tk.Frame(self.right_frame, bg="#f0f0f0")
        self.entry_frame.pack(fill=tk.X, pady=5)

        # Inmatningsfältet (Entry) där man skriver nya uppgifter
        self.task_entry = ttk.Entry(self.entry_frame, font=("Arial", 11))
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        # Gör så att man kan trycka på "Enter" på tangentbordet för att lägga till uppgiften
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        # "Lägg till"-knappen
        self.add_btn = ttk.Button(
            self.entry_frame, text="Lägg till", command=self.add_task
        )
        self.add_btn.pack(side=tk.RIGHT)

        # Ram för listboxen och dess tillhörande rullningslist (Scrollbar)
        self.list_frame = tk.Frame(self.right_frame)
        self.list_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.scrollbar = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL)

        # Listboxen som visar alla uppgifter. activestyle="none" tar bort den fula understrykningen vid markering.
        self.task_listbox = tk.Listbox(
            self.list_frame,
            font=("Arial", 11, "bold"),
            selectmode=tk.SINGLE,  # Tillåt bara att man väljer en uppgift i taget
            yscrollcommand=self.scrollbar.set,  # Koppla listboxen till rullningslisten
            activestyle="none",
        )
        self.scrollbar.config(
            command=self.task_listbox.yview
        )  # Gör rullningslisten funktionell

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Ram längst ner för åtgärdsknapparna
        self.btn_frame = tk.Frame(self.right_frame, bg="#f0f0f0")
        self.btn_frame.pack(fill=tk.X, pady=(5, 0))

        # Knapp: Markera som klar / Ångra
        self.complete_btn = ttk.Button(
            self.btn_frame,
            text="Markera som klar / Ångra",
            command=self.toggle_task,
        )
        self.complete_btn.pack(side=tk.LEFT, padx=(0, 5))

        # Knapp: Ta bort
        self.delete_btn = ttk.Button(
            self.btn_frame, text="Ta bort", command=self.delete_task
        )
        self.delete_btn.pack(side=tk.LEFT, padx=(0, 5))

        # Knapp: Visa rapport (placeras till höger i knappraden)
        self.report_btn = ttk.Button(
            self.btn_frame,
            text="Visa rapport (Ej klara)",
            command=self.show_report_window,
        )
        self.report_btn.pack(side=tk.RIGHT)

        # Läs automatiskt in uppgifter för dagens datum så fort programmet startar
        self.load_tasks()

    # ==========================================
    # DATABASFUNKTIONER (SQLite)
    # ==========================================

    def init_db(self):
        """Skapar databasfilen och tabellen om de saknas."""
        conn = sqlite3.connect("todo.db")  # Skapar/öppnar filen todo.db
        cursor = conn.cursor()
        # TEXT för datum (YYYY-MM-DD), TEXT för uppgiften, INTEGER för status (0=ej klar, 1=klar)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                task TEXT NOT NULL,
                status INTEGER DEFAULT 0
            )
        """
        )
        conn.commit()  # Sparar ändringarna
        conn.close()  # Stänger anslutningen

    def load_tasks(self, event=None):
        """Hämtar och visar uppgifter i listboxen baserat på valt datum i kalendern."""
        selected_date = self.cal.get_date()  # Hämtar valt datum (sträng)
        self.date_label.config(
            text=f"Uppgifter för: {selected_date}"
        )  # Uppdaterar rubriken
        self.task_listbox.delete(0, tk.END)  # Tömer listboxen innan vi laddar ny data

        # Denna lista lagrar SQLite-ID för de uppgifter som visas på skärmen just nu.
        # Det gör att vi kan identifiera exakt vilken rad i databasen som ska tas bort/ändras.
        self.current_task_ids = []

        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()
        # Hämtar ID, text och status för det valda datumet
        cursor.execute(
            "SELECT id, task, status FROM tasks WHERE date = ?",
            (selected_date,),
        )
        rows = cursor.fetchall()
        conn.close()

        # Loopar igenom resultatet från databasen
        for row in rows:
            task_id, task_text, status = row
            self.current_task_ids.append(
                task_id
            )  # Sparar ID på samma index som i listboxen

            # Bestämmer symbol och färg baserat på om uppgiften är klar (1) eller ej (0)
            if status == 1:
                display_text = f"✓ {task_text}"
                text_color = "#2e7d32"  # Mörkgrön
            else:
                display_text = f"☐ {task_text}"
                text_color = "#c62828"  # Mörkröd

            self.task_listbox.insert(
                tk.END, display_text
            )  # Lägger till texten sist i listboxen
            self.task_listbox.itemconfig(
                tk.END, {"fg": text_color}
            )  # Färgar den specifika raden

    def add_task(self):
        """Sparar en ny uppgift i databasen."""
        task_text = self.task_entry.get().strip()  # Hämtar texten och tar bort extra mellanslag
        selected_date = self.cal.get_date()

        # Validering: Tillåt inte tomma uppgifter
        if task_text == "":
            messagebox.showwarning("Varning", "Du kan inte lägga till en tom uppgift.")
            return

        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()
        # Sätter in datum och text. Status blir automatiskt 0 enligt tabellstrukturen.
        cursor.execute(
            "INSERT INTO tasks (date, task) VALUES (?, ?)",
            (selected_date, task_text),
        )
        conn.commit()
        conn.close()

        self.task_entry.delete(0, tk.END)  # Tömmer inmatningsfältet
        self.load_tasks()  # Uppdaterar listboxen så den nya uppgiften syns

    def toggle_task(self):
        """Växlar status på den markerade uppgiften (Klar <-> Ej klar)."""
        try:
            # Hämtar indexet för den markerade raden i listboxen
            selected_index = self.task_listbox.curselection()[0]
            # Hittar motsvarande SQLite-ID med hjälp av vår dolda ID-lista
            task_id = self.current_task_ids[selected_index]
        except IndexError:
            # Om användaren inte har markerat något i listboxen visas en varning
            messagebox.showwarning("Varning", "Välj en uppgift i listan först.")
            return

        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()

        # 1. Ta reda på uppgiftens nuvarande status
        cursor.execute("SELECT status FROM tasks WHERE id = ?", (task_id,))
        current_status = cursor.fetchone()[0]

        # 2. Invertera statusen: Om den var 1 blir den 0, om den var 0 blir den 1
        new_status = 0 if current_status == 1 else 1

        # 3. Uppdatera raden i databasen
        cursor.execute(
            "UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id)
        )
        conn.commit()
        conn.close()

        self.load_tasks()  # Rita ut listan på nytt med den nya färgen/symbolen

    def delete_task(self):
        """Raderar den markerade uppgiften permanent från databasen."""
        try:
            selected_index = self.task_listbox.curselection()[0]
            task_id = self.current_task_ids[selected_index]
        except IndexError:
            messagebox.showwarning("Varning", "Välj en uppgift i listan först.")
            return

        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()
        # Tar bort raden baserat på dess unika ID
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()

        self.load_tasks()  # Uppdaterar listboxen

    # ==========================================
    # RAPPORT-FUNKTION (Nytt Fönster)
    # ==========================================

    def show_report_window(self):
        """Hämtar ALLA ej klara uppgifter och visar dem i ett nytt popup-fönster."""
        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()
        # Hämtar alla rader där status är 0, sorterat äldsta datum först
        cursor.execute(
            "SELECT date, task FROM tasks WHERE status = 0 ORDER BY date ASC"
        )
        rows = cursor.fetchall()
        conn.close()

        # Om databasen inte returnerar några rader, avbryt och beröm användaren
        if not rows:
            messagebox.showinfo(
                "Info", "Snyggt jobbat! Det finns inga ogjorda uppgifter just nu."
            )
            return

        # --- Skapa popup-fönstret (Toplevel) ---
        report_win = tk.Toplevel(self.root)
        report_win.title("Rapport: Oavslutade Uppgifter")
        report_win.geometry("450x400")
        report_win.configure(bg="#f0f0f0")

        # Fönsterlåsning (Modalt): Gör att popup-fönstret lägger sig överst
        # och blockerar klick i huvudfönstret tills rapporten stängs.
        report_win.transient(self.root)
        report_win.grab_set()

        # Titeltext inuti popup-fönstret
        title_lbl = tk.Label(
            report_win,
            text="Ej avklarade uppgifter",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            fg="#c62828",
        )
        title_lbl.pack(pady=10)

        # Skapa en ram för textrutan och rullningslisten
        text_frame = tk.Frame(report_win)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        text_scroll = ttk.Scrollbar(text_frame, orient=tk.VERTICAL)

        # En Text-widget används istället för Listbox för att vi vill kunna formatera
        # fri text med rubriker och indrag på ett snyggt sätt.
        report_text = tk.Text(
            text_frame,
            font=("Consolas", 11),  # Monospace-typsnitt gör att strukturen blir spikrak
            yscrollcommand=text_scroll.set,
            bg="white",
            spacing1=3,  # Lägger till lite extra luft mellan raderna
        )
        text_scroll.config(command=report_text.yview)

        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        report_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Skriv ut en snygg header i textrutan
        report_text.insert(tk.END, "=========================================\n")
        report_text.insert(tk.END, "  Sorterat kronologiskt efter datum\n")
        report_text.insert(tk.END, "=========================================\n")

        # Loopa igenom alla oavklarade uppgifter och lägg till i textrutan
        current_date = ""
        for date, task in rows:
            # Om det är ett nytt datum, skriv ut en datumsrubrik först
            if date != current_date:
                report_text.insert(tk.END, f"\n📅 {date}\n")
                current_date = date
            # Skriv ut själva uppgiften med ett indrag
            report_text.insert(tk.END, f"  ❌ {task}\n")

        # Stäng av skrivrättigheter (DISABLED) för textrutan. 
        # Detta gör att användaren kan läsa och markera texten, men inte ändra eller radera den.
        report_text.config(state=tk.DISABLED)

        # Stäng-knapp längst ner i popup-fönstret. .destroy stänger bara detta specifika fönster.
        close_btn = ttk.Button(
            report_win, text="Stäng", command=report_win.destroy
        )
        close_btn.pack(pady=10)


# ==========================================
# APPENS STARTPUNKT
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()  # Skapar huvudfönstret
    app = TodoApp(root)  # Initierar vår klass med fönstret som argument
    root.mainloop()  # Startar Tkinter-loopen som håller fönstret vid liv och lyssnar på klick