"""Command-line entry point for the autonomous research agent."""

import argparse
from langgraph.prebuilt import create_react_agent
from src.llm_factory import build_llm
from src.research_tools import build_research_tools
from src.innovation_tool import build_innovation_tool

SYSTEM_PROMPT = """You are an autonomous research assistant. Produce a concise,
well-structured report and research-grounded innovation ideas.

Workflow:
1. Call plan_research_queries first.
2. Use no more than TWO distinct web_search calls and ONE arxiv_search call.
   Use wikipedia_search at most once and only for essential background.
3. Do not repeat searches or request large collections of results. Search tools
   already limit their output to protect the model context window.
4. Synthesize the retrieved evidence. Separate established findings, emerging
   evidence, and uncertainty. Do not invent citations, papers, or statistics.
5. Call generate_innovation_ideas exactly once, passing the original topic and
   a concise synthesis (roughly 5-8 evidence-based bullet points) from the
   research actually retrieved.
6. Return a final report with Executive Summary, Key Findings, Applications,
   Limitations and Open Challenges, and Innovation & Project Ideas. Include
   source titles/URLs returned by tools when available.

For healthcare topics, do not diagnose, prescribe, or claim clinical validation.
Flag privacy, bias, safety, regulation, and clinician oversight. Ideas are
proposals, not proof of global novelty or clinical effectiveness.
"""


def run_research(topic: str) -> str:
    """Run the research agent and return its final response."""
    llm = build_llm()
    tools = build_research_tools(llm)
    tools.append(build_innovation_tool(llm))
    agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)
    result = agent.invoke(
        {"messages": [{"role": "user", "content": f"Research topic: {topic}"}]},
        config={"recursion_limit": 20},
    )
    messages = result.get("messages", [])
    if not messages:
        return "The agent returned no messages."
    final_message = messages[-1]
    content = getattr(final_message, "content", str(final_message))
    if isinstance(content, list):
        return "\n".join(
            item.get("text", str(item)) if isinstance(item, dict) else str(item)
            for item in content
        )
    return str(content)


def main():
    parser = argparse.ArgumentParser(description="Autonomous Research Agent")
    parser.add_argument("topic", nargs="*", help="Research topic")
    args = parser.parse_args()
    topic = " ".join(args.topic).strip() or input("Enter a research topic: ").strip()
    if not topic:
        parser.error("Please provide a research topic.")
    print(f"\n# Autonomous Research Report: {topic}\n")
    print(run_research(topic))


if __name__ == "__main__":
    main()
