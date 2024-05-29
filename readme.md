# TreeOfThought

TreeOfThought est une bibliothèque Python puissante et flexible conçue pour résoudre des problèmes complexes en utilisant des modèles de langage avancés comme GPT-3.5-turbo. Cette bibliothèque permet la décomposition dynamique des problèmes, la génération et l'évaluation des pensées, ainsi que l'exportation des arbres de pensée générés.

## Fonctionnalités

- **Décomposition dynamique des problèmes** : Décompose les problèmes en étapes intermédiaires configurables, permettant une analyse approfondie et structurée.
- **Génération de pensées** : Génère des pensées candidates à partir d'un état donné, en utilisant des modèles de langage avancés pour proposer des solutions créatives et variées.
- **Évaluation des états** : Évalue les états intermédiaires pour déterminer leur pertinence, en utilisant des critères configurables pour scorer chaque état.
- **Recherche en profondeur avec retour arrière** : Explore les solutions potentielles en profondeur avec la possibilité de revenir en arrière, assurant une exploration exhaustive de l'espace des solutions.
- **Mode interactif** : Permet aux utilisateurs d'interagir avec le processus en temps réel, offrant une flexibilité et une adaptabilité accrues.
- **Support multi-API** : Utilise plusieurs API pour la décomposition et l'évaluation des états, garantissant une redondance et une fiabilité accrues.
- **Export des arbres de pensées** : Exporte les arbres sous forme de fichiers JSON ou images, facilitant le partage et l'analyse des résultats.
- **Utilisation de modèles locaux** : Ajout de la possibilité d'utiliser des modèles de langage locaux, offrant une alternative aux modèles hébergés sur des serveurs distants.

## Spécifications Techniques

- **Langage de programmation** : Python
- **Modèles de langage** : GPT-3.5-turbo et autres modèles compatibles avec l'API LiteLLM
- **Format de configuration** : JSON
- **Bibliothèques utilisées** :
  - `graphviz` : Pour la visualisation des arbres de pensée.
  - `litellm` : Pour l'intégration avec les modèles de langage GPT.
  - `requests` : Pour les appels API.
  - `logging` : Pour la gestion des logs et des erreurs.
- **Compatibilité** : Python 3.7 et versions ultérieures

## Installation

```bash
pip install -r requirements.txt


```bash
treeofthought/
    __init__.py
    tree.py
    utils.py
    config.py
    interactive.py
    exporters.py
tests/
    test_tree.py
    test_interactive.py
    test_exporters.py
config.json



# Configuration

Le fichier de configuration `config.json` doit contenir toutes les configurations nécessaires, y compris les URL d'API, les étapes de décomposition et d'autres paramètres.

```json
{
    "model_name": "gpt-3.5-turbo",
    "api_key": "your-api-key",
    "decompose_function": "dynamic_decomposition",
    "num_candidates": 5,
    "max_depth": 5,
    "breadth_limit": 5,
    "value_threshold": 0.5,
    "decomposition_steps": [
        "Étape 1: Analyser le problème.",
        "Étape 2: Diviser en sous-problèmes.",
        "Étape 3: Résoudre chaque sous-problème."
    ],
    "api_urls": {
        "primary": "https://api.example.com/decompose",
        "secondary": "https://api.alternate.com/decompose"
    }
}
```

## Utilisation

### Classe Principale : TreeOfThought

#### Initialisation

```python
from treeofthought.tree import TreeOfThought

tot = TreeOfThought(config_path='config.json')
```

#### Décomposition d'un Problème

```python
problem = "Trouver une équation pour obtenir 24 avec les nombres 4, 9, 10, 13."
steps = tot.decompose_problem(problem)
print(steps)
```

#### Génération de Pensées

```python
state = "Analyser le problème"
thoughts = tot.generate_thoughts(state)
print(thoughts)
```

#### Évaluation des États

```python
states = ["State 1", "State 2"]
evaluated_states = tot.evaluate_states(states)
print(evaluated_states)
```

#### Recherche en Profondeur avec Retour Arrière

```python
solution = tot.backtrack_search(problem)
print("Solution trouvée:", solution)
```

### Mode Interactif : InteractiveTreeOfThought

#### Initialisation

```python
from treeofthought.interactive import InteractiveTreeOfThought

itot = InteractiveTreeOfThought(config_path='config.json')
```

#### Démarrage du Mode Interactif

```python
itot.interactive_mode(problem)
```

### Export des Arbres de Pensées

#### Export en JSON

```python
from treeofthought.exporters import export_tree_to_json

tree = ["Root", "Node 1", "Node 2"]
export_tree_to_json(tree, 'tree.json')
```

#### Export en Image

```python
from treeofthought.exporters import export_tree_to_image

tree = ["Root", "Node 1", "Node 2"]
export_tree_to_image(tree, 'tree')
```

## Tests Unitaires

### Installation des Dépendances de Test

```bash
pip install -r test_requirements.txt
```

### Exécution des Tests

```bash
python -m unittest discover -s tests
```

### Fichiers de Test

#### tests/test_tree.py

```python
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
```

#### tests/test_interactive.py

```python
import unittest
from unittest.mock import patch
from treeofthought.interactive import InteractiveTreeOfThought

class TestInteractiveTreeOfThought(unittest.TestCase):
    def setUp(self):
        self.config_path = 'config.json'
        self.itot = InteractiveTreeOfThought(self.config_path)

    @patch('builtins.input', side_effect=['next', 'eval', 'exit'])
    def test_interactive_mode(self, mock_input):
        problem = "Trouver une équation pour obtenir 24 avec les nombres 4, 9, 10, 13."
        self.itot.interactive_mode(problem)
        # Ce test vérifie que les commandes interactives fonctionnent

if __name__ == '__main__':
    unittest.main()
```

#### tests/test_exporters.py

```python
import unittest
import os
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
        self.assertTrue(os.path.exists('tree.pdf'))

if __name__ == '__main__':
    unittest.main()
```

## Contributions

Les contributions sont les bienvenues ! Veuillez soumettre une pull request pour toute amélioration ou correction.

## License

Ce projet est sous licence MIT.
