"""Research-driven innovation and project idea generation tool.

The tool transforms findings already collected by the research agent into
practical ideas. It does not perform another search and does not claim that
an idea is globally novel or clinically validated.
"""

from langchain_core.tools import tool


INNOVATION_PROMPT = """You are an Innovation Research Analyst.

Generate 3 to 5 distinct, useful project or product ideas inspired by the
research findings below. The ideas must be grounded in the supplied findings,
not generic ideas unrelated to the research.

For each idea, use this structure:
1. **Title**
2. **Problem addressed** — the specific problem or limitation.
3. **Proposed solution** — how the idea could work.
4. **Research inspiration** — which supplied finding motivates it. Do not
   invent papers, statistics, or findings.
5. **Suggested technologies** — relevant methods, models, or tools.
6. **Implementation outline** — 3 to 5 practical steps.
7. **Potential impact** — who could benefit and how.
8. **Feasibility** — Low, Medium, or High, with a short explanation.
9. **Risks and limitations** — technical, ethical, privacy, or deployment risks.

After the ideas, include:
- **Top recommendation:** choose one idea and explain why it is the strongest.
- **What needs validation:** list assumptions that would require further
  research, user interviews, experiments, or expert review.

Important rules:
- Be specific, creative, and realistic.
- Make the ideas meaningfully different from one another.
- Distinguish established research findings from your own proposed ideas.
- Do not claim an idea is completely new, patented, safe, or proven unless
  the supplied findings establish that.
- For healthcare topics, treat ideas as research or decision-support concepts.
  Do not provide diagnoses, treatment instructions, or claims of clinical
  effectiveness. Highlight the need for clinical validation, privacy
  protection, and qualified professional oversight where relevant.

RESEARCH TOPIC:
{topic}

COLLECTED RESEARCH FINDINGS:
{research_findings}
"""


def build_innovation_tool(llm):
    """Create the innovation tool using the agent's configured chat model."""

    @tool
    def generate_innovation_ideas(topic: str, research_findings: str) -> str:
        """Generate 3-5 practical innovation ideas grounded in collected research findings.

        Use this after web and/or academic research has been collected.
        Pass the original research topic and a concise synthesis of the findings.
        """
        if not topic.strip():
            return "Please provide a research topic."
        if not research_findings.strip():
            return (
                "No research findings were provided. Collect research evidence "
                "before generating ideas."
            )

        # Keep the second LLM call bounded even if the agent passes raw tool output.\n        compact_findings = research_findings.strip()[:6000]\n        prompt = INNOVATION_PROMPT.format(\n            topic=topic.strip(),\n            research_findings=compact_findings,\n        )
        response = llm.invoke(prompt)
        content = getattr(response, "content", response)
        if isinstance(content, str):
            return content
        return str(content)

    return generate_innovation_ideas
