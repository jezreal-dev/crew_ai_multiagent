import os
import sys
import argparse
import warnings
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai_tools import ScrapeWebsiteTool


# -----------------------------------------------------------------------------
# 1. Environment & Encoding Setup
# -----------------------------------------------------------------------------


def setup_environment() -> str:
    """Configures console encoding, suppresses warnings, and loads Fireworks key."""

    # Ensure Windows console renders emojis and typography correctly
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass
    warnings.filterwarnings("ignore")

    # Load environment variables
    load_dotenv(override=True)
    api_key = os.getenv("FIREWORKS_API_KEY", "").strip().strip("'\"")
    if not api_key or api_key.startswith("your-"):
        print("\n" + "=" * 70)
        print("[!] ACTION REQUIRED: Fireworks API Key Missing")
        print("=" * 70)
        print("Please edit your '.env' file and add your key:")
        print("  FIREWORKS_API_KEY=fw_your_actual_key_here")
        print("Get your key from: https://fireworks.ai/api-keys")
        print("=" * 70 + "\n")
        sys.exit(1)
    return api_key


# -----------------------------------------------------------------------------
# 2. LLM Factory (Fireworks AI)
# -----------------------------------------------------------------------------

def get_llm(api_key: str) -> LLM:
    """Instantiates the modern CrewAI LLM connected to Fireworks AI."""
    return LLM(
        model="openai/accounts/fireworks/models/deepseek-v4-flash-0731",
        base_url="https://api.fireworks.ai/inference/v1",
        api_key=api_key,
        temperature=0.5,  # Moderate temperature for factual accuracy
    )


# -----------------------------------------------------------------------------
# 3. Agent Factory
# -----------------------------------------------------------------------------

def create_agents(llm: LLM) -> tuple[Agent, Agent]:
    """Creates the Support Agent and the QA Specialist."""

    support_agent = Agent(
        role="Senior Support Representative",
        goal="Be the most friendly and helpful support representative in your team",
        backstory=(
            "You work at crewAI (https://crewai.com) and are now working on providing "
            "support to {customer}, a super important customer for your company. "
            "You need to make sure that you provide the best support! "
            "Make sure to provide full, complete answers and make no assumptions."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=True,
    )

    # In CrewAI 1.x, allow_delegation must be True for the QA agent to delegate back
    qa_agent = Agent(
        role="Support Quality Assurance Specialist",
        goal="Get recognition for providing the best support quality assurance in your team",
        backstory=(
            "You work at crewAI (https://crewai.com) and are now working with your team "
            "on a request from {customer} ensuring that the support representative is "
            "providing the best support possible.\n"
            "You need to make sure that the support representative is providing full, "
            "complete answers, and make no assumptions."
        ),
        llm=llm,
        allow_delegation=True,
        verbose=True,
    )
    return support_agent, qa_agent


# -----------------------------------------------------------------------------
# 4. Task Factory
# -----------------------------------------------------------------------------

def create_tasks(
    support_agent: Agent, qa_agent: Agent, docs_url: str
) -> tuple[Task, Task]:
    """Builds the inquiry resolution task (with tool) and the QA review task."""
    docs_scrape_tool = ScrapeWebsiteTool(website_url=docs_url)

    inquiry_resolution = Task(
        description=(
            "{customer} just reached out with a super important ask:\n"
            "{inquiry}\n\n"
            "{person} from {customer} is the one that reached out. "
            "Make sure to use the documentation tool to provide the best, factually grounded support possible.\n"
            "You must strive to provide a complete and accurate response to the customer's inquiry."
        ),
        expected_output=(
            "A detailed, informative response to the customer's inquiry that addresses "
            "all aspects of their question.\n"
            "The response should include references to everything you used to find the answer, "
            "including external data or solutions. "
            "Ensure the answer is complete, leaving no questions unanswered, and maintain "
            "a helpful and friendly tone throughout."
        ),
        tools=[docs_scrape_tool],
        agent=support_agent,
    )
    quality_assurance_review = Task(
        description=(
            "Review the response drafted by the Senior Support Representative for {customer}'s inquiry.\n"
            "Ensure that the answer is comprehensive, accurate, and adheres to the high-quality standards "
            "expected for customer support.\n"
            "Verify that all parts of the customer's inquiry have been addressed thoroughly, "
            "with a helpful and friendly tone.\n"
            "If the draft lacks critical details or is incomplete, delegate back with constructive feedback.\n"
            "Check for references and sources used to find the information."
        ),
        expected_output=(
            "A final, detailed, and informative response ready to be sent to the customer.\n"
            "This response should fully address the customer's inquiry, incorporating all "
            "relevant feedback and improvements.\n"
            "Don't be too formal—maintain a professional, friendly, and approachable tone throughout."
        ),
        agent=qa_agent,
    )
    return inquiry_resolution, quality_assurance_review

# -----------------------------------------------------------------------------
# 5. Pipeline Orchestrator
# -----------------------------------------------------------------------------
def run_customer_support(
    customer: str,
    person: str,
    inquiry: str,
    docs_url: str = "https://docs.crewai.com/en/enterprise/guides/kickoff-crew",
):
    """Initializes the components, executes the crew, and saves the output."""
    api_key = setup_environment()
    llm = get_llm(api_key)
    support_agent, qa_agent = create_agents(llm)
    task1, task2 = create_tasks(support_agent, qa_agent, docs_url)

    crew = Crew(
        agents=[support_agent, qa_agent],
        tasks=[task1, task2],
        verbose=True,
    )
    print(f"\n[+] Starting Customer Support Crew for: {customer} ({person})")
    print(f"[+] Inquiry: {inquiry}\n")

    inputs = {"customer": customer, "person": person, "inquiry": inquiry}

    result = crew.kickoff(inputs=inputs)

    # 1. Print final response to terminal
    print("\n" + "=" * 60)
    print("FINAL APPROVED SUPPORT REPLY:")
    print("=" * 60)
    print(result.raw)

    # 2. Print token usage summary
    print("\n" + "=" * 60)
    print("TOKEN USAGE METRICS:")
    print("=" * 60)
    print(result.token_usage)

    # 3. Save copy to markdown file
    output_path = Path("support_ticket_reply.md")
    output_path.write_text(result.raw, encoding="utf-8")
    print(f"\n[✓] Reply exported to: {output_path.resolve()}\n")
    return result


# -----------------------------------------------------------------------------
# 6. Command-Line Interface
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Run CrewAI Multi-Agent Customer Support"
    )
    parser.add_argument(
        "--customer", default="DeepLearningAI", help="Customer/Company name"
    )
    parser.add_argument(
        "--person", default="Andrew Ng", help="Contact person name"
    )
    parser.add_argument(
        "--inquiry",
        default=(
            "I need help with setting up a Crew and kicking it off, specifically "
            "how can I add memory to my crew? Can you provide guidance?"
        ),
        help="The customer inquiry",
    )
    parser.add_argument(
        "--docs-url",
        default="https://docs.crewai.com/en/enterprise/guides/kickoff-crew",
        help="CrewAI documentation URL to scrape",
    )
    args = parser.parse_args()
    run_customer_support(
        customer=args.customer,
        person=args.person,
        inquiry=args.inquiry,
        docs_url=args.docs_url,
    )

if __name__ == "__main__":
    main()