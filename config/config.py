import os
import sys

# Add this to import environment variables
from dotenv import load_dotenv

# Set the base directory to the root of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

load_dotenv()

DEFAULT_EXTENSIONS = ['.py', '.java', '.json', '.xml', '.html', '.csv', '.md']


def get_allowed_extensions():
    return DEFAULT_EXTENSIONS


# Function to get the API key from environment variables
def get_api_key():
    return os.getenv("OPENAI_API_KEY")