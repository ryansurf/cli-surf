# Tests

Tests can be run using the `Makefile` in the root of the project

`make test`

Alternatively, navigate to `/test` and run:

`pytest`

On a push/pull request, git will run `pytest` for you to catch any errors.

## Writing Tests

In `/tests`, there are multiple files for different types of test cases.

- `test_helper.py`: Tests functions in `src/helper.py` (functions like rounding decimals, etc.)
- `test_api.py`: Tests functions in `src/api.py`.
- `test_server.py`: Tests the Flask server in `src/server.py`
- `test_gpt.py`: Tests functions server in `src/gpt.py`
- `test_cli.py`: Tests the function server in `src/cli.py`

Writing tests is encouraged, especially if you introduce a new function/feature!

## Coverage Report

On each commit/Pull Request a coverage report should be automatically generated and posted
in the commit's comments. It is helpful to get an idea of where tests are lacking.

<p align="center">
    <img src="https://github.com/ryansurf/cli-surf/blob/main/images/coverage_report.PNG?raw=true" alt="coverage report png">
</p>