import copy
import pytest

from flask_api_tools.rate_limiting.in_memory_limiter import InMemoryLimiter
from limits.errors import ConfigurationError


class TestInMemoryLimiter:
    def test_check_storage_successful(self, app):
        local_in_memory_limiter = copy.deepcopy(InMemoryLimiter)
        limiter = local_in_memory_limiter(app=app)

        limiter._storage.check = lambda: True
        limiter._check_storage()

    def test_check_storage_error(self, app):
        local_in_memory_limiter = copy.deepcopy(InMemoryLimiter)
        limiter = local_in_memory_limiter(app=app)

        limiter._storage.check = lambda: False
        with pytest.raises(ConfigurationError):
            limiter._check_storage()
