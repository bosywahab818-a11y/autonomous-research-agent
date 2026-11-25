"""Environment-based configuration for the research agent."""

import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "groq").strip().lower()
MODEL_NAMES = {
    "groq": os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
    "google": os.getenv("GOOGLE_MODEL", "gemini-2.5-flash"),
    "anthropic": os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5"),
}
API_KEY_NAMES = {
    "groq": "GROQ_API_KEY",
    "google": "GOOGLE_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
}


def get_settings():
    """Return validated settings for the selected model provider."""
    if PROVIDER not in MODEL_NAMES:
        raise ValueError("LLM_PROVIDER must be groq, google, or anthropic.")
    key_name = API_KEY_NAMES[PROVIDER]
    api_key = os.getenv(key_name)
    if not api_key:
        raise EnvironmentError(f"Missing {key_name}. Add it to your .env file.")
    return {
        "provider": PROVIDER,
        "model": MODEL_NAMES[PROVIDER],
        "api_key": api_key,
        "temperature": float(os.getenv("LLM_TEMPERATURE", "0.2")),
        # Leave room for prompt, tool descriptions, and retrieved evidence
        # under providers with a shared input/output tokens-per-minute quota.
        "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "1500")),
    }
