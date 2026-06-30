from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_DIR = PROJECT_ROOT / "src" / "database"
DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"

DATABASE_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

CANDIDATE_DB = DATABASE_DIR / "candidates.db"
CRM_DB = DATABASE_DIR / "crm.db"

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-4.1-mini"
TEMPERATURE = 0.2

#  Agent
MAX_STEPS = 8
MAX_RETRIES = 2

# Logging
LOG_FILE = LOG_DIR / "agent.log"
LOG_LEVEL = "INFO"

# Search
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Email
DEFAULT_SENDER = "outreach@wynisco.ai"
