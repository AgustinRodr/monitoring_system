import requests
import psutil
import socket
import time

SERVER_URL = "http://127.0.0.1:5000/api/data"

def get_data():
    return {
        "hostname": socket.gethostname(),
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent
    }

try:
    while True:
        try:
            data = get_data()
            requests.post(SERVER_URL, json=data)
            print("Enviado:", data)
        except Exception as e:
            print("Error:", e)

        time.sleep(5)

except KeyboardInterrupt:
    print("\nCliente detenido correctamente")