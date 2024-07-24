# Cheat Sheet!

When developing, these commands may come in handy:

## Terminal commands

| Argument    | Description|
| -------- | ------- |
| `sudo ss -lptn 'sport = :<port>'`  |  List the processes running on port `<port>`. |
| `sudo kill -9 <pid>`  |  Kill the process with with id `<pid>` |

## [Poetry Commands](https://python-poetry.org/docs/basic-usage/)

| Argument    | Description|
| -------- | ------- |
| `poetry install`  |  Install project dependencies |
| `poetry shell`  |  Activate the virtual environment |
|  `poetry add <package-name>` |  Add a new dependency to Poetry |
| `poetry add --group dev <package-name>`  |  Add a new developer dependency to Poetry |
| `poetry show`  |  List all available dependencies with descriptions |
| `poetry run pre-commit run --all-files`  |  Run the Linter & Formatter |

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


## [Git](https://education.github.com/git-cheat-sheet-education.pdf)

| Argument    | Description|
| -------- | ------- |
| `git clone <repo URL>`  |  Clones git repository to your local machine|
| `git add <file>`  |  Adds file to your next commit |
| `git commit -m <message>`  |  Commit your staged content (from `git add <file>`) |
| `git push`  |  Pushes local changes to remote repo branch |
| `git status`  |  Shows modified files |
| `git branch`  |  Shows the branches |
| `git checkout -b <branch>`  |  Creates a new branch, `branch`, and switches into it |
| `git branch -d <branch>`  |  Delete a local branch |
| `git push -u origin <branch-name>`  |  Pushes a local branch to the upstream remote repo |
| `git log --branches --not --remotes`  |  View commits that have not yet been pushed |