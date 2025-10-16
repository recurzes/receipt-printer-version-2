from dotenv import load_dotenv
import os
import todoist_api_python
from todoist_api_python.api import TodoistAPI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_TOKEN = os.getenv("GEMINI_API_KEY")
TODOIST_SECRET = os.getenv("TODOIST_SECRET")
TODOIST_VERIFICATION_TOKEN = os.getenv("TODOIST_VERIFICATION_TOKEN")
TODOIST_TEST_TOKEN = os.getenv("TODOIST_TEST_TOKEN")
TODOIST_API_TOKEN = os.getenv("TODOIST_API_TOKEN")

todoist = TodoistAPI(TODOIST_API_TOKEN)