import logging
from config import load_config
from agent import Agent, SupervisorAgent
from graphviz import Digraph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TreeOfThought:
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self.knowledge_base = {}
        self.max_depth = 3  # Vous pouvez ajuster selon vos besoins
        self.graph = None  # Initialisez votre graphe ici si nécessaire

    def decompose_problem(self, problem):
        try:
            #supervisor = SupervisorAgent(self.config_path, problem)
            steps = [] # supervisor.select_best_thought(problem)
            config = load_config(self.config_path)
            steps = config.get("decomposition_steps", [])
    
            logger.info(f"Problème décomposé en étapes: {steps}")
            return steps
        except Exception as e:
            logger.error(f"Erreur lors de la décomposition du problème : {e}")
            return []

    def generate_thoughts(self, problem, state):
        thoughts = []
        try:
            agent = Agent(self.config_path, problem, state, agent_id=0)  # Créez un agent pour générer des pensées
            thoughts = agent.evaluate_thought()
            logger.info(f"Pensées générées pour l'état '{state}': {thoughts}")
        except Exception as e:
            logger.error(f"Erreur lors de la génération des pensées : {e}")
        return thoughts

    def evaluate_thoughts_with_agents(self, problem, agent):
        try:
            config = load_config(self.config_path)
            num_agents = config.get('num_agents', 1)
            agents = [Agent(self.config_path, problem, f"Thought for agent {agent_id}, Thought: {agent['thought']} et justification :  {agent['justification']}", agent_id) for agent_id in range(1, num_agents + 1)]
            evaluated_thoughts_with_info = [agent.evaluate_thought() for agent in agents]
            supervisor = SupervisorAgent(self.config_path, problem)
            best_thought = supervisor.select_best_thought(evaluated_thoughts_with_info)

            # retourne  la meilleure pensée mais devrait retourner un dictionnaire contenant les informations sur la pensée et l'agent
            # return evaluated_thoughts_with_info
            return best_thought
        except Exception as e:
            logger.error(f"Erreur lors de l'évaluation des pensées par les agents : {e}")
            return {
                "agent_id": None,
                "thought": "Erreur lors de l'évaluation",
                "justification": "Erreur lors de l'évaluation",
                "history": []
            }