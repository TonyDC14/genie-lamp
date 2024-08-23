import logging
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.project_processor import ProjectProcessor
from config.config import ConfigManager
from src.user_interface import UserInterface
from src.openai_client import OpenAIClient
from src.prompt_generator import PromptBuilder, PromptProcessor


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    user_interface = UserInterface()
    user_interface.setup_page()

    if user_interface.submit_button_pressed():
        project_processor = ProjectProcessor(user_interface.get_project_folder())
        project_files_content = project_processor.read_files_recursively()
        logger.debug("-------------- Project processed successfully")
        logger.debug(project_files_content)

        if project_files_content:
            logger.debug("-------------- Building model prompt request")
            prompt_generator = PromptBuilder(
                project_files_content,
                user_interface.get_new_requirements(),
                user_interface.get_additional_context(),
                PromptProcessor(ConfigManager.get_openai_model(), ConfigManager.get_openai_model_max_tpm())
            ).build()
            logger.debug(f"-------------- Built prompt with ({len(prompt_generator.generated_prompts)}) elements")

            openai_client = OpenAIClient(
                api_key=ConfigManager.get_openai_api_key(), model=ConfigManager.get_openai_model()
            )
            response = openai_client.ask_by_chunks(prompt_generator.generated_prompts)
            user_interface.display_response(response)
        else:
            user_interface.display_error("No files found with the allowed extensions.")


if __name__ == "__main__":
    main()
