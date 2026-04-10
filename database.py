import sqlite3

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