# Multi-Agent Systems with CrewAI 🤖🚀

A modernized, production-ready implementation of multi-agent workflows based on the DeepLearning.AI **Multi-AI Agent Systems with crewAI** course, updated for **CrewAI 1.x** (`1.15.20+`).

This repository demonstrates how to architect, ground, and run autonomous AI agents in parallel and sequence using cloud LLMs (Fireworks AI, Groq, or OpenAI) without local hardware constraints or deprecated LangChain wrappers.

---

## 📂 Projects Included

### 1. Research & Content Creation Crew (Lesson 2)
A sequential multi-agent editorial team that researches, drafts, and proofreads articles on any given topic.
* **Notebook:** [`crewai_agent.ipynb`](crewai_agent.ipynb)
* **Script:** [`main.py`](main.py)
* **Agents:**
  * 📋 **Content Planner:** Outlines key trends, audience analysis, and SEO keywords.
  * ✍️ **Content Writer:** Drafts a cohesive, insightful article based on the outline.
  * 🧐 **Editor:** Polishes grammar, verifies tone, and ensures journalistic integrity.

### 2. Automated Customer Support with Web Scraping (Lesson 3)
A collaborative customer support pipeline that retrieves live documentation via web scraping and performs quality-assurance audits with agent delegation.
* **Notebook:** [`customer_support.ipynb`](customer_support.ipynb)
* **Script:** [`customer_support.py`](customer_support.py)
* **Exported Sample Output:** [`support_ticket_reply.md`](support_ticket_reply.md)
* **Agents & Tools:**
  * 🎧 **Senior Support Representative:** Uses `ScrapeWebsiteTool` to extract real-time documentation and formulate factually grounded replies.
  * 🛡️ **QA Specialist:** Audits answers for accuracy, completeness, and friendly tone, with `allow_delegation=True` to send feedback back to the Support Agent for revisions.

---

## ⚡ Key Modernizations (Course v0.28 vs. Modern v1.x)

| Feature | Legacy Course (`0.28.x`) | Modern Implementation (`1.15.x`) |
| :--- | :--- | :--- |
| **LLM Engine** | Tied to legacy `langchain_community` wrappers | Native CrewAI `LLM` class connecting to any OpenAI-compatible cloud provider |
| **Credentials** | Interactive `getpass.getpass()` (freezes in notebooks) | Robust `.env` loading via `python-dotenv` |
| **Agent Delegation** | Defaulted to `True` | Defaulted to `False` (explicitly configured `allow_delegation=True` on QA) |
| **Tool Execution** | Basic scraping | Grounded `ScrapeWebsiteTool` preventing hallucination on real URLs |
| **Terminal Output** | Crashed on Windows PowerShell with emoji encodings | Built-in UTF-8 stdout configuration (`sys.stdout.reconfigure`) |
| **Output Object** | Raw string | Modern `CrewOutput` interface (`result.raw` and `result.token_usage`) |

---

## 🛠️ Tech Stack & Requirements

* **Python:** `3.10+` (Tested on `3.13`)
* **Framework:** `crewai==1.15.20`
* **Tools:** `crewai-tools==1.15.20`
* **Supported Cloud LLMs:**
  * **Fireworks AI** (`deepseek-v4-flash-0731`) — *Recommended: High throughput, sub-second latency*
  * **Groq** (`llama-3.3-70b-versatile` / `gpt-oss-20b`) — *Free cloud tier*
  * **OpenAI** (`gpt-4o-mini` / `gpt-4o`)

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
# Or directly:
pip install "crewai[tools]==1.15.20" python-dotenv requests
```

### 3. Configure API Keys
Copy the example environment file:
```bash
cp .env.example .env
```
Open `.env` and add your API keys:
```env
# Fireworks AI (Recommended)
FIREWORKS_API_KEY=fw_your_actual_key_here

# Groq (Optional free cloud backup)
GROQ_API_KEY=gsk_your_actual_key_here

# OpenAI (Optional)
OPENAI_API_KEY=sk-your_actual_key_here
```

---

## 💻 Running the Projects

### Running Customer Support Automation
```bash
# Run with default inquiry (Andrew Ng / DeepLearningAI)
python customer_support.py

# Or pass custom ticket parameters from the command line:
python customer_support.py --customer "TechCorp" --person "Alice" --inquiry "How do custom tools work in CrewAI?"
```
*The finalized, QA-approved response will be automatically exported to `support_ticket_reply.md`.*

### Running the Article Generator
```bash
# Run with default topic
python main.py

# Or pass a custom topic:
python main.py "Quantum Computing"
```

### Running in Jupyter Notebook
If you prefer an interactive notebook experience:
1. Launch Jupyter:
   ```bash
   jupyter notebook
   ```
2. Open [`crewai_agent.ipynb`](crewai_agent.ipynb) or [`customer_support.ipynb`](customer_support.ipynb).
3. Click **Restart Kernel** and **Run All Cells**.

---

## 📁 Repository Structure

```text
├── .env.example              # Template environment variables file
├── .gitignore                # Safeguards API keys and checkpoints
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── main.py                   # Standalone Content Creation Crew (Lesson 2)
├── crewai_agent.ipynb        # Content Creation Notebook (Lesson 2)
├── customer_support.py       # Standalone Customer Support Crew (Lesson 3)
├── customer_support.ipynb    # Customer Support Notebook (Lesson 3)
├── support_ticket_reply.md   # Sample output generated by customer support agents
└── utils.py                  # Environment and credential utility functions
```

---

## 📜 License
MIT License. Feel free to use, modify, and learn from this implementation!
