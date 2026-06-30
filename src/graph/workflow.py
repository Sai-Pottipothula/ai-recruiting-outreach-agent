from langgraph.graph import START, END, StateGraph

from src.utils.config import MAX_STEPS
from src.graph.nodes import (
    approval_node,
    candidate_node,
    crm_node,
    email_node,
    finish_node,
    hiring_manager_node,
    research_company_node,
)
from src.graph.state import AgentState


def should_generate_email(state: AgentState):
    """
    Continue only if a matching candidate was found.
    """

    if state["candidate"] is None:
        state["status"] = "NO_CANDIDATE_FOUND"
        return END

    return "email"


def should_continue(state: AgentState):
    """
    Decide whether the workflow should continue after
    the human approval checkpoint.
    """

    if state["steps"] >= MAX_STEPS:
        state["status"] = "MAX_STEPS"
        return END

    if not state["approved"]:
        state["status"] = "REJECTED"
        return END

    return "crm"


builder = StateGraph(AgentState)

# Nodes
builder.add_node("research", research_company_node)
builder.add_node("manager", hiring_manager_node)
builder.add_node("candidate", candidate_node)
builder.add_node("email", email_node)
builder.add_node("approval", approval_node)
builder.add_node("crm", crm_node)
builder.add_node("finish", finish_node)

# Workflow
builder.add_edge(START, "research")
builder.add_edge("research", "manager")
builder.add_edge("manager", "candidate")

builder.add_conditional_edges(
    "candidate",
    should_generate_email,
    {
        "email": "email",
        END: END,
    },
)

builder.add_edge("email", "approval")

builder.add_conditional_edges(
    "approval",
    should_continue,
    {
        "crm": "crm",
        END: END,
    },
)

builder.add_edge("crm", "finish")
builder.add_edge("finish", END)

graph = builder.compile()
