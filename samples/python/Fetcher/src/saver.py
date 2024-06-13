import os
import logging

logging.basicConfig(level=logging.INFO)

class SaverError(Exception):
    pass

class Saver:
    @staticmethod
    def save_text_to_file(text: str, filepath: str):
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(text)
            logging.info(f"Text successfully saved to {filepath}")
        except IOError as e:
            logging.error(f"Failed to write text to file {filepath}: {e}")
            raise SaverError(f"Failed to write text to file {filepath}: {e}")