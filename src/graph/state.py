from typing import TypedDict
from src.database.models import Candidate


class AgentState(TypedDict, total=False):
    company_name: str
    company_summary: str
    recent_news: list[str]
    required_skills: list[str]
    required_skill: str
    hiring_manager: dict
    candidate: Candidate | None
    generated_email: dict
    crm_id: int
    approved: bool
    status: str
    steps: int
    evaluation: bool
