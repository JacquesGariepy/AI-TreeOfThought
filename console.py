import argparse
import logging
from .interactive import InteractiveTreeOfThought

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Console:
    def __init__(self, config_path='config.json'):
        self.interactive_tree = InteractiveTreeOfThought(config_path)

    def run(self):
        print("Bienvenue dans InteractiveTreeOfThought!")
        problem = input("Veuillez entrer la description du problème: ")
        self.interactive_tree.interactive_mode(problem)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run InteractiveTreeOfThought from the console")
    parser.add_argument('--config', type=str, default='config.json', help='Path to the configuration file')
    args = parser.parse_args()

    console = Console(config_path=args.config)
    console.run()
