import logging
import os
import sys
import streamlit as st
import tiktoken

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from config.config import get_allowed_extensions, get_api_key
from src.project_processor import ProjectProcessor
from src.openai_client import OpenAIClient

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def display_response(response):
    """ Displays the OpenAI response as Markdown. """
    st.markdown(response, unsafe_allow_html=True)


def split_text(text, max_tokens=4096):
    encoding = tiktoken.encoding_for_model("gpt-4")
    tokens = encoding.encode(text)
    chunks = []
    current_chunk = []

    for token in tokens:
        current_chunk.append(token)
        if len(current_chunk) >= max_tokens:
            chunks.append(current_chunk)
            current_chunk = []

    if current_chunk:
        chunks.append(current_chunk)

    return [encoding.decode(chunk) for chunk in chunks]


def main():
    st.set_page_config(layout="wide")
    st.title("Genie LAMP Interface")
    st.write("Use the sidebar to input your project details.")

    with st.sidebar:
        project_folder = st.text_input("Select Project Folder")
        new_requirements = st.text_area("New Requirements / Changes", height=200)
        additional_docs = st.text_area("Additional Documentation (Optional)", height=200)
        submit_button = st.button("Submit")

    st.markdown("---")

    if submit_button:
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

        combined_prompt = f"This is my current programming project:\n{project_files_content}"
        if new_requirements:
            combined_prompt += f"\n\nNew Requirements:\n{new_requirements}"
        if additional_docs:
            combined_prompt += f"\n\nDocumentation:\n{additional_docs}"

        logging.debug("Combined prompt created successfully")
        logging.debug("Prompt:" + str(combined_prompt))

        openai_client = OpenAIClient(api_key=get_api_key())
        chunks = split_text(combined_prompt, max_tokens=2000000)
        final_prompt = ("Now given all this context, I need you to solve the <requirements>, generate a full detailed "
                        "explanation of how to solve the requirements with code snippets if possible")
        response = openai_client.send_chunks_with_context(chunks, final_prompt, max_tokens=2000000)

        logging.debug("Response received from OpenAI API")
        logging.debug(str(response))
        display_response(response)


if __name__ == "__main__":
    main()