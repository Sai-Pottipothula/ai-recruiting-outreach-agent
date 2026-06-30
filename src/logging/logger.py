import logging
import time
from functools import wraps
from pathlib import Path

from src.utils.config import LOG_FILE, LOG_LEVEL


def get_logger(name: str) -> logging.Logger:
    """
    Create and configure a logger.
    """

    Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(LOG_LEVEL)

        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        logger.propagate = False

    return logger


logger = get_logger("outreach-agent")


def summarize(value):
    if value is None:
        return "None"

    if isinstance(value, str):
        if len(value) > 60:
            return f"String({len(value)} chars)"

        return value

    if isinstance(value, list):
        return f"{len(value)} items"

    if isinstance(value, dict):
        return f"{len(value)} fields"

    if hasattr(value, "name"):
        return value.name

    return str(value)


def log_tool(func):
    """
    Log every tool execution.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("▶ %s", func.__name__)

        start = time.perf_counter()

        try:
            result = func(*args, **kwargs)

            elapsed = time.perf_counter() - start

            logger.info(
                "✓ %s (%.2f sec)",
                func.__name__,
                elapsed,
            )

            return result

        except Exception:
            elapsed = time.perf_counter() - start

            logger.exception(
                "✗ %s FAILED (%.2f sec)",
                func.__name__,
                elapsed,
            )

            raise

    return wrapper
