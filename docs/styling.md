# Styling

## Code Style and Quality
The [PEP 8](https://realpython.com/python-pep8/) styling convention is used.

This is achieved using the ruff Linter and Formatter.

The Linter and Formatter are automatically executed before committing via pre-commit.

If you want to run the Linter and Formatter at any time, execute `pre-commit run --all-files`.

You may also run `make lint` or `make format` to run the linter/formatter on its own.
