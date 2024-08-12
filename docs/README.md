# Project Enhancer

## Overview

This project provides a Streamlit interface to enhance your programming projects by interacting with OpenAI's API. You can upload your project files, specify new requirements, and provide additional documentation. The application will then generate prompts to OpenAI, which will return suggestions and changes for your project.

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/TonyDC14/genie-lamp.git
    cd genie-lamp
    ```

2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Run the application:
    ```
    streamlit run src/main.py
    ```

## Usage

- **Project Folder**: Select the folder of your project.
- **New Requirements/Changes**: Specify the changes you want to make.
- **Additional Documentation**: Optionally, provide additional documentation.
- **Submit**: The application will process the files and send requests to OpenAI.

## Testing

Run the tests:
    ```
    python -m unittest discover -s tests
    ```