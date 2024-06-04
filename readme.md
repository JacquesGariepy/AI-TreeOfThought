# AI-TreeOfThought

TreeOfThought est une bibliothèque Python puissante et flexible conçue pour résoudre des problèmes complexes en utilisant des modèles de langage avancés comme GPT4, GPT4o, etc. Cette bibliothèque permet la décomposition dynamique des problèmes, la génération et l'évaluation des pensées, ainsi que l'exportation des arbres de pensée générés.

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
- **Modèles de langage** : GPT4o, GPT4, GPT-3.5-turbo et autres modèles compatibles avec autogen
- **Format de configuration** : JSON
- **Bibliothèques utilisées** :
  - `graphviz` : Pour la visualisation des arbres de pensée. (non implémenté dans cette version)
  - `autogen` : Pour l'intégration des agents.
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

## Contributions

Les contributions sont les bienvenues ! Veuillez soumettre une pull request pour toute amélioration ou correction.

## License

Ce projet est sous licence MIT.
