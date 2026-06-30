import json

from openai import OpenAI

from src.utils.config import MODEL_NAME, OPENAI_API_KEY
from src.database.models import Candidate
from src.logging.logger import log_tool
from src.utils.prompts import (
    EMAIL_IMPROVE_SYSTEM_PROMPT,
    EMAIL_SYSTEM_PROMPT,
    build_email_prompt,
    build_improve_email_prompt,
)

client = OpenAI(api_key=OPENAI_API_KEY)


@log_tool
def generate_outreach_email(
    company: str,
    hiring_manager: dict,
    candidate: Candidate,
    company_summary: str,
    recent_news: list[str],
) -> dict:
    """
    Generate a personalized outreach email.
    """

    prompt = build_email_prompt(
        company=company,
        hiring_manager=hiring_manager,
        candidate=candidate,
        company_summary=company_summary,
        recent_news=recent_news,
    )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0.5,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": EMAIL_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError("OpenAI returned an empty email response.")

        return json.loads(content)

    except json.JSONDecodeError as e:
        raise RuntimeError(
            "OpenAI returned invalid JSON while generating the outreach email."
        ) from e

    except Exception as e:
        raise RuntimeError("Failed to generate outreach email.") from e


@log_tool
def improve_email(
    email: dict,
    feedback: str,
) -> dict:
    """
    Improve an existing outreach email.
    """

    prompt = build_improve_email_prompt(
        email=email,
        feedback=feedback,
    )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0.3,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": EMAIL_IMPROVE_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError("OpenAI returned an empty improved email.")

        return json.loads(content)

    except json.JSONDecodeError as e:
        raise RuntimeError(
            "OpenAI returned invalid JSON while improving the email."
        ) from e

    except Exception as e:
        raise RuntimeError("Failed to improve the outreach email.") from e


@log_tool
def preview_email(email: dict) -> None:
    """
    Pretty-print the generated email.
    """

    print("\n" + "=" * 80)
    print("SUBJECT")
    print("-" * 80)
    print(email["subject"])

    print("\nBODY")
    print("-" * 80)
    print(email["body"])
    print("=" * 80)


if __name__ == "__main__":
    candidate = Candidate(
        name="Emily Davis",
        email="emily@example.com",
        role="AI Engineer",
        experience=5,
        skills="Python, LangGraph, MCP, FastAPI, OpenAI",
        location="Boston",
        resume_summary="AI Engineer specializing in enterprise agentic systems.",
        projects="Built a production RAG platform and autonomous AI agents.",
    )

    manager = {
        "name": "Jane Doe",
        "title": "Engineering Manager",
    }

    email = generate_outreach_email(
        company="Stripe",
        hiring_manager=manager,
        candidate=candidate,
        company_summary="Stripe builds financial infrastructure for the internet.",
        recent_news=[
            "Stripe expanded AI investments.",
            "Stripe announced new developer tools.",
        ],
    )

    preview_email(email)
