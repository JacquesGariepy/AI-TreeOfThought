import os
import unittest
from src.saver import Saver, SaverError

class TestSaver(unittest.TestCase):

    def test_save_text_to_file(self):
        text = "Sample text."
        filepath = "data/test_output.txt"
        Saver.save_text_to_file(text, filepath)

        self.assertTrue(os.path.exists(filepath))

        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        self.assertEqual(content, text)

        os.remove(filepath)

if __name__ == '__main__':
    unittest.main()