import json
import logging
from datetime import datetime
from autogen import ConversableAgent
from config import load_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Agent:
    def __init__(self, config_path, problem, thought, agent_id):
        self.config_list = load_config("aiconfig.json")
        
        self.generator = ConversableAgent(
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
            prompt = f"Problem: {self.problem}\nEvaluate this thought: {self.thought}"
            evaluated_thought = self.generator.generate_reply(messages=[{"content": prompt, "role": "user"}])
            
            if not evaluated_thought:
                raise ValueError("The generated response is empty.")
            logger.info(f"Response from agent {self.agent_id} : {evaluated_thought}")
            
            justification_prompt = f"Problem: {self.problem}\nJustify this thought: {evaluated_thought}"
            justification_response = self.generator.generate_reply(messages=[{"content": justification_prompt, "role": "user"}])
            
            if not justification_response:
                raise ValueError("The generated justification response is empty.")
            
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
            logger.error(f"Error during the evaluation of the thought by agent {self.agent_id} : {e}")
            return {
                "agent_id": self.agent_id,
                "thought": "Error during evaluation",
                "justification": "Error during evaluation",
                "history": self.history
            }

class SupervisorAgent:
    def __init__(self, config_path, problem):
        self.config_list = load_config("aiconfig.json")
        self.generator = ConversableAgent(
            name=f"SuperVisorAgent",
            system_message="You are a problem solver. Evaluate and justify thoughts based on given problems and generate refined responses.",
            llm_config=self.config_list,
        )
        self.problem = problem
        self.history = []

    def select_best_thought(self, thoughts_with_info):
        try:
            thoughts = [info["thought"] for info in thoughts_with_info if info["thought"] != "Error during evaluation"]
            justifications = [info["justification"] for info in thoughts_with_info if info["justification"] != "Error during evaluation"]

            if not thoughts:
                raise ValueError("All thoughts are errors.")

            prompt = f"For the problem {self.problem}. Here is the list of evaluated thoughts for each agent : {thoughts}. For each item in the list of thoughts, here are their justifications : {justifications}. As a supervisor, select and provide me the best thought with its justification. Provide me the entire selected thought and justification."
            best_thought = self.generator.generate_reply(messages=[{"content": prompt, "role": "user"}])
            response =  f"{best_thought} : {prompt}"
            if not best_thought:
                raise ValueError("The generated response is empty.")

            if best_thought is None:
                raise ValueError("Unable to find the best thought among the provided thoughts.")
            
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
            logger.error(f"Error during the selection of the best thought : {e}")
            return {
                "agent_id": None,
                "thought": "Error during the selection of the best thought",
                "justification": "Error during the selection of the best thought",
                "history": self.history
            }
