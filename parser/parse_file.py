from pathlib import Path
import ast
from tqdm.auto import tqdm

PROJECT_PATH = "/projekt_4/"


def python_parse_file(file_path):
    file = Path(file_path)
    if not file.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")
        # if not file_path.startswith(PROJECT_PATH):
        raise ValueError(
            f"The file {file_path} is not within the allowed path {PROJECT_PATH}."
        )
    if not file.suffix == ".py":
        raise ValueError(f"The file {file_path} is not a Python (.py) file.")

    # no need to tokenize, as ast can extract docstrings
    # parse file with ast
    with open(file_path) as file:
        code = file.read()
    file_tree = ast.parse(code)
    # get list of functions
    function_nodes = [
        node for node in file_tree.body if isinstance(node, ast.FunctionDef)
    ]
    # get list of classes
    class_nodes = [node for node in file_tree.body if isinstance(node, ast.ClassDef)]

    function_list = []
    class_list = []

    # function_list = [
    #     {
    #         "name": node.name,
    #         "docstring": ast.get_docstring(node),
    #         "source": ast.get_source_segment(code, node),
    #         "node": node,
    #         "file": file_path,
    #     }
    #     for node in function_nodes
    # ]
    # class_list = [
    #     {
    #         "name": node.name,
    #         "docstring": ast.get_docstring(node),
    #         "source": ast.get_source_segment(code, node),
    #         "node": node,
    #         "file": file_path,
    #     }
    #     for node in class_nodes
    # ]

    def parse_node(node, code):
        """Recursively parse a node to extract its structure."""
        if isinstance(node, ast.FunctionDef):
            new_node = {
                "name": node.name,
                "docstring": ast.get_docstring(node),
                "source": ast.get_source_segment(code, node),
                "node": node,
                "children": [
                    parse_node(child, code)
                    for child in node.body
                    if isinstance(child, (ast.FunctionDef, ast.ClassDef))
                ],
            }
            function_list.append(new_node)
            return new_node
        elif isinstance(node, ast.ClassDef):
            new_node = {
                "name": node.name,
                "docstring": ast.get_docstring(node),
                "source": ast.get_source_segment(code, node),
                "node": node,
                "children": [
                    parse_node(child, code)
                    for child in node.body
                    if isinstance(child, (ast.FunctionDef, ast.ClassDef))
                ],
            }
            class_list.append(new_node)
            return new_node
        return None

    nodes = [parse_node(node, code) for node in file_tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))]

    return function_list, class_list


def python_parse_folder(folder_path, recursive=True):
    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"The folder {folder_path} does not exist.")
    if not folder_path.startswith(PROJECT_PATH):
        raise ValueError(
            f"The folder {folder_path} is not within the allowed path {PROJECT_PATH}."
        )

    function_list = []
    class_list = []
    # only get subfolders if recursive is True
    if recursive:
        file_list = folder_path.glob("**/*.py")
    else:
        file_list = folder_path.glob("*.py")

    for file in tqdm(file_list):
        file_functions, file_classes = python_parse_file(file)
        function_list.extend(file_functions)
        class_list.extend(file_classes)

    return function_list, class_list
