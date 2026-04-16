from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,
    decode_token
)
from monitor import get_system_info, check_internet
from database import init_db, init_users, get_logs, get_user
from werkzeug.security import check_password_hash
from datetime import datetime
from database import insert_log, get_logs
from functools import wraps
import os

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"

jwt = JWTManager(app)

external_data = {}

init_db()
init_users()



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("access_token")
        if not token:
            return redirect(url_for("login_page"))
        try:
            decode_token(token)  
        except Exception:
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)
    return decorated_function



@app.route("/login_page")
def login_page():
    return render_template("login.html")



@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = get_user(username)

    if user and check_password_hash(user[2], password):
        token = create_access_token(identity=username)
        return jsonify(access_token=token)
    else:
        return jsonify({"msg": "Credenciales inválidas"}), 401




@app.route("/logout")
def logout():
    response = redirect(url_for("login_page"))
    response.delete_cookie("access_token")
    return response



@app.route("/")
def root():
    return redirect(url_for("login_page"))


@app.route("/performance")
@login_required
def performance():
    return jsonify(get_system_info())


@app.route("/dashboard")
@login_required
def dashboard():
    local_data = get_system_info()
    internet, latency = check_internet()

    
    insert_log(
        local_data["cpu"],
        local_data["ram_percent"],
        local_data["disk_percent"],
        1 if internet else 0
    )

    
    logs = get_logs(20)

    offline_hosts = []
    for host, info in external_data.items():
        last_seen = info["last_seen"]
        diff = (datetime.now() - last_seen).seconds
        if diff > 15:
            offline_hosts.append(host)

    return render_template(
        "index.html",
        local=local_data,
        internet=internet,
        latency=latency,
        external_data=external_data,
        offline_hosts=offline_hosts,
        logs=logs
    )




@app.route("/api/data", methods=["POST"])
@jwt_required()
def receive_data():
    data = request.json
    print("=== DATA RECIBIDA ===")
    print(data)
    print("====================")
    hostname = data["hostname"]

    external_data[hostname] = {
        "data": data,
        "last_seen": datetime.now()
    }

    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
