import os
from dotenv import load_dotenv
import ast
from projekt_4.api_clients import AI_API, GoogleGenAI_API, Ollama_API
from parser.parse_file import python_parse_file

def parse_code():
    code = None

    file_path = os.path.join(os.path.dirname(__file__), "projekt_4", "api_clients.py")
    with open (file_path, "r") as file:
        code = file.read()

    ast_code = python_parse_file(file_path)
    return ast_code, code

def generate_docs_from_ast(ast_tree, llm_api: AI_API):
    code = ast.unparse(ast_tree)
    docstrings = llm_api.generate_docs(code)
    # for node in ast.walk(ast_tree):
    #     if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
    #         try:
    #             # Insert the generated docstring into the AST node
    #             docstring = "test"
    #             if (ast.get_docstring(node)):
    #                 node.body[0] = ast.Expr(value=ast.Constant(value=docstring))
    #             else:
    #                 node.body.insert(0, ast.Expr(value=ast.Constant(value=docstring)))
    #         except StopIteration:
    #             break
    
    class DocstringTransformer(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            self.generic_visit(node)  # Ensure we visit all children
            docstring = self.find_docstring(node)
            return self.insert_docstring(node, docstring=docstring)

        def visit_ClassDef(self, node):
            self.generic_visit(node)  # Ensure we visit all children
            docstring = self.find_docstring(node)
            return self.insert_docstring(node, docstring=docstring)
            
        def find_docstring(self, node):
            """
            Finds the docstring for a given AST node.
            """
            if isinstance(node, ast.FunctionDef):
                type = 'function'
            else:
                type = 'class'

            for comment in docstrings.comments:
                if comment.type == type and comment.name == node.name:
                    return comment.documentation
            
            return None

        def insert_docstring(self, node, docstring):
            """
            Inserts a docstring into the given AST node.
            """
            if hasattr(node, 'body') and isinstance(node.body, list):
                if node.body and isinstance(node.body[0], ast.Expr):
                    # If there's already a docstring, replace it
                    node.body[0] = ast.Expr(value=ast.Constant(value=docstring))
                else:
                    # Otherwise, insert a new docstring
                    node.body.insert(0, ast.Expr(value=ast.Constant(value=docstring)))

            return node

    ast.fix_missing_locations(DocstringTransformer().visit(ast_tree))
    return ast_tree

# Example usage
if __name__ == "__main__":
    load_dotenv()
    # gemini = GoogleGenAI_API(GoogleGenAI_API.Models.GEMINI_2x0_FLASH)
    ollama = Ollama_API(Ollama_API.Models.LLAMA3_70B)
    # print(ai_api.simple_prompt("what is the capital of denmark?"))

    ast_tree, code = parse_code()

    # docu = ollama.generate_docs(code)

    ast_tree_with_docs = generate_docs_from_ast(ast_tree, ollama)

    docu_code = ast.unparse(ast_tree_with_docs)

    # docu = gemini.generate_docs(code)

    print(docu_code)