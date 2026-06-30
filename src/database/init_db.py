import sqlite3
from utils.config import CANDIDATE_DB, CRM_DB


def create_candidates_table() -> None:
    conn = sqlite3.connect(CANDIDATE_DB)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL,
            experience INTEGER NOT NULL,
            skills TEXT NOT NULL,
            location TEXT NOT NULL,
            resume_summary TEXT NOT NULL,
            projects TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()
    conn.close()


def create_crm_table() -> None:
    conn = sqlite3.connect(CRM_DB)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS outreach_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            hiring_manager TEXT NOT NULL,
            manager_email TEXT,
            candidate_name TEXT NOT NULL,
            generated_email TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()
    conn.close()


def initialize_database() -> None:
    create_candidates_table()
    create_crm_table()
    print("Databases initialized successfully.")


if __name__ == "__main__":
    initialize_database()
