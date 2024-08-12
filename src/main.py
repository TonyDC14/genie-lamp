# src/main.py

import streamlit as st
from config.config import get_allowed_extensions
from src.project_processor import ProjectProcessor
from src.prompt_generator import PromptGenerator
from src.openai_client import OpenAIClient

def main():
    st.title("Project Enhancement Interface")

    project_folder = st.text_input("Select Project Folder")
    new_requirements = st.text_area("New Requirements / Changes", height=200)
    additional_docs = st.text_area("Additional Documentation (Optional)", height=200)

    if st.button("Submit"):
        if not project_folder:
            st.error("Please select a project folder.")
            return
        
        allowed_extensions = get_allowed_extensions()
        processor = ProjectProcessor(project_folder, allowed_extensions)
        project_files_content = processor.read_files_recursively()

        if not project_files_content:
            st.error("No files found with the allowed extensions.")
            return

        prompt_generator = PromptGenerator(project_files_content, new_requirements, additional_docs)
        project_prompts = prompt_generator.generate_prompts(max_length=2048)

        openai_client = OpenAIClient(api_key="your-api-key-here")
        responses = openai_client.send_prompts_in_chunks(project_prompts)

        st.write("OpenAI Responses:")
        for i, response in enumerate(responses):
            st.text_area(f"Response {i + 1}", response, height=200)

if __name__ == "__main__":
    main()
