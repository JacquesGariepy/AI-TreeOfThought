import json
import logging
from datetime import datetime
from autogen import ConversableAgent, AssistantAgen
config_list_from_json from config import load_config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Agent:
    def __init__(self, config_path, problem, thought, agent_id):
        self.config_list = load_config("aiconfig.json")
        
        self.generator = AssistantAgent(
            name=f"agent_{agent_id}",
            system_message="You are a problem solver. Evaluate and justify thoughts based on given problems and generate refined responses.",
            llm_config=self.config_list,
        )
        self.problem = problem
        self.thought = thought
        self.agent_id = agent_id
        self.history = []

    def evaluate_thought(self):
        try:
            prompt = f"Problème: {self.problem}\nÉvalue cette pensée: {self.thought}"
            evaluated_thought = self.generator.generate_reply(messages=[{"content": prompt, "role": "user"}])
            
            if not evaluated_thought:
                raise ValueError("La réponse générée est vide.")
            logger.info(f"Response from agent {self.agent_id} : {evaluated_thought}")
            # evaluated_thought = response['choices'][0]['text'].strip()
            
            justification_prompt = f"Problème: {self.problem}\nJustifiez cette pensée: {evaluated_thought}"
            justification_response = self.generator.generate_reply(messages=[{"content": justification_prompt, "role": "user"}])
            
            if not justification_response:
                raise ValueError("La réponse de justification générée est vide.")
            
            # justification = justification_response['choices'][0]['text'].strip()
            
            activity = {
                "action": "evaluate",
                "thought": self.thought,
                "evaluated_thought": evaluated_thought,
                "justification": justification_response,
                "timestamp": datetime.now().isoformat()
            }
            self.history.append(activity)
            logger.info(f"Agent {self.agent_id}: {activity}")
            
            return {
                "agent_id": self.agent_id,
                "thought": evaluated_thought,
                "justification": justification_response,
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
    def __init__(self, config_path, problem):
        self.config_list = load_config("aiconfig.json")
        system_message="You are a problem solver. Evaluate and justify thoughts based on given problems and generate refined responses.",
            llm_config=self.config_list,
        )
        self.problem = problem
        self.thought = thought
        self.agent_id = agent_id
        self.history = []

    def select_best_thought(self, thoughts_with_info):
        try:
            thoughts = [info["thought"] for info in thoughts_with_info if info["thought"] != "Erreur lors de l'évaluation"]
            justifications = [info["justification"] for info in thoughts_with_info if info["justification"] != "Erreur lors de l'évaluation"]

            if not thoughts:
                raise ValueError("Toutes les pensées sont des erreurs.")

            prompt = f"Pour le problème {self.problem}. Voici la liste des pensées évaluées pour chaque agent : {thoughts}. Pour chaque item de la liste des pensées, voici leurs justifications : {justifications}. En tant que superviseur, sélectionne et fournis-moi la meilleure pensée avec sa justification. Refournis moi intégralement la pensée et la justification sélectionné."
            best_thought = self.generator.generate_reply(messages=[{"content": prompt, "role": "user"}])
            response =  f"{best_thought} : {prompt}"
            if not best_thought:
                raise ValueError("La réponse générée est vide.")

            if best_thought is None:
                raise ValueError("Impossible de trouver la meilleure pensée parmi les pensées fournies.")
            
            activity = {
                "action": "select_best",
                "thoughts": thoughts,
                "justifications": justifications,
                "best_thought": response,
                "best_info": "__not_implemented__",
                "timestamp": datetime.now().isoformat()
            }
            self.history.append(activity)
            logger.info(f"Supervisor: {activity}")
            
            return response
        except Exception as e:
            logger.error(f"Erreur lors de la sélection de la meilleure pensée : {e}")
            return {
                "agent_id": None,
                "thought": "Erreur lors de la sélection de la meilleure pensée",
                "justification": "Erreur lors de la sélection de la meilleure pensée",
                "history": self.history
            }
