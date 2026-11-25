"""Construct a chat model from environment configuration."""

from src.config import get_settings


def build_llm():
    settings = get_settings()
    provider = settings["provider"]
    common = {
        "model": settings["model"],
        "temperature": settings["temperature"],
        "max_tokens": settings["max_tokens"],
        "api_key": settings["api_key"],
    }
    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(**common)
    if provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=settings["model"],
            temperature=settings["temperature"],
            max_output_tokens=settings["max_tokens"],
            google_api_key=settings["api_key"],
        )
    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=settings["model"],
            temperature=settings["temperature"],
            max_tokens=settings["max_tokens"],
            api_key=settings["api_key"],
        )
    raise ValueError(f"Unsupported provider: {provider}")
