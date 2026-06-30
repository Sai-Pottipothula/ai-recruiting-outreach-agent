from src.database.db import get_outreach_logs, log_outreach
from src.database.models import Candidate, OutreachLog
from src.logging.logger import log_tool


@log_tool
def save_outreach(
    company: str,
    hiring_manager: dict,
    candidate: Candidate,
    email: dict,
    status: str = "PENDING",
) -> int:
    """
    Save an outreach email to the CRM.
    """

    record = OutreachLog(
        company=company,
        hiring_manager=hiring_manager.get("name", ""),
        manager_email=hiring_manager.get("email", ""),
        candidate_name=candidate.name,
        generated_email=email["body"],
        status=status,
    )

    return log_outreach(record)


@log_tool
def mark_as_sent(log_id: int) -> None:
    """
    Update an outreach record as SENT.
    """

    from utils.config import CRM_DB
    import sqlite3

    conn = sqlite3.connect(CRM_DB)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE outreach_logs
        SET status='SENT'
        WHERE id=?
        """,
        (log_id,),
    )

    conn.commit()
    conn.close()


@log_tool
def mark_as_rejected(log_id: int) -> None:
    """
    Update an outreach record as REJECTED.
    """

    from utils.config import CRM_DB
    import sqlite3

    conn = sqlite3.connect(CRM_DB)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE outreach_logs
        SET status='REJECTED'
        WHERE id=?
        """,
        (log_id,),
    )

    conn.commit()
    conn.close()


@log_tool
def list_outreach_logs():
    """
    Return all CRM records.
    """

    return get_outreach_logs()


@log_tool
def print_crm():
    """
    Pretty-print CRM records.
    """

    logs = list_outreach_logs()

    print("\n" + "=" * 100)

    for log in logs:
        print(f"ID         : {log.id}")
        print(f"Company    : {log.company}")
        print(f"Manager    : {log.hiring_manager}")
        print(f"Candidate  : {log.candidate_name}")
        print(f"Status     : {log.status}")
        print(f"Created At : {log.created_at}")

        print("-" * 100)


if __name__ == "__main__":
    candidate = Candidate(
        name="Emily Davis",
        email="emily@example.com",
        role="AI Engineer",
    )

    manager = {
        "name": "Jane Doe",
        "email": "jane@stripe.com",
    }

    email = {
        "subject": "Outstanding AI Engineer",
        "body": "Hi Jane,\n\nI'd like to introduce Emily...",
    }

    crm_id = save_outreach(
        company="Stripe",
        hiring_manager=manager,
        candidate=candidate,
        email=email,
    )

    print(f"Saved CRM Record: {crm_id}")

    print_crm()
