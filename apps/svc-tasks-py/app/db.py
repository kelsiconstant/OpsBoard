import os, uuid
import psycopg2
from contextlib import contextmanager


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/opsboard")

@contextmanager
def get_conn():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()

def insert_task(t):
    with get_conn as conn:
        cur = conn.cursor()
        tid = str(uuid.uuid4())
        cur.execute("""
            INSERT INTO tasks (id, project_id, title, status, assignee, due_date) 
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (tid, str(t.projectId), t.title, t.status, t.assignee, t.dueDate))
        conn.commit()
        return tid

def list_tasks(project_id=None):
    with get_conn() as conn:
        cur = conn.cursor()
        if project_id:
            cur.execute("SELECT id, project_id, title, status, assignee, due_date FROM tasks WHERE project_id=%s ORDER BY title", (str(project_id),))
        else:
            cur.execute("SELECT id, project_id, title, status, assignee, due_date FROM tasks ORDER BY title") 
        rows = cur.fetchall()
        return [
            {
                "id": r[0], "projectId": r[1], "title": r[2],
                "status": r[3], "assignee": r[4], "dueDate": r[5]
            } for r in rows
        ]