# this image uses esbuilt and everything es as defined in the run yarbuild:* scritps , to bundle the assets and save them in the public/ folder (wokrs cause this whole diretory is mounted in the docker-compose.yml file)
FROM node:22.14.0-bookworm-slim AS assets
LABEL maintainer="Nick Janetakis <nick.janetakis@gmail.com>"

WORKDIR /app/assets

ARG UID=1000
ARG GID=1000

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && groupmod -g "${GID}" node && usermod -u "${UID}" -g "${GID}" node \
  && mkdir -p /node_modules && chown node:node -R /node_modules /app

RUN npm install -g corepack

USER node

COPY --chown=node:node assets/package.json assets/*yarn* ./


RUN corepack enable

RUN yarn install && yarn cache clean

ARG NODE_ENV="production"
ENV NODE_ENV="${NODE_ENV}" \
  PATH="${PATH}:/node_modules/.bin" \
  USER="node"

COPY --chown=node:node . ..

RUN if [ "${NODE_ENV}" != "development" ]; then \
  ../bin/run yarn:build:js && ../bin/run yarn:build:css; else mkdir -p /app/public; fi

CMD ["bash"]

###############################################################################

# this images uses the uv tool to install the dependencies in a iamge, to be copied over sometime later
FROM python:3.13.2-slim-bookworm AS app-build
LABEL maintainer="Nick Janetakis <nick.janetakis@gmail.com>"

WORKDIR /app

ARG UID=1000
ARG GID=1000

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && groupadd -g "${GID}" python \
  && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" python \
  && chown python:python -R /app

COPY --from=ghcr.io/astral-sh/uv:0.6.9 /uv /uvx /usr/local/bin/

USER python

COPY --chown=python:python pyproject.toml uv.lock* ./
COPY --chown=python:python bin/ ./bin

ENV PYTHONUNBUFFERED="true" \
  PYTHONPATH="." \
  UV_COMPILE_BYTECODE=1 \
  UV_PROJECT_ENVIRONMENT="/home/python/.local" \
  PATH="${PATH}:/home/python/.local/bin" \
  USER="python"

RUN chmod 0755 bin/* && bin/uv-install

CMD ["bash"]

###############################################################################
# this image 
# - copies the bundled assests from /app/public (mount volume) into it /public (on image)
# - copies the installed dependencies from the app-build image into it

FROM python:3.13.2-slim-bookworm AS app
LABEL maintainer="Nick Janetakis <nick.janetakis@gmail.com>"

WORKDIR /app

ARG UID=1000
ARG GID=1000

RUN apt-get update \
  && apt-get install -y --no-install-recommends curl libpq-dev \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && groupadd -g "${GID}" python \
  && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" python \
  && chown python:python -R /app

USER python

ARG FLASK_DEBUG="false"
ENV FLASK_DEBUG="${FLASK_DEBUG}" \
  FLASK_APP="projekt_4.app" \
  FLASK_SKIP_DOTENV="true" \
  PYTHONUNBUFFERED="true" \
  PYTHONPATH="." \
  UV_PROJECT_ENVIRONMENT="/home/python/.local" \
  PATH="${PATH}:/home/python/.local/bin" \
  USER="python"

COPY --chown=python:python --from=assets /app/public /public
COPY --chown=python:python --from=app-build /home/python/.local /home/python/.local
COPY --from=app-build /usr/local/bin/uv /usr/local/bin/uvx /usr/local/bin/
COPY --chown=python:python . .

RUN if [ "${FLASK_DEBUG}" == "true" ]; then \
  ln -s /public /app/public; fi

RUN if [ "${FLASK_DEBUG}" != "true" ]; then \
  ln -s /public /app/public && SECRET_KEY=dummy flask digest compile && rm -rf /app/public; fi

ENTRYPOINT ["/app/bin/docker-entrypoint-web"]

EXPOSE 8000

CMD ["gunicorn", "-c", "python:config.gunicorn", "projekt_4.app:app"]
