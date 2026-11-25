"""Command-line entry point for the autonomous research agent."""

import argparse
from langgraph.prebuilt import create_react_agent
from src.llm_factory import build_llm
from src.research_tools import build_research_tools
from src.innovation_tool import build_innovation_tool

SYSTEM_PROMPT = """You are an autonomous research assistant. Produce a useful, structured
research report based on retrieved information, and then generate practical
innovation ideas grounded in that research.

Workflow:
1. Start by using plan_research_queries to create focused research angles.
2. Search the web and academic sources. Use Wikipedia only for background.
   Use several distinct queries and more than one source type where relevant.
3. Synthesize what the sources say. Clearly distinguish established findings,
   emerging evidence, and uncertainty. Do not invent citations or statistics.
4. Once you have collected enough findings, call generate_innovation_ideas.
   Pass the original topic and a concise but information-rich synthesis of the
   research you actually retrieved. Do not call it with empty or invented findings.
5. Present a final report with: Executive Summary, Key Findings, Applications,
   Limitations and Open Challenges, and Innovation & Project Ideas. Include
   source details returned by tools when available.

For healthcare research, do not diagnose, prescribe, or claim clinical
validation. Flag privacy, bias, safety, regulation, and clinician oversight.
The innovation tool proposes ideas; it does not establish global novelty.
"""


def run_research(topic: str) -> str:
    """Run the research agent and return its final response."""
    llm = build_llm()
    tools = build_research_tools(llm)
    tools.append(build_innovation_tool(llm))
    agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)
    result = agent.invoke(
        {"messages": [{"role": "user", "content": f"Research topic: {topic}"}]},
        config={"recursion_limit": 50},
    )
    messages = result.get("messages", [])
    if not messages:
        return "The agent returned no messages."
    final_message = messages[-1]
    content = getattr(final_message, "content", str(final_message))
    if isinstance(content, list):
        return "\\n".join(
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
    print(f"\\n# Autonomous Research Report: {topic}\\n")
    print(run_research(topic))


if __name__ == "__main__":
    main()
