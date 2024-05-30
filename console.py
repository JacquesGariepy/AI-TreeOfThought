import argparse
from interactive import InteractiveTreeOfThought

def main():
    parser = argparse.ArgumentParser(description="Interactive Tree of Thought")
    parser.add_argument("--config", type=str, default="config.json", help="Path to the configuration file")
    parser.add_argument("--problem", type=str, help="Problem to solve")
    args = parser.parse_args()

    config_path = args.config

    if not args.problem:
        problem = input("Veuillez entrer le problème à résoudre: ")
        if not problem:
            print("Erreur: Aucun problème fourni.")
            return
    else:
        problem = args.problem

    tree = InteractiveTreeOfThought(config_path=config_path)
    tree.interactive_mode(problem)

if __name__ == "__main__":
    main()
