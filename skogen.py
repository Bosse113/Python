import os
import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random

class AgentyrsSpel:
    def __init__(self, root):
        self.root = root
        self.root.title("🌲 Den Magiska Skogen: Det Stora Äventyret 🌲")
        self.root.geometry("620x600")
        self.root.configure(bg="#e0f2f1")

        # Startvärden
        self.liv = 5  # Ökat till 5 liv eftersom det finns fler faror nu!
        self.ryggsack = []
        self.matte_tal = (0, 0)
        self.stig_sida = 1  # Sida 1 till 4 för stigar

        # Mål: Alla 12 föremål krävs nu!
        self.mal_foremal = [
            "Magiskt Äpple", "Guldnyckel", "Magisk Karta", 
            "Kristallhonung", "Gammalt Mynt", "Häxbrygd",
            "Vindens Fjäder", "Sjörövarguld", "Lysande Lykta",
            "Älvstoft", "Magisk Brosten", "Gammal Bok"
        ]

        # Textruta för äventyret
        self.text_label = tk.Label(
            root, 
            text="Välkommen till Den Magiska Skogen!\n\nUppdrag: Samla ALLA 12 föremål för att rädda guld-enhörningen!\nBläddra mellan stigarna med knapparna längst ner.", 
            font=("Helvetica", 11), 
            wraplength=520, 
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

        # Knappar för valen (3 stycken per stig-sida)
        self.knapp1 = tk.Button(root, text="Starta Äventyret", font=("Helvetica", 11), command=self.visa_startstig, width=42, bg="#4caf50", fg="white")
        self.knapp1.pack(pady=5)

        self.knapp2 = tk.Button(root, text="", font=("Helvetica", 11), command=None, width=42, bg="#2196f3", fg="white")
        self.knapp2.pack_forget()

        self.knapp3 = tk.Button(root, text="", font=("Helvetica", 11), command=None, width=42, bg="#9c27b0", fg="white")
        self.knapp3.pack_forget()

        # Navigeringsknappar för att bläddra stigar
        self.nav_frame = tk.Frame(root, bg="#e0f2f1")
        
        self.knapp_bakat = tk.Button(self.nav_frame, text="⬅️ Föregående stigar", font=("Helvetica", 10, "bold"), command=self.stig_bakat, bg="#ff5722", fg="white")
        self.knapp_framat = tk.Button(self.nav_frame, text="➡️ Fler stigar", font=("Helvetica", 10, "bold"), command=self.stig_framat, bg="#ff5722", fg="white")

        # Inputfält för text-svar
        self.svar_entry = tk.Entry(root, font=("Helvetica", 12), width=20)
        self.svar_knapp = tk.Button(root, text="Svara", font=("Helvetica", 12), command=None, bg="#ff9800", fg="white")

    def uppdatera_status(self):
        self.liv_label.config(text=f"❤️ Liv kvar: {self.liv}")
        
        if len(self.ryggsack) == 0:
            self.ryggsack_label.config(text="🎒 Ryggsäck: Tom (0/12)")
        else:
            saker = ", ".join(self.ryggsack)
            self.ryggsack_label.config(text=f"🎒 Ryggsäck ({len(self.ryggsack)}/12):\n{saker}")

        if self.liv <= 0:
            messagebox.showinfo("👻 Spel Slut!", "Slut på liv! Spelet är över den här gången.")
            self.fraga_spela_igen()

    def stig_framat(self):
        if self.stig_sida < 4:
            self.stig_sida += 1
            self.visa_startstig()

    def stig_bakat(self):
        if self.stig_sida > 1:
            self.stig_sida -= 1
            self.visa_startstig()

    def visa_startstig(self):
        self.svar_entry.pack_forget()
        self.svar_knapp.pack_forget()
        
        self.knapp1.pack(pady=5)
        self.knapp2.pack(pady=5)
        self.knapp3.pack(pady=5)
        
        self.nav_frame.pack(pady=15)
        self.knapp_bakat.pack(side=tk.LEFT, padx=5)
        self.knapp_framat.pack(side=tk.RIGHT, padx=5)

        # Hantera synlighet på bläddringsknappar
        self.knapp_bakat.config(state=tk.NORMAL if self.stig_sida > 1 else tk.DISABLED)
        self.knapp_framat.config(state=tk.NORMAL if self.stig_sida < 4 else tk.DISABLED)

        if self.stig_sida == 1:
            self.text_label.config(text="Vägskälet - Sida 1 av 4:\nVart vill du gå?")
            self.knapp1.config(text="1. VÄNSTER: Till den glittrande sjön", command=self.visa_sjon, bg="#00bcd4")
            self.knapp2.config(text="2. MITTEN: In i den mörka skogen", command=self.visa_morka_skogen, bg="#5d4037")
            self.knapp3.config(text="3. HÖGER: Till den djupa grottan", command=self.visa_grottan, bg="#78909c")
            
        elif self.stig_sida == 2:
            self.text_label.config(text="Vägskälet - Sida 2 av 4:\nVart vill du gå?")
            self.knapp1.config(text="4. ÄNGEN: Till den blommiga ängen", command=self.visa_angen, bg="#8bc34a")
            self.knapp2.config(text="5. RUINEN: Till den gamla slottsruinen", command=self.visa_ruinen, bg="#9e9e9e")
            self.knapp3.config(text="6. TRÄDGÅRDEN: Till häxans trädgård", command=self.visa_haxans_tradgard, bg="#e040fb")
            
        elif self.stig_sida == 3:
            self.text_label.config(text="Vägskälet - Sida 3 av 4:\nVart vill du gå?")
            self.knapp1.config(text="7. BERGSTOPPEN: Upp i de blåsiga bergen", command=self.visa_bergstoppen, bg="#009688")
            self.knapp2.config(text="8. SKEPPET: Dyk ner till det sjunkna skeppet", command=self.visa_skeppet, bg="#3f51b5")
            self.knapp3.config(text="9. LABYRINTEN: In i dimskogs-labyrinten", command=self.visa_labyrint, bg="#607d8b")
            
        elif self.stig_sida == 4:
            self.text_label.config(text="Vägskälet - Sida 4 av 4:\nVart vill du gå?")
            self.knapp1.config(text="10. ÄLVRINGEN: Besök den glittrande älvringen", command=self.visa_alvringen, bg="#e91e63")
            self.knapp2.config(text="11. JÄTTENS BRO: Gå till stenbron i norr", command=self.visa_jattens_bro, bg="#795548")
            self.knapp3.config(text="12. BIBLIOTEKET: Gå till det glömda biblioteket", command=self.visa_bibliotek, bg="#ff9800")

    # --- UPPGIFT 1: SJÖN ---
    def visa_sjon(self):
        self.nav_frame.pack_forget()
        self.knapp3.pack_forget()
        self.text_label.config(text="--- VID DEN GLITTRANDE SJÖN ---\n\nSjön glänser vackert. På stranden växer ett träd med glödande röda äpplen. En drake simmar lugnt i vattnet.")
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

    # --- UPPGIFT 2: SKOGEN ---
    def visa_morka_skogen(self):
        self.nav_frame.pack_forget()
        self.text_label.config(text="--- DEN MÖRKA SKOGEN ---\n\nEn talande ekorre sitter på en gren:\n'Svara rätt på min gåta så får du min skatt!'\n\nGåta: Vad blir blötare ju mer man torkar?")
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
                messagebox.showinfo("🔑 Rätt svar!", "Ekorren tjoar av lycka och ger dig en Guldnyckel!")
            else:
                messagebox.showinfo("Ekorren säger:", "Du har ju redan min nyckel!")
            self.uppdatera_status()
            self.visa_startstig()
        else:
            self.liv -= 1
            messagebox.showwarning("❌ Fel svar", "Ekorren kastar en kotte i pannan på dig! Du förlorar 1 liv.")
            self.uppdatera_status()
            if self.liv > 0:
                self.visa_startstig()

    # --- UPPGIFT 3: GROTTAN ---
    def visa_grottan(self):
        self.nav_frame.pack_forget()
        tal1 = random.randint(3, 12)
        tal2 = random.randint(3, 12)
        self.matte_tal = (tal1, tal2)

        self.text_label.config(text=f"--- DEN DJUPA GROTTAN ---\n\nI grottan möter du en gammal, snäll trollkarl. Han höjer sin glödande stav och säger:\n'Om du kan lösa min matteformel ska du få en karta!'\n\nVad är {tal1} + {tal2}?")
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
                    messagebox.showinfo("🗺️ Rätt svar!", "Trollkarlen ler och trollar fram en Magisk Karta!")
                else:
                    messagebox.showinfo("Trollkarlen säger:", "Du har redan min karta!")
                self.uppdatera_status()
                self.visa_startstig()
            else:
                self.liv -= 1
                messagebox.showwarning("⚡ Fel svar", "En liten blixt slår ner framför dina fötter! Du förlorar 1 liv.")
                self.uppdatera_status()
                if self.liv > 0:
                    self.visa_startstig()
        except ValueError:
            messagebox.showerror("Hoppsan", "Skriv svaret med siffror!")

    # --- UPPGIFT 4: ÄNGEN ---
    def visa_angen(self):
        self.nav_frame.pack_forget()
        self.knapp3.pack_forget()
        self.text_label.config(text="--- DEN BLOMMIGA ÄNGEN ---\n\nEn drottninghumla har fastnat under ett tungt löv. Hon surrar sorgset.\nHjälper du henne att lyfta bort det?")
        self.knapp1.config(text="Lyft bort lövet", command=self.hjalp_humla, bg="#4caf50")
        self.knapp2.config(text="Gå tillbaka", command=self.visa_startstig, bg="#78909c")

    def hjalp_humla(self):
        if random.choice([True, False]):
            if "Kristallhonung" not in self.ryggsack:
                self.ryggsack.append("Kristallhonung")
                messagebox.showinfo("🐝 Tack!", "Humlan blir jätteglad och ger dig söt Kristallhonung!")
            else:
                messagebox.showinfo("Humlan surrar:", "Du har redan fått min honung!")
        else:
            self.liv -= 1
            messagebox.showwarning("🐝 Aj!", "Lövet faller tillbaka och humlan råkar sticka dig! Du förlorar 1 liv.")
        self.uppdatera_status()
        if self.liv > 0:
            self.visa_startstig()

    # --- UPPGIFT 5: RUINEN ---
    def visa_ruinen(self):
        self.nav_frame.pack_forget()
        self.text_label.config(text="--- DEN GAMLA SLOTTSruinen ---\n\nEn stentataty vaktar skattkammaren. \n'Slå mig i Sten-Sax-Påse så får du min skatt!'")
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
                messagebox.showinfo("🪙 Du vann!", f"Statyn valde {dator_val}. Du vinner ett Gammalt Mynt!")
            else:
                messagebox.showinfo("Statyn säger:", "Du har redan fått mitt mynt.")
            self.uppdatera_status()
            self.visa_startstig()
        else:
            self.liv -= 1
            messagebox.showwarning("❌ Du förlorade", f"Statyn valde {dator_val}! Du förlorar 1 liv.")
            self.uppdatera_status()
            if self.liv > 0:
                self.visa_startstig()

    # --- UPPGIFT 6: HÄXANS TRÄDGÅRD ---
    def visa_haxans_tradgard(self):
        self.nav_frame.pack_forget()
        self.text_label.config(text="--- HÄXANS TRÄDGÅRD ---\n\nHäxan rör om i sin kittel och väser:\n'Kasta in rätt motsatsord i min gryta!'\n\nVad är motsatsen till ordet 'KALL'?")
        self.knapp1.pack_forget()
        self.knapp2.pack_forget()
        self.knapp3.pack_forget()
        
        self.svar_entry.delete(0, tk.END)
        self.svar_entry.pack(pady=10)
        self.svar_knapp.config(command=self.kolla_haxpussel)
        self.svar_knapp.pack(pady=5)

    def kolla_haxpussel(self):
        svar = self.svar_entry.get().lower().strip()
        if svar in ["varm", "het"]:
            if "Häxbrygd" not in self.ryggsack:
                self.ryggsack.append("Häxbrygd")
                messagebox.showinfo("🧪 Perfekt!", "Grytan bubblar mysigt och du får en flaska grön Häxbrygd!")
            else:
                messagebox.showinfo("Häxan väser:", "Du har redan din flaska!")
            self.uppdatera_status()
            self.visa_startstig()
        else:
            self.liv -= 1
            messagebox.showwarning("❌ Hoppsan!", "Grytan ryker surt! Du förlorar 1 liv.")
            self.uppdatera_status()
            if self.liv > 0:
                self.visa_startstig()

    # 🌟 NY UPPGIFT 7: BERGSTOPPEN (Gåta)
    def visa_bergstoppen(self):
        self.nav_frame.pack_forget()
        self.text_label.config(text="--- DE BLÅSIGA BERGEN ---\n\nPå bergstoppen visslar vinden en gåta till dig:\n'Jag har inga vingar men jag kan flyga. Jag har inga ögon men jag kan gråta. Vad är jag?'")
        self.knapp1.pack_forget()
        self.knapp2.pack_forget()
        self.knapp3.pack_forget()
        
        self.svar_entry.delete(0, tk.END)
        self.svar_entry.pack(pady=10)
        self.svar_knapp.config(command=self.kolla_vinds_gata)
        self.svar_knapp.pack(pady=5)

    def kolla_vinds_gata(self):
        svar = self.svar_entry.get().lower().strip()
        if "moln" in svar:
            if "Vindens Fjäder" not in self.ryggsack:
                self.ryggsack.append("Vindens Fjäder")
                messagebox.showinfo("🪶 Rätt svar!", "Vinden blåser ner en vacker och lätt 'Vindens Fjäder' till dig!")
            else:
                messagebox.showinfo("Vinden viskar:", "Du bär redan min fjäder.")
            self.uppdatera_status()
            self.visa_startstig()
        else:
            self.liv -= 1
            messagebox.showwarning("💨 Kall vind", "En kraftig stormvind blåser omkull dig! Du förlorar 1 liv.")
            self.uppdatera_status()
            if self.liv > 0:
                self.visa_startstig()

    # 🌟 NY UPPGIFT 8: SJUNKNA SKEPPET (Matte - Subtraktion)
    def visa_skeppet(self):
        self.nav_frame.pack_forget()
        tal1 = random.randint(15, 30)
        tal2 = random.randint(5, 14)
        self.matte_tal = (tal1, tal2)

        self.text_label.config(text=f"--- DET SJUNKNA SKEPPET ---\n\nDu dyker ner till vraket och möter en vaktande bläckfisk:\n'Svara på mitt mattetal för att få öppna skattkistan!'\n\nVad är {tal1} - {tal2}?")
        self.knapp1.pack_forget()
        self.knapp2.pack_forget()
        self.knapp3.pack_forget()
        
        self.svar_entry.delete(0, tk.END)
        self.svar_entry.pack(pady=10)
        self.svar_knapp.config(command=self.kolla_subtraktion)
        self.svar_knapp.pack(pady=5)

    def kolla_subtraktion(self):
        try:
            svar = int(self.svar_entry.get())
            ratt_svar = self.matte_tal[0] - self.matte_tal[1]
            if svar == ratt_svar:
                if "Sjörövarguld" not in self.ryggsack:
                    self.ryggsack.append("Sjörövarguld")
                    messagebox.showinfo("🪙 Guld!", "Kistan öppnas och du plockar upp glänsande Sjörövarguld!")
                else:
                    messagebox.showinfo("Bläckfisken bubblar:", "Du har redan tömt kistan!")
                self.uppdatera_status()
                self.visa_startstig()
            else:
                self.liv -= 1
                messagebox.showwarning("🦑 Bläck", "Bläckfisken sprutar svart bläck på dig! Du förlorar 1 liv.")
                self.uppdatera_status()
                if self.liv > 0:
                    self.visa_startstig()
        except ValueError:
            messagebox.showerror("Hoppsan", "Skriv ditt svar med siffror!")

    # 🌟 NY UPPGIFT 9: DIMSPEL (Slump / Val)
    def visa_labyrint(self):
        self.nav_frame.pack_forget()
        self.knapp3.pack_forget()
        self.text_label.config(text="--- DIMSKOGS-LABYRINTEN ---\n\nDimman ligger tät. Du hör ett svagt ljud.\nVilken väg väljer du för att hitta ut?")
        self.knapp1.config(text="Gå mot det mystiska ljuset", command=lambda: self.valj_labyrint_vag(True), bg="#e0f7fa")
        self.knapp2.config(text="Följ det porlande ljudet", command=lambda: self.valj_labyrint_vag(False), bg="#80deea")

    def valj_labyrint_vag(self, ljus_val):
        # 50% chans att välja rätt väg
        ratt_vag = random.choice([True, False])
        if ljus_val == ratt_vag:
            if "Lysande Lykta" not in self.ryggsack:
                self.ryggsack.append("Lysande Lykta")
                messagebox.showinfo("🔦 Hittat ut!", "Du hittar en vacker gammal Lysande Lykta som visar vägen!")
            else:
                messagebox.showinfo("Info", "Du hittade ut lätt eftersom du redan har lyktan!")
            self.uppdatera_status()
            self.visa_startstig()
        else:
            self.liv -= 1
            messagebox.showwarning("🌪️ Vilsen!", "Du går vilse i dimman och snubblar på en rot! Du förlorar 1 liv.")
            self.uppdatera_status()
            if self.liv > 0:
                self.visa_startstig()

    # 🌟 NY UPPGIFT 10: ÄLVRINGEN (Färggissning)
    def visa_alvringen(self):
        self.nav_frame.pack_forget()
        self.text_label.config(text="--- DEN GLITTRANDE ÄLVRINGEN ---\n\nÄlvorna dansar i en ring. De lovar dig magiskt älvstoft om du kan gissa vilken färg deras drottning tänker på!")
        self.knapp1.config(text="Gissa på ROSA", command=lambda: self.gissa_farg("rosa"), bg="#ec407a")
        self.knapp2.config(text="Gissa på BLÅ", command=lambda: self.gissa_farg("blå"), bg="#42a5f5")
        self.knapp3.config(text="Gissa på GRÖN", command=lambda: self.gissa_farg("grön"), bg="#66bb6a")

    def gissa_farg(self, farg_val):
        ratt_farg = random.choice(["rosa", "blå", "grön"])
        if farg_val == ratt_farg:
            if "Älvstoft" not in self.ryggsack:
                self.ryggsack.append("Älvstoft")
                messagebox.showinfo("✨ Magi!", f"Helt rätt! Drottningen tänkte på {ratt_farg}. Älvorna ger dig glittrande Älvstoft!")
            else:
                messagebox.showinfo("Älvorna skrattar:", "Du har redan älvstoft i fickan!")
            self.uppdatera_status()
            self.visa_startstig()
        else:
            self.liv -= 1
            messagebox.showwarning("✨ Kittlande magi", f"Fel gissat! Drottningen tänkte på {ratt_farg}. Älvorna kittlar dig tills du tappar balansen! Du förlorar 1 liv.")
            self.uppdatera_status()
            if self.liv > 0:
                self.visa_startstig()

    # 🌟 NY UPPGIFT 11: JÄTTENS BRO (Matte - Multiplikation)
    def visa_jattens_bro(self):
        self.nav_frame.pack_forget()
        tal1 = random.randint(2, 5)
        tal2 = random.randint(3, 6)
        self.matte_tal = (tal1, tal2)

        self.text_label.config(text=f"--- JÄTTENS STENBRO ---\n\nEn enorm stentroll-jätte blockerar bron:\n'Ingen slipper över utan att lösa min multiplikations-gåta!'\n\nVad är {tal1} * {tal2}?")
        self.knapp1.pack_forget()
        self.knapp2.pack_forget()
        self.knapp3.pack_forget()
        
        self.svar_entry.delete(0, tk.END)
        self.svar_entry.pack(pady=10)
        self.svar_knapp.config(command=self.kolla_multiplikation)
        self.svar_knapp.pack(pady=5)

    def kolla_multiplikation(self):
        try:
            svar = int(self.svar_entry.get())
            ratt_svar = self.matte_tal[0] * self.matte_tal[1]
            if svar == ratt_svar:
                if "Magisk Brosten" not in self.ryggsack:
                    self.ryggsack.append("Magisk Brosten")
                    messagebox.showinfo("🪨 Tackar!", "Jätten tar ett kliv åt sidan och ger dig en bit av bron - en Magisk Brosten!")
                else:
                    messagebox.showinfo("Jätten mullrar:", "Gå över du bara, du har redan min sten!")
                self.uppdatera_status()
                self.visa_startstig()
            else:
                self.liv -= 1
                messagebox.showwarning("💥 Jättesteg", "Jätten trampar hårt i marken så du flyger bakåt! Du förlorar 1 liv.")
                self.uppdatera_status()
                if self.liv > 0:
                    self.visa_startstig()
        except ValueError:
            messagebox.showerror("Hoppsan", "Skriv svaret i siffror!")

    # 🌟 NY UPPGIFT 12: GLÖMDA BIBLIOTEKET (Ord-anagram)
    def visa_bibliotek(self):
        self.nav_frame.pack_forget()
        self.text_label.config(text="--- DET GLÖMDA BIBLIOTEKET ---\n\nEn magisk svävande bok talar till dig:\n'Lås upp min kunskap genom att kasta om bokstäverna till ett riktigt ord!'\n\nOrdpussel: Vad blir ordet 'O K B'?")
        self.knapp1.pack_forget()
        self.knapp2.pack_forget()
        self.knapp3.pack_forget()
        
        self.svar_entry.delete(0, tk.END)
        self.svar_entry.pack(pady=10)
        self.svar_knapp.config(command=self.kolla_ordpussel)
        self.svar_knapp.pack(pady=5)

    def kolla_ordpussel(self):
        svar = self.svar_entry.get().lower().strip()
        if svar == "bok":
            if "Gammal Bok" not in self.ryggsack:
                self.ryggsack.append("Gammal Bok")
                messagebox.showinfo("📖 Öppnad!", "Boken slår upp sig själv och flyger ner i din ryggsäck!")
            else:
                messagebox.showinfo("Boken viskar:", "Du bär redan på min visdom.")
            self.uppdatera_status()
            self.visa_startstig()
        else:
            self.liv -= 1
            messagebox.showwarning("📕 Stängd!", "Boken smäller igen precis framför din näsa! Du förlorar 1 liv.")
            self.uppdatera_status()
            if self.liv > 0:
                self.visa_startstig()

    # --- FINALEN ---
    def mot_enhorning(self):
        self.nav_frame.pack_forget()
        self.text_label.config(text="--- ENHÖRNINGENS GLÄNTA ---\n\nDraken landar säkert i den gömda gläntan. Den vackra guld-enhörningen står bunden vid altaret. Det krävs ALLA 12 magiska föremål för att bryta låset!")
        self.knapp1.config(text="Försök frigöra enhörningen", command=self.kolla_vinst, bg="#9c27b0")
        self.knapp2.config(text="Gå tillbaka till stigen", command=self.visa_startstig, bg="#78909c")

    def kolla_vinst(self):
        allafremal = all(sak in self.ryggsack for sak in self.mal_foremal)
        
        if allafremal:
            messagebox.showinfo("🦄 DU VANN DET STORA ÄVENTYRET!", "Fantastiskt! Med alla 12 magiska föremål skapas en kraftfull ljusvåg. Gallret sprängs och guld-enhörningen är äntligen fri!\n\nDu har räddat hela Den Magiska Skogen!")
            self.fraga_spela_igen()
        else:
            saknas = [sak for sak in self.mal_foremal if sak not in self.ryggsack]
            messagebox.showwarning(
                "🔒 Magin räcker inte till...", 
                f"Du har inte alla 12 saker än!\n\n"
                f"Du saknar fortfarande {len(saknas)} föremål:\n{', '.join(saknas)}"
            )

    def fraga_spela_igen(self):
        svar = messagebox.askyesno("Spela igen?", "Vill du starta ett nytt äventyr?")
        if svar:
            self.liv = 5
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