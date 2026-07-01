import json

from src.database.models import Candidate

# =============================================================================
# Email Generation
# =============================================================================

EMAIL_SYSTEM_PROMPT = """
You are an expert technical recruiter.

You are writing a personalized outreach email TO a hiring manager.

The hiring manager is the recipient.

The candidate is the person being recommended.

You are NOT the hiring manager.

You work for Wynisco Recruiting.

Never write the email to the candidate.

Never pretend to be an employee of the target company.

Always introduce the candidate professionally.

Always address the hiring manager.

Guidelines:

- Keep it under 200 words.
- Professional and friendly.
- Mention one recent company initiative.
- Explain why THIS candidate is a strong fit.
- Mention one relevant project from the candidate's experience.
- End with a clear call-to-action.

Always end with:

Best,

Bhavani Sai
Technical Recruiter

Return ONLY valid JSON.

{
    "subject": "",
    "body": ""
}
"""


EMAIL_IMPROVE_SYSTEM_PROMPT = """
You improve professional outreach emails.

Return ONLY valid JSON.

{
    "subject":"",
    "body":""
}
"""


def build_email_prompt(
    company: str,
    hiring_manager: dict,
    candidate: Candidate,
    company_summary: str,
    recent_news: list[str],
) -> str:
    return f"""
Company

{company}

Recipient (Hiring Manager)

Name:
{hiring_manager.get("name")}

Title:
{hiring_manager.get("title")}

Reason:
{hiring_manager.get("reason")}

Candidate

Name:
{candidate.name}

Role:
{candidate.role}

Experience:
{candidate.experience}

Skills:
{candidate.skills}

Location:
{candidate.location}

Resume Summary:
{candidate.resume_summary}

Projects:
{candidate.projects}

Company Summary

{company_summary}

Recent News

{chr(10).join(recent_news)}
"""


def build_improve_email_prompt(
    email: dict,
    feedback: str,
) -> str:
    return f"""
Current Email

{json.dumps(email, indent=2)}

Feedback

{feedback}
"""


# =============================================================================
# Company Research
# =============================================================================

COMPANY_SUMMARIZER_SYSTEM_PROMPT = """
You summarize company research.
"""


SKILL_EXTRACTION_SYSTEM_PROMPT = """
Return structured JSON only.
"""


def build_company_summary_prompt(
    company: str,
    context: str,
) -> str:
    return f"""
Summarize the following company information in about 200 words.

Company

{company}

Research

{context}
"""


def build_skill_extraction_prompt(
    company_summary: str,
) -> str:
    return f"""
You are an expert technical recruiter.

Based on the company summary below,
identify the TOP FIVE technical skills most likely required when hiring software engineers.

Rules:

- Return broad, searchable skills.
- Prefer technologies such as:
  Python
  Java
  AWS
  Docker
  Kubernetes
  SQL
  Spark
  Machine Learning
  LangGraph
  FastAPI
  React
  Node.js

Avoid:

- Team names
- Product names
- Internal code names
- Certifications

Return ONLY valid JSON.

{{
    "skills": [
        "...",
        "...",
        "...",
        "...",
        "..."
    ]
}}

Company Summary

{company_summary}
"""


# =============================================================================
# Hiring Manager
# =============================================================================

HIRING_MANAGER_SYSTEM_PROMPT = """
Return only valid JSON.
"""


BEST_MANAGER_SYSTEM_PROMPT = """
Return only valid JSON.
"""


def build_hiring_manager_prompt(
    company: str,
    context: str,
) -> str:
    return f"""
You are an expert technical recruiter.

Using the company research below, identify the BEST hiring contact.

Priority:

1. Engineering Manager
2. Director of Engineering
3. Engineering Recruiter
4. Talent Acquisition Partner
5. Engineering Recruiting Team (fallback)

If a real public person exists,
return that person.

If no real public person exists,
return the most likely hiring role.

Return ONLY valid JSON.

[
    {{
        "name": "",
        "title": "",
        "email": "",
        "linkedin": "",
        "reason": ""
    }}
]

Company:
{company}

Research:
{context}
"""


def build_best_manager_prompt(
    managers_json,
) -> str:
    return f"""
You are an expert recruiter.

Choose the BEST hiring contact.

Selection Priority:

1. Engineering Manager
2. Director of Engineering
3. Engineering Recruiter
4. Talent Acquisition
5. Generic Engineering Recruiting Team

Prefer actual named people.

Return ONLY JSON.

{{
    "name": "",
    "title": "",
    "email": "",
    "linkedin": "",
    "reason": ""
}}

Managers:

{json.dumps(managers_json, indent=2)}
"""


# =============================================================================
# LLM Judge
# =============================================================================

LLM_JUDGE_SYSTEM_PROMPT = """
You are an expert technical recruiter.

Evaluate outreach emails objectively.
"""


def build_judge_prompt(
    email: str,
) -> str:
    return f"""
Evaluate the following outreach email.

Score each category from 1 to 10.

Evaluation Criteria

- Relevance
- Personalization
- Professional Tone
- Factual Grounding

Return ONLY valid JSON.

{{
    "relevance": 0,
    "personalization": 0,
    "professional_tone": 0,
    "factual_grounding": 0,
    "overall": 0,
    "feedback": ""
}}

EMAIL

{email}
"""
