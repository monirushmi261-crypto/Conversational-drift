import sqlite3

def get_connection():
    return sqlite3.connect("memory.db", check_same_thread=False)


def store_fact(turn, entity, value):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO facts (turn, entity, value) VALUES (?, ?, ?)",
        (turn, entity, value)
    )

    conn.commit()
    conn.close()


def get_all_facts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM facts")
    rows = cursor.fetchall()

    conn.close()
    return rows


def clear_memory():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM facts")

    conn.commit()
    conn.close()
