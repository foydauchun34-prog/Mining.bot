import sqlite3
from datetime import datetime, timedelta

DB_NAME = "bot.db"


def connect():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            balance REAL DEFAULT 0,
            is_banned INTEGER DEFAULT 0,
            is_vip INTEGER DEFAULT 0,
            referral_id INTEGER,
            mining_started_at TEXT,
            mining_ends_at TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def add_user(user_id, username, first_name, referral_id=None):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (id, username, first_name, referral_id)
        VALUES (?, ?, ?, ?)
    """, (user_id, username, first_name, referral_id))

    conn.commit()
    conn.close()


def get_user(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    )

    result = cursor.fetchone()
    conn.close()

    return result


def start_mining(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT mining_ends_at
        FROM users
        WHERE id = ?
    """, (user_id,))

    row = cursor.fetchone()

    if not row:
        conn.close()
        return False, "Foydalanuvchi topilmadi."

    if row[0]:
        end_time = datetime.fromisoformat(row[0])

        if end_time > datetime.now():
            conn.close()
            return False, "Mining hali davom etmoqda."

    start_time = datetime.now()
    end_time = start_time + timedelta(hours=24)

    cursor.execute("""
        UPDATE users
        SET mining_started_at = ?,
            mining_ends_at = ?
        WHERE id = ?
    """, (
        start_time.isoformat(),
        end_time.isoformat(),
        user_id
    ))

    conn.commit()
    conn.close()

    return True, end_time


def get_mining_status(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT mining_started_at, mining_ends_at
        FROM users
        WHERE id = ?
    """, (user_id,))

    row = cursor.fetchone()
    conn.close()

    if not row or not row[1]:
        return None

    end_time = datetime.fromisoformat(row[1])

    if end_time <= datetime.now():
        return "finished"

    return {
        "started_at": row[0],
        "ends_at": row[1]
    }
