import json

from openai import OpenAI
from tavily import TavilyClient

from src.logging.logger import log_tool
from src.utils.config import (
    MODEL_NAME,
    OPENAI_API_KEY,
    TAVILY_API_KEY,
)
from src.utils.prompts import (
    COMPANY_SUMMARIZER_SYSTEM_PROMPT,
    SKILL_EXTRACTION_SYSTEM_PROMPT,
    build_company_summary_prompt,
    build_skill_extraction_prompt,
)

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
llm = OpenAI(api_key=OPENAI_API_KEY)


@log_tool
def search_company(company: str) -> dict:
    """
    Research a company using Tavily Search.
    """

    try:
        return tavily_client.search(
            query=f"""
Research the company {company}.

Return:
- Company overview
- Industry
- Products
- Recent news
- Hiring trends
- Engineering culture
""",
            search_depth="advanced",
            max_results=5,
        )

    except Exception as e:
        raise RuntimeError(f"Failed to research '{company}' using Tavily.") from e


@log_tool
def get_company_summary(company: str) -> str:
    """
    Generate a concise company summary from Tavily search results.
    """

    response = search_company(company)

    context = "\n\n".join(result["content"] for result in response.get("results", []))

    if not context:
        raise RuntimeError(f"No research results found for '{company}'.")

    prompt = build_company_summary_prompt(
        company=company,
        context=context,
    )

    try:
        response = llm.chat.completions.create(
            model=MODEL_NAME,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": COMPANY_SUMMARIZER_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        summary = response.choices[0].message.content

        if not summary:
            raise RuntimeError("OpenAI returned an empty summary.")

        return summary

    except Exception as e:
        raise RuntimeError("Failed to generate the company summary.") from e


@log_tool
def get_recent_company_news(company: str) -> list[str]:
    """
    Return recent company news headlines.
    """

    try:
        response = tavily_client.search(
            query=f"Latest news about {company}",
            topic="news",
            max_results=5,
        )

        return [item["title"] for item in response.get("results", [])]

    except Exception as e:
        raise RuntimeError(f"Failed to retrieve news for '{company}'.") from e


@log_tool
def extract_required_skills(
    company_summary: str,
) -> list[str]:
    """
    Extract the top technical skills required by the company.
    """

    prompt = build_skill_extraction_prompt(
        company_summary=company_summary,
    )

    try:
        response = llm.chat.completions.create(
            model=MODEL_NAME,
            temperature=0,
            response_format={
                "type": "json_object",
            },
            messages=[
                {
                    "role": "system",
                    "content": SKILL_EXTRACTION_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        result = json.loads(response.choices[0].message.content)

        return result["skills"]

    except json.JSONDecodeError as e:
        raise RuntimeError(
            "OpenAI returned invalid JSON while extracting skills."
        ) from e

    except Exception as e:
        raise RuntimeError("Failed to extract required skills.") from e


if __name__ == "__main__":
    company = "Stripe"

    summary = get_company_summary(company)

    print(summary)

    print("\n" + "=" * 80)

    print(get_recent_company_news(company))

    print("\n" + "=" * 80)

    print(extract_required_skills(summary))
