import os
import sys
import warnings
from dotenv import load_dotenv
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

# Ensure Windows PowerShell handles UTF-8 (emojis and special punctuation)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Suppress unnecessary third-party warnings
warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew, LLM

def run_crew(topic: str = "Jezreal Oseiwe Momoh"):
    # Load environment variables
    load_dotenv(override=True)
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    if not groq_api_key or groq_api_key.strip() == "" or groq_api_key.startswith("your-"):
        print("\n" + "="*70)
        print("[!] ACTION REQUIRED: Groq API Key Not Set")
        print("="*70)
        print("1. Visit: https://console.groq.com/keys (free signup)")
        print("2. Create a free API key (starts with 'gsk_')")
        print("3. In your '.env' file, paste:")
        print("   GROQ_API_KEY=gsk_...")
        print("="*70 + "\n")
        return None

    model_name = os.getenv("MODEL_NAME", "groq/llama-3.3-70b-versatile")
    print(f"Initializing CrewAI with Groq model: {model_name}...")

    # Modern CrewAI: Connect to Groq's 20B model via native OpenAI-compatible endpoint
    llm = LLM(
        model="openai/openai/gpt-oss-20b",
        base_url="https://api.groq.com/openai/v1",
        api_key=groq_api_key,
        temperature=0.7
    )

    search_tool = SerperDevTool()
    # 1. Modern Agent Definitions
    planner = Agent(
        role="Content Planner",
        goal=f"Plan engaging and factually accurate content on {topic}",
        tools=[search_tool],
        backstory="You're working on planning a blog article "
                  f"about the topic: {topic}. "
                  "You collect key information to help the reader learn something valuable. "
                  "Keep outlines focused and actionable.",
        llm=llm,
        verbose=True
    )

    writer = Agent(
        role="Content Writer",
        goal=f"Write insightful and factually accurate opinion piece about the topic: {topic}",
        backstory=f"You're writing a concise article about the topic: {topic}. "
                  "You base your writing on the Content Planner's outline. "
                  "You provide objective and impartial insights clearly and concisely.",
        llm=llm,
        verbose=True
    )

    editor = Agent(
        role="Editor",
        goal="Edit a given blog post to align with the writing style of the organization.",
        backstory="You are an editor reviewing the blog post to ensure clarity, "
                  "journalistic best practices, and balanced viewpoints.",
        llm=llm,
        verbose=True
    )

    # 2. Modern Task Definitions (concise to optimize for cloud TPM limits)
    plan = Task(
        description=(
            f"1. Identify the key trends and takeaways on {topic}.\n"
            "2. Create a concise content outline (intro, 2 main points, conclusion).\n"
            "3. Keep the outline under 200 words."
        ),
        expected_output="A concise content outline under 200 words.",
        agent=planner,
    )

    write = Task(
        description=(
            f"1. Use the content plan to craft a compelling, concise blog post on {topic}.\n"
            "2. Structure with an introduction, 2 short body sections, and a conclusion.\n"
            "3. Total length should be around 300-400 words."
        ),
        expected_output="A polished 300-400 word blog post in markdown format.",
        agent=writer,
    )

    edit = Task(
        description="Proofread and polish the given blog post for grammar, tone, and readability. Keep it concise.",
        expected_output="The final publication-ready markdown blog post.",
        agent=editor,
    )

    # 3. Modern Crew Definition
    crew = Crew(
        agents=[planner, writer, editor],
        tasks=[plan, write, edit],
        verbose=True
    )

    # 4. Kickoff & Output Handling
    print(f"\nStarting Crew execution for topic: '{topic}'...\n")
    result = crew.kickoff(inputs={"topic": topic})

    print("\n" + "="*50)
    print("FINAL ARTICLE (MARKDOWN):")
    print("="*50)
    print(result.raw)

    print("\n" + "="*50)
    print("TOKEN USAGE:")
    print("="*50)
    print(result.token_usage)

    return result

if __name__ == "__main__":
    topic_input = sys.argv[1] if len(sys.argv) > 1 else "Jezreal Oseiwe Momoh"
    run_crew(topic_input)
