import logging
from config import load_config
from tree import TreeOfThought
from agent import Agent, SupervisorAgent

# Configuration du logger pour sauvegarder les logs dans un fichier
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('interactive_tree_of_thought.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class InteractiveTreeOfThought(TreeOfThought):
    def __init__(self, config_path='config.json'):
        super().__init__(config_path)
        self.current_step_index = 0
        self.steps = []
        self.thoughts_history = []
        self.config_path = config_path
        self.config_list = load_config(config_path)

    def interactive_mode(self, problem):
        print("Démarrage du mode interactif...")
        logger.info("Démarrage du mode interactif...")
        self.steps = self.decompose_problem(problem)
        if not self.steps:
            print("Aucune étape de décomposition trouvée. Utilisation du problème brut.")
            logger.warning("Aucune étape de décomposition trouvée. Utilisation du problème brut.")
            self.steps = [problem]
        self.current_step_index = 0
        current_state = self.steps[self.current_step_index]

        while self.current_step_index < len(self.steps):
            print(f"Étape actuelle {self.current_step_index + 1}/{len(self.steps)}: {current_state}")
            logger.info(f"Étape actuelle {self.current_step_index + 1}/{len(self.steps)}: {current_state}")
            command = input("Entrez 'next' pour générer des pensées, 'eval' pour évaluer des états, 'exit' pour quitter: ")
            if command == 'next':
                thoughts = self.generate_thoughts(problem, current_state)
                if not thoughts:
                    print("Aucune pensée générée. Veuillez réessayer.")
                    logger.warning("Aucune pensée générée.")
                    continue
                print(f"Pensées générées: {thoughts}")
                logger.info(f"Pensées générées: {thoughts}")
                best_thought = self.evaluate_thoughts_with_agents(problem, thoughts)
                #best_thought = best_info["thought"]
                #best_justification = best_info["justification"]
                self.thoughts_history.append(best_thought)
                print(f"Meilleure pensée: {best_thought}")
                #print(f"Meilleure pensée: {best_thought} avec justification: {best_justification} par l'agent {best_info['agent_id']}")
                #print(f"Historique de l'agent {best_info['agent_id']}: {best_info['history']}")
                #logger.info(f"Meilleure pensée: {best_thought} avec justification: {best_justification} par l'agent {best_info['agent_id']}")
                #logger.info(f"Historique de l'agent {best_info['agent_id']}: {best_info['history']}")
                if self.current_step_index + 1 < len(self.steps):
                    self.current_step_index += 1
                    current_state = f"{self.steps[self.current_step_index]} | Contexte précédent: {best_thought}"
                else:
                    self.current_step_index += 1  # Sortir de la boucle après la dernière étape
            elif command == 'eval':
                states = [current_state]
                evaluated_states = self.evaluate_states(problem, states)
                print(f"États évalués: {evaluated_states}")
                logger.info(f"États évalués: {evaluated_states}")
            elif command == 'exit':
                return
            else:
                print("Commande non reconnue. Veuillez réessayer.")
                logger.warning("Commande non reconnue. Veuillez réessayer.")
        
        #final_result = self.generate_final_result(problem, self.thoughts_history)
        #print(f"Résultat final: {final_result}")
        #logger.info(f"Résultat final: {final_result}")

    def evaluate_states(self, problem, states):
        evaluated_states = []
        try:
            for state in states:
                if state in self.knowledge_base:
                    score = self.knowledge_base[state]
                else:
                    response = self.generator.generate_reply(
                        messages=[
                            {"role": "system", "content": f"Problème: {problem}"},
                            {"role": "user", "content": f"État actuel: {state}"}
                        ]
                    )
                    score = response['choices'][0]['text'].strip()
                    self.knowledge_base[state] = score
                evaluated_states.append((state, score))
                logger.info(f"État évalué: {state} avec score: {score}")
        except Exception as e:
            logger.error(f"Erreur lors de l'évaluation des états : {e}")
        return evaluated_states

    def generate_final_result(self, problem, thoughts_history):
        try:
            thoughts = [info["thought"] for info in thoughts_history]
            justifications = [info["justification"] for info in thoughts_history]

            response = self.generator.generate_reply(
                messages=[
                    {"role": "system", "content": f"Problème: {problem}"},
                    {"role": "user", "content": f"Pensées générées: {thoughts}. Justifications: {justifications}"}
                ]
            )
            final_result = response['choices'][0]['text'].strip()
        except Exception as e:
            logger.error(f"Erreur lors de la génération du résultat final : {e}")
            final_result = "Erreur lors de la génération du résultat final."
        logger.info(f"Résultat final généré: {final_result}")
        return final_result