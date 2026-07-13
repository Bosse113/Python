import os
import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random

class AgentyrsSpel:
    def __init__(self, root):
        self.root = root
        self.root.title("🌲 Den Magiska Skogen 🌲")
        self.root.geometry("600x550")
        self.root.configure(bg="#e0f2f1")

        # Startvärden
        self.liv = 3
        self.ryggsack = []
        self.matte_tal = (0, 0)
        self.stig_sida = 1  # Håller koll på vilken sida med stigar som visas

        # Mål: Alla 6 föremål krävs nu!
        self.mal_foremal = [
            "Magiskt Äpple", "Guldnyckel", "Magisk Karta", 
            "Kristallhonung", "Gammalt Mynt", "Häxbrygd"
        ]

        # Textruta för äventyret
        self.text_label = tk.Label(
            root, 
            text="Välkommen till Den Magiska Skogen!\n\nUppdrag: Samla ALLA 6 föremål för att kunna rädda guld-enhörningen!\nDu behöver: Äpple, Nyckel, Karta, Honung, Mynt och Häxbrygd.", 
            font=("Helvetica", 11), 
            wraplength=500, 
            bg="#e0f2f1",
            fg="#2e7d32"
        )
        self.text_label.pack(pady=15)

        # Statusrad för liv
        self.liv_label = tk.Label(
            root, 
            text=f"❤️ Liv kvar: {self.liv}", 
            font=("Helvetica", 12, "bold"), 
            bg="#e0f2f1",
            fg="#c62828"
        )
        self.liv_label.pack(pady=2)

        # Statusrad för ryggsäck
        self.ryggsack_label = tk.Label(
            root, 
            text="🎒 Ryggsäck: Tom", 
            font=("Helvetica", 11, "italic"), 
            bg="#e0f2f1",
            fg="#455a64"
        )
        self.ryggsack_label.pack(pady=2)

        # Knappar för valen
        self.knapp1 = tk.Button(root, text="Starta Äventyret", font=("Helvetica", 11), command=self.visa_startstig, width=40, bg="#4caf50", fg="white")
        self.knapp1.pack(pady=5)

        self.knapp2 = tk.Button(root, text="", font=("Helvetica", 11), command=None, width=40, bg="#2196f3", fg="white")
        self.knapp2.pack_forget()

        self.knapp3 = tk.Button(root, text="", font=("Helvetica", 11), command=None, width=40, bg="#9c27b0", fg="white")
        self.knapp3.pack_forget()

        # Extra knapp för att bläddra mellan stigar
        self.knapp_sida = tk.Button(root, text="➡️ Visa fler stigar", font=("Helvetica", 10, "bold"), command=self.byt_stig_sida, width=20, bg="#ff5722", fg="white")
        self.knapp_sida.pack_forget()

        # Inputfält för text-svar
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

    def byt_stig_sida(self):
        """Växlar mellan sida 1 och 2 vid vägskälet."""
        self.stig_sida = 2 if self.stig_sida == 1 else 1
        self.visa_startstig()

    def visa_startstig(self):
        self.svar_entry.pack_forget()
        self.svar_knapp.pack_forget()
        
        self.knapp1.pack(pady=5)
        self.knapp2.pack(pady=5)
        self.knapp3.pack(pady=5)
        self.knapp_sida.pack(pady=10)

        if self.stig_sida == 1:
            self.text_label.config(text="Du står vid vägskälet. Sida 1/2.\nVart vill du gå?")
            self.knapp1.config(text="1. VÄNSTER: Till den glittrande sjön", command=self.visa_sjon, bg="#00bcd4")
            self.knapp2.config(text="2. MITTEN: In i den mörka skogen", command=self.visa_morka_skogen, bg="#5d4037")
            self.knapp3.config(text="3. HÖGER: Till den djupa grottan", command=self.visa_grottan, bg="#78909c")
            self.knapp_sida.config(text="➡️ Se fler stigar (Sida 2)")
        else:
            self.text_label.config(text="Du utforskar djupare stigar. Sida 2/2.\nVart vill du gå?")
            self.knapp1.config(text="4. ÄNGEN: Till den blommiga ängen", command=self.visa_angen, bg="#8bc34a")
            self.knapp2.config(text="5. RUINEN: Till den gamla slottsruinen", command=self.visa_ruinen, bg="#9e9e9e")
            self.knapp3.config(text="6. TRÄDGÅRDEN: Till häxans trädgård", command=self.visa_haxans_tradgard, bg="#e040fb")
            self.knapp_sida.config(text="⬅️ Gå tillbaka (Sida 1)")

    # --- PLATS 1: SJÖN ---
    def visa_sjon(self):
        self.knapp_sida.pack_forget()
        self.knapp3.pack_forget()
        self.text_label.config(text="--- VID DEN GLITTRANDE SJÖN ---\n\nSjön glänser. På stranden växer ett träd med glödande röda äpplen. En drake väntar i vattnet.")
        self.knapp1.config(text="Plocka ett Magiskt Äpple", command=self.plocka_apple, bg="#e91e63")
        self.knapp2.config(text="Åk med draken till Enhörningen 🦄", command=self.mot_enhorning, bg="#4caf50")

    def plocka_apple(self):
        if "Magiskt Äpple" not in self.ryggsack:
            self.ryggsack.append("Magiskt Äpple")
            messagebox.showinfo("🍏 Hittat!", "Du stoppade ett Magiskt Äpple i ryggsäcken!")
        else:
            messagebox.showinfo("Obs!", "Du har redan ett äpple.")
        self.uppdatera_status()
        self.visa_startstig()

    # --- PLATS 2: SKOGEN ---
    def visa_morka_skogen(self):
        self.knapp_sida.pack_forget()
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

    # --- PLATS 3: GROTTAN ---
    def visa_grottan(self):
        self.knapp_sida.pack_forget()
        tal1 = random.randint(2, 10)
        tal2 = random.randint(2, 9)
        self.matte_tal = (tal1, tal2)

        self.text_label.config(text=f"--- DEN DJUPA GROTTAN ---\n\nI grottans mörker möter du en gammal, snäll trollkarl. Han tänder sin stav och säger:\n'Om du kan lösa mitt magiska mattetal ska du få en karta!'\n\nVad är {tal1} + {tal2}?")
        
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
                    messagebox.showinfo("🗺️ Rätt svar!", "Trollkarlen trollar fram en Magisk Karta!")
                else:
                    messagebox.showinfo("Trollkarlen säger:", "Du har redan kartan!")
                self.uppdatera_status()
                self.visa_startstig()
            else:
                self.liv -= 1
                messagebox.showwarning("⚡ Fel svar", "Det sprakar till från staven! Du förlorar 1 liv.")
                self.uppdatera_status()
                if self.liv > 0:
                    self.visa_startstig()
        except ValueError:
            messagebox.showerror("Hoppsan", "Skriv svaret med siffror!")

    # 🌟 NY PLATS 4: DEN BLOMMIGA ÄNGEN (UPPGIFT 4)
    def visa_angen(self):
        self.knapp_sida.pack_forget()
        self.knapp3.pack_forget()
        self.text_label.config(text="--- DEN BLOMMIGA ÄNGEN ---\n\nEn stor drottninghumla har fastnat under ett löv. Hon surrar sorgset.\nHjälper du henne att lyfta bort det tunga lövet?")
        self.knapp1.config(text="Lyft bort lövet (Kräver styrka)", command=self.hjalp_humla, bg="#4caf50")
        self.knapp2.config(text="Gå tillbaka", command=self.visa_startstig, bg="#78909c")

    def hjalp_humla(self):
        # 50% chans att lyckas, annars blir man stucken
        if random.choice([True, False]):
            if "Kristallhonung" not in self.ryggsack:
                self.ryggsack.append("Kristallhonung")
                messagebox.showinfo("🐝 Tack!", "Humlan flyger fritt och belönar dig med söt Kristallhonung!")
            else:
                messagebox.showinfo("Humlan surrar:", "Tack igen för hjälpen!")
        else:
            self.liv -= 1
            messagebox.showwarning("🐝 Aj!", "Lövet glider och humlan råkar sticka dig i ren panik! Du förlorar 1 liv.")
        self.uppdatera_status()
        if self.liv > 0:
            self.visa_startstig()

    # 🌟 NY PLATS 5: SLOTTSruinen (UPPGIFT 5 - Sten, sax, påse)
    def visa_ruinen(self):
        self.knapp_sida.pack_forget()
        self.text_label.config(text="--- DEN GAMLA SLOTTSruinen ---\n\nEn levande stentataty vaktar ruinens skattkammare. \n'Slå mig i Sten-Sax-Påse så får du min skatt!'")
        self.knapp1.config(text="Välj 👊 STEN", command=lambda: self.spela_ssp("sten"), bg="#e57373")
        self.knapp2.config(text="Välj ✋ PÅSE", command=lambda: self.spela_ssp("påse"), bg="#fff176")
        self.knapp3.config(text="Välj ✌️ SAX", command=lambda: self.spela_ssp("sax"), bg="#64b5f6")

    def spela_ssp(self, spelar_val):
        dator_val = random.choice(["sten", "sax", "påse"])
        
        if spelar_val == dator_val:
            messagebox.showinfo("Oavgjort!", f"Statyn valde också {dator_val}. Försök igen!")
            return
            
        vinst = (spelar_val == "sten" and dator_val == "sax") or \
                (spelar_val == "påse" and dator_val == "sten") or \
                (spelar_val == "sax" and dator_val == "påse")
                
        if vinst:
            if "Gammalt Mynt" not in self.ryggsack:
                self.ryggsack.append("Gammalt Mynt")
                messagebox.showinfo("🪙 Du vann!", f"Statyn valde {dator_val}. Du vinner och får ett Gammalt Mynt!")
            else:
                messagebox.showinfo("Statyn säger:", "Du har redan mitt mynt.")
            self.uppdatera_status()
            self.visa_startstig()
        else:
            self.liv -= 1
            messagebox.showwarning("❌ Du förlorade", f"Statyn valde {dator_val} och krossade ditt drag! Du förlorar 1 liv.")
            self.uppdatera_status()
            if self.liv > 0:
                self.visa_startstig()

    # 🌟 NY PLATS 6: HÄXANS TRÄDGÅRD (UPPGIFT 6 - Ordpussel)
    def visa_haxans_tradgard(self):
        self.knapp_sida.pack_forget()
        self.text_label.config(text="--- HÄXANS TRÄDGÅRD ---\n\nHäxan kokar en trolldryck och flinar:\n'Kasta in rätt ingrediens i grytan så får du en flaska!'\n\nKasta in motsatsen till ordet 'KALL':")
        self.knapp1.pack_forget()
        self.knapp2.pack_forget()
        self.knapp3.pack_forget()
        
        self.svar_entry.delete(0, tk.END)
        self.svar_entry.pack(pady=10)
        self.svar_knapp.config(command=self.kolla_haxpussel)
        self.svar_knapp.pack(pady=5)

    def kolla_haxpussel(self):
        svar = self.svar_entry.get().lower().strip()
        if svar == "varm" or svar == "het":
            if "Häxbrygd" not in self.ryggsack:
                self.ryggsack.append("Häxbrygd")
                messagebox.showinfo("🧪 Perfekt!", "Grytan bubblar grönt och häxan ger dig en flaska Häxbrygd!")
            else:
                messagebox.showinfo("Häxan väser:", "Du har redan din brygd!")
            self.uppdatera_status()
            self.visa_startstig()
        else:
            self.liv -= 1
            messagebox.showwarning("❌ Fel ingrediens", "Grytan exploderar i ansiktet på dig! Du förlorar 1 liv.")
            self.uppdatera_status()
            if self.liv > 0:
                self.visa_startstig()

    # --- FINALEN ---
    def mot_enhorning(self):
        self.knapp_sida.pack_forget()
        self.text_label.config(text="--- ENHÖRNINGENS GLÄNTA ---\n\nDraken flyger dig till en magisk glänta. Där står den vackra guld-enhörningen låst bakom ett kraftfullt magiskt galler. Den behöver alla 6 magiska element för att bli fri!")
        self.knapp1.config(text="Rädda enhörningen med dina föremål", command=self.kolla_vinst, bg="#9c27b0")
        self.knapp2.config(text="Gå tillbaka till stigen", command=self.visa_startstig, bg="#78909c")

    def kolla_vinst(self):
        # Kolla om ALLA sex saker finns i ryggsäcken
        allafremal = all(sak in self.ryggsack for sak in self.mal_foremal)
        
        if allafremal:
            messagebox.showinfo("🦄 DU VANN SPELET!", "Wow! Med alla 6 föremål bryter du förtrollningen, öppnar gallret och räddar guld-enhörningen! Du är hela skogens sanna hjälte!")
            self.fraga_spela_igen()
        else:
            saknas = [sak for sak in self.mal_foremal if sak not in self.ryggsack]
            messagebox.showwarning(
                "🔒 Gallret är för starkt...", 
                f"Du har inte alla saker än!\n\n"
                f"Du saknar fortfarande: {', '.join(saknas)}"
            )

    def fraga_spela_igen(self):
        svar = messagebox.askyesno("Spela igen?", "Vill du spela en gång till?")
        if svar:
            self.liv = 3
            self.ryggsack = []
            self.stig_sida = 1
            self.uppdatera_status()
            self.visa_startstig()
        else:
            self.root.quit()

if __name__ == "__main__":
    fönster = tk.Tk()
    app = AgentyrsSpel(fönster)
    fönster.mainloop()