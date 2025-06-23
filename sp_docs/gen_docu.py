import os
import sys
from sphinx.application import Sphinx


def sphinx_gen_docs(repo_path, output_path):
    """
    Generate documentation using Sphinx from docstrings in the given code repository.

    Args:
        repo_path (str): Path to the root folder of the code repository.
        output_path (str): Path to the folder where documentation will be generated.
    """
    # Ensure the repository path exists
    if not os.path.isdir(repo_path):
        raise ValueError(
            f"The repository path '{repo_path}' does not exist or is not a directory."
        )

    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Paths for Sphinx
    source_dir = os.path.join(output_path, "source")
    build_dir = os.path.join(output_path, "build")
    os.makedirs(source_dir, exist_ok=True)

    # Add the repository path to sys.path for autodoc to work
    sys.path.insert(0, os.path.abspath(repo_path))

    # Create a minimal `conf.py` configuration dynamically
    conf_py_content = f"""
import os
import sys
sys.path.insert(0, os.path.abspath('{repo_path}'))

extensions = [
    'sphinx.ext.autodoc', 
    "sphinx.ext.viewcode",
    'sphinx.ext.napoleon',  # For Google/NumPy style docstrings
]

templates_path = ['_templates']
exclude_patterns = []
html_theme = 'alabaster'
"""
    conf_py_path = os.path.join(source_dir, "conf.py")
    with open(conf_py_path, "w") as conf_file:
        conf_file.write(conf_py_content)

    # Create a minimal `index.rst` file dynamically
    index_rst_content = f"""
.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. automodule:: your_module
   :members:
   :undoc-members:
   :show-inheritance:
"""
    index_rst_path = os.path.join(source_dir, "index.rst")
    with open(index_rst_path, "w") as index_file:
        index_file.write(index_rst_content)

    # Run Sphinx programmatically
    app = Sphinx(
        srcdir=source_dir,
        confdir=source_dir,
        outdir=build_dir,
        doctreedir=os.path.join(output_path, "doctrees"),
        buildername="html",
    )
    app.build()

    print(f"Documentation generated successfully in '{build_dir}'.")


# Example usage
if __name__ == "__main__":
    repo_path = input("Enter the path to the root folder of the code repository: ")
    sphinx_gen_docs(repo_path)
