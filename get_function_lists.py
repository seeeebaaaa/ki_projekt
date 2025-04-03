import ast
import tokenize
import os

def extract_functions_and_comments(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        tokens = tokenize.generate_tokens(f.readline)
        comments = []
        last_comment = []

        # Extract comments, both inline (#) and multiline (""" """)
        for token in tokens:
            if token.type == tokenize.COMMENT:
                last_comment.append(token.string.strip("# ").strip())
            elif token.type == tokenize.STRING and token.start[0] == token.end[0]:  # Single-line string
                #last_comment.append(token.string.strip('"').strip("'").strip())
                pass
            elif token.type == tokenize.STRING:  # Multiline string (potential comment)
                if token.start[0] != token.end[0]:  # Ensure it's a multiline string
                    last_comment.append(token.string.strip('"""').strip())
            
            elif token.type not in {tokenize.NL, tokenize.NEWLINE}:
                if last_comment:
                    comments.append((token.start[0], "\n".join(last_comment)))  # Store line number and comment
                    last_comment = []

    with open(file_path, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())

    functions = {}

    # Extract functions and their docstrings
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            docstring = ast.get_docstring(node)
            functions[func_name] = {
                "docstring": docstring,
                "comments": []
            }

            # Find comments before the function
            func_line = node.lineno
            for line, comment in comments:
                if func_line - 3 <= line <= func_line - 1:  # Check if a comment is right above the function
                    functions[func_name]["comments"].append(comment)

    return functions

def get_function_source(code, func_name):
    """Extracts the source code of a function given its name."""
    tree = ast.parse(code)
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            return ast.get_source_segment(code, node)
    
    return None

module_path = os.path.abspath("./projekt_4")
python_files = [os.path.join(module_path, file) for file in os.listdir(module_path) if file.endswith(".py")]
for python_file in python_files:
    # with open(python_file) as file:
    #     node = ast.parse(file.read())
    # functions = [n for n in node.body if isinstance(n, ast.FunctionDef)]
    # [show_function(f) for f in functions]
    # classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
    # print(classes)

    functions_data = extract_functions_and_comments(python_file)
    with open(python_file, 'r', encoding='utf-8') as f:
        source = get_function_source(f.read(),"world")
        print(source)
    # Print results
    for func, details in functions_data.items():
        print(f"Function: {func}")
        print(f"  Docstring: {details['docstring']}")
        print(f"  Comments: {details['comments']}")
        print("-" * 40)