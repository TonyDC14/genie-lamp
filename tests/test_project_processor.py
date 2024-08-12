import unittest
from src.project_processor import ProjectProcessor
import os

class TestProjectProcessor(unittest.TestCase):

    def test_read_files_recursively(self):
        folder_path = "test_folder"
        allowed_extensions = ['.py']
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, "test.py")
        with open(file_path, 'w') as f:
            f.write("print('Hello, World!')")
        
        processor = ProjectProcessor(folder_path, allowed_extensions)
        content = processor.read_files_recursively()
        
        self.assertIn("print('Hello, World!')", content)
        
        os.remove(file_path)
        os.rmdir(folder_path)

if __name__ == '__main__':
    unittest.main()
