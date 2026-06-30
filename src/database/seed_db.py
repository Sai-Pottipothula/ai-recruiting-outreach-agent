import json
import sqlite3
from pathlib import Path
from src.database.db import create_candidate
from src.database.models import Candidate

DATA_FILE = Path("data/candidates.json")


def seed_database():
    with open(DATA_FILE, "r") as f:
        candidates = json.load(f)
    print(f"Loading {len(candidates)} candidates...\n")
    for item in candidates:
        try:
            candidate = Candidate(**item)
            create_candidate(candidate)
            print(f"✓ Added {candidate.name}")
        except sqlite3.IntegrityError:
            print(f"• Skipped {candidate.name}")
    print("\nDatabase seeded successfully.")


if __name__ == "__main__":
    seed_database()
