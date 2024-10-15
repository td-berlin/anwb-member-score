# anwb-member-score

[![check.yml](https://github.com/MedAmineGBerry/anwb-member-score/actions/workflows/check.yml/badge.svg)](https://github.com/MedAmineGBerry/anwb-member-score/actions/workflows/check.yml)
[![publish.yml](https://github.com/MedAmineGBerry/anwb-member-score/actions/workflows/publish.yml/badge.svg)](https://github.com/MedAmineGBerry/anwb-member-score/actions/workflows/publish.yml)
[![Documentation](https://img.shields.io/badge/documentation-available-brightgreen.svg)](https://MedAmineGBerry.github.io/anwb-member-score/)
[![License](https://img.shields.io/github/license/MedAmineGBerry/anwb-member-score)](https://github.com/MedAmineGBerry/anwb-member-score/blob/main/LICENCE.txt)
[![Release](https://img.shields.io/github/v/release/MedAmineGBerry/anwb-member-score)](https://github.com/MedAmineGBerry/anwb-member-score/releases)

This is the repo for ANWB Member score.

# Installation

Use the package manager [Poetry](https://python-poetry.org/):

```bash
poetry install
```

# Usage

```bash
poetry run anwb-member-score
```

# Possible commands to invoke: inv {command}:

```bash
inv --list
Available tasks:
  checks.all (checks)           Run all check tasks.
  checks.code                   Check the codes with ruff.
  checks.coverage               Check the coverage with coverage.
  checks.format                 Check the formats with ruff.
  checks.poetry                 Check poetry config files.
  checks.security               Check the security with bandit.
  checks.test                   Check the tests with pytest.
  checks.type                   Check the types with mypy.
  cleans.all (cleans)           Run all tools and folders tasks.
  cleans.cache                  Clean the cache folder.
  cleans.coverage               Clean the coverage tool.
  cleans.dist                   Clean the dist folder.
  cleans.docs                   Clean the docs folder.
  cleans.environment            Clean the project environment file.
  cleans.folders                Run all folders tasks.
  cleans.mlruns                 Clean the mlruns folder.
  cleans.mypy                   Clean the mypy tool.
  cleans.outputs                Clean the outputs folder.
  cleans.poetry                 Clean poetry lock file.
  cleans.projects               Run all projects tasks.
  cleans.pytest                 Clean the pytest tool.
  cleans.python                 Clean python caches and bytecodes.
  cleans.requirements           Clean the project requirements file.
  cleans.reset                  Run all tools, folders, sources, and projects tasks.
  cleans.ruff                   Clean the ruff tool.
  cleans.sources                Run all sources tasks.
  cleans.tools                  Run all tools tasks.
  cleans.venv                   Clean the venv folder.
  commits.all (commits)         Run all commit tasks.
  commits.bump                  Bump the version of the package.
  commits.commit                Commit all changes with a message.
  commits.info                  Print a guide for messages.
  containers.all (containers)   Run all container tasks.
  containers.build              Build the container image.
  containers.compose            Start up docker compose.
  containers.run                Run the container image.
  docs.all (docs)               Run all docs tasks.
  docs.api                      Generate the API docs with pdoc.
  docs.serve                    Serve the API docs with pdoc.
  formats.all (formats)         Run all format tasks.
  formats.imports               Format python imports with ruff.
  formats.sources               Format python sources with ruff.
  installs.all (installs)       Run all install tasks.
  installs.poetry               Install poetry packages.
  installs.pre-commit           Install pre-commit hooks on git.
  mlflow.all (mlflow)           Run all mlflow tasks.
  mlflow.doctor                 Run mlflow doctor.
  mlflow.serve                  Start the mlflow server.
  packages.all (packages)       Run all package tasks.
  packages.build                Build the python package.
  projects.all (projects)       Run all project tasks.
  projects.environment          Export the project environment file.
  projects.requirements         Export the project requirements file.
  projects.run                  Run an mlflow project from the MLproject file.

Default task: projects
```
