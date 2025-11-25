from strands import Agent
from strands.models.gemini import GeminiModel
import os
from dotenv import load_dotenv

load_dotenv()

# Check if API key exists
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in .env file")
    exit(1)

model = GeminiModel(
        client_args={"api_key": os.getenv("GEMINI_API_KEY")},
        model_id="gemini-2.5-flash",
        params={"temperature": 0.15},  # Lower temperature for consistent test behavior
    )


def get_agent(tools):
    return Agent(model=model, tools=tools)
