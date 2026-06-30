from mcp.server.fastmcp import FastMCP

from src.mcp.candidate_tools import (
    get_candidate,
    list_candidates,
    recommend_candidate,
    search_candidates_by_skill,
)

mcp = FastMCP("Candidate Database MCP Server")


@mcp.tool()
def list_all_candidates():
    """
    Return every candidate in the database.
    """
    return list_candidates()


@mcp.tool()
def search_candidates(skill: str):
    """
    Search candidates by skill.

    Args:
        skill: Skill such as Python, LangGraph, AWS
    """
    return search_candidates_by_skill(skill)


@mcp.tool()
def get_candidate_details(candidate_id: int):
    """
    Return detailed information for a candidate.
    """
    return get_candidate(candidate_id)


@mcp.tool()
def recommend_best_candidate(skill: str):
    """
    Recommend the best candidate based on experience.
    """
    return recommend_candidate(skill)


if __name__ == "__main__":
    mcp.run()
