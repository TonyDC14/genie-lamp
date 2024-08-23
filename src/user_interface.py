import streamlit as st


class UserInterface:
    def __init__(self):
        self.__project_folder = None
        self.__new_requirements = None
        self.__additional_docs = None

    def setup_page(self):
        st.set_page_config(layout="wide")
        st.title("Genie LAMP Interface")
        st.write("Use the sidebar to input your project details.")
        self.__collect_sidebar_inputs()

    def __collect_sidebar_inputs(self):
        with st.sidebar:
            self.__project_folder = st.text_input("Select Project Folder")
            self.__new_requirements = st.text_area("New Requirements / Changes", height=200)
            self.__additional_docs = st.text_area("Additional Documentation (Optional)", height=200)
            self.__submit_button = st.button("Submit")

    def submit_button_pressed(self):
        return self.__submit_button

    def get_project_folder(self):
        return self.__project_folder

    def get_new_requirements(self):
        return self.__new_requirements

    def get_additional_docs(self):
        return self.__additional_docs

    def get_additional_context(self):
        context = ""
        if self.__new_requirements:
            context += f"\n\nNew Requirements:\n{self.__new_requirements}"
        if self.__additional_docs:
            context += f"\n\nDocumentation:\n{self.__additional_docs}"
        return context

    @staticmethod
    def display_response(response):
        st.markdown("---")
        st.markdown(response, unsafe_allow_html=True)

    @staticmethod
    def display_error(message):
        st.error(message)
