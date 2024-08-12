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
        """
        file_contents = []
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                if any(file.endswith(ext) for ext in self.allowed_extensions):
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                        file_contents.append(f"---\n{file}\n---\n{content}\n")
        return "\n".join(file_contents)
