from dataclasses import asdict

from src.database.db import (
    get_all_candidates,
    get_candidate_by_id,
    search_candidates,
)
from src.logging.logger import log_tool


@log_tool
def search_candidates_by_skill(skill: str) -> list[dict]:
    """
    Search candidates by skill.
    """

    candidates = search_candidates(skill)

    return [asdict(candidate) for candidate in candidates]


@log_tool
def get_candidate(candidate_id: int) -> dict:
    """
    Get candidate by ID.
    """

    candidate = get_candidate_by_id(candidate_id)

    if candidate is None:
        return {"error": "Candidate not found"}

    return asdict(candidate)


@log_tool
def list_candidates() -> list[dict]:
    """
    Return all candidates.
    """

    candidates = get_all_candidates()

    return [asdict(candidate) for candidate in candidates]


@log_tool
def recommend_candidate(skill: str) -> dict:
    """
    Return the highest experienced candidate matching the skill.
    """

    candidates = search_candidates(skill)

    if not candidates:
        return {"error": "No matching candidate found"}

    best = max(candidates, key=lambda candidate: candidate.experience)

    return asdict(best)


if __name__ == "__main__":
    print(list_candidates())

    print()

    print(search_candidates_by_skill("Python"))

    print()

    print(recommend_candidate("LangGraph"))
