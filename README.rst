# ki_projekt

Todos:
- Rausfinden wie LLM mit funtktion + docstring (oder sphinx docs?) dokoumentation überprüfen kann, bzw. erstellen kann. (was für LLm, API? etc)
- Rausfinden wie/was/wo Sphinx kann
- Python Code erstellen
- Maybe frage nach UML/Mermaid/etc klären

# installation
install moduel with `pip install -e .`

# manual sphinx run

```zsh
# cd into docs directory
cd docs/
# generate source files from module
sphinx-apidoc -f -o ../docs/source ../projekt_4
# generate html docs in docs/build/html
make html
```