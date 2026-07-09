import tkinter as tk
from tkinter import ttk
import platform
import socket
import psutil
import subprocess

def get_system_info():
    info = {
        "Datornamn": socket.gethostname(),
        "Operativsystem": f"{platform.system()} {platform.release()}",
        "Version": platform.version(),
        "Processor": platform.processor(),
        "Arkitektur": platform.machine(),
        "Python-version": platform.python_version(),
        "CPU-kärnor (fysiska)": psutil.cpu_count(logical=False),
        "CPU-kärnor (logiska)": psutil.cpu_count(logical=True),
        "CPU-användning": f"{psutil.cpu_percent(interval=1)} %",
    }

    memory = psutil.virtual_memory()
    info["RAM totalt"] = f"{memory.total / (1024**3):.2f} GB"
    info["RAM används"] = f"{memory.used / (1024**3):.2f} GB"
    info["RAM ledigt"] = f"{memory.available / (1024**3):.2f} GB"

    disk = psutil.disk_usage("/")
    info["Disk totalt"] = f"{disk.total / (1024**3):.2f} GB"
    info["Disk används"] = f"{disk.used / (1024**3):.2f} GB"
    info["Disk ledigt"] = f"{disk.free / (1024**3):.2f} GB"

    info["GPU Effekt"] = get_gpu_power()
    info["CPU Temperatur"] = get_cpu_temperature()
#
    return info

def get_cpu_temperature():
    try:
        w = wmi.WMI(namespace="root\\LibreHardwareMonitor")

        for sensor in w.Sensor():
            if sensor.SensorType == "Temperature" and "CPU" in sensor.Name:
                return f"{sensor.Value:.1f} °C"

        return "Ej tillgänglig"

    except Exception:
        return "LibreHardwareMonitor körs inte"
    
def get_gpu_power():
    try:
        result = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=power.draw,power.limit",
                "--format=csv,noheader,nounits"
            ],
            encoding="utf-8"
        )

        values = result.strip().split(",")
        power_draw = values[0].strip()
        power_limit = values[1].strip()

        return f"{power_draw} W / {power_limit} W"

    except Exception:
        return "Ej tillgänglig"

def update_info():
    tree.delete(*tree.get_children())
    info = get_system_info()
    for key, value in info.items():
        tree.insert("", tk.END, values=(key, value))

root = tk.Tk()
root.title("Systeminformation")
root.geometry("700x600")

title = tk.Label(root, text="Systeminformation", font=("Arial", 16, "bold"))
title.pack(pady=10)

tree = ttk.Treeview(root, columns=("Namn", "Värde"), show="headings")
tree.heading("Namn", text="Information")
tree.heading("Värde", text="Värde")
tree.column("Namn", width=220)
tree.column("Värde", width=430)
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

refresh_btn = tk.Button(root, text="Uppdatera", command=update_info)
refresh_btn.pack(pady=10)

update_info()

root.mainloop()