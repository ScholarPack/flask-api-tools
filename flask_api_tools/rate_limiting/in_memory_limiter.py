from flask_limiter import Limiter
from flask import Flask
from limits.errors import ConfigurationError


class InMemoryLimiter(Limiter):
    """
    Class extends Flask-Limiter with Redis (or any other supported in-memory storage backend)
    configuration and automatic checks
    """

    def init_app(self, app: Flask) -> None:
        """
        patch self._check_storage into Flask-limiter, and ensure the storage backend is connected properly
        Attach limiter to Flask log handlers
        Called by ``self.__init__`` (if app supplied), else called directly - storage checks and
        log configuration below are run in all instances.
        :param app: ``Flask`` instance to initialize the extension with.
        :return: None
        :raise ConfigurationError: if storage is incorrectly configured
        """
        super().init_app(app=app)
        self._check_storage()

        if app:
            # Attach any existing Flask log handlers
            for handler in app.logger.handlers:
                self.logger.debug(f"Adding log handler to limiter: {str(handler)}")
                self.logger.addHandler(handler)

    def _check_storage(self) -> None:
        """
        Check the storage backed is connected correctly
        :return: None
        :raise ConfigurationError: if storage is incorrectly configured
        """
        if not self._storage.check():
            self.logger.critical(f"Invalid storage configuration: {self._storage_uri}")
            raise ConfigurationError(
                f"Invalid storage configuration: {self._storage_uri}"
            )
