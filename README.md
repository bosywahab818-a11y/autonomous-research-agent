# Autonomous Research Agent

An extensible research assistant built with LangChain and LangGraph. It combines web search, academic-paper discovery, background knowledge, and a custom evidence-auditing tool to produce structured research reports.

## Features

- **Multiple LLM providers:** Groq, Google Gemini, and Anthropic Claude. Select a provider with `LLM_PROVIDER`.
- **Multi-angle research:** an LLM-powered query planner creates focused sub-queries before retrieval.
- **Multiple sources:** Tavily web search, arXiv, and Wikipedia.
- **Evidence auditing:** a custom tool checks report claims against retrieved source excerpts and labels them Supported, Partially supported, or Unsupported. Treat this as an assistive review, not a guarantee of truth.
- **Secret-safe configuration:** API keys are read from environment variables and are never stored in source files.

## Project structure

```text
autonomous-research-agent/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── llm_factory.py
│   ├── research_tools.py
│   ├── evidence_auditor.py
│   └── agent.py
├── tests/
│   └── test_evidence_auditor.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

Python 3.10+ is recommended.

```bash
git clone https://github.com/bosywahab818-a11y/autonomous-research-agent.git
cd autonomous-research-agent
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add the keys for the provider and tools you intend to use. Never commit `.env`.

```env
LLM_PROVIDER=groq
GROQ_API_KEY=...
GROQ_MODEL=openai/gpt-oss-120b
TAVILY_API_KEY=...
```

Optional provider settings are documented in `.env.example`. The app requires the API key for the selected LLM provider and a Tavily key for web search. arXiv and Wikipedia do not require API keys.

## Run

```bash
python -m src.agent "Quantum Error Correction breakthroughs in 2025"
```

Or run interactively:

```bash
python -m src.agent
```

## Switch LLM provider

Set `LLM_PROVIDER` to one of `groq`, `google`, or `anthropic`. Set the matching API key and optionally override the model name with `GROQ_MODEL`, `GOOGLE_MODEL`, or `ANTHROPIC_MODEL`.

## Research workflow

1. The query planner expands the topic into complementary research questions.
2. The agent searches web, arXiv, and Wikipedia as appropriate.
3. Retrieved results are normalized and de-duplicated by URL/title before being returned to the agent.
4. The agent synthesizes a report with source references.
5. The evidence auditor compares report claims with the evidence excerpts gathered during the run.

Search quality is improved through query decomposition, multiple focused searches, source diversity, de-duplication, and evidence review. Retrieval ranking is not a substitute for checking the original source.

## Security

- Do not paste API keys into notebooks, source code, README files, screenshots, or GitHub commits.
- If a key was previously exposed, revoke it and generate a new one.
- For Colab, store credentials in **Secrets** and read them with `google.colab.userdata.get(...)`.

## Limitations

The evidence auditor is an LLM-assisted reviewer. It can miss unsupported statements or incorrectly judge evidence. Verify important claims and citations manually, especially for medical, legal, financial, or safety-critical research. arXiv results may be preprints and are not necessarily peer-reviewed.

## License

Add a license if you want to specify reuse permissions.
