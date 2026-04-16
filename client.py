from dotenv import load_dotenv
import requests
import psutil
import socket
import platform
import time
import os
from datetime import timedelta

load_dotenv()

SERVER_URL = "http://192.168.0.188:5000"
USERNAME = os.getenv("MONITOR_USER")
PASSWORD = os.getenv("MONITOR_PASSWORD")

token = None

def login():
    global token
    try:
        r = requests.post(f"{SERVER_URL}/login", json={
            "username": USERNAME,
            "password": PASSWORD
        })
        if r.status_code == 200:
            token = r.json()["access_token"]
            print("Login exitoso")
        else:
            print("Login fallido:", r.text)
            token = None
    except Exception as e:
        print("Error al conectar con el servidor:", e)
        token = None

def get_data():
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('C:\\')

    boot_time = psutil.boot_time()
    uptime = str(timedelta(seconds=int(time.time() - boot_time)))

    net1 = psutil.net_io_counters()
    time.sleep(1)
    net2 = psutil.net_io_counters()
    net_sent = round((net2.bytes_sent - net1.bytes_sent) / 1024, 2)
    net_recv = round((net2.bytes_recv - net1.bytes_recv) / 1024, 2)

    battery = psutil.sensors_battery()

    return {
        "hostname": socket.gethostname(),
        "cpu": psutil.cpu_percent(interval=1),
        "ram_percent": ram.percent,
        "ram_used": round(ram.used / (1024**3), 2),
        "ram_total": round(ram.total / (1024**3), 2),
        "disk_percent": disk.percent,
        "disk_used": round(disk.used / (1024**3), 2),
        "disk_total": round(disk.total / (1024**3), 2),
        "os": f"{platform.system()} {platform.release()}",
        "uptime": uptime,
        "net_sent": net_sent,
        "net_recv": net_recv,
        "battery_percent": round(battery.percent, 1) if battery else None,
        "battery_charging": battery.power_plugged if battery else None,
    }

def send_data():
    global token
    data = get_data()
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(f"{SERVER_URL}/api/data", json=data, headers=headers)

    if r.status_code == 401:
        print(" Token expirado, renovando...")
        login()
        if token:
            headers = {"Authorization": f"Bearer {token}"}
            r = requests.post(f"{SERVER_URL}/api/data", json=data, headers=headers)

    print(f"Enviado | CPU: {data['cpu']}% RAM: {data['ram_percent']}% | Status: {r.status_code}")

# Login inicial
login()

try:
    while True:
        try:
            if token:
                send_data()
            else:
                print("Sin token, reintentando login...")
                login()
        except Exception as e:
            print("Error:", e)
        time.sleep(5)

except KeyboardInterrupt:
    print("\nCliente detenido correctamente")