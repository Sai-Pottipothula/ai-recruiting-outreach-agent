import asyncio
import json
from src.database.models import Candidate
from src.graph.state import AgentState
from src.logging.logger import log_tool
from src.mcp.client import CandidateMCPClient
from src.tools.crm import save_outreach
from src.tools.email_generator import generate_outreach_email
from src.tools.hiring_manager import (
    choose_best_manager,
    extract_hiring_managers,
)
from src.tools.company_research import (
    extract_required_skills,
    get_company_summary,
    get_recent_company_news,
)


@log_tool
def research_company_node(state: AgentState) -> AgentState:
    """
    Research the target company and identify the most relevant technical skills.
    """
    state["company_summary"] = get_company_summary(state["company_name"])
    state["recent_news"] = get_recent_company_news(state["company_name"])
    state["required_skills"] = extract_required_skills(state["company_summary"])
    # Will be updated after a successful candidate match
    state["required_skill"] = ""
    state["steps"] += 1
    return state


@log_tool
def hiring_manager_node(state: AgentState) -> AgentState:
    """
    Find the best hiring manager.
    """
    managers = extract_hiring_managers(state["company_name"])
    state["hiring_manager"] = choose_best_manager(managers)
    state["steps"] += 1
    return state


@log_tool
def candidate_node(state: AgentState) -> AgentState:
    """
    Retrieve the best candidate from the MCP Server.
    Multiple required skills are tried until a matching candidate is found.
    """

    async def get_candidate(skill: str):
        client = CandidateMCPClient()

        try:
            await client.connect()

            return await client.call_tool(
                "recommend_best_candidate",
                {
                    "skill": skill,
                },
            )

        finally:
            await client.close()

    for skill in state["required_skills"]:
        try:
            response = asyncio.run(get_candidate(skill))

            if not response.content or not response.content[0].text:
                continue

            candidate_json = json.loads(response.content[0].text)

        except json.JSONDecodeError:
            state["status"] = "FAILED"
            state["error"] = "Invalid response received from the MCP server."
            state["steps"] += 1

            return state

        except Exception as e:
            state["status"] = "FAILED"
            state["error"] = f"MCP server error: {e}"
            state["steps"] += 1

            return state

        if "error" in candidate_json:
            continue

        candidate = Candidate(
            id=candidate_json["id"],
            name=candidate_json["name"],
            email=candidate_json["email"],
            role=candidate_json["role"],
            experience=candidate_json["experience"],
            skills=candidate_json["skills"],
            location=candidate_json["location"],
            resume_summary=candidate_json["resume_summary"],
            projects=candidate_json["projects"],
        )

        state["candidate"] = candidate
        state["required_skill"] = skill
        state["steps"] += 1

        return state

    state["candidate"] = None
    state["status"] = "NO_CANDIDATE_FOUND"
    state["steps"] += 1

    return state


@log_tool
def email_node(state: AgentState) -> AgentState:
    """
    Generate a personalized outreach email.
    """

    candidate: Candidate = state["candidate"]

    email = generate_outreach_email(
        company=state["company_name"],
        hiring_manager=state["hiring_manager"],
        candidate=candidate,
        company_summary=state["company_summary"],
        recent_news=state["recent_news"],
    )

    state["generated_email"] = email

    state["steps"] += 1

    return state


@log_tool
def approval_node(state: AgentState) -> AgentState:
    """
    Human approval checkpoint.
    """

    # Skip manual approval during evaluation
    if state.get("evaluation", False):
        state["approved"] = True
        state["steps"] += 1

        return state

    print("\n")
    print("=" * 80)
    print("GENERATED EMAIL")
    print("=" * 80)

    print("\nSubject:")
    print(state["generated_email"]["subject"])

    print()

    print(state["generated_email"]["body"])

    print("\n")
    print("Approve Email?")
    print("[1] Yes")
    print("[2] No")

    choice = input("\nChoice: ").strip().lower()

    state["approved"] = choice in (
        "1",
        "y",
        "yes",
    )

    state["steps"] += 1

    return state


@log_tool
def crm_node(state: AgentState) -> AgentState:
    """
    Save the approved outreach email to the CRM.
    """

    crm_id = save_outreach(
        company=state["company_name"],
        hiring_manager=state["hiring_manager"],
        candidate=state["candidate"],
        email=state["generated_email"],
        status="APPROVED" if state["approved"] else "REJECTED",
    )

    state["crm_id"] = crm_id

    state["steps"] += 1

    return state


@log_tool
def finish_node(state: AgentState) -> AgentState:
    """
    Mark the workflow as successfully completed.
    """

    state["status"] = "SUCCESS"

    return state
