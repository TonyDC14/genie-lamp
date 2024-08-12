# src/project_processor.py

import os

class ProjectProcessor:
    """
    Handles the processing of project files, reading their contents based on allowed extensions.
    """
    def __init__(self, folder_path, allowed_extensions):
        self.folder_path = folder_path
        self.allowed_extensions = allowed_extensions

    def read_files_recursively(self):
        """
        Recursively reads files from the specified folder path, filtering by allowed extensions.
        Tries to handle different file encodings gracefully.
        """
        file_contents = []
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                if any(file.endswith(ext) for ext in self.allowed_extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except UnicodeDecodeError:
                        # If utf-8 decoding fails, try with a different encoding (ISO-8859-1)
                        try:
                            with open(file_path, 'r', encoding='ISO-8859-1') as f:
                                content = f.read()
                        except UnicodeDecodeError:
                            # If all decodings fail, skip the file
                            print(f"Skipping file due to encoding issues: {file_path}")
                            continue
                    
                    file_contents.append(f"---\n{file}\n---\n{content}\n")
        return "\n".join(file_contents)
