import unittest
from treeofthought.exporters import export_tree_to_json, export_tree_to_image

class TestExporters(unittest.TestCase):
    def test_export_tree_to_json(self):
        tree = ["Root", "Node 1", "Node 2"]
        export_tree_to_json(tree, 'tree.json')
        with open('tree.json', 'r') as file:
            data = file.read()
            self.assertIn("Root", data)

    def test_export_tree_to_image(self):
        tree = ["Root", "Node 1", "Node 2"]
        export_tree_to_image(tree, 'tree')
        self.assertTrue(os.path.exists('tree.png'))

if __name__ == '__main__':
    unittest.main()
