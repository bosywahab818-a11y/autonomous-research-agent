"""Research planning and bounded multi-source retrieval tools."""

import os
from langchain_core.tools import tool


def deduplicate_text_results(text: str) -> str:
    """Remove repeated text blocks while preserving their original order."""
    if not text:
        return text
    blocks = [part.strip() for part in text.split("\n\n") if part.strip()]
    seen = set()
    unique = []
    for block in blocks:
        normalized = " ".join(block.lower().split())
        if normalized not in seen:
            seen.add(normalized)
            unique.append(block)
    return "\n\n".join(unique)


def limit_result_text(text: str, max_chars: int) -> str:
    """Bound a retrieved result so tool output cannot flood the agent context."""
    text = str(text or "").strip()
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + "\n...[result shortened to control context size]"


def build_research_tools(llm):
    """Build research tools with conservative result limits."""
    from langchain_tavily import TavilySearch
    from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
    from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper

    tavily_key = os.getenv("TAVILY_API_KEY")
    if not tavily_key:
        raise EnvironmentError("Missing TAVILY_API_KEY. Add it to your .env file.")

    web_max_results = int(os.getenv("TAVILY_MAX_RESULTS", "2"))
    web_max_chars = int(os.getenv("WEB_RESULT_MAX_CHARS", "2200"))
    arxiv_max_chars = int(os.getenv("ARXIV_RESULT_MAX_CHARS", "1800"))
    wiki_max_chars = int(os.getenv("WIKIPEDIA_RESULT_MAX_CHARS", "900"))

    web = TavilySearch(max_results=web_max_results, api_key=tavily_key)
    arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper(
        top_k_results=2, doc_content_chars_max=1200))
    wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(
        top_k_results=1, doc_content_chars_max=900))

    @tool
    def plan_research_queries(topic: str) -> str:
        """Create four focused research angles for a topic."""
        prompt = (
            "Create exactly four short, distinct search queries for this topic. "
            "Cover recent advances, real-world applications, limitations, and open "
            "challenges. Return one query per line, no introduction.\n\n"
            f"Topic: {topic}"
        )
        answer = llm.invoke(prompt)
        content = getattr(answer, "content", answer)
        return limit_result_text(str(content), 700)

    @tool
    def web_search(query: str) -> str:
        """Search the web and return a compact set of recent results."""
        result = deduplicate_text_results(str(web.invoke({"query": query})))
        return limit_result_text(result, web_max_chars)

    @tool
    def arxiv_search(query: str) -> str:
        """Search academic papers on arXiv and return concise evidence."""
        result = deduplicate_text_results(str(arxiv.invoke(query)))
        return limit_result_text(result, arxiv_max_chars)

    @tool
    def wikipedia_search(query: str) -> str:
        """Retrieve brief introductory background from Wikipedia."""
        result = deduplicate_text_results(str(wiki.invoke(query)))
        return limit_result_text(result, wiki_max_chars)

    return [plan_research_queries, web_search, arxiv_search, wikipedia_search]
