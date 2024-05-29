from tree import TreeOfThought
from litellm import completion  # Ajoutez cette ligne

class InteractiveTreeOfThought(TreeOfThought):
    def __init__(self, config_path='config.json'):
        super().__init__(config_path)
        self.current_step_index = 0
        self.steps = []
        self.thoughts_history = []

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

        while self.current_step_index < len(self.steps):
            print(f"Étape actuelle {self.current_step_index + 1}/{len(self.steps)}: {current_state}")
            command = input("Entrez 'next' pour générer des pensées, 'eval' pour évaluer des états, 'exit' pour quitter: ")
            if command == 'next':
                thoughts = self.generate_thoughts(problem, current_state)
                print(f"Pensées générées: {thoughts}")
                best_thought = self.select_best_thought(thoughts)
                self.thoughts_history.append(best_thought)
                if self.current_step_index + 1 < len(self.steps):
                    self.current_step_index += 1
                    current_state = self.steps[self.current_step_index]
                else:
                    self.current_step_index += 1  # Sortir de la boucle après la dernière étape
            elif command == 'eval':
                states = [current_state]
                evaluated_states = self.evaluate_states(problem, states)
                print(f"États évalués: {evaluated_states}")
            elif command == 'exit':
                return
            else:
                print("Commande non reconnue. Veuillez réessayer.")
        
        final_result = self.generate_final_result(problem, self.thoughts_history)
        print(f"Résultat final: {final_result}")

    def select_best_thought(self, thoughts):
        """
        Sélectionne la meilleure pensée parmi celles générées.

        :param thoughts: Liste des pensées générées.
        :return: La meilleure pensée sélectionnée.
        """
        # Implémentation simple basée sur la première pensée pour cet exemple.
        # Vous pouvez ajouter une logique plus complexe pour sélectionner la meilleure pensée.
        return thoughts[0] if thoughts else ""

    def generate_final_result(self, problem, thoughts_history):
        """
        Génère un résultat final basé sur l'historique des pensées.

        :param problem: Le problème complet.
        :param thoughts_history: L'historique des pensées générées.
        :return: Un résumé ou une conclusion basée sur les pensées générées.
        """
        try:
            response = completion(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": f"Problème: {problem}"},
                    {"role": "user", "content": f"Pensées générées: {thoughts_history}"}
                ]
            )
            final_result = response['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"Erreur lors de la génération du résultat final : {e}")
            final_result = "Erreur lors de la génération du résultat final."
        return final_result
