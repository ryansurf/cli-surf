<a href=""><img src="https://github.com/ryansurf/cli-surf/blob/main/images/wave.png" width="100 " align="right" /></a>

# Contributing to cli-surf

Thank you for your interest in contributing to cli-surf! All contributions are welcome, from commenting issues to reviewing or sending Pull Requests.

Join the [Discord](https://discord.gg/He2UpxRuJP)!

## How to contribute?

If you are new to GitHub, visit the [first-contributions instructions](https://github.com/firstcontributions/first-contributions/blob/master/README.md) to learn how to contribute on GitHub.

To find issues you can help with, go though the list of [good first issues](https://github.com/ryansurf/cli-surf/labels/good%20first%20issue) or issues labeled with [help wanted](https://github.com/ryansurf/cli-surf/labels/help%20wanted).

Once you find an interesting issue let us know that you want to work on it by commenting on the issue.

## Development
### Install our development environment
1. Please set up your development environment by referring to the `Setup` section in the `README.md`.

2. Install the `pre-commit`:
    ```
    pre-commit install
    ```

### Code Style and Quality
- The [PEP 8](https://realpython.com/python-pep8/) styling convention is used.
- This is achieved using the `ruff` Linter and Formatter.
- The Linter and Formatter are automatically executed before committing via pre-commit.
  - If you want to run the Linter and Formatter at any time, execute `pre-commit run --all-files`.

### Testing
> [!NOTE]
> This project uses `Makefile` as a task runner. You need to set up your environment to be able to run the `make` command.

Run the following command in the project's root directory:
```bash
# Run tests locally using Poetry
make test

# Run tests Docker container
make test_docker
```
You can generate a coverage report with the following command:
```bash
# Generate a coverage report locally using Poetry
make output_coverage

# Generate a coverage report in a Docker container
make output_coverage_docker
```
Additionally, when a PR is raised, pytest will be executed by the GitHub Actions CI.


## Questions, suggestions or new ideas

Please don't open an issue to ask a question or suggestion. Instead, use the [GitHub Discussions](https://github.com/ryansurf/cli-surf/discussions) page. New ideas and enhacements are also welcome as discussion posts.

## Issue reporting

Feel free to [create a new issue](https://github.com/ryansurf/cli-surf/issues/new) if you have an issue to report! But first, make sure that the issue has not been reported yet.

Be sure to explain in details the context and the outcome that you are lookign for. If reporting bugs, provide basic information like your OS version, whether using Docker, etc.

Thanks! :ocean: :surfer:
