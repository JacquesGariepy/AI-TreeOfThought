import unittest
from treeofthought.interactive import InteractiveTreeOfThought

class TestInteractiveTreeOfThought(unittest.TestCase):
    def setUp(self):
        self.config_path = 'config.json'
        self.itot = InteractiveTreeOfThought(self.config_path)

    def test_interactive_mode(self):
        # Simuler une session interactive
        problem = "Trouver une équation pour obtenir 24 avec les nombres 4, 9, 10, 13."
        self.itot.interactive_mode(problem)
        # Ce test nécessiterait des méthodes de mock pour les entrées utilisateur

if __name__ == '__main__':
    unittest.main()
