import psutil
import socket
import platform
import time
from datetime import timedelta

def get_system_info():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('C:\\')

    # Uptime
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    uptime = str(timedelta(seconds=int(uptime_seconds)))

    # Red - velocidad
    net1 = psutil.net_io_counters()
    time.sleep(1)
    net2 = psutil.net_io_counters()
    net_sent = round((net2.bytes_sent - net1.bytes_sent) / 1024, 2)
    net_recv = round((net2.bytes_recv - net1.bytes_recv) / 1024, 2)

    # Bateria
    battery = psutil.sensors_battery()
    if battery:
        battery_percent = round(battery.percent, 1)
        battery_charging = battery.power_plugged
    else:
        battery_percent = None
        battery_charging = None

    # Temperatura (no todos los sistemas lo soportan)
    try:
        temps = psutil.sensors_temperatures()
        cpu_temp = temps.get("coretemp") or temps.get("cpu_thermal") or None
        cpu_temp = round(cpu_temp[0].current, 1) if cpu_temp else None
    except:
        cpu_temp = None

    return {
        "cpu": cpu,
        "ram_percent": ram.percent,
        "ram_used": round(ram.used / (1024**3), 2),
        "ram_total": round(ram.total / (1024**3), 2),
        "disk_percent": disk.percent,
        "disk_used": round(disk.used / (1024**3), 2),
        "disk_total": round(disk.total / (1024**3), 2),
        "hostname": socket.gethostname(),
        "os": f"{platform.system()} {platform.release()}",
        "uptime": uptime,
        "net_sent": net_sent,
        "net_recv": net_recv,
        "battery_percent": battery_percent,
        "battery_charging": battery_charging,
        "cpu_temp": cpu_temp
    }

def check_internet():
    try:
        start = time.time()
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        latency = round((time.time() - start) * 1000, 1)
        return True, latency
    except:
        return False, None