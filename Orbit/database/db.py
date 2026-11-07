import sqlite3
import os
import hashlib
import secrets
from pathlib import Path
from datetime import date

DATABASE_PATH = Path(__file__).resolve().parent / "orbit.db"

# ------------------------------------------------ database setup
#creates all tables used by Orbit and keeps the database beside this file so it can be moved with the project

def create_database():
    os.makedirs(DATABASE_PATH.parent, exist_ok=True)

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL COLLATE NOCASE UNIQUE,
            email TEXT NOT NULL COLLATE NOCASE UNIQUE,
            password_hash TEXT NOT NULL,
            password_salt TEXT NOT NULL,
            display_name TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")

        connection.execute("""CREATE TABLE IF NOT EXISTS settings (
            user_id INTEGER PRIMARY KEY,
            theme TEXT NOT NULL DEFAULT 'System',
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )""")

        connection.execute("""CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            due_date TEXT DEFAULT '',
            priority TEXT NOT NULL DEFAULT 'Medium',
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )""")

        connection.execute("""CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            event_date TEXT NOT NULL,
            event_time TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )""")

        connection.execute("""CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT 'Personal',
            content TEXT DEFAULT '',
            attachment_path TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )""")

        connection.execute("CREATE INDEX IF NOT EXISTS tasks_user_due_idx ON tasks(user_id, due_date)")
        connection.execute("CREATE INDEX IF NOT EXISTS events_user_date_idx ON events(user_id, event_date)")
        connection.execute("CREATE INDEX IF NOT EXISTS notes_user_category_idx ON notes(user_id, category)")
        connection.commit()

# ------------------------------------------------ account functions
#passwords are saved as salted hashes instead of plain text

def register_user(username, email, password):
    username = username.strip()
    email = email.strip().lower()
    if not username or not email or not password:
        return False, "Please fill in every field.", None
    if len(password) < 6:
        return False, "Password must contain at least 6 characters.", None
    if "@" not in email or "." not in email.split("@")[-1]:
        return False, "Enter a valid email address.", None

    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 200000).hex()

    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            cursor = connection.execute("INSERT INTO users(username,email,password_hash,password_salt,display_name) VALUES(?,?,?,?,?)",
                (username, email, password_hash, salt, username))
            user_id = cursor.lastrowid
            connection.execute("INSERT INTO settings(user_id,theme) VALUES(?,?)", (user_id, "System"))
            connection.commit()
            return True, "Account created successfully.", user_id
    except sqlite3.IntegrityError:
        return False, "That username or email is already registered.", None


def login_user(username_or_email, password):
    username_or_email = username_or_email.strip()
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.row_factory = sqlite3.Row
        user = connection.execute("SELECT * FROM users WHERE username = ? COLLATE NOCASE OR email = ? COLLATE NOCASE",
            (username_or_email, username_or_email)).fetchone()

    if user is None:
        return None

    password_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), user["password_salt"].encode("utf-8"), 200000).hex()
    if not secrets.compare_digest(password_hash, user["password_hash"]):
        return None

    return dict(user)


def get_user(user_id):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.row_factory = sqlite3.Row
        user = connection.execute("SELECT id,username,email,display_name,created_at FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(user) if user else None


def update_user_profile(user_id, display_name, email):
    display_name = display_name.strip()
    email = email.strip().lower()
    if not display_name or not email or "@" not in email or "." not in email.split("@")[-1]:
        return False, "Enter a display name and a valid email address."
    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute("UPDATE users SET display_name = ?, email = ? WHERE id = ?", (display_name, email, user_id))
            connection.commit()
        return True, "Profile updated successfully."
    except sqlite3.IntegrityError:
        return False, "That email address is already being used."


def change_user_password(user_id, old_password, new_password):
    if len(new_password) < 6:
        return False, "New password must contain at least 6 characters."
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.row_factory = sqlite3.Row
        user = connection.execute("SELECT password_hash,password_salt FROM users WHERE id = ?", (user_id,)).fetchone()
        if user is None:
            return False, "Account not found."
        old_hash = hashlib.pbkdf2_hmac("sha256", old_password.encode("utf-8"), user["password_salt"].encode("utf-8"), 200000).hex()
        if not secrets.compare_digest(old_hash, user["password_hash"]):
            return False, "Current password is incorrect."
        salt = secrets.token_hex(16)
        new_hash = hashlib.pbkdf2_hmac("sha256", new_password.encode("utf-8"), salt.encode("utf-8"), 200000).hex()
        connection.execute("UPDATE users SET password_hash = ?, password_salt = ? WHERE id = ?", (new_hash, salt, user_id))
        connection.commit()
    return True, "Password changed successfully."

# ------------------------------------------------ settings functions

def get_user_settings(user_id):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.row_factory = sqlite3.Row
        settings = connection.execute("SELECT * FROM settings WHERE user_id = ?", (user_id,)).fetchone()
        if settings:
            return dict(settings)
        connection.execute("INSERT OR IGNORE INTO settings(user_id,theme) VALUES(?,?)", (user_id, "System"))
        connection.commit()
        return {"user_id": user_id, "theme": "System"}


def update_user_settings(user_id, theme):
    if theme not in ["Light", "Dark", "System"]:
        return False
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("INSERT INTO settings(user_id,theme) VALUES(?,?) ON CONFLICT(user_id) DO UPDATE SET theme = excluded.theme",
            (user_id, theme))
        connection.commit()
    return True

# ------------------------------------------------ task functions

def add_task(user_id, title, description="", due_date="", priority="Medium"):
    title = title.strip()
    if not title:
        return False
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("INSERT INTO tasks(user_id,title,description,due_date,priority) VALUES(?,?,?,?,?)",
            (user_id, title, description.strip(), due_date.strip(), priority))
        connection.commit()
    return True


def get_tasks(user_id, status=None, limit=None):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.row_factory = sqlite3.Row
        if status:
            tasks = connection.execute("SELECT * FROM tasks WHERE user_id = ? AND status = ? ORDER BY CASE WHEN due_date = '' THEN 1 ELSE 0 END,due_date,created_at DESC",
                (user_id, status)).fetchall()
        else:
            tasks = connection.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY CASE WHEN due_date = '' THEN 1 ELSE 0 END,due_date,created_at DESC",
                (user_id,)).fetchall()
        if limit:
            tasks = tasks[:limit]
        return [dict(task) for task in tasks]


def update_task(task_id, user_id, title, description, due_date, priority):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("UPDATE tasks SET title = ?,description = ?,due_date = ?,priority = ? WHERE id = ? AND user_id = ?",
            (title.strip(), description.strip(), due_date.strip(), priority, task_id, user_id))
        connection.commit()
    return True


def update_task_status(task_id, user_id, status):
    if status not in ["Pending", "Completed"]:
        return False
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?", (status, task_id, user_id))
        connection.commit()
    return True


def delete_task(task_id, user_id):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        connection.commit()
    return True


def get_task_counts(user_id):
    today = date.today().isoformat()
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        total = connection.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND status = 'Pending'", (user_id,)).fetchone()[0]
        completed = connection.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND status = 'Completed'", (user_id,)).fetchone()[0]
        overdue = connection.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND status = 'Pending' AND due_date != '' AND due_date < ?",
            (user_id, today)).fetchone()[0]
    return {"pending": total, "completed": completed, "overdue": overdue}

# ------------------------------------------------ calendar event functions

def add_event(user_id, title, description, event_date, event_time=""):
    title = title.strip()
    if not title or not event_date:
        return False
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("INSERT INTO events(user_id,title,description,event_date,event_time) VALUES(?,?,?,?,?)",
            (user_id, title, description.strip(), event_date, event_time.strip()))
        connection.commit()
    return True


def get_events(user_id, start_date=None, end_date=None, limit=None):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.row_factory = sqlite3.Row
        if start_date and end_date:
            events = connection.execute("SELECT * FROM events WHERE user_id = ? AND event_date BETWEEN ? AND ? ORDER BY event_date,event_time",
                (user_id, start_date, end_date)).fetchall()
        else:
            events = connection.execute("SELECT * FROM events WHERE user_id = ? ORDER BY event_date,event_time", (user_id,)).fetchall()
        if limit:
            events = events[:limit]
        return [dict(event) for event in events]


def update_event(event_id, user_id, title, description, event_date, event_time=""):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("UPDATE events SET title = ?,description = ?,event_date = ?,event_time = ? WHERE id = ? AND user_id = ?",
            (title.strip(), description.strip(), event_date, event_time.strip(), event_id, user_id))
        connection.commit()
    return True


def delete_event(event_id, user_id):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("DELETE FROM events WHERE id = ? AND user_id = ?", (event_id, user_id))
        connection.commit()
    return True

# ------------------------------------------------ notes functions

def add_note(user_id, title, category="Personal", content="", attachment_path=""):
    title = title.strip() or "Untitled note"
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.execute("INSERT INTO notes(user_id,title,category,content,attachment_path) VALUES(?,?,?,?,?)",
            (user_id, title, category, content, attachment_path))
        connection.commit()
        return cursor.lastrowid


def get_notes(user_id, category=None, search_text=""):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.row_factory = sqlite3.Row
        if category and category != "All Notes":
            notes = connection.execute("SELECT * FROM notes WHERE user_id = ? AND category = ? AND (title LIKE ? OR content LIKE ?) ORDER BY updated_at DESC",
                (user_id, category, f"%{search_text}%", f"%{search_text}%")).fetchall()
        else:
            notes = connection.execute("SELECT * FROM notes WHERE user_id = ? AND (title LIKE ? OR content LIKE ?) ORDER BY updated_at DESC",
                (user_id, f"%{search_text}%", f"%{search_text}%")).fetchall()
        return [dict(note) for note in notes]


def update_note(note_id, user_id, title, category, content, attachment_path=""):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("UPDATE notes SET title = ?,category = ?,content = ?,attachment_path = ?,updated_at = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?",
            (title.strip() or "Untitled note", category, content, attachment_path, note_id, user_id))
        connection.commit()
    return True


def delete_note(note_id, user_id):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("DELETE FROM notes WHERE id = ? AND user_id = ?", (note_id, user_id))
        connection.commit()
    return True
