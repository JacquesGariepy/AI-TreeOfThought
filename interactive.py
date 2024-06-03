import logging
import json
import time
from config import load_config
from tree import TreeOfThought
from agent import Agent, SupervisorAgent

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
        print("Starting interactive mode...")
        logger.info("Starting interactive mode...")
        self.steps = self.decompose_problem(problem)
        if not self.steps:
            print("No decomposition steps found. Using raw problem.")
            logger.warning("No decomposition steps found. Using raw problem.")
            self.steps = [problem]
        self.current_step_index = 0
        current_state = self.steps[self.current_step_index]

        while self.current_step_index < len(self.steps):
            print(f"Current step {self.current_step_index + 1}/{len(self.steps)}: {current_state}")
            logger.info(f"Current step {self.current_step_index + 1}/{len(self.steps)}: {current_state}")
            command = input(f"Enter 'next' to launch {current_state}, 'eval' to evaluate states, 'exit' to quit: ")
            if command == 'next':
                agent = self.generate_thoughts(problem, current_state)
                if not agent:
                    print("No thought generated. Please try again.")
                    logger.warning("No thought generated.")
                    continue

                print(f"Agent ID: {agent['agent_id'] + 1}")
                print(f"Thought: {agent['thought']}")
                print(f"Justification: {agent['justification']}")
                                   
                logger.info(f"Generated thoughts: {agent}")
                self.best_thought = self.evaluate_thoughts_with_agents(problem, agent)
                self.thoughts_history.append(self.best_thought)
                print(f"Best thought: {self.best_thought}")
                if self.current_step_index + 1 < len(self.steps):
                    self.current_step_index += 1
                    current_state = f"{self.steps[self.current_step_index]} | Previous context: {self.best_thought}"
                else:
                    self.current_step_index += 1  # Exit the loop after the last step
            elif command == 'eval':
                states = [current_state]
                evaluated_states = self.evaluate_states(problem, states)
                print(f"Evaluated states: {evaluated_states}")
                logger.info(f"Evaluated states: {evaluated_states}")
            elif command == 'exit':
                return
            else:
                print("Unrecognized command. Please try again.")
                logger.warning("Unrecognized command. Please try again.")
        # save to final result to a file
        self.save_result()
        print("End of interactive mode.")

    def evaluate_states(self, problem, states):
        evaluated_states = []
        #not implemented yet

        # try:
        #     for state in states:
        #         if state in self.knowledge_base:
        #             score = self.knowledge_base[state]
        #         else:
        #             agent = Agent(self.config_path, problem, state, agent_id=0)
        #             score = agent.evaluate_state()
        #             self.knowledge_base[state] = score
        #         evaluated_states.append((state, score))
        #         logger.info(f"Evaluated state: {state} with score: {score}")
        # except Exception as e:
        #     logger.error(f"Error during the evaluation of states : {e}")
        return evaluated_states

    def generate_final_result(self, problem, thoughts_history):
        try:
            thoughts = [info["thought"] for info in thoughts_history]
            justifications = [info["justification"] for info in thoughts_history]

            response = self.generator.generate_reply(
                messages=[
                    {"role": "system", "content": f"Problem: {problem}"},
                    {"role": "user", "content": f"Generated thoughts: {thoughts}. Justifications: {justifications}"}
                ]
            )
            final_result = response['choices'][0]['text'].strip()
        except Exception as e:
            logger.error(f"Error during the generation of the final result : {e}")
            final_result = "Error during the generation of the final result."
        logger.info(f"Generated final result: {final_result}")
        return final_result
    
    def save_result(self):
        # Get filename from configuration
        filename = self.config_list.get('filename_result', 'result')
        # Add timestamp to filename
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename_with_timestamp = f"{filename}_{timestamp}.json"

        result = {
            "best_thought": self.best_thought,
            "thoughts_history": self.thoughts_history,
            "steps": self.steps,  # Replace this with your other elements
        }

        with open(filename_with_timestamp, 'w') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        print(f"Result saved to {filename_with_timestamp}")
        logger.info(f"Result saved to {filename_with_timestamp}")

