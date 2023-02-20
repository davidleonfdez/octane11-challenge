# syntax=docker/dockerfile:1
FROM python:3.11-slim-buster

RUN useradd --create-home --shell /bin/bash octane_user
USER octane_user
WORKDIR /home/octane_user

COPY requirements.txt ./
# This is redundant since we are installing from setup.py in a subsequent step,
# but safer, as requirements.txt contains dependencies with pinned versions.
# Installing from setup won't override these and will only install our package
# octanexchange, needed for some of our modules to work correctly
RUN pip install --no-cache-dir -r requirements.txt

COPY setup.cfg setup.py ./
COPY --chown=octane_user src src

# Install octanexchange package from setup.py
RUN pip install .

ENTRYPOINT [ "python", "src/octanexchange/exrates.py" ]
