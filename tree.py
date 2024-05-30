import logging
from agent import Agent, SupervisorAgent

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
            #response = self.generator.generate_reply(messages=[{"role": "user", "content": problem}])
            #decomposition_steps = response['choices'][0]['text'].strip().split('\n')
            
            #supervisor = SupervisorAgent(self.config_path, problem)
            steps = [] # supervisor.select_best_thought(problem)
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

    def evaluate_thoughts_with_agents(self, problem, thoughts):
        try:
            agents = [Agent(self.config_path, problem, thought, agent_id) for agent_id, thought in enumerate(thoughts)]
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

    def evaluate_states(self, problem, states):
        evaluated_states = []
        try:
            for state in states:
                if state in self.knowledge_base:
                    score = self.knowledge_base[state]
                else:
                    agent = Agent(self.config_path, problem, state, agent_id=0)
                    score = agent.evaluate_state()
                    self.knowledge_base[state] = score
                evaluated_states.append((state, score))
                logger.info(f"État évalué: {state} avec score: {score}")
        except Exception as e:
            logger.error(f"Erreur lors de l'évaluation des états : {e}")
        return evaluated_states

    def backtrack_search(self, problem):
        initial_state = self.decompose_problem(problem)[0]
        path = [initial_state]
        frontier = [initial_state]
        for depth in range(self.max_depth):
            next_frontier = []
            for state in frontier:
                logger.info(f"Exploration de l'état à la profondeur {depth}: {state}")
                thoughts = self.generate_thoughts(problem, state)
                best_thought = self.evaluate_thoughts_with_agents(problem, thoughts)
                #best_thought = best_info["thought"]
                logger.info(f"Meilleure pensée: {best_thought}")
                if best_thought not in path:
                    path.append(best_thought)
                    result = self.backtrack_search(problem)
                    if result:
                        return result
                    path.pop()
                next_frontier.append(best_thought)
            frontier = next_frontier
        return path[-1]

    def visualize_tree(self, path):
        for i, state in enumerate(path):
            self.graph.node(str(i), state)
            if i > 0:
                self.graph.edge(str(i-1), str(i))
        self.graph.render('tree_of_thoughts', view=True)
        logger.info(f"Graphique sauvegardé sous le nom 'tree_of_thoughts.png'")
