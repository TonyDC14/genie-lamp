import logging
import sys
import os
import streamlit as st

# Set the base directory to the root of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


from config.config import get_allowed_extensions
from src.project_processor import ProjectProcessor
from src.prompt_generator import PromptGenerator
from src.openai_client import OpenAIClient


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def display_response(response):
    """
    Displays the OpenAI response in a formatted and readable way.
    """
    in_code_block = False
    code_block_content = ""

    # Use expander to allow collapsing large responses
    with st.expander("OpenAI Response", expanded=True):
        for line in response.splitlines():
            # Detect start and end of code blocks
            if line.strip().startswith("```") and not in_code_block:
                in_code_block = True
                code_block_content = ""
            elif line.strip().startswith("```") and in_code_block:
                in_code_block = False
                st.code(code_block_content, language="python")
            elif in_code_block:
                code_block_content += line + "\n"
            else:
                st.markdown(line)

def main():
    st.title("Project Enhancement Interface")

    project_folder = st.text_input("Select Project Folder")
    new_requirements = st.text_area("New Requirements / Changes", height=200)
    additional_docs = st.text_area("Additional Documentation (Optional)", height=200)

    if st.button("Submit"):
        logging.debug("Submit button clicked")
        if not project_folder:
            logging.error("No project folder provided")
            st.error("Please select a project folder.")
            return
        
        logging.debug(f"Project folder selected: {project_folder}")
        allowed_extensions = get_allowed_extensions()
        logging.debug(f"Allowed extensions: {allowed_extensions}")

        processor = ProjectProcessor(project_folder, allowed_extensions)
        project_files_content = processor.read_files_recursively()

        if not project_files_content:
            logging.error("No files found with the allowed extensions")
            st.error("No files found with the allowed extensions.")
            return

        logging.debug("Project files content successfully read")
        
        # Combine all information into a single prompt
        combined_prompt = f"This is my current programming project:\n{project_files_content}"
        if new_requirements:
            combined_prompt += f"\n\nNew Requirements:\n{new_requirements}"
        if additional_docs:
            combined_prompt += f"\n\nDocumentation:\n{additional_docs}"

        logging.debug("Combined prompt created successfully")

        # Initialize OpenAI client
        openai_client = OpenAIClient(api_key="your-api-key-here")

        # Send the single, combined prompt to OpenAI
        response = openai_client.openai_chat_request_prompt("This is a programming project", combined_prompt, max_tokens=2048)

        logging.debug("Response received from OpenAI API")
        logging.debug(str(response))

        # Display the single, final response
        display_response(response)

if __name__ == "__main__":
    main()
