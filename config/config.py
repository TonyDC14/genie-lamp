import os
import sys

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

load_dotenv()


class ConfigManager:
    DEFAULT_EXTENSIONS = ['.py', '.java', '.md']

    @classmethod
    def get_allowed_extensions(cls):
        extensions = os.getenv("DEFAULT_EXTENSIONS")
        return extensions.split(",") if extensions else cls.DEFAULT_EXTENSIONS

    @classmethod
    def get_openai_model_max_tpm(cls):
        return os.getenv("OPENAI_MODEL_MAX_TPM")

    @classmethod
    def get_openai_model(cls):
        return os.getenv("OPENAI_MODEL")

    @classmethod
    def get_openai_api_key(cls):
        return os.getenv("OPENAI_API_KEY")

    @classmethod
    def get_ignored_folders(cls):
        folders = os.getenv("IGNORED_FOLDERS")
        return folders.split(",") if folders else []
