import os
import tempfile
import shutil
from dotenv import load_dotenv
from parser import build_docu
from sp_docs.gen_docu import sphinx_gen_docs

def process_folder_and_generate_docs(input_folder, output_folder="docs"):
    """
    Process a folder of Python source files, add docstrings, save them in a temp folder,
    and generate documentation using Sphinx.

    Args:
        input_folder (str): Path to the folder containing Python source files.
        output_folder (str): Path to the folder where documentation will be generated.
    """
    if not os.path.isdir(input_folder):
        raise ValueError(f"The input folder '{input_folder}' does not exist or is not a directory.")

    # Create a temporary folder to store modified files
    temp_folder = os.path.join(os.path.dirname(input_folder), "temp")
    os.makedirs(temp_folder, exist_ok=True)

    try:
        # Process each Python file in the input folder
        for root, _, files in os.walk(input_folder):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r") as f:
                        original_code = f.read()

                    # Use build_docu to add docstrings
                    modified_code = build_docu(file_path)

                    # Save the modified code to the temp folder
                    relative_path = os.path.relpath(file_path, input_folder)
                    temp_file_path = os.path.join(temp_folder, relative_path)
                    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
                    with open(temp_file_path, "w") as temp_file:
                        temp_file.write(modified_code)

        # Generate documentation using sphinx_gen_docs
        sphinx_gen_docs(temp_folder, output_folder)

    finally:
        # Clean up the temporary folder
        shutil.rmtree(temp_folder)

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file if needed
    input_folder = "D:/OTH/6. Semester/KIP/ki_projekt/prompter"
    output_folder = "D:/OTH/6. Semester/KIP/ki_projekt/docs"
    process_folder_and_generate_docs(input_folder, output_folder)