import os
import sys
from sphinx.application import Sphinx
from pathlib import Path
import subprocess
import shutil

def sphinx_gen_docs(repo_path, output_path, theme="alabaster"):
    """
    Generate documentation using Sphinx from docstrings in the given code repository.

    Args:
        repo_path (str): Path to the root folder of the code repository.
        output_path (str): Path to the folder where documentation will be generated.
    """
    if not os.path.isdir(repo_path):
        raise ValueError(f"The repository path '{repo_path}' does not exist or is not a directory.")

    os.makedirs(output_path, exist_ok=True)
    source_dir = Path(output_path) / "source"
    build_dir = Path(output_path) / "build"

    # Clear the folders first if they exist
    if source_dir.exists():
        shutil.rmtree(source_dir)
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if (Path(output_path)/"doctrees").exists():
        shutil.rmtree(Path(output_path)/"doctrees")

    os.makedirs(source_dir, exist_ok=True)
    os.makedirs(build_dir, exist_ok=True)

    sys.path.insert(0, str(Path(repo_path).absolute()))

    conf_py_content = f"""
import os
import sys
from pathlib import Path
import shutil
sys.path.insert(0, str(Path("{repo_path}").absolute()))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []
html_theme = '{theme}'
"""
    conf_py_path = source_dir / "conf.py"
    with open(conf_py_path, "w") as conf_file:
        conf_file.write(conf_py_content)

    # Ensure repo_path has an __init__.py to allow discovery
    for root, dirs, files in os.walk(repo_path):
        if "__init__.py" not in files:
            with open(os.path.join(root, "__init__.py"), "w"):
                pass

    # Identify only valid Python modules/packages (i.e., containing at least one .py file)
    valid_paths = []
    for root, dirs, files in os.walk(repo_path):
        if any(f.endswith(".py") for f in files):
            valid_paths.append(root)

    # Generate .rst files only for valid paths
    for path in valid_paths:
        subprocess.run([
            "sphinx-apidoc",
            "-o", str(source_dir),
            str(path),
            "--force",
            "--no-toc"
        ], check=True)

    # Create index.rst with toctree directive
    index_rst_path = source_dir / "index.rst"
    with open(index_rst_path, "w") as index_file:
        index_file.write("""
.. toctree::
   :maxdepth: 2
   :caption: API Documentation

""")
        for rst_file in sorted(source_dir.glob("*.rst")):
            if rst_file.name != "index.rst":
                index_file.write(f"   {rst_file.stem}\n")

    app = Sphinx(
        srcdir=str(source_dir),
        confdir=str(source_dir),
        outdir=str(build_dir),
        doctreedir=str(Path(output_path) / "doctrees"),
        buildername="html",
    )
    app.build()

    print(f"Documentation generated successfully in '{build_dir}'.")


# Example usage
if __name__ == "__main__":
    repo_path = input("Enter the path to the root folder of the code repository: ")
    sphinx_gen_docs(repo_path)
