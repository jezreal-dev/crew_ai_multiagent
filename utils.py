import os
from pathlib import Path
from dotenv import load_dotenv

def get_groq_api_key():
    """Load Groq API key from .env file or environment variable."""
    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(dotenv_path=env_path, override=True)
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key.strip() == "" or api_key.startswith("your-"):
        raise ValueError(
            "\n[!] GROQ_API_KEY is not set or is still the placeholder.\n"
            "1. Visit https://console.groq.com/keys (free signup)\n"
            "2. Create an API key (starts with 'gsk_')\n"
            "3. Paste it in your .env file:\n"
            "   GROQ_API_KEY=gsk_...\n"
        )
    
    api_key = api_key.strip().strip("'\"")
    os.environ["GROQ_API_KEY"] = api_key
    return api_key

def get_openai_api_key():
    """Alias for backwards compatibility with the course."""
    return get_groq_api_key()