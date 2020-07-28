![Validate Build](https://github.com/ScholarPack/flask-api-tools/workflows/Validate%20Build/badge.svg)

# Flask API Tools
Utilities for building, running, and maintaining Python APIs with Flask and 
associated Flask extensions.

# Installation
Install and update using `pip`:

```bash 
pip install -U flask-api-tools
```

# Tools
* [Storage Backed Rate Limiting](https://github.com/ScholarPack/flask-api-tools/blob/master/flask_api_tools/rate_limiting/README.md)
* [Validators](https://github.com/ScholarPack/flask-api-tools/blob/master/flask_api_tools/validators/README.md)

# Developing
__The build pipeline requires your tests to pass and code to be formatted__

Make sure you have Python 3.x installed on your machine (use [pyenv](https://github.com/pyenv/pyenv)).

Install the dependencies with [pipenv](https://github.com/pypa/pipenv) (making sure to include dev and pre-release packages):

```bash
pipenv install --dev --pre
```

Configure your environment:

```bash
pipenv shell && export PYTHONPATH="$PWD"
```

Run the tests:

```bash
pytest
```

Or with logging:

```bash
pytest -s
```

Or tests with coverage:

```bash
pytest --cov=./
```

Format the code with [Black](https://github.com/psf/black):

```bash
black $PWD
```

# Releases
Cleanup the (.gitignored) `dist` folder (if you have one):

```bash
rm -rf dist
```

Notch up the version number in `setup.py` and build:

```bash
python3 setup.py sdist bdist_wheel
```

Push to PyPi (using the ScholarPack credentials when prompted)

```bash
python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```

# Links
* Releases: https://pypi.org/project/flask-api-tools/
* Code: https://github.com/ScholarPack/flask-api-tools
