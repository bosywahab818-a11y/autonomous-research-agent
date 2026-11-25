from src.innovation_tool import build_innovation_tool


class FakeResponse:
    content = "Idea: AI-assisted medical report explainer."


class FakeLLM:
    def __init__(self):
        self.last_prompt = None

    def invoke(self, prompt):
        self.last_prompt = prompt
        return FakeResponse()


def test_innovation_tool_uses_topic_and_research_findings():
    llm = FakeLLM()
    tool = build_innovation_tool(llm)
    result = tool.invoke({
        "topic": "Generative AI in Healthcare",
        "research_findings": "RAG can ground generated answers in medical documents.",
    })
    assert "medical report explainer" in result
    assert "Generative AI in Healthcare" in llm.last_prompt
    assert "RAG can ground" in llm.last_prompt


def test_innovation_tool_rejects_missing_findings():
    tool = build_innovation_tool(FakeLLM())
    result = tool.invoke({"topic": "Healthcare AI", "research_findings": " "})
    assert "No research findings" in result
