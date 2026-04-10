from flask import Flask, render_template, request
from monitor import get_system_info, check_internet
from database import init_db, insert_log
from datetime import datetime

app = Flask(__name__)

external_data = {}

init_db()


@app.route("/")
def index():
    local_data = get_system_info()
    internet = check_internet()

    offline_hosts = []

    for host, info in external_data.items():
        last_seen = info["last_seen"]
        diff = (datetime.now() - last_seen).seconds

        if diff > 15:
            offline_hosts.append(host)
            
    return render_template(
        "index.html",
        data=local_data,
        internet=internet,
        external_data=external_data,
        offline_hosts=offline_hosts
    )

@app.route("/api/data", methods=["POST"])
def receive_data():
    data = request.json
    hostname = data["hostname"]

    external_data[hostname] = {
        "data": data,
        "last_seen": datetime.now()
    }

    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
