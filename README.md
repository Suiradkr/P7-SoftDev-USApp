# gudlift-registration

### Why

This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

### Getting Started

This project uses the following technologies:

* Python v3.x+
* [Flask](https://flask.palletsprojects.com/)
* [Virtual environment](https://docs.python.org/3/library/venv.html)


### Installation

- Clone the repository and create a new virtual (```python -m venv <VENV_FOLDER>```)

- Make sure the virtual environment you created is active ```source <VENV_FOLDER>/bin/activate```


- Install the requirements based on the `requirements.txt` file: `pip install -r requirements.txt`

- Run the application with `python server.py`. The app will start and display in the terminal a link where you can access it (locally) using your browser.

### Current setup

The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). They live in the `data` folder.
    
* `competitions.json` - list of competitions
* `clubs.json` - list of clubs with relevant information. Inspect this file to find email addresses you can use to login.

### Testing

The project uses [pytest](https://docs.pytest.org/). You should also use [coverage](https://coverage.readthedocs.io/) to create a coverage report.

Make sure your virtual environment is active and the testing tools are installed:

```
pip install pytest coverage flake8
```

To run the tests:

```
python -m pytest
```

Add `-v` for the name of each test as it runs:

```
python -m pytest -v
```

To run the tests with a coverage report:

```
python -m coverage run -m pytest
python -m coverage report
```

We aim to keep coverage above 80%.

### Code style

The Python code is PEP 8 compliant and checked with
[Flake8](https://flake8.pycqa.org/). The project's settings (line length and
excluded folders) live in `setup.cfg`.

```
python -m flake8
```

### Branch naming

Work never lands directly on `main`. Create a branch named
`<feature/bug/enhancement>/<issue-number>-<description>`, for example
`bug/4-book-in-past-competitions`. When the tests pass, the branch is merged
into the `QA` branch for code review.
