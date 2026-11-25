# Autonomous Research Agent

An extensible research assistant built with **LangChain** and **LangGraph**. It researches a topic using web and academic sources, then turns the collected findings into structured research insights and practical innovation ideas.

## Main capabilities

- **Multiple LLM providers:** Groq, Google Gemini, and Anthropic Claude.
- **Research planning:** decomposes a broad topic into focused search questions.
- **Multi-source research:** Tavily web search, arXiv academic search, and Wikipedia background search.
- **Research-driven innovation:** generates 3–5 project/product ideas grounded in the findings already collected. It does not run a separate search or claim that an idea is globally novel.
- **Healthcare-aware safeguards:** healthcare ideas are framed as research or decision-support concepts, not diagnoses or treatment recommendations.
- **Secret-safe configuration:** API keys are loaded from environment variables and are not stored in source files.

## Architecture

```text
User topic
   |
   v
LangGraph ReAct research agent
   |
   +--> Query planner
   |
   +--> Tavily web search
   +--> arXiv academic search
   +--> Wikipedia background search
   |
   v
Research synthesis
   |
   v
Innovation & Idea Generator
   |
   v
Research report + practical ideas
```

The agent is instructed to plan searches, collect evidence from multiple sources, synthesize the findings, and then call the innovation tool with the research it has gathered.

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
├── .env.example
├── .gitignore
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

Open `.env` and add:
- The key for your chosen LLM provider.
- Your `TAVILY_API_KEY`.

Choose your provider with `LLM_PROVIDER=groq`, `google`, or `anthropic`. The model names can be overridden in `.env`.

**Never commit your `.env` file or expose API keys in notebooks, screenshots, or source code.** The `.gitignore` excludes it.

## 4. Run the agent

Run the requested healthcare example:

```bash
python -m src.agent "Generative AI in Healthcare"
```

Or launch interactive mode:

```bash
python -m src.agent
```

The agent will research the topic and produce a report with an innovation section. The exact number and content of ideas depend on the findings retrieved and the selected LLM.

## 5. Innovation & Idea Generator

The custom tool receives:
- The original research topic.
- A synthesis of the research findings collected by the agent.

For each idea, it returns:
1. Title
2. Problem addressed
3. Proposed solution
4. Research inspiration
5. Suggested technologies
6. Implementation outline
7. Potential impact
8. Feasibility
9. Risks and limitations

It also selects a top recommendation and lists assumptions that need validation. Ideas are proposals, not proof of novelty, feasibility, or clinical effectiveness.

## 6. Run tests

The tests use a fake LLM and do not require API keys:

```bash
pytest -q
```

## Research quality and limitations

The query planner encourages complementary searches across multiple sources. Results from the same URL or title are de-duplicated where applicable. Search ranking and LLM synthesis can still miss important work, misinterpret sources, or produce incomplete conclusions. Check original papers and trusted sources before relying on important claims.

arXiv includes preprints that may not have undergone peer review. Wikipedia is used for introductory context, not as a substitute for primary research.

For healthcare topics, generated concepts must undergo expert review, privacy/security assessment, and appropriate clinical validation before real-world use. This project is for research and educational purposes, not medical advice.

## License

No license has been added. Add one if you want to define reuse permissions.
