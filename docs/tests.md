# Tests

To run tests, install pytest, `pip install pytest` and navigate to `/test`.

Run `pytest`

On a push/pull request, git will run `pytest` for you to catch any errors.

## Writing Tests

In `/tests`, there are multiple files for different types of test cases.

- `test_helper.py`: Tests functions in `src/helper.py` (functions like rounding decimals, etc.)
- `test_api.py`: Tests functions in `src/api.py`.
- `test_server.py`: Tests the Flask server in `src/server/py`

Writing tests is encouraged, especially if you introduce a new function/feature!
