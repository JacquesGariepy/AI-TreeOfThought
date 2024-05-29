from tree import TreeOfThought

class InteractiveTreeOfThought(TreeOfThought):
    def __init__(self, config_path='config.json'):
        super().__init__(config_path)
        self.current_step_index = 0
        self.steps = []

    def interactive_mode(self, problem):
        """
        Démarre le mode interactif pour la résolution de problèmes.

        :param problem: Le problème à résoudre.
        """
        print("Démarrage du mode interactif...")
        self.steps = self.decompose_problem(problem)
        if not self.steps:
            print("Aucune étape de décomposition trouvée. Utilisation du problème brut.")
            self.steps = [problem]
        self.current_step_index = 0
        current_state = self.steps[self.current_step_index]

        while True:
            print(f"Étape actuelle {self.current_step_index + 1}/{len(self.steps)}: {current_state}")
            command = input("Entrez 'next' pour générer des pensées, 'eval' pour évaluer des états, 'exit' pour quitter: ")
            if command == 'next':
                thoughts = self.generate_thoughts(problem, current_state)
                print(f"Pensées générées: {thoughts}")
                if self.current_step_index + 1 < len(self.steps):
                    self.current_step_index += 1
                    current_state = self.steps[self.current_step_index]
            elif command == 'eval':
                states = [current_state]
                evaluated_states = self.evaluate_states(problem, states)
                print(f"États évalués: {evaluated_states}")
            elif command == 'exit':
                break
            else:
                print("Commande non reconnue. Veuillez réessayer.")
