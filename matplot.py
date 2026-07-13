import sys
import tkinter as tk
from tkinter import ttk

# Matplotlib-moduler för att baka in grafer i Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

#Hjälp av AI
class Graph3DApp:

    def __init__(self, root):
        self.root = root
        self.root.title("3D Graf-generator")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")

        # --- Layout-uppdelning ---
        # Vänster panel för kontrollknappar
        self.control_frame = tk.Frame(root, bg="#e0e0e0", width=200)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.control_frame.pack_propagate(
            False
        )  # Förhindrar att ramen krymper ihop

        # Höger panel för själva 3D-grafen
        self.plot_frame = tk.Frame(root, bg="white")
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Skapa kontrollknappar ---
        self.label = tk.Label(
            self.control_frame,
            text="Välj graftyp:",
            font=("Arial", 12, "bold"),
            bg="#e0e0e0",
        )
        self.label.pack(pady=20)

        # Knappar för de olika 3D-funktionerna
        self.btn_surface = ttk.Button(
            self.control_frame,
            text="3D Ytgraf (Surface)",
            command=self.plot_surface,
        )
        self.btn_surface.pack(fill=tk.X, padx=10, pady=5)

        self.btn_line = ttk.Button(
            self.control_frame, text="3D Linje (Line Plot)", command=self.plot_line
        )
        self.btn_line.pack(fill=tk.X, padx=10, pady=5)

        self.btn_scatter = ttk.Button(
            self.control_frame,
            text="3D Punkter (Scatter)",
            command=self.plot_scatter,
        )
        self.btn_scatter.pack(fill=tk.X, padx=10, pady=5)

        # --- Initiera Matplotlib-figuren ---
        # Vi skapar en tom figur som vi senare ritar 3D-axlar på
        self.fig = Figure(figsize=(6, 5), dpi=100)

        # Skapa canvasen som gör att Matplotlib kan visas inuti Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Rita en startgraf så att fönstret inte är tomt vid öppning
        self.plot_surface()

    def clear_plot(self):
        """Rensar figuren inför en ny ritning."""
        self.fig.clear()

    def plot_surface(self):
        """Genererar en 3D-ytgraf (en klassisk 'matematisk hatt')."""
        self.clear_plot()

        # Lägg till ett 3D-koordinatsystem till figuren
        ax = self.fig.add_subplot(111, projection="3d")

        # Skapa 3D-data med NumPy
        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X**2 + Y**2)
        Z = np.sin(R)  # Sinusvåg som skapar krusningar

        # Rita ytan (plot_surface) med färgtemat 'viridis'
        surf = ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none")

        # Sätt titlar och etiketter
        ax.set_title("3D Ytgraf (Sinusvåg)")
        ax.set_xlabel("X-axel")
        ax.set_ylabel("Y-axel")
        ax.set_zlabel("Z-axel")

        # Uppdatera gränssnittet så grafen syns
        self.canvas.draw()

    def plot_line(self):
        """Genererar en 3D-linje (en helix/spiral)."""
        self.clear_plot()
        ax = self.fig.add_subplot(111, projection="3d")

        # Skapa data för en spiral som rör sig uppåt
        theta = np.linspace(-4 * np.pi, 4 * np.pi, 200)
        z = np.linspace(-2, 2, 200)
        r = z**2 + 1
        x = r * np.sin(theta)
        y = r * np.cos(theta)

        # Rita linjen i 3D
        ax.plot(x, y, z, label="3D Spiral", color="crimson", lw=2)

        ax.set_title("3D Linjegraf (Helix)")
        ax.set_xlabel("X-axel")
        ax.set_ylabel("Y-axel")
        ax.set_zlabel("Z-axel")

        self.canvas.draw()

    def plot_scatter(self):
        """Genererar ett 3D-punktdiagram med slumpmässig data."""
        self.clear_plot()
        ax = self.fig.add_subplot(111, projection="3d")

        # Generera 100 slumpmässiga punkter
        n = 100
        x = np.random.standard_normal(n)
        y = np.random.standard_normal(n)
        z = np.random.standard_normal(n)

        # Färga punkterna baserat på deras Z-värde
        scatter = ax.scatter(x, y, z, c=z, cmap="plasma", s=40)

        ax.set_title("Slumpmässigt 3D Punktdiagram")
        ax.set_xlabel("X-axel")
        ax.set_ylabel("Y-axel")
        ax.set_zlabel("Z-axel")

        self.canvas.draw()


# --- Starta GUI-applikationen ---
if __name__ == "__main__":
    root = tk.Tk()
    app = Graph3DApp(root)
    root.mainloop()