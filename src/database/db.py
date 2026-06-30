import sqlite3
from typing import List, Optional
from src.utils.config import CANDIDATE_DB, CRM_DB
from src.database.models import Candidate, OutreachLog


# Candidate Database
def _candidate_connection():
    return sqlite3.connect(CANDIDATE_DB)


def create_candidate(candidate: Candidate) -> int:
    conn = _candidate_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO candidates (
            name,
            email,
            role,
            experience,
            skills,
            location,
            resume_summary,
            projects
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            candidate.name,
            candidate.email,
            candidate.role,
            candidate.experience,
            candidate.skills,
            candidate.location,
            candidate.resume_summary,
            candidate.projects,
        ),
    )
    conn.commit()
    candidate_id = cursor.lastrowid
    conn.close()
    return candidate_id


def get_candidate_by_id(candidate_id: int) -> Optional[Candidate]:
    conn = _candidate_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM candidates WHERE id = ?",
        (candidate_id,),
    )
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    return Candidate(**dict(row))


def get_all_candidates() -> List[Candidate]:
    conn = _candidate_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates")
    rows = cursor.fetchall()
    conn.close()
    return [Candidate(**dict(row)) for row in rows]


def search_candidates(skill: str) -> List[Candidate]:
    conn = _candidate_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM candidates
        WHERE LOWER(skills) LIKE LOWER(?)
        ORDER BY experience DESC
        """,
        (f"%{skill}%",),
    )
    rows = cursor.fetchall()
    conn.close()
    return [Candidate(**dict(row)) for row in rows]


def update_candidate(candidate: Candidate) -> None:
    conn = _candidate_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE candidates
        SET
            name=?,
            email=?,
            role=?,
            experience=?,
            skills=?,
            location=?,
            resume_summary=?,
            projects=?
        WHERE id=?
        """,
        (
            candidate.name,
            candidate.email,
            candidate.role,
            candidate.experience,
            candidate.skills,
            candidate.location,
            candidate.resume_summary,
            candidate.projects,
            candidate.id,
        ),
    )
    conn.commit()
    conn.close()


def delete_candidate(candidate_id: int) -> None:
    conn = _candidate_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM candidates WHERE id=?",
        (candidate_id,),
    )
    conn.commit()
    conn.close()


# CRM Database
def _crm_connection():
    return sqlite3.connect(CRM_DB)


def log_outreach(log: OutreachLog) -> int:
    conn = _crm_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO outreach_logs (
            company,
            hiring_manager,
            manager_email,
            candidate_name,
            generated_email,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            log.company,
            log.hiring_manager,
            log.manager_email,
            log.candidate_name,
            log.generated_email,
            log.status,
        ),
    )
    conn.commit()
    log_id = cursor.lastrowid
    conn.close()
    return log_id


def get_outreach_logs() -> List[OutreachLog]:
    conn = _crm_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM outreach_logs
        ORDER BY created_at DESC
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return [OutreachLog(**dict(row)) for row in rows]
