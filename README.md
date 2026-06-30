# AI Recruiting Outreach Agent

An AI-powered recruiting workflow for staffing and recruitment agencies. 
Given a target company, the agent researches the company, identifies the most relevant hiring manager, recommends the best-matching candidate from an internal talent database through a Model Context Protocol (MCP) server, generates a personalized outreach email, includes a Human-in-the-Loop (HITL) approval step, and logs approved outreach to a CRM.

**Built with:** LangGraph • OpenAI • MCP • Tavily Search • SQLite • Docker

---

## Key Features

- Researches target companies using Tavily Search
- Identifies the most relevant hiring manager
- Retrieves the best-matching candidate through an MCP server
- Generates personalized outreach emails using OpenAI
- Includes a Human-in-the-Loop (HITL) approval step before CRM logging
- Workflow orchestration using LangGraph
- Structured logging with execution timing
- Automated evaluation using an LLM-as-a-Judge
- Containerized deployment with Docker

---

## Architecture

```text
                        +--------------------+
                        |     Recruiter      |
                        +----------+---------+
                                   |
                                   v
                    +------------------------------+
                    |      LangGraph Workflow      |
                    +--------------+---------------+
                                   |
        +--------------------------+---------------------------+
        |                          |                           |
        v                          v                           v
+---------------+        +--------------------+      +------------------+
| Company       |        | Hiring Manager     |      | Candidate        |
| Research      |        | Identification     |      | Recommendation   |
| (Tavily)      |        |                    |      | (MCP Server)     |
+---------------+        +--------------------+      +--------+---------+
                                                             |
                                                             v
                                                  +----------------------+
                                                  | Talent Database      |
                                                  | (SQLite)             |
                                                  +----------------------+
                                   |
                                   v
                        +---------------------------+
                        | Generate Outreach Email   |
                        | (OpenAI)                 |
                        +------------+-------------+
                                     |
                                     v
                        +---------------------------+
                        | Human Approval (HITL)     |
                        +------------+-------------+
                                     |
                                     v
                        +---------------------------+
                        | CRM Logger (SQLite)       |
                        +---------------------------+
```

---

## Workflow

1. Enter a target company.
2. Research the company using Tavily Search.
3. Identify the most relevant hiring manager.
4. Retrieve the best-matching candidate from the internal talent database through the MCP server.
5. Generate a personalized outreach email using OpenAI.
6. Request recruiter approval before outreach.
7. Log approved outreach to the CRM database.

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.11 |
| Agent Framework | LangGraph |
| LLM | OpenAI GPT-4.1 Mini |
| Search | Tavily Search |
| Tool Protocol | Model Context Protocol (MCP) |
| Database | SQLite |
| Containerization | Docker |
| Evaluation | LLM-as-a-Judge |

---

## Project Structure

```text
.
├── data/
├── logs/
├── src/
│   ├── database/
│   ├── evaluation/
│   ├── graph/
│   ├── logging/
│   ├── mcp/
│   ├── tools/
│   └── utils/
├── app.py
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<username>/ai-recruiting-outreach-agent.git
cd ai-recruiting-outreach-agent
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

**macOS/Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install .
```

Create a `.env` file:

```text
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
```

---

## Running the Agent

```bash
python app.py
```

Example:

```text
Enter company name: Stripe
```

The workflow will:

- Research the company
- Find a hiring manager
- Recommend a candidate
- Generate an outreach email
- Request approval
- Save the outreach to the CRM

---

## Running with Docker

Build and start the application:

```bash
docker compose up
```

Or run the container directly:

```bash
docker run --rm -it --env-file .env ai-recruiting-outreach-agent
```

---

## Evaluation

The project includes an automated evaluation pipeline using an LLM-as-a-Judge.

Run:

```bash
python -m src.evaluation.run_eval
```

The evaluation measures:

- Relevance
- Personalization
- Professional Tone
- Factual Grounding
- Overall Quality

Results are saved to:

```text
src/evaluation/evaluation_results.json
```

---

## Future Improvements

- Integrate Apollo.io for real hiring contact discovery
- Send approved outreach using the Gmail API
- Replace the SQLite CRM with a production CRM (Salesforce, HubSpot, etc.)
- Add LangSmith or OpenTelemetry tracing
- Extend the workflow with additional recruiter tools
- Deploy as a web application

---

## License

This project is licensed under the MIT License.