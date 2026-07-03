import time
import requests

#py -m pip install rich requests

from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from rich.align import Align

# =========================
# INSTÄLLNINGAR
# =========================

API_KEY = "5cf8099c0d5875905ddb54096d96efdb"

CITIES = ["Sundbyberg", "Sorunda"]

console = Console()

# =========================
# API-FUNKTION
# =========================

def get_weather(city):
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}"
        f"&appid={API_KEY}"
        "&units=metric"
        "&lang=sv"
    )

    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()


# =========================
# IKON
# =========================

def icon(desc):
    d = desc.lower()

    if "klar" in d:
        return "☀️"
    if "moln" in d:
        return "☁️"
    if "regn" in d:
        return "🌧️"
    if "snö" in d:
        return "❄️"
    if "åska" in d:
        return "⛈️"
    return "🌤️"


# =========================
# BYGG STAD-PANEL
# =========================

def city_panel(city):
    try:
        data = get_weather(city)

        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        table = Table(show_header=False, box=None)

        table.add_row("☁️ Väder", f"{icon(weather)} {weather}")
        table.add_row("🌡 Temperatur", f"{temp:.1f} °C")
        table.add_row("💧 Luftfukt", f"{humidity}%")
        table.add_row("💨 Vind", f"{wind} m/s")

        return Panel(
            table,
            title=f"📍 {city}",
            border_style="cyan"
        )

    except Exception as e:
        return Panel(
            f"[red]Fel vid hämtning:[/] {e}",
            title=f"📍 {city}",
            border_style="red"
        )


# =========================
# LAYOUT
# =========================

layout = Layout()

layout.split_column(
    Layout(name="header", size=3),
    Layout(name="body"),
    Layout(name="footer", size=3),
)

layout["body"].split_row(
    Layout(name="city1"),
    Layout(name="city2"),
)

# =========================
# HEADER & FOOTER
# =========================

def build_header():
    return Panel(
        Align.center("[bold cyan]🌍 LIVE WEATHER DASHBOARD[/bold cyan]"),
        border_style="cyan"
    )


def build_footer():
    now = time.strftime("%H:%M:%S")

    return Panel(
        Align.center(f"Senast uppdaterad: {now} | Uppdaterar varje 60 sekunder"),
        border_style="green"
    )


# =========================
# LIVE LOOP
# =========================

def build():
    layout["header"].update(build_header())

    layout["city1"].update(city_panel(CITIES[0]))
    layout["city2"].update(city_panel(CITIES[1]))
  

    layout["footer"].update(build_footer())

    return layout


with Live(build(), refresh_per_second=4, screen=True) as live:
    while True:
        live.update(build())
        time.sleep(60)