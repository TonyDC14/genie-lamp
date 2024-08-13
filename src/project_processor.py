import os
import re


class ProjectProcessor:
    """
    Handles the processing of project files, reading their contents based on allowed extensions.
    """

    def __init__(self, folder_path, allowed_extensions):
        self.folder_path = folder_path
        self.allowed_extensions = allowed_extensions

    def read_files_recursively(self):
        """
        Recursively reads files from the specified folder path, filtering by allowed extensions
        and ignoring files inside hidden folders (folders starting with a dot).
        Tries to handle different file encodings gracefully.
        """
        file_contents = []
        for root, dirs, files in os.walk(self.folder_path):
            # Filter out hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for file in files:
                file_extension = os.path.splitext(file)[1]  # Extract file extension
                if any(file.endswith(ext) for ext in self.allowed_extensions):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(str(file_path), str(self.folder_path))  # Get relative path
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            content = self.remove_comments(content, file_extension)
                            content = self.clean_content(content)  # Clean the content of the file
                    except UnicodeDecodeError:
                        # If utf-8 decoding fails, try with a different encoding (ISO-8859-1)
                        try:
                            with open(file_path, 'r', encoding='ISO-8859-1') as f:
                                content = f.read()
                                content = self.remove_comments(content, file_extension)
                                content = self.clean_content(content)  # Clean the content of the file
                        except UnicodeDecodeError:
                            # If all decodings fail, skip the file
                            print(f"Skipping file due to encoding issues: {file_path}")
                            continue

                    file_contents.append(f"§{relative_path}§{content}§")  # Using § as a delimiter
        return "\n".join(file_contents)

    @staticmethod
    def remove_comments(content, file_extension):
        """
        Removes comments from the content based on file extension.
        """
        if file_extension in ['.py', '.sh']:  # Python, Shell scripts
            # Remove comments starting with #
            content = re.sub(r'#.*$', '', content, flags=re.MULTILINE)
        elif file_extension in ['.js', '.cpp', '.c']:  # JavaScript, C++, C
            # Remove comments starting with // and /* */
            content = re.sub(r'//.*?$|/\*.*?\*/', '', content, flags=re.MULTILINE | re.DOTALL)
        return content

    @staticmethod
    def clean_content(content):
        """
        Cleans up the content by replacing multiple newlines and excessive whitespace with a single space.
        """
        cleaned_content = re.sub(r'\s+', ' ', content)
        return cleaned_content.strip()  # Remove leading and trailing spaces
