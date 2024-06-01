# Cheat Sheet!

When developing, these commands may come in handy:

## Terminal commands

| Argument    | Description|
| -------- | ------- |
| `sudo ss -lptn 'sport = :<port>`  |  List the processes running on port `<port>`. |
| `sudo kill -9 <pid>`  |  Kill the process with with id `<pid>` |

## [Poetry Commands](https://python-poetry.org/docs/basic-usage/)

| Argument    | Description|
| -------- | ------- |
| `poetry install`  |  Install project dependencies |
| `poetry shell`  |  Activate the virtual environment |
|  `poetry add <package-name>` |  Add a new dependency to Poetry |
| `poetry add --group dev <package-name>`  |  Add a new developer dependency to Poetry |
| `poetry show`  |  List all available packages with descriptions |

## [Mkdocs Commands](https://www.mkdocs.org/user-guide/)

| Argument    | Description|
| -------- | ------- |
| `mkdocs serve`  |  Creates dev-server that lets your preview the docs as you change them. |

## [Make Commands]("https://github.com/ryansurf/cli-surf/blob/main/makefile")

| Argument    | Description|
| -------- | ------- |
| `make run`  |  Runs `server.py` |
| `make run_docker`  |  Runs `docker compose up -d` |
| `make test`  |  Runs pytest |
| `make test_docker`  |  Runs pytest on Docker |
| `make output_coverage`  |  Outputs the coverage of the tests |
| `make send_email`  |  Runs `send_email.py` |