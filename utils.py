import requests

def dynamic_decomposition(problem, config):
    """
    Fonction de décomposition dynamique utilisant les étapes de décomposition définies dans la configuration.

    :param problem: Le problème à résoudre.
    :param config: La configuration chargée depuis le fichier JSON.
    :return: Une liste d'étapes intermédiaires pour décomposer le problème.
    """
    steps = config.get("decomposition_steps", [])
    return steps

def enhanced_decomposition(problem, config):
    """
    Utilise une API externe pour enrichir la décomposition.

    :param problem: Le problème à résoudre.
    :param config: La configuration chargée depuis le fichier JSON.
    :return: Une liste d'étapes intermédiaires pour décomposer le problème.
    """
    api_urls = config.get("api_urls")
    response = requests.get(f"{api_urls['primary']}?problem={problem}")
    if response.status_code != 200:
        response = requests.get(f"{api_urls['secondary']}?problem={problem}")
    
    if response.status_code == 200:
        steps = response.json().get('steps', config.get("decomposition_steps", []))
    else:
        steps = config.get("decomposition_steps", [])
    return steps

def get_decompose_function(name):
    """
    Récupère la fonction de décomposition par son nom.
    """
    functions = {
        "dynamic_decomposition": dynamic_decomposition,
        "enhanced_decomposition": enhanced_decomposition
    }
    return functions.get(name, dynamic_decomposition)