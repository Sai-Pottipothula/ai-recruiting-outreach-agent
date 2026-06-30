from src.graph.workflow import graph


def main():
    """
    Entry point for the AI Outreach Agent.
    """

    company = input("Enter company name: ").strip()

    initial_state = {
        "company_name": company,
        "company_summary": "",
        "recent_news": [],
        "required_skills": [],
        "required_skill": "",
        "hiring_manager": {},
        "candidate": None,
        "generated_email": {},
        "crm_id": 0,
        "approved": False,
        "status": "STARTED",
        "steps": 0,
        "error": "",
    }

    print("\n" + "=" * 80)
    print("STARTING AI OUTREACH AGENT")
    print("=" * 80)

    try:
        final_state = graph.invoke(initial_state)

        print("\n" + "=" * 80)

        status = final_state["status"]

        if status == "SUCCESS":
            print("WORKFLOW COMPLETED")

        elif status == "NO_CANDIDATE_FOUND":
            print("WORKFLOW STOPPED")

        elif status == "REJECTED":
            print("WORKFLOW REJECTED")

        elif status == "MAX_STEPS":
            print("WORKFLOW TERMINATED")

        elif status == "FAILED":
            print("WORKFLOW FAILED")

        else:
            print("WORKFLOW FINISHED")

        print("=" * 80)

        print(f"Company        : {final_state['company_name']}")

        if final_state["required_skill"]:
            print(f"Matched Skill  : {final_state['required_skill']}")

        else:
            print("Skills         : " + ", ".join(final_state["required_skills"]))

        if final_state["candidate"] is not None:
            print(f"Candidate      : {final_state['candidate'].name}")

        else:
            print("Candidate      : None")

        if status == "SUCCESS":
            print(f"CRM ID         : {final_state['crm_id']}")

        elif status == "NO_CANDIDATE_FOUND":
            print("Reason         : No matching candidate found.")

        elif status == "REJECTED":
            print("Reason         : Email was rejected during human approval.")

        elif status == "MAX_STEPS":
            print("Reason         : Maximum workflow step limit reached.")

        elif status == "FAILED":
            print(f"Reason         : {final_state.get('error', 'Unknown error.')}")

        print(f"Status         : {status}")
        print(f"Steps          : {final_state['steps']}")

        print("=" * 80)

    except KeyboardInterrupt:
        print("\n")
        print("=" * 80)
        print("WORKFLOW CANCELLED")
        print("=" * 80)

    except Exception as e:
        print("\n")
        print("=" * 80)
        print("UNEXPECTED ERROR")
        print("=" * 80)
        print(e)
        print("=" * 80)


if __name__ == "__main__":
    main()
