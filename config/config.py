# config/config.py

DEFAULT_EXTENSIONS = ['.py', '.java', '.json', '.xml', '.html', '.csv', '.md']

def get_allowed_extensions():
    """
    Returns the default list of file extensions to include in the project processing.
    """
    return DEFAULT_EXTENSIONS
