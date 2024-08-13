import logging
import os
import sys

import streamlit as st

# Set the base directory to the root of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


from config.config import get_allowed_extensions, get_api_key
from src.project_processor import ProjectProcessor
from src.openai_client import OpenAIClient


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def display_response(response):
    """ Displays the OpenAI response in a formatted and readable way, handling nested code blocks. """
    in_code_block = False
    code_block_content = ""
    final_output = []

    with st.expander("OpenAI Response", expanded=True):
        lines = response.splitlines()
        for line in lines:
            if line.strip().startswith("```"):
                if not in_code_block:
                    # Entering a code block
                    in_code_block = True
                    code_block_content = ""
                else:
                    # Exiting a code block
                    in_code_block = False
                    final_output.append("```")
                    final_output.append(code_block_content.strip())
                    final_output.append("```")
            elif in_code_block:
                # Add lines to code block content, ignoring nested code blocks
                if not line.strip().startswith("```"):
                    code_block_content += line + "\n"
            else:
                # Normal line outside of code blocks
                final_output.append(line)

        # Render the final output
        for item in final_output:
            if item.startswith("```"):
                # It's a code block, render as code
                st.code(item, language="python")
            else:
                # It's normal text, render as Markdown
                st.markdown(item)


def main():
    st.title("Genie LAMP Interface")

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
        logging.debug("Prompt:" + str(combined_prompt))

        # Initialize OpenAI client
        openai_client = OpenAIClient(api_key=get_api_key())

        # Send the single, combined prompt to OpenAI
        response = openai_client.openai_chat_request_prompt("This is a programming project", combined_prompt, max_tokens=2048)

        logging.debug("Response received from OpenAI API")
        logging.debug(str(response))

        # Display the single, final response
        display_response(response)


if __name__ == "__main__":
    main()
