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
        self.max_depth = 3
        self.graph = None

    def decompose_problem(self, problem):
        try:
            config = load_config(self.config_path)
            steps = config.get("decomposition_steps", [])
            logger.info(f"Problem decomposed into steps: {steps}")
            return steps
        except Exception as e:
            logger.error(f"Error decomposing the problem: {e}")
            return []

    def generate_thoughts(self, problem, state):
        thoughts = []
        try:
            agent = Agent(self.config_path, problem, state, agent_id=0)
            thoughts = agent.evaluate_thought()
            logger.info(f"Thoughts generated for state '{state}': {thoughts}")
        except Exception as e:
            logger.error(f"Error generating thoughts: {e}")
        return thoughts

    def evaluate_thoughts_with_agents(self, problem, agent):
        try:
            config = load_config(self.config_path)
            num_agents = config.get('num_agents', 1)
            agents = [Agent(self.config_path, problem, f"Thought for agent {agent_id}, Thought: {agent['thought']} and justification: {agent['justification']}", agent_id) for agent_id in range(1, num_agents + 1)]
            evaluated_thoughts_with_info = [agent.evaluate_thought() for agent in agents]
            supervisor = SupervisorAgent(self.config_path, problem)
            best_thought = supervisor.select_best_thought(evaluated_thoughts_with_info)
            return best_thought
        except Exception as e:
            logger.error(f"Error evaluating thoughts by agents: {e}")
            return {
                "agent_id": None,
                "thought": "Error during evaluation",
                "justification": "Error during evaluation",
                "history": []
            }
