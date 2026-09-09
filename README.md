<div align="center">
  <img src="assets/crewai_logo.png" alt="CrewAI Logo" width="420"/>
  <h3>Multi-Agent Workflows with CrewAI 1.x</h3>
  <p>Production-ready multi-agent implementations based on the DeepLearning.AI course, refactored for modern CrewAI standards.</p>
</div>

---

## Overview

This repository contains modernized implementations of the agentic workflows taught in DeepLearning.AI's **Multi-AI Agent Systems with crewAI**. The original course material was built on CrewAI `0.28.x` and LangChain wrappers; this repository updates those patterns to **CrewAI 1.x** (`1.15.20+`), utilizing native cloud LLM providers, structured environment configuration, and explicit agent delegation.

## Included Pipelines

### 1. Research & Editorial Pipeline (Lesson 2)
A sequential multi-agent workflow that coordinates planning, drafting, and editorial review.
* **Implementation:** [`main.py`](main.py) | [`crewai_agent.ipynb`](crewai_agent.ipynb)
* **Agents:**
  * **Content Planner:** Outlines topics, identifies key trends, target audiences, and SEO requirements.
  * **Content Writer:** Drafts the piece following the planner's structural outline.
  * **Editor:** Audits the draft for tone, factual framing, readability, and brand compliance.

### 2. Customer Support Automation with Grounded Scraping (Lesson 3)
A collaborative customer support workflow integrating live web scraping and quality assurance delegation.
* **Implementation:** [`customer_support.py`](customer_support.py) | [`customer_support.ipynb`](customer_support.ipynb)
* **Sample Output:** [`support_ticket_reply.md`](support_ticket_reply.md)
* **Agents & Tools:**
  * **Senior Support Representative:** Uses `ScrapeWebsiteTool` to fetch real-time documentation and construct grounded replies.
  * **Support QA Specialist:** Evaluates the draft for technical accuracy and tone, delegating back to the support agent if revisions are required.

---

## Technical Differences: Course (v0.28.x) vs. Modern (v1.x)

| Dimension | Legacy Course Code (`0.28.x`) | Modern Implementation (`1.15.x`) |
| :--- | :--- | :--- |
| **LLM Provider** | Dependent on deprecated `langchain_community` wrappers | Native CrewAI `LLM` engine via standard OpenAI-compatible endpoints |
| **Secret Management** | Interactive `getpass` calls (unstable in notebooks) | File-based `.env` loading via `python-dotenv` |
| **Agent Delegation** | Defaulted to `True` | Defaulted to `False`; explicitly configured (`allow_delegation=True`) on QA |
| **Tool Grounding** | Generic prompts prone to hallucination | Factual data retrieval through `ScrapeWebsiteTool` |
| **Logging Configuration** | Integer verbosity levels (`verbose=2`) | Strict boolean configuration (`verbose=True`) |
| **Output Schema** | Plain string return | Structured `CrewOutput` interface (`result.raw`, `result.token_usage`) |
| **Platform Compatibility** | Windows console character encoding crashes | Standardized UTF-8 stdout reconfiguration |

---

## Requirements

* Python 3.10 to 3.13
* Active API key for an OpenAI-compatible cloud provider:
  * **Fireworks AI** (`deepseek-v4-flash-0731`) &mdash; *Default, low latency*
  * **Groq** (`gpt-oss-20b` / `llama-3.3-70b-versatile`)
  * **OpenAI** (`gpt-4o-mini` / `gpt-4o`)

---

## Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Credentials
Copy the sample environment file:
```bash
cp .env.example .env
```
Populate `.env` with your API credentials:
```env
# Fireworks AI (Primary)
FIREWORKS_API_KEY=your_fireworks_api_key

# Groq (Alternative)
GROQ_API_KEY=your_groq_api_key

# OpenAI (Alternative)
OPENAI_API_KEY=your_openai_api_key
```

---

## Execution

### Customer Support Automation (`customer_support.py`)
Run with default ticket parameters:
```bash
python customer_support.py
```

Pass custom ticket arguments:
```bash
python customer_support.py --customer "AcmeCorp" --person "Jane Doe" --inquiry "How do I configure memory in CrewAI?"
```
*The audited response is printed to the console and exported to `support_ticket_reply.md`.*

### Content Generation Pipeline (`main.py`)
```bash
python main.py
```
Or specify a custom topic:
```bash
python main.py "Quantum Computing"
```

### Jupyter Notebooks
Both pipelines are available as standalone notebooks for interactive analysis:
* [`crewai_agent.ipynb`](crewai_agent.ipynb)
* [`customer_support.ipynb`](customer_support.ipynb)

---

## Repository Structure

```text
├── .env.example              # Sample environment configuration
├── .gitignore                # Excludes secrets, caches, and checkpoints
├── LICENSE                   # MIT License
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── main.py                   # Research & Editorial pipeline
├── crewai_agent.ipynb        # Research & Editorial notebook
├── customer_support.py       # Customer Support automation pipeline
├── customer_support.ipynb    # Customer Support automation notebook
├── support_ticket_reply.md   # Sample output from customer support execution
└── utils.py                  # Shared environment utilities
```

---

## License

This project is open source and available under the [MIT License](LICENSE).
