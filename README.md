# Autonomous Research Agent

An extensible research assistant built with **LangChain** and **LangGraph**. It plans research, retrieves evidence from web and academic sources, synthesizes the findings, and generates practical innovation ideas grounded in that research.

## Main capabilities

- **Multiple LLM providers:** Groq, Google Gemini, and Anthropic Claude.
- **Research planning:** creates focused search angles for a broad topic.
- **Multi-source research:** Tavily web search, arXiv academic search, and Wikipedia background search.
- **Research-driven innovation:** generates 3–5 project/product ideas from findings already collected. It does not run a separate search or claim global novelty.
- **Healthcare-aware safeguards:** healthcare ideas are framed as research or decision-support concepts, not diagnoses or treatment recommendations.
- **Context controls:** limits the number and size of retrieved results to reduce oversized LLM requests.
- **Secret-safe configuration:** API keys are loaded from environment variables and are not stored in source files.

## Architecture

```text
User topic
   |
   v
LangGraph ReAct research agent
   |
   +--> Query planner
   +--> Tavily web search (bounded results)
   +--> arXiv academic search (bounded results)
   +--> Wikipedia background search (optional)
   |
   v
Concise research synthesis
   |
   v
Innovation & Idea Generator
   |
   v
Research report + practical ideas
```

## Project structure

```text
autonomous-research-agent/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── llm_factory.py
│   ├── research_tools.py
│   ├── innovation_tool.py
│   └── agent.py
├── tests/
│   ├── test_innovation_tool.py
│   └── test_research_tools.py
├── .github/workflows/tests.yml
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## 1. Requirements

- Python 3.10 or newer
- An API key for one supported LLM provider
- A Tavily API key for web search

arXiv and Wikipedia searches do not require API keys.

## 2. Installation

Clone the repository:

```bash
git clone https://github.com/bosywahab818-a11y/autonomous-research-agent.git
cd autonomous-research-agent
```

Create and activate a virtual environment:

**Windows PowerShell**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure API keys

Copy the example environment file:

**Windows PowerShell**
```powershell
Copy-Item .env.example .env
```

**macOS / Linux**
```bash
cp .env.example .env
```

Open `.env` and add the key for your chosen LLM provider and your `TAVILY_API_KEY`. The default Groq output allowance is 1500 tokens to leave more room for the prompt and retrieved evidence under shared token-per-minute limits.

You can tune these settings in `.env`:

| Variable | Default | Purpose |
|---|---:|---|
| `TAVILY_MAX_RESULTS` | 2 | Web results per search |
| `WEB_RESULT_MAX_CHARS` | 2200 | Maximum web tool output |
| `ARXIV_RESULT_MAX_CHARS` | 1800 | Maximum arXiv tool output |
| `WIKIPEDIA_RESULT_MAX_CHARS` | 900 | Maximum Wikipedia tool output |
| `LLM_MAX_TOKENS` | 1500 | Maximum generated output tokens |

Choose your provider with `LLM_PROVIDER=groq`, `google`, or `anthropic`. Model names can be overridden in `.env`.

**Never commit your `.env` file or expose API keys in notebooks, screenshots, or source code.** The `.gitignore` excludes it.

## 4. Run the agent

```bash
python -m src.agent "Generative AI in Healthcare"
```

Or launch interactive mode:

```bash
python -m src.agent
```

The agent plans searches, uses a bounded number of web and academic searches, synthesizes the retrieved findings, and calls the innovation tool.

## 5. Innovation & Idea Generator

The custom tool receives the original topic and a concise synthesis of research findings. It generates 3–5 distinct ideas, each with the problem, proposed solution, research inspiration, suggested technologies, implementation outline, potential impact, feasibility, and risks. It also selects a top recommendation and lists assumptions requiring validation.

Ideas are proposals, not proof of novelty, feasibility, or clinical effectiveness.

## 6. Run tests

From the repository root, run:

```bash
pytest -q
```

The included `pytest.ini` adds the project root to the Python import path. Tests use a fake LLM where applicable and do not require API keys.

## Research quality and limitations

Retrieved text is bounded to help control model context size. This is a practical safeguard, not a guarantee that every provider request will fit its rate limits; quotas vary by model and account tier. If a provider still reports a token-per-minute limit, lower `LLM_MAX_TOKENS` or the per-tool result limits in `.env`.

Exact repeated text blocks are removed. This does not guarantee that semantically similar results or different URLs describing the same work will be deduplicated. Search ranking and LLM synthesis can still miss important work, misinterpret sources, or produce incomplete conclusions. Check original papers and trusted sources before relying on important claims.

arXiv includes preprints that may not have undergone peer review. Wikipedia is used for introductory context, not as a substitute for primary research.

For healthcare topics, generated concepts require expert review, privacy/security assessment, and appropriate clinical validation before real-world use. This project is for research and educational purposes, not medical advice.

## License

No license has been added. Add one if you want to define reuse permissions.
