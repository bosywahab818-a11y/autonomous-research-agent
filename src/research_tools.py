"""Research planning and multi-source retrieval tools."""

from langchain_core.tools import tool


def deduplicate_text_results(text: str) -> str:
    """Remove repeated result blocks while preserving their original order."""
    if not text:
        return text
    blocks = [part.strip() for part in text.split("\\n\\n") if part.strip()]
    seen = set()
    unique = []
    for block in blocks:
        normalized = " ".join(block.lower().split())
        if normalized not in seen:
            seen.add(normalized)
            unique.append(block)
    return "\\n\\n".join(unique)


def build_research_tools(llm):
    """Build tools using the installed LangChain integrations."""
    from langchain_tavily import TavilySearch
    from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
    from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
    import os

    tavily_key = os.getenv("TAVILY_API_KEY")
    if not tavily_key:
        raise EnvironmentError("Missing TAVILY_API_KEY. Add it to your .env file.")

    web = TavilySearch(max_results=int(os.getenv("TAVILY_MAX_RESULTS", "5")),
                       api_key=tavily_key)
    arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper(
        top_k_results=4, doc_content_chars_max=3000))
    wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(
        top_k_results=2, doc_content_chars_max=2000))

    @tool
    def plan_research_queries(topic: str) -> str:
        """Break a research topic into 4-6 focused, complementary research questions."""
        prompt = (
            "Create 4-6 concise, non-overlapping research queries for this topic. "
            "Cover fundamentals, recent advances, applications, limitations, and "
            "open challenges. Return one query per line, without commentary.\\n\\n"
            f"Topic: {topic}"
        )
        answer = llm.invoke(prompt)
        return str(getattr(answer, "content", answer))

    @tool
    def web_search(query: str) -> str:
        """Search the web for recent and relevant sources using Tavily."""
        return deduplicate_text_results(str(web.invoke({"query": query})))

    @tool
    def arxiv_search(query: str) -> str:
        """Search arXiv for relevant academic papers and preprints."""
        return deduplicate_text_results(str(arxiv.invoke(query)))

    @tool
    def wikipedia_search(query: str) -> str:
        """Find introductory background information on a research subject."""
        return deduplicate_text_results(str(wiki.invoke(query)))

    return [plan_research_queries, web_search, arxiv_search, wikipedia_search]
