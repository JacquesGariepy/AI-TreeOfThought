import logging
from datetime import datetime
from litellm import completion

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Agent:
    def __init__(self, model_name, api_key, problem, thought, agent_id):
        self.model_name = model_name
        self.api_key = api_key
        self.problem = problem
        self.thought = thought
        self.agent_id = agent_id
        self.history = []

    def evaluate_thought(self):
        """
        Évalue la pensée actuelle et fournit une justification détaillée.
        """
        try:
            response = completion(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": f"Problème: {self.problem}"},
                    {"role": "user", "content": f"Évalue cette pensée: {self.thought}"}
                ]
            )
            evaluated_thought = response['choices'][0]['message']['content']
            
            justification_response = completion(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": f"Problème: {self.problem}"},
                    {"role": "user", "content": f"Justifiez cette pensée: {evaluated_thought}"}
                ]
            )
            justification = justification_response['choices'][0]['message']['content']
            
            activity = {
                "action": "evaluate",
                "thought": self.thought,
                "evaluated_thought": evaluated_thought,
                "justification": justification,
                "timestamp": datetime.now().isoformat()
            }
            self.history.append(activity)
            logger.info(f"Agent {self.agent_id}: {activity}")
            
            return {
                "agent_id": self.agent_id,
                "thought": evaluated_thought,
                "justification": justification,
                "history": self.history
            }
        except Exception as e:
            logger.error(f"Erreur lors de l'évaluation de la pensée par l'agent {self.agent_id} : {e}")
            return {
                "agent_id": self.agent_id,
                "thought": "Erreur lors de l'évaluation",
                "justification": "Erreur lors de l'évaluation",
                "history": self.history
            }

class SupervisorAgent:
    def __init__(self, model_name, api_key, problem):
        self.model_name = model_name
        self.api_key = api_key
        self.problem = problem
        self.history = []

    def select_best_thought(self, thoughts_with_info):
        """
        Sélectionne la meilleure pensée parmi celles fournies par les agents.
        """
        try:
            if not thoughts_with_info:
                raise ValueError("Aucune pensée à évaluer.")

            thoughts = [info["thought"] for info in thoughts_with_info if info["thought"] != "Erreur lors de l'évaluation"]
            justifications = [info["justification"] for info in thoughts_with_info if info["justification"] != "Erreur lors de l'évaluation"]

            if not thoughts:
                raise ValueError("Toutes les pensées sont des erreurs.")

            response = completion(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": f"Problème: {self.problem}"},
                    {"role": "user", "content": f"Pensées évaluées: {thoughts}. Justifications: {justifications}. Sélectionnez la meilleure pensée."}
                ]
            )
            best_thought = response['choices'][0]['message']['content']
            best_info = next((info for info in thoughts_with_info if info["thought"] == best_thought), None)
            
            if best_info is None:
                raise ValueError("Impossible de trouver la meilleure pensée parmi les pensées fournies.")
            
            activity = {
                "action": "select_best",
                "thoughts": thoughts,
                "justifications": justifications,
                "best_thought": best_thought,
                "best_info": best_info,
                "timestamp": datetime.now().isoformat()
            }
            self.history.append(activity)
            logger.info(f"Supervisor: {activity}")
            
            return best_info
        except Exception as e:
            logger.error(f"Erreur lors de la sélection de la meilleure pensée : {e}")
            return {
                "agent_id": None,
                "thought": "Erreur lors de la sélection de la meilleure pensée",
                "justification": "Erreur lors de la sélection de la meilleure pensée",
                "history": self.history
            }
