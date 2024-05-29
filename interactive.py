from .tree import TreeOfThought

class InteractiveTreeOfThought(TreeOfThought):
    def __init__(self, config_path='config.json'):
        super().__init__(config_path)
    
    def interactive_mode(self, problem):
        """
        Démarre le mode interactif pour la résolution de problèmes.

        :param problem: Le problème à résoudre.
        """
        print("Démarrage du mode interactif...")
        current_state = self.decompose_problem(problem)[0]
        while True:
            print(f"État actuel: {current_state}")
            command = input("Entrez 'next' pour générer des pensées, 'eval' pour évaluer des états, 'exit' pour quitter: ")
            if command == 'next':
                thoughts = self.generate_thoughts(current_state)
                print(f"Pensées générées: {thoughts}")
            elif command == 'eval':
                states = [current_state]
                evaluated_states = self.evaluate_states(states)
                print(f"États évalués: {evaluated_states}")
            elif command == 'exit':
                break
            else:
                print("Commande non reconnue. Veuillez réessayer.")
