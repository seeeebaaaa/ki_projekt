## ki_projekt

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

run with `docker compose up -d --build` from root
install yarn/npm packages with `yarn add ... --modules-folder node_modules` from ./assets
install python dependencies/packages with `uv ...` from root
activate python enviroment with `uv sync`