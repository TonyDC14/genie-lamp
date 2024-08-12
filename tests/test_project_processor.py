import unittest
from src.project_processor import ProjectProcessor
import os

class TestProjectProcessor(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment before each test.
        """
        self.folder_path = "test_folder"
        self.allowed_extensions = ['.py', '.md', '.txt']
        os.makedirs(self.folder_path, exist_ok=True)

    def tearDown(self):
        """
        Clean up the test environment after each test.
        """
        # Remove all files and the test folder after each test
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                os.remove(os.path.join(root, file))
        os.rmdir(self.folder_path)

    def test_read_files_recursively_python_file(self):
        """
        Test reading a single Python file.
        """
        file_path = os.path.join(self.folder_path, "test.py")
        with open(file_path, 'w') as f:
            f.write("print('Hello, World!')")
        
        processor = ProjectProcessor(self.folder_path, self.allowed_extensions)
        content = processor.read_files_recursively()
        
        self.assertIn("print('Hello, World!')", content)
    
    def test_read_files_recursively_markdown_file(self):
        """
        Test reading a single Markdown file.
        """
        file_path = os.path.join(self.folder_path, "README.md")
        with open(file_path, 'w') as f:
            f.write("# This is a markdown file")
        
        processor = ProjectProcessor(self.folder_path, self.allowed_extensions)
        content = processor.read_files_recursively()
        
        self.assertIn("# This is a markdown file", content)

    def test_read_files_recursively_ignore_non_allowed_files(self):
        """
        Test that files with non-allowed extensions are ignored.
        """
        file_path = os.path.join(self.folder_path, "test.txt")
        with open(file_path, 'w') as f:
            f.write("This is a text file.")
        
        processor = ProjectProcessor(self.folder_path, ['.py'])  # Only allow .py files
        content = processor.read_files_recursively()
        
        self.assertNotIn("This is a text file.", content)
    
    def test_read_files_recursively_multiple_files(self):
        """
        Test reading multiple files with different allowed extensions.
        """
        file1_path = os.path.join(self.folder_path, "test.py")
        file2_path = os.path.join(self.folder_path, "README.md")
        with open(file1_path, 'w') as f1, open(file2_path, 'w') as f2:
            f1.write("print('Hello, World!')")
            f2.write("# This is a markdown file")
        
        processor = ProjectProcessor(self.folder_path, self.allowed_extensions)
        content = processor.read_files_recursively()
        
        self.assertIn("print('Hello, World!')", content)
        self.assertIn("# This is a markdown file", content)

    def test_read_files_recursively_empty_folder(self):
        """
        Test reading from an empty folder.
        """
        processor = ProjectProcessor(self.folder_path, self.allowed_extensions)
        content = processor.read_files_recursively()
        
        self.assertEqual(content, "")

    def test_read_files_recursively_non_utf8_file(self):
        """
        Test reading a file with non-UTF-8 encoding.
        """
        file_path = os.path.join(self.folder_path, "test.py")
        with open(file_path, 'wb') as f:  # Writing in binary mode with a different encoding
            f.write(b'\xe9\x61\x62\xc3\xa9')  # Non-UTF-8 encoded content

        processor = ProjectProcessor(self.folder_path, self.allowed_extensions)
        content = processor.read_files_recursively()
        
        # Ensure that the file content was read correctly despite the encoding issue
        self.assertIn("�abé", content)  # The � represents an invalid character decoded

if __name__ == '__main__':
    unittest.main()
