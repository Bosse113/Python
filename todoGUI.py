import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# --- DATABASFUNKTIONER ---
def initiera_databas():
    conn = sqlite3.connect("uppgifter_gui.db")
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

def hämta_från_databas():
    conn = sqlite3.connect("uppgifter_gui.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, titel, klar FROM todos")
    rader = cursor.fetchall()
    conn.close()
    return rader

def lagg_till_i_databas(titel):
    conn = sqlite3.connect("uppgifter_gui.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (titel) VALUES (?)", (titel,))
    conn.commit()
    conn.close()

def uppdatera_i_databas(uppgift_id, klar_status):
    conn = sqlite3.connect("uppgifter_gui.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET klar = ? WHERE id = ?", (klar_status, uppgift_id))
    conn.commit()
    conn.close()

def ta_bort_fran_databas(uppgift_id):
    conn = sqlite3.connect("uppgifter_gui.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ?", (uppgift_id,))
    conn.commit()
    conn.close()


# --- GUI APPLIKATION ---
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Att göra-lista med SQLite")
        self.root.geometry("500x450")
        
        initiera_databas()
        
        # --- Övre sektionen: Inmatning ---
        ram_inmatning = tk.Frame(self.root, padx=10, pady=10)
        ram_inmatning.pack(fill=tk.X)
        
        self.ent_uppgift = tk.Entry(ram_inmatning, font=("Arial", 12))
        self.ent_uppgift.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.ent_uppgift.bind("<Return>", lambda event: self.lagg_till())
        
        btn_lagg_till = tk.Button(ram_inmatning, text="Lägg till", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=self.lagg_till)
        btn_lagg_till.pack(side=tk.RIGHT)
        
        # --- Mitten: Listan (Treeview) ---
        ram_lista = tk.Frame(self.root, padx=10, pady=5)
        ram_lista.pack(fill=tk.BOTH, expand=True)
        
        self.trv = ttk.Treeview(ram_lista, columns=("ID", "Uppgift", "Status"), show="headings", selectmode="browse")
        self.trv.heading("ID", text="ID")
        self.trv.heading("Uppgift", text="Uppgift")
        self.trv.heading("Status", text="Status")
        
        self.trv.column("ID", width=40, anchor=tk.CENTER)
        self.trv.column("Uppgift", width=300, anchor=tk.W)
        self.trv.column("Status", width=100, anchor=tk.CENTER)
        
        self.trv.pack(fill=tk.BOTH, expand=True)
        
        # Färgkonfiguration för rader
        self.trv.tag_configure("klar_rad", foreground="#1b5e20", font=("Arial", 10, "italic"))
        self.trv.tag_configure("ej_klar_rad", foreground="#b71c1c", font=("Arial", 10, "bold"))
        
        # --- Undre sektionen: Knappar ---
        ram_knappar = tk.Frame(self.root, padx=10, pady=10)
        ram_knappar.pack(fill=tk.X)
        
        # Ändrad text till "Ändra status" (växlar mellan klar/ej klar)
        btn_status = tk.Button(ram_knappar, text="Ändra status (Klar / Ej klar)", bg="#2196F3", fg="white", font=("Arial", 10), command=self.vaxla_status)
        btn_status.pack(side=tk.LEFT, padx=(0, 5))
        
        btn_ta_bort = tk.Button(ram_knappar, text="Ta bort", bg="#f44336", fg="white", font=("Arial", 10), command=self.ta_bort)
        btn_ta_bort.pack(side=tk.RIGHT)
        
        self.ladda_data()

    def ladda_data(self):
        """Rensar listan och hämtar ny data. Applicerar färgtags på raderna."""
        for rad in self.trv.get_children():
            self.trv.delete(rad)
            
        for rad in hämta_från_databas():
            if rad[2] == 1:
                status = "Klar"
                tagg = "klar_rad"
            else:
                status = "Ej klar"
                tagg = "ej_klar_rad"
                
            self.trv.insert("", tk.END, values=(rad[0], rad[1], status), tags=(tagg,))

    def lagg_till(self):
        titel = self.ent_uppgift.get().strip()
        if titel:
            lagg_till_i_databas(titel)
            self.ent_uppgift.delete(0, tk.END)
            self.ladda_data()
        else:
            messagebox.showwarning("Varning", "Du kan inte lägga till en tom uppgift!")

    def hamta_vald_rad_info(self):
        """Hjälpfunktion för att hämta både ID och nuvarande Status från vald rad."""
        valt_objekt = self.trv.selection()
        if not valt_objekt:
            messagebox.showwarning("Varning", "Du måste välja en uppgift i listan först!")
            return None, None
        
        id_varde = self.trv.item(valt_objekt)['values'][0]
        status_varde = self.trv.item(valt_objekt)['values'][2]
        return id_varde, status_varde

    def vaxla_status(self):
        """Kollar nuvarande status och ändrar till motsatsen i databasen."""
        uppgift_id, nuvarande_status = self.hamta_vald_rad_info()
        
        if uppgift_id:
            # Om den var "Klar", sätt till 0 (Ej klar). Annars sätt till 1 (Klar).
            ny_status = 0 if nuvarande_status == "Klar" else 1
            uppdatera_i_databas(uppgift_id, ny_status)
            self.ladda_data()

    def ta_bort(self):
        valt_objekt = self.trv.selection()
        if not valt_objekt:
            messagebox.showwarning("Varning", "Du måste välja en uppgift i listan först!")
            return
            
        uppgift_id = self.trv.item(valt_objekt)['values'][0]
        if messagebox.askyesno("Bekräfta", "Är du säker på att du vill ta bort uppgiften?"):
            ta_bort_fran_databas(uppgift_id)
            self.ladda_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()