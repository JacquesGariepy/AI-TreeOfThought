import json
from graphviz import Digraph

def export_tree_to_json(tree, file_path):
    """
    Exporte l'arbre de pensées au format JSON.

    :param tree: L'arbre de pensées à exporter.
    :param file_path: Le chemin du fichier où sauvegarder l'arbre.
    """
    with open(file_path, 'w') as json_file:
        json.dump(tree, json_file)

def export_tree_to_image(tree, file_path):
    """
    Exporte l'arbre de pensées au format image.

    :param tree: L'arbre de pensées à exporter.
    :param file_path: Le chemin du fichier où sauvegarder l'image.
    """
    dot = Digraph(comment='Tree of Thoughts')
    for i, node in enumerate(tree):
        dot.node(str(i), node)
        if i > 0:
            dot.edge(str(i-1), str(i))
    dot.render(file_path, view=False)
