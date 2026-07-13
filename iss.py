import sqlite3  # Kan användas om du vill spara historik senare
import tkinter as tk
from tkinter import ttk
import requests
import tkintermapview
#Funkar inte då den inte får kontakt med API

class IssTrackerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("ISS Live Tracker")
        self.root.geometry("900x650")

        # --- Layout ---
        # Övre panel för att visa textinformation
        self.info_frame = tk.Frame(root, bg="#1e1e2e", height=80)
        self.info_frame.pack(side=tk.TOP, fill=tk.X)
        self.info_frame.pack_propagate(False)

        # Huvudpanel för kartan
        self.map_frame = tk.Frame(root)
        self.map_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # --- Textetiketter (Labels) ---
        self.title_label = tk.Label(
            self.info_frame,
            text="Internationella Rymdstationen (ISS)",
            font=("Arial", 12, "bold"),
            bg="#1e1e2e",
            fg="white",
        )
        self.title_label.pack(anchor="w", padx=20, pady=(10, 2))

        self.coord_label = tk.Label(
            self.info_frame,
            text="Hämtar position...",
            font=("Arial", 10),
            bg="#1e1e2e",
            fg="#a6adc8",
        )
        self.coord_label.pack(anchor="w", padx=20)

        # --- Karta (TkinterMapView) ---
        # Vi skapar kartan och sätter startzoom till en global vy (nivå 2)
        self.map_widget = tkintermapview.TkinterMapView(
            self.map_frame, corner_radius=0
        )
        self.map_widget.pack(fill=tk.BOTH, expand=True)
        self.map_widget.set_zoom(2)

        # Variabel för att hålla koll på markören på kartan
        self.iss_marker = None

        # Flagga för att centrera kartan på ISS endast vid första hämtningen
        self.first_run = True

        # Starta loopen som uppdaterar positionen
        self.update_iss_position()

    def update_iss_position(self):
        """Hämtar ISS-position från API och uppdaterar kartan."""
        url = "http://api.opennotify.org/iss-now.json"

        try:
            # Gör ett nätverksanrop för att få JSON-data
            response = requests.get(url, timeout=4)
            data = response.json()

            # Extrahera latitud och longitud från svaret
            lat = float(data["iss_position"]["latitude"])
            lon = float(data["iss_position"]["longitude"])

            # Uppdatera texten i GUI:t
            self.coord_label.config(
                text=f"Position just nu: Latitud: {lat:.4f} | Longitud: {lon:.4f}"
            )

            # Om en markör redan finns på kartan, ta bort den gamla först
            if self.iss_marker:
                self.iss_marker.delete()

            # Sätt ut en ny markör (en röd plupp) där ISS befinner sig
            self.iss_marker = self.map_widget.set_marker(
                lat, lon, text="ISS", marker_color="red", text_color="black"
            )

            # Endast första gången appen startar flyttar vi kameran till ISS
            # (Användaren kan efter det skrolla fritt på kartan utan att bli avbruten)
            if self.first_run:
                self.map_widget.set_position(lat, lon)
                self.map_widget.set_zoom(3)
                self.first_run = False

        except Exception as e:
            # Om internet ligger nere eller API:et strular visas ett felmeddelande i texten
            self.coord_label.config(
                text="Kunde inte hämta ISS-position. Kontrollera internetanslutningen."
            )

        # root.after(millisekunder, funktion) gör att den här funktionen körs igen om 5 sekunder.
        # Detta skapar en evig loop utan att frysa gränssnittet.
        self.root.after(5000, self.update_iss_position)


if __name__ == "__main__":
    root = tk.Tk()
    app = IssTrackerApp(root)
    root.mainloop()