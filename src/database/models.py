from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Candidate:
    id: int | None = None
    name: str = ""
    email: str = ""
    role: str = ""
    experience: int = 0
    skills: str = ""
    location: str = ""
    resume_summary: str = ""
    projects: str = ""
    created_at: datetime | None = None


@dataclass(slots=True)
class OutreachLog:
    id: int | None = None
    company: str = ""
    hiring_manager: str = ""
    manager_email: str = ""
    candidate_name: str = ""
    generated_email: str = ""
    status: str = ""
    created_at: datetime | None = None
