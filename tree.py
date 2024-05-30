from graphviz import Digraph
import os
import logging
from datetime import datetime
from utils import get_decompose_function
from config import load_config
from agent import Agent, SupervisorAgent
from litellm import completion

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TreeOfThought:
    def __init__(self, config_path='config.json'):
        """
        Initialise la classe TreeOfThought avec les paramètres de configuration spécifiés.

        :param config_path: Chemin vers le fichier de configuration JSON.
        """
        self.config = load_config(config_path)
        self.model_name = self.config['model_name']
        self.api_key = self.config['api_key']
        self.decompose_function = get_decompose_function(self.config['decompose_function'])
        self.num_candidates = self.config['num_candidates']
        self.max_depth = self.config['max_depth']
        self.breadth_limit = self.config['breadth_limit']
        self.value_threshold = self.config['value_threshold']
        self.num_responses = self.config.get('num_responses', 1)  # Default to 1 if not set
        
        os.environ["OPENAI_API_KEY"] = self.api_key
        self.knowledge_base = {}
        self.graph = Digraph(comment='Tree of Thoughts', format='png')
    
    def decompose_problem(self, problem):
        """
        Utilise la fonction de décomposition dynamique pour décomposer le problème en étapes de pensée intermédiaires.

        :param problem: Le problème à résoudre.
        :return: Une liste d'étapes intermédiaires.
        """
        steps = self.decompose_function(problem, self.config)
        if steps:
            logger.info(f"Problème décomposé en étapes: {steps}")
        else:
            logger.warning("Aucune étape de décomposition trouvée.")
        return steps

    def generate_thoughts(self, problem, state):
        """
        Génère des pensées candidates à partir d'un état donné et du problème complet.

        :param problem: Le problème complet.
        :param state: L'état actuel.
        :return: Une liste de pensées candidates.
        """
        thoughts = []
        try:
            response = completion(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": f"Problème: {problem}"},
                    {"role": "user", "content": f"Étape actuelle: {state}"}
                ],
                n=self.num_responses
            )
            for choice in response['choices']:
                thought = choice['message']['content']
                thoughts.append(thought)
                self.knowledge_base[thought] = self.knowledge_base.get(thought, 0) + 1
            logger.info(f"Pensées générées pour l'état '{state}': {thoughts}")
        except Exception as e:
            logger.error(f"Erreur lors de la génération des pensées : {e}")
        return thoughts

    def evaluate_thoughts_with_agents(self, problem, thoughts):
        """
        Évalue les pensées générées en utilisant des agents.
        
        :param problem: Le problème complet.
        :param thoughts: Les pensées générées.
        :return: La meilleure pensée évaluée et sa justification.
        """
        try:
            agents = [Agent(self.model_name, self.api_key, problem, thought, agent_id) for agent_id, thought in enumerate(thoughts)]
            evaluated_thoughts_with_info = [agent.evaluate_thought() for agent in agents]
            
            supervisor = SupervisorAgent(self.model_name, self.api_key, problem)
            best_info = supervisor.select_best_thought(evaluated_thoughts_with_info)
            
            return best_info
        except Exception as e:
            logger.error(f"Erreur lors de l'évaluation des pensées par les agents : {e}")
            return {
                "agent_id": None,
                "thought": "Erreur lors de l'évaluation",
                "justification": "Erreur lors de l'évaluation",
                "history": []
            }

    def backtrack_search(self, problem):
        """
        Recherche avec possibilité de revenir en arrière si une branche ne mène pas à une solution satisfaisante.

        :param problem: Le problème à résoudre.
        :return: Le meilleur état trouvé.
        """
        initial_state = self.decompose_problem(problem)[0]
        path = [initial_state]
        frontier = [initial_state]
        self.graph.node(initial_state, label=initial_state)
        for depth in range(self.max_depth):
            next_frontier = []
            for state in frontier:
                logger.info(f"Exploration de l'état à la profondeur {depth}: {state}")
                thoughts = self.generate_thoughts(problem, state)
                best_info = self.evaluate_thoughts_with_agents(problem, thoughts)
                best_thought = best_info["thought"]
                best_justification = best_info["justification"]
                self.graph.edge(state, best_thought, label=f"Best Thought: {best_thought}")
                logger.info(f"Meilleure pensée: {best_thought} avec justification: {best_justification}")
                if best_thought not in path:
                    path.append(best_thought)
                    result = self.backtrack_search(problem)  # Passer le problème ici
                    if result:
                        self.visualize_tree(path)
                        return result
                    path.pop()
                next_frontier.append(best_thought)
            frontier = next_frontier
        self.visualize_tree(path)
        return path[-1]

    def visualize_tree(self, path):
        """
        Crée une visualisation de l'arbre de pensées.

        :param path: Liste des états représentant le chemin de pensée.
        """
        for i, state in enumerate(path):
            self.graph.node(str(i), state)
            if i > 0:
                self.graph.edge(str(i-1), str(i))
        self.graph.render('tree_of_thoughts', view=True)
        logger.info(f"Graphique sauvegardé sous le nom 'tree_of_thoughts.png'")
