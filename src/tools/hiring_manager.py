import json

from openai import OpenAI

from src.logging.logger import log_tool
from src.tools.company_research import search_company
from src.utils.config import (
    MODEL_NAME,
    OPENAI_API_KEY,
)
from src.utils.prompts import (
    BEST_MANAGER_SYSTEM_PROMPT,
    HIRING_MANAGER_SYSTEM_PROMPT,
    build_best_manager_prompt,
    build_hiring_manager_prompt,
)

client = OpenAI(api_key=OPENAI_API_KEY)


@log_tool
def extract_hiring_managers(company: str) -> list[dict]:
    """
    Research a company and identify the best hiring contacts.
    """

    search_results = search_company(company)

    context = "\n\n".join(
        result["content"] for result in search_results.get("results", [])
    )

    if not context:
        raise RuntimeError(f"No hiring manager information found for '{company}'.")

    prompt = build_hiring_manager_prompt(
        company=company,
        context=context,
    )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0,
            response_format={
                "type": "json_object",
            },
            messages=[
                {
                    "role": "system",
                    "content": HIRING_MANAGER_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError("OpenAI returned an empty hiring manager response.")

        return json.loads(content)

    except json.JSONDecodeError as e:
        raise RuntimeError(
            "OpenAI returned invalid JSON while extracting hiring managers."
        ) from e

    except Exception as e:
        raise RuntimeError("Failed to extract hiring managers.") from e


@log_tool
def choose_best_manager(
    managers_json,
) -> dict:
    """
    Select the best hiring manager from the extracted contacts.
    """

    prompt = build_best_manager_prompt(
        managers_json,
    )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0,
            response_format={
                "type": "json_object",
            },
            messages=[
                {
                    "role": "system",
                    "content": BEST_MANAGER_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError("OpenAI returned an empty manager selection.")

        return json.loads(content)

    except json.JSONDecodeError as e:
        raise RuntimeError(
            "OpenAI returned invalid JSON while selecting the hiring manager."
        ) from e

    except Exception as e:
        raise RuntimeError("Failed to choose the best hiring manager.") from e


if __name__ == "__main__":
    company = "Stripe"

    managers = extract_hiring_managers(company)

    print(
        json.dumps(
            managers,
            indent=2,
        )
    )

    print()

    best = choose_best_manager(managers)

    print(
        json.dumps(
            best,
            indent=2,
        )
    )
