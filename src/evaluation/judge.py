import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from src.utils.prompts import (
    LLM_JUDGE_SYSTEM_PROMPT,
    build_judge_prompt,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")
llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0,
)


def judge_email(email: str) -> dict:
    """
    Evaluate a generated outreach email using an LLM.
    """

    prompt = build_judge_prompt(email)

    try:
        response = llm.invoke(
            [
                {
                    "role": "system",
                    "content": LLM_JUDGE_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ]
        )

        if not response.content:
            raise RuntimeError("LLM returned an empty evaluation.")

        return json.loads(response.content)

    except json.JSONDecodeError as e:
        raise RuntimeError("LLM returned invalid JSON during evaluation.") from e

    except Exception as e:
        raise RuntimeError("Failed to evaluate the generated email.") from e
