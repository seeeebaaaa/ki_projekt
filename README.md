## ki_projekt

## Todos:

- Rausfinden wie LLM mit funtktion + docstring (oder sphinx docs?) dokoumentation überprüfen kann, bzw. erstellen kann. (was für LLm, API? etc)
- Rausfinden wie/was/wo Sphinx kann
- Python Code erstellen
- Maybe frage nach UML/Mermaid/etc klären

## Installation
Run the projekt via docker.
Make sure you have [Docker installed](https://docs.docker.com/desktop/) and execute all commands in the right folder.
```zsh
# go into source folder
cd src/
# start up docker images, volumes and networks
docker compose up -d --build
# check status of images
docker compose ps
# to stop it simply run
docker compose down
```


# manual sphinx run

[see](https://github.com/cimarieta/sphinx-autodoc-example)
```zsh
# cd into docs directory
cd docs/
# generate source files from module
sphinx-apidoc -f -o ../docs/source ../projekt_4
# generate html docs in docs/build/html
make html
```