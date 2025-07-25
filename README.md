## ki_projekt


## Installation
Das Projekt kann easy mit [Docker](https://docs.docker.com/desktop/) gestartet werden, ohne das irgendetwas anderes gemacht werden muss.
```zsh
git clone https://github.com/seeeebaaaa/ki_projekt.git
cd ki_projekt/
docker compose up --build -d
```
Damit wird alles relevante geladen und gestartet. Anschließend ist die Seite über [http://localhost:8000](http://localhost:8000) erreichbar.
Manchmal ist es trotzdem nötig die NPM/Yarn Dependencies schon selber zu installieren. Dafür einfach unter [#yarn](#yarn) lesen.

# Dev-Installation
Ansich kann auch direkt so damit gearbeitet werden, aber damit z.B. VS Code alle Pakete und Abhängigkeiten (Python/JS) finden kann, müssen diese mit [*uv*](https://github.com/astral-sh/uv?tab=readme-ov-file#installation) (Schnelleres **pip*) und [*yarn*](https://yarnpkg.com/getting-started/install) (Schnelleres *npm*) installiert werden.
## uv
[Installation Anleitung](https://github.com/astral-sh/uv?tab=readme-ov-file#installation)
Anschließend kann ganz einfach ein Python-Enviroment erstellt werden mit:
```zsh
uv sync
```
Dannach das Enviroment einfach mit `source .venv/bin/activate` (oder für windows: `./.venv/Scripts/activate`) aktivieren.
###### Hilfreiche Befehle:
```zsh
uv tree # Zeigt Dependency Graphen für benötigte Projekte an
uv add numpy # = pip install numpy 
uv remove numpy # = pip uninstall numpy 
uv lock # erstellt  die uv.lock file
```
## yarn
[Installation Anleitung](https://yarnpkg.com/getting-started/install)
Alles relevante für yarn passiert in dem `assets/` Ordner, da dort die JavScript und CSS Dateien liegen, sowie die `yarn.lock` Datei.
Sprich, `yarn` **immer** nur im `assets/` Ordner nutzen/asuführen.
> **Wichtig:** es muss (fast) immer `--modules-folder node_modules/` als Argument angegeben werden, da per default, auf Grund des Setups mit Docker, Yarn versuchen wird die Pakete unter `/node_modules` zu installieren.
###### Hilfreiche Befehle
```zsh
yarn info # Zeigt Dependency Graphen für benötigte Projekte an
yarn add jquer --modules-folder node_modules/ # = npm install jquery 
yarn remove jquery --modules-folder node_modules/ # = npm uninstall jquery 
```

## Additional Info

Um die Logs (und eventuelle Probleme einzusehen, einfach `docker compose logs` nutzen, bzw. um die Logs von einem bestimmtem Container zu sehen den Namen (ast,web,js,css,...) anhängen. Z.B: `docker compose logs web`)
Wenn Änderungen an `tasks.py`, oder Sachen die `task.py` u.ä. nutzt, gemacht wurden, dann muss es neu gebuilded/gestartet werden, da Celery sonst die Taskts nicht aktualisiert. (vmtl reichts den worker container neu zu starten/builden, aber idk)


## Sphinx

In /docs können testweise Docs mit Sphinx generiert werden. Dazu im Root des projekts diesen Befehl aufrufen und <ordner> mit dem entsprechenden ordner mit den source files ersetzen:
```shell
sphinx-apidoc -o docs <ordner>/
```
Danach 
```shell
./docs/make html
```
Damit wird die Website gebaut, die man dann browsen und klicken kann