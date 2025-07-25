import ast

from .api_clients import AI_API, GoogleGenAI_API, Ollama_API

def build_docu(json_ast: ast.AST):
    llm_api = Ollama_API(Ollama_API.Models.LLAMA3_70B)  
    ast_tree = ast.literal_eval(json_ast)
    docu_tree = generate_docs_from_ast(ast_tree, llm_api)

    return ast.unparse(docu_tree)

def generate_docs_from_ast(ast_tree, llm_api: AI_API):
    code = ast.unparse(ast_tree)
    docstrings = llm_api.generate_docs(code)
    
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