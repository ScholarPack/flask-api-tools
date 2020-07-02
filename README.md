![Validate Build](https://github.com/ScholarPack/flask-api-tools/workflows/Validate%20Build/badge.svg)

# Flask API Tools
Utilities for building, running, and maintaining Python APIs with Flask and 
associated Flask extensions.

# Installation
Install and update using `pip`:

```bash 
pip install -U flask-api-tools
```

## Storage Backed Rate Limiting
The ```InMemoryLimiter``` class is an extension of Flask-Limiter. This class
implements storage-backed rate limiting. You'll need to follow the rate limiting steps
outlined in [Flask-Limiter](https://flask-limiter.readthedocs.io/en/stable/), and 
you must provide a ```RATELIMIT_STORAGE_URL``` to a redis (or other in-memory data
structure) instance. 

This class attaches any existing Flask log handlers to Flask-Limiter.

Basic Flask usage:

```python
from flask import Flask
from flask_api_tools.rate_limiting.in_memory_limiter import InMemoryLimiter

app = Flask(__name__)
limiter = InMemoryLimiter(app=app, storage_uri="redis://localhost:6379")
```

This will raise a ```ConfigurationError``` (from ```limits.errors```) if the backend
storage is inaccessible. 

Alternatively, you can still benefit from the configuration checking when using
Flask-Limiter's ```init_app``` function:

```python
from flask import Flask
from flask_api_tools.rate_limiting.in_memory_limiter import InMemoryLimiter

app = Flask(__name__)
limiter = InMemoryLimiter(storage_uri="redis://localhost:6379")
# Do some other things with the limiter...
limiter.init_app(app=app)
```

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
