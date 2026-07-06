import tkinter as tk
import requests
import threading
import time

# For start without console in background
# =========================
# INSTÄLLNINGAR
# =========================

API_KEY = "5cf8099c0d5875905ddb54096d96efdb"

CITIES = ["Rissne", "Sorunda", "Cypern", "Las Palmas"]

# =========================
# API
# =========================

def get_weather(city):
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric&lang=sv"
    )
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()

# =========================
# VÄDERTEXT
# =========================

def format_weather(data):
    desc = data["weather"][0]["description"].capitalize()
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]

    return f"{desc}\n🌡 {temp:.1f} °C\n💧 {humidity}%\n💨 {wind} m/s"

# =========================
# GUI
# =========================

root = tk.Tk()
root.title("Weather Dashboard")
root.geometry("800x500")
root.configure(bg="#1e1e1e")

frames = {}
labels = {}

# =========================
# SKAPA 2x2 GRID
# =========================

for i, city in enumerate(CITIES):
    frame = tk.Frame(root, bg="#2b2b2b", bd=2, relief="ridge")
    frame.grid(row=i//2, column=i%2, sticky="nsew", padx=10, pady=10)

    title = tk.Label(
        frame,
        text=city,
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#2b2b2b"
    )
    title.pack(pady=10)

    label = tk.Label(
        frame,
        text="Laddar...",
        font=("Arial", 14),
        fg="lightblue",
        bg="#2b2b2b",
        justify="left"
    )
    label.pack(pady=10)

    frames[city] = frame
    labels[city] = label

# =========================
# GRID RESIZE
# =========================

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# =========================
# UPPDATERA DATA
# =========================

def update_weather():
    while True:
        for city in CITIES:
            try:
                data = get_weather(city)
                text = format_weather(data)
                labels[city].config(text=text)
            except Exception as e:
                labels[city].config(text=f"Fel:\n{e}")

        time.sleep(60)

# =========================
# STARTA TRÅD
# =========================

thread = threading.Thread(target=update_weather, daemon=True)
thread.start()

# =========================
# STARTA APP
# =========================

root.mainloop()