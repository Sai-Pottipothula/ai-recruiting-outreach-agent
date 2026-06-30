import json

from src.evaluation.dataset import TEST_CASES
from src.evaluation.judge import judge_email
from src.graph.workflow import graph

results = []

print("\n" + "=" * 80)
print("RUNNING EVALUATION")
print("=" * 80)

for index, case in enumerate(TEST_CASES, start=1):
    print(f"\n[{index}/{len(TEST_CASES)}] {case['company']}")

    state = graph.invoke(
        {
            "company_name": case["company"],
            "company_summary": "",
            "recent_news": [],
            "required_skill": "",
            "required_skills": [],
            "hiring_manager": {},
            "candidate": None,
            "generated_email": {},
            "crm_id": 0,
            "approved": False,
            "status": "STARTED",
            "steps": 0,
            "evaluation": True,
        }
    )

    if state["status"] == "SUCCESS":
        scores = judge_email(state["generated_email"]["body"])

    else:
        scores = {
            "relevance": 0,
            "personalization": 0,
            "professional_tone": 0,
            "factual_grounding": 0,
            "overall": 0,
            "feedback": state["status"],
        }

    results.append(
        {
            "company": case["company"],
            "status": state["status"],
            "scores": scores,
        }
    )

with open(
    "src/evaluation/evaluation_results.json",
    "w",
) as file:
    json.dump(
        results,
        file,
        indent=4,
    )

successful_runs = [r for r in results if r["status"] == "SUCCESS"]

if successful_runs:
    avg_relevance = sum(r["scores"]["relevance"] for r in successful_runs) / len(
        successful_runs
    )

    avg_personalization = sum(
        r["scores"]["personalization"] for r in successful_runs
    ) / len(successful_runs)

    avg_professional_tone = sum(
        r["scores"]["professional_tone"] for r in successful_runs
    ) / len(successful_runs)

    avg_factual_grounding = sum(
        r["scores"]["factual_grounding"] for r in successful_runs
    ) / len(successful_runs)

    avg_overall = sum(r["scores"]["overall"] for r in successful_runs) / len(
        successful_runs
    )

    print("\n" + "=" * 80)
    print("EVALUATION SUMMARY")
    print("=" * 80)
    print(f"Total Test Cases      : {len(TEST_CASES)}")
    print(f"Successful Runs       : {len(successful_runs)}")
    print(f"Failed Runs           : {len(TEST_CASES) - len(successful_runs)}")
    print()
    print(f"Average Relevance     : {avg_relevance:.2f}/10")
    print(f"Average Personalization : {avg_personalization:.2f}/10")
    print(f"Average Professional Tone : {avg_professional_tone:.2f}/10")
    print(f"Average Grounding     : {avg_factual_grounding:.2f}/10")
    print(f"Average Overall       : {avg_overall:.2f}/10")
    print("=" * 80)

print("\nResults saved to: src/evaluation/evaluation_results.json")

print("Evaluation Complete")
