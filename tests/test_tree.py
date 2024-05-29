import unittest
from treeofthought.tree import TreeOfThought

class TestTreeOfThought(unittest.TestCase):
    def setUp(self):
        self.config_path = 'config.json'
        self.tot = TreeOfThought(self.config_path)

    def test_decompose_problem(self):
        problem = "Trouver une équation pour obtenir 24 avec les nombres 4, 9, 10, 13."
        steps = self.tot.decompose_problem(problem)
        self.assertGreater(len(steps), 0)
        self.assertIn("Étape 1: Analyser le problème.", steps)

    def test_generate_thoughts(self):
        state = "Analyser le problème"
        thoughts = self.tot.generate_thoughts(state)
        self.assertGreater(len(thoughts), 0)

    def test_evaluate_states(self):
        states = ["State 1", "State 2"]
        evaluated_states = self.tot.evaluate_states(states)
        self.assertEqual(len(evaluated_states), 2)

    def test_backtrack_search(self):
        problem = "Trouver une équation pour obtenir 24 avec les nombres 4, 9, 10, 13."
        solution = self.tot.backtrack_search(problem)
        self.assertIsNotNone(solution)

if __name__ == '__main__':
    unittest.main()
