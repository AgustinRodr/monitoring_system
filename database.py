import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def init_db():
    conn = sqlite3.connect("monitor.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpu REAL,
            ram REAL,
            disk REAL,
            internet INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def init_users():
    conn = sqlite3.connect("monitor.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()

    # Si no hay ningun usuario, crea uno por defecto
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    if count == 0:
        hashed_pw = generate_password_hash("admin123")
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", hashed_pw)
        )
        conn.commit()
        print("Usuario por defecto creado: admin / admin123")

    conn.close()

def add_user(username, password):
    conn = sqlite3.connect("monitor.db")
    cursor = conn.cursor()
    hashed_pw = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect("monitor.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def insert_log(cpu, ram, disk, internet):
    conn = sqlite3.connect("monitor.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO logs (cpu, ram, disk, internet)
        VALUES (?, ?, ?, ?)
    """, (cpu, ram, disk, internet))

    conn.commit()
    conn.close()

def get_logs(limit=20):
    conn = sqlite3.connect("monitor.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT cpu, ram, disk, timestamp 
        FROM logs 
        WHERE id IN (
            SELECT id FROM logs ORDER BY timestamp DESC LIMIT ?
        )
        ORDER BY timestamp ASC
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return rows