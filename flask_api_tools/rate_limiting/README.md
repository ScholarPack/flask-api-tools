# Flask API Tools - Rate Limiting
A tool for handling rate limiting.

# Installation/Setup
See [README.md](https://github.com/ScholarPack/flask-api-tools/blob/master/README.md#installation)

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