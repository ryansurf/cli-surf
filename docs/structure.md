# Structure

The basic structure of the project is:

```
├── docs
├── images
├── src
│   ├── __pycache__
│   ├── static
│   └── templates
├── tests
```

- `docs`: Contains markdown for the documentation (this website!)
- `images`: Images/GIFs/Media
- `src`: Source code!
    - `src/static`: JavaScript
    - `src/templates`: HTML
- `tests`: Testing files



More in-depth structure:

<!-- STRUCTURE START -->
```
.
├── compose.yaml
├── CONTRIBUTING.md
├── dist
│   ├── cli_surf-0.1.0-py3-none-any.whl
│   └── cli_surf-0.1.0.tar.gz
├── Dockerfile
├── docs
│   ├── cheat_sheet.md
│   ├── faq.md
│   ├── index.md
│   ├── install.md
│   ├── setup.md
│   ├── structure.md
│   ├── styling.md
│   └── tests.md
├── help.txt
├── images
│   ├── cli.gif
│   ├── coverage_report.PNG
│   ├── ocean.gif
│   ├── old_cli.gif
│   ├── wave.png
│   └── website.gif
├── makefile
├── mkdocs.yml
├── poetry.lock
├── pyproject.toml
├── README.md
├── src
│   ├── api.py
│   ├── art.py
│   ├── cli.py
│   ├── dev_streamlit.py
│   ├── gpt.py
│   ├── helper.py
│   ├── __init__.py
│   ├── __pycache__
│   ├── send_email.py
│   ├── server.py
│   ├── settings.py
│   ├── static
│   ├── streamlit_helper.py
│   └── templates
└── tests
    ├── __init__.py
    ├── __pycache__
    ├── test_api.py
    ├── test_cli.py
    ├── test_gpt.py
    ├── test_helper.py
    └── test_server.py

10 directories, 42 files
```
<!-- STRUCTURE END  -->
