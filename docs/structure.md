# Structure

The basic structure of the project is:

```
├── docs
├── images
├── src
    ├── static
    ├── templates
    └── tests
```

- `docs`: Contains markdown for the documentation (this website!)
- `images`: Images/GIFs/Media
- `src`: Source code!
    - `src/static`: JavaScript
    - `src/templates`: HTML
    - `src/tests`: Testing files



More in-depth structure:

```
├── CONTRIBUTING.md
├── Dockerfile
├── docs
│   ├── faq.md
│   ├── index.md
│   ├── install.md
│   ├── setup.md
│   ├── styling.md
│   └── tests.md
├── help.txt
├── images
│   ├── ocean.gif
│   ├── surf.gif
│   ├── wave.png
│   └── website.gif
├── mkdocs.yml
├── README.md
├── requirements.txt
├── src
│   ├── api.py
│   ├── art.py
│   ├── cli.py
│   ├── helper.py
│   ├── __init__.py
│   ├── send_email.py
│   ├── server.py
│   ├── static
│   │   └── script.js
│   ├── templates
│   │   └── index.html
│   └── tests
│       ├── __init__.py
│       └── test_code.py
├── start_venv.sh
└── venv
```