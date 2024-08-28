# Genie Lamp

## Overview

This project provides a Streamlit interface to enhance your programming projects by interacting with OpenAI's API. You can upload your project files, specify new requirements, and provide additional documentation. The application will then generate prompts to OpenAI, which will return suggestions and changes for your project.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/TonyDC14/genie-lamp.git
    cd genie-lamp
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
   If you're using Anaconda or Miniconda, you can install the necessary dependencies directly using conda:
   ```bash
   conda install -c conda-forge pillow python-dotenv tenacity
   ```

3. Run the application:
    ```bash
    streamlit run genie.py
    ```

## Usage

Once the application is running, you will see three main input fields:

### 1. **Project Folder**

This field allows you to specify the folder that contains your project files. The application will recursively read all files with the allowed extensions from this folder.

**Example:**

```plaintext
/home/user/my_python_project/
```

### 2. **New Requirements / Changes**

In this text area, you can describe the new requirements or changes you want to implement in your project. Be as detailed as possible so that OpenAI can provide accurate suggestions.

**Example:**

```plaintext
I need to refactor the existing codebase to improve performance. Specifically, I want to optimize the database queries to reduce load times. Additionally, I would like to add a new feature that allows users to export data to CSV format.
```

### 3. **Additional Documentation (Optional)**

Here, you can provide any additional documentation that might be relevant to the project, such as API documentation, design guidelines, or specific constraints. This field is optional, but including it can help OpenAI provide more accurate and context-aware suggestions.

**Example:**

```plaintext
The project uses the Django web framework. Please refer to the Django REST framework documentation for handling API requests. Additionally, the project follows the MVC architectural pattern.
```

### Submitting the Form

After filling in these fields, click the "Submit" button. The application will:

1. **Process the Project Files:** Read all files in the specified folder with the allowed extensions.
2. **Generate Prompts:** Combine the project files, new requirements, and any additional documentation into one or more prompts.
3. **Interact with OpenAI:** Send the prompts to OpenAI and receive suggestions or changes.
4. **Display Responses:** Show the responses from OpenAI in the Streamlit interface.

## Example Workflow

1. **Project Folder:** `/home/user/my_python_project/`
2. **New Requirements / Changes:**
    ```plaintext
    I want to implement user authentication using OAuth2. Additionally, I need to refactor the existing code to use async functions where appropriate to improve performance.
    ```
3. **Additional Documentation:**
    ```plaintext
    This project uses FastAPI. Refer to the FastAPI documentation on asynchronous programming for best practices.
    ```

After clicking "Submit," the application will process this information and provide detailed responses on how to achieve these requirements and changes.

## License
None -> We don´t do that here ;)