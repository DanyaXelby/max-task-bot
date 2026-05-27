import sqlite3
from datetime import datetime

class TaskDatabase:
    def __init__(self, db_name="tasks.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    assignee TEXT NOT NULL,
                    deadline TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active'
                )
            ''')

    def add_task(self, title, description, assignee, deadline):
        with self.conn:
            self.conn.execute(
                'INSERT INTO tasks (title, description, assignee, deadline) VALUES (?, ?, ?, ?)',
                (title, description, assignee, deadline)
            )

    def get_tasks_by_assignee(self, assignee):
        cursor = self.conn.execute(
            'SELECT * FROM tasks WHERE assignee = ? AND status = "active"',
            (assignee,)
        )
        return cursor.fetchall()

    def get_overdue_tasks(self):
        now = datetime.now().isoformat()
        cursor = self.conn.execute(
            'SELECT * FROM tasks WHERE deadline < ? AND status = "active"',
            (now,)
        )
        return cursor.fetchall()

    def mark_task_completed(self, task_id):
        with self.conn:
            self.conn.execute(
                'UPDATE tasks SET status = "completed" WHERE id = ?',
                (task_id,)
            )