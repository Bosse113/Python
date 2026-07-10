import tkinter as tk
from tkinter import messagebox
import random
#Grunden gjord med AI
#Ett litet spel tänkt för barn som nyss lärt sig läsa
class AgentyrsSpel:
    def __init__(self, root):
        self.root = root
        self.root.title("🌲 Den Magiska Skogen 🌲")
        self.root.geometry("600x500")
        self.root.configure(bg="#e0f2f1")

        # Startvärden
        self.liv = 3
        self.ryggsack = []
        self.matte_tal = (0, 0) # Sparar talen för trollkarlen

        # Textruta för äventyret
        self.text_label = tk.Label(
            root, 
            text="Välkommen till Den Magiska Skogen!\n\nUppdrag: Samla alla 3 föremål för att kunna rädda guld-enhörningen!\nDu behöver: Magiskt Äpple, Guldnyckel och en Magisk Karta.", 
            font=("Helvetica", 12), 
            wraplength=500, 
            bg="#e0f2f1",
            fg="#2e7d32"
        )
        self.text_label.pack(pady=20)

        # Statusrad för liv
        self.liv_label = tk.Label(
            root, 
            text=f"❤️ Liv kvar: {self.liv}", 
            font=("Helvetica", 12, "bold"), 
            bg="#e0f2f1",
            fg="#c62828"
        )
        self.liv_label.pack(pady=5)

        # Statusrad för ryggsäck
        self.ryggsack_label = tk.Label(
            root, 
            text="🎒 Ryggsäck: Tom", 
            font=("Helvetica", 12, "italic"), 
            bg="#e0f2f1",
            fg="#455a64"
        )
        self.ryggsack_label.pack(pady=5)

        # Knappar för valen
        self.knapp1 = tk.Button(root, text="Starta Äventyret", font=("Helvetica", 12), command=self.visa_startstig, width=35, bg="#4caf50", fg="white")
        self.knapp1.pack(pady=8)

        self.knapp2 = tk.Button(root, text="", font=("Helvetica", 12), command=None, width=35, bg="#2196f3", fg="white")
        self.knapp2.pack_forget()

        self.knapp3 = tk.Button(root, text="", font=("Helvetica", 12), command=None, width=35, bg="#9c27b0", fg="white")
        self.knapp3.pack_forget()

        # Inputfält för text-svar (gåta och matte)
        self.svar_entry = tk.Entry(root, font=("Helvetica", 12), width=20)
        self.svar_knapp = tk.Button(root, text="Svara", font=("Helvetica", 12), command=None, bg="#ff9800", fg="white")

    def uppdatera_status(self):
        self.liv_label.config(text=f"❤️ Liv kvar: {self.liv}")
        
        if len(self.ryggsack) == 0:
            self.ryggsack_label.config(text="🎒 Ryggsäck: Tom")
        else:
            saker = ", ".join(self.ryggsack)
            self.ryggsack_label.config(text=f"🎒 Ryggsäck: {saker}")

        if self.liv <= 0:
            messagebox.showinfo("👻 Spel Slut!", "Slut på liv! Spelet är över den här gången.")
            self.fraga_spela_igen()

    def visa_startstig(self):
        self.text_label.config(text="Du står vid vägskälet. Det finns tre stigar här nu!\nVart vill du gå för att leta efter föremål?")
        
        # Visa alla tre knapparna för de tre platserna
        self.knapp1.pack(pady=8)
        self.knapp2.pack(pady=8)
        self.knapp3.pack(pady=8)
        
        self.knapp1.config(text="1. VÄNSTER till den glittrande sjön", command=self.visa_sjon, bg="#00bcd4")
        self.knapp2.config(text="2. MITTEN in i den mörka skogen", command=self.visa_morka_skogen, bg="#5d4037")
        self.knapp3.config(text="3. HÖGER till den djupa grottan", command=self.visa_grottan, bg="#78909c")
        
        self.svar_entry.pack_forget()
        self.svar_knapp.pack_forget()

    # --- PLATS 1: SJÖN ---
    def visa_sjon(self):
        self.knapp3.pack_forget() # Vi behöver bara två knappar här
        self.text_label.config(text="--- VID DEN GLITTRANDE SJÖN ---\n\nSjön glänser. På stranden växer ett träd med glödande röda äpplen. En drake väntar i vattnet.")
        self.knapp1.config(text="Plocka ett Magiskt Äpple", command=self.plocka_apple, bg="#e91e63")
        self.knapp2.config(text="Åk med draken till Enhörningen", command=self.mot_enhorning, bg="#4caf50")

    def plocka_apple(self):
        if "Magiskt Äpple" not in self.ryggsack:
            self.ryggsack.append("Magiskt Äpple")
            messagebox.showinfo("🍏 Hittat!", "Du stoppade ett Magiskt Äpple i ryggsäcken!")
        else:
            messagebox.showinfo("Obs!", "Du har redan ett äpple.")
        self.uppdatera_status()

    # --- PLATS 2: SKOGEN ---
    def visa_morka_skogen(self):
        self.text_label.config(text="--- DEN MÖRKA SKOGEN ---\n\nEkorren sitter på en gren:\n'Svara rätt på min gåta så får du min skatt!'\n\nGåta: Vad blir blötare ju mer man torkar?")
        self.knapp1.pack_forget()
        self.knapp2.pack_forget()
        self.knapp3.pack_forget()
        
        self.svar_entry.delete(0, tk.END)
        self.svar_entry.pack(pady=10)
        self.svar_knapp.config(command=self.kolla_gata)
        self.svar_knapp.pack(pady=5)

    def kolla_gata(self):
        svar = self.svar_entry.get().lower()
        if "handduk" in svar:
            if "Guldnyckel" not in self.ryggsack:
                self.ryggsack.append("Guldnyckel")
                messagebox.showinfo("🔑 Rätt svar!", "Ekorren jublar och ger dig en Guldnyckel!")
            else:
                messagebox.showinfo("Ekorren säger:", "Du har ju redan min nyckel!")
            self.uppdatera_status()
            self.visa_startstig()
        else:
            self.liv -= 1
            messagebox.showwarning("❌ Fel svar", "Ekorren kastar en kotte på dig! Du förlorar 1 liv.")
            self.uppdatera_status()
            if self.liv > 0:
                self.visa_startstig()

    # --- PLATS 3: GROTTAN (NY!) ---
    def visa_grottan(self):
        # Slumpa fram ett enkelt mattetal, t.ex. mellan 1 och 10
        tal1 = random.randint(2, 10)
        tal2 = random.randint(2, 9)
        self.matte_tal = (tal1, tal2)

        self.text_label.config(text=f"--- DEN DJUPA GROTTAN ---\n\nI grottans mörker möter du en gammal, snäll trollkarl. Han tänder sin stav och säger:\n'Om du kan lösa mitt magiska mattetal ska du få en karta som visar vägen till enhörningen!'\n\nVad är {tal1} + {tal2}?")
        
        self.knapp1.pack_forget()
        self.knapp2.pack_forget()
        self.knapp3.pack_forget()
        
        self.svar_entry.delete(0, tk.END)
        self.svar_entry.pack(pady=10)
        self.svar_knapp.config(command=self.kolla_matte)
        self.svar_knapp.pack(pady=5)

    def kolla_matte(self):
        try:
            svar = int(self.svar_entry.get())
            ratt_svar = self.matte_tal[0] + self.matte_tal[1]
            
            if svar == ratt_svar:
                if "Magisk Karta" not in self.ryggsack:
                    self.ryggsack.append("Magisk Karta")
                    messagebox.showinfo("🗺️ Rätt svar!", "Trollkarlen ler och trollar fram en Magisk Karta till din ryggsäck!")
                else:
                    messagebox.showinfo("Trollkarlen säger:", "Du har redan kartan, unge äventyrare!")
                self.uppdatera_status()
                self.visa_startstig()
            else:
                self.liv -= 1
                messagebox.showwarning("⚡ Fel svar", "Det sprakar till från trollkarlens stav! Du blir lite snurrig och förlorar 1 liv.")
                self.uppdatera_status()
                if self.liv > 0:
                    self.visa_startstig()
        except ValueError:
            messagebox.showerror("Hoppsan", "Skriv svaret med siffror!")

    # --- FINALEN ---
    def mot_enhorning(self):
        self.text_label.config(text="--- ENHÖRNINGENS GLÄNTA ---\n\nDraken flyger dig till en magisk glänta. Där står den vackra guld-enhörningen låst bakom ett guldgaller. Den ser hungrig ut och väntar på att bli räddad!")
        self.knapp1.config(text="Rädda enhörningen med dina föremål", command=self.kolla_vinst, bg="#9c27b0")
        self.knapp2.config(text="Gå tillbaka till stigen", command=self.visa_startstig, bg="#78909c")

    def kolla_vinst(self):
        # Här kollas ALLA TRE uppgifter!
        if "Guldnyckel" in self.ryggsack and "Magiskt Äpple" in self.ryggsack and "Magisk Karta" in self.ryggsack:
            messagebox.showinfo("🦄 DU VANN SPELET!", "Med kartan hittade du rätt lås, med nyckeln låste du upp gallret, och med äpplet matade du enhörningen så att den blev glad! Du är skogens hjälte!")
            self.fraga_spela_igen()
        else:
            messagebox.showwarning(
                "🔒 Det saknas något...", 
                f"Du har inte alla saker ännu!\n\n"
                f"Du har just nu: {', '.join(self.ryggsack) if self.ryggsack else 'Ingenting'}\n\n"
                f"Du måste hämta Äpplet (Sjön), Nyckeln (Skogen) OCH Kartan (Grottan) först!"
            )

    def fraga_spela_igen(self):
        svar = messagebox.askyesno("Spela igen?", "Vill du spela en gång till?")
        if svar:
            self.liv = 3
            self.ryggsack = []
            self.uppdatera_status()
            self.visa_startstig()
        else:
            self.root.quit()

if __name__ == "__main__":
    fönster = tk.Tk()
    app = AgentyrsSpel(fönster)
    fönster.mainloop()