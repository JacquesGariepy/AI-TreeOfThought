import argparse
import logging
from interactive import InteractiveTreeOfThought

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Interactive Tree of Thought")
    parser.add_argument('--config', type=str, default='config.json', help='Path to the configuration file')
    parser.add_argument('--problem', type=str, default=None, help='Problem to solve')

    args = parser.parse_args()
    config_path = args.config
    problem = args.problem

    if not problem:
        problem = input("Veuillez entrer le problème à résoudre: ")

    tree = InteractiveTreeOfThought(config_path)
    tree.interactive_mode(problem)

if __name__ == "__main__":
    main()
