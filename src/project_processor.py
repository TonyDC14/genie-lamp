import os
import re

from config.config import ConfigManager


class ProjectProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.allowed_extensions = ConfigManager.get_allowed_extensions()
        self.ignored_folders = ConfigManager.get_ignored_folders()

    def read_files_recursively(self) -> str:
        file_reader = FileReader(self.folder_path, self.allowed_extensions, self.ignored_folders)
        return file_reader.read_files()


class FileReader:
    def __init__(self, folder_path, allowed_extensions, ignored_folders):
        self.folder_path = folder_path
        self.allowed_extensions = allowed_extensions
        self.ignored_folders = ignored_folders

    def read_files(self):
        contents = []
        for root, dirs, files in self.__walk_directory():
            contents.extend(self.__process_files(root, files))
        return "\n".join(contents)

    def __walk_directory(self):
        for root, dirs, files in os.walk(self.folder_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in self.ignored_folders]
            yield root, dirs, files

    def __process_files(self, root, files):
        contents = []
        for file in files:
            if self.__is_allowed_extension(file):
                contents.append(self.__read_file_content(root, file))
        return contents

    def __is_allowed_extension(self, file):
        return any(file.endswith(ext) for ext in self.allowed_extensions)

    def __read_file_content(self, root, file):
        file_path = os.path.join(root, file)
        relative_path = os.path.relpath(str(file_path), str(self.folder_path))
        return FileContentProcessor(file_path, relative_path).get_processed_content()


class FileContentProcessor:
    def __init__(self, file_path, relative_path):
        self.file_path = file_path
        self.relative_path = relative_path

    def get_processed_content(self):
        content = self.__try_open_file('utf-8') or self.__try_open_file('ISO-8859-1')
        if not content:
            print(f"Skipping file due to encoding issues: {self.file_path}")
            return ''
        return f"§ {self.relative_path} § {content} §"

    def __try_open_file(self, encoding):
        try:
            with open(self.file_path, 'r', encoding=encoding) as f:
                content = f.read()
                return self.__process_content(content)
        except UnicodeDecodeError:
            return None

    def __process_content(self, content):
        content = CommentRemover.remove_comments(content, self.__get_extension())
        return ContentCleaner.clean(content)

    def __get_extension(self):
        return os.path.splitext(self.file_path)[1]


class CommentRemover:
    @staticmethod
    def remove_comments(content, file_extension):
        if file_extension in ['.py', '.sh']:
            return re.sub(r'#.*$', '', content, flags=re.MULTILINE)
        elif file_extension in ['.js', '.cpp', '.c']:
            return re.sub(r'//.*?$|/\*.*?\*/', '', content, flags=re.MULTILINE | re.DOTALL)
        return content


class ContentCleaner:
    @staticmethod
    def clean(content):
        return re.sub(r'\s+', ' ', content).strip()
