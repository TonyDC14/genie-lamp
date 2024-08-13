import os

# Add this to import environment variables
from dotenv import load_dotenv
load_dotenv()

DEFAULT_EXTENSIONS = ['.py', '.java', '.json', '.xml', '.html', '.csv', '.md']


def get_allowed_extensions():
    return DEFAULT_EXTENSIONS


# Function to get the API key from environment variables
def get_api_key():
    return os.getenv("OPENAI_API_KEY")