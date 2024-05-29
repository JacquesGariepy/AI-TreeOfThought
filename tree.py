from graphviz import Digraph
from litellm import completion
import os
import logging
from .utils import get_decompose_function
from .config import load_config

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
        
        os.environ["LITELLM_API_KEY"] = self.api_key
        self.knowledge_base = {}
        self.graph = Digraph(comment='Tree of Thoughts')

    def decompose_problem(self, problem):
        """
        Utilise la fonction de décomposition dynamique pour décomposer le problème en étapes de pensée intermédiaires.

        :param problem: Le problème à résoudre.
        :return: Une liste d'étapes intermédiaires.
        """
        return self.decompose_function(problem, self.config)

    def generate_thoughts(self, state):
        """
        Génère des pensées candidates à partir d'un état donné.

        :param state: L'état actuel.
        :return: Une liste de pensées candidates.
        """
        thoughts = []
        try:
            for _ in range(self.num_candidates):
                response = completion(
                    model=self.model_name,
                    messages=[{"role": "system", "content": state}]
                )
                thought = response['choices'][0]['message']['content']
                thoughts.append(thought)
                self.knowledge_base[thought] = self.knowledge_base.get(thought, 0) + 1
        except OpenAIError as e:
            logger.error(f"Erreur lors de la génération des pensées : {e}")
        except Exception as e:
            logger.error(f"Erreur inattendue : {e}")
        return thoughts

    def evaluate_states(self, states):
        """
        Évalue les états intermédiaires.

        :param states: Une liste d'états à évaluer.
        :return: Une liste d'états évalués avec leurs scores.
        """
        evaluated_states = []
        try:
            for state in states:
                if state in self.knowledge_base:
                    score = self.knowledge_base[state]
                else:
                    response = completion(
                        model=self.model_name,
                        messages=[{"role": "system", "content": state}]
                    )
                    score = response['choices'][0]['message']['content']
                    self.knowledge_base[state] = score
                evaluated_states.append((state, score))
        except OpenAIError as e:
            logger.error(f"Erreur lors de l'évaluation des états : {e}")
        except Exception as e:
            logger.error(f"Erreur inattendue : {e}")
        return evaluated_states

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
                thoughts = self.generate_thoughts(state)
                evaluated_thoughts = self.evaluate_states(thoughts)
                evaluated_thoughts.sort(key=lambda x: x[1], reverse=True)
                for next_state, score in evaluated_thoughts[:self.breadth_limit]:
                    self.graph.edge(state, next_state, label=f"Score: {score}")
                    if score > self.value_threshold:
                        path.append(next_state)
                        result = self.backtrack_search(next_state)
                        if result:
                            self.visualize_tree(path)
                            return result
                        path.pop()
                    next_frontier.append(next_state)
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
