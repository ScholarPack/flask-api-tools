import pytest
import fakeredis

from flask import Flask


@pytest.fixture(scope="function", autouse=True)
def app():
    app = Flask(__name__)
    server = fakeredis.FakeServer()
    server.connected = True
    app.redis = fakeredis.FakeStrictRedis(server=server)
    app.app_context().push()
    yield app
