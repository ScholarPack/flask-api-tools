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

        if app:
            for handler in app.logger.handlers:
                self.logger.addHandler(handler)
                self.logger.debug(f"Added log handler to limiter: {str(handler)}")

        self._check_storage()

    def _check_storage(self) -> None:
        """
        Check the storage backed is connected correctly
        :return: None
        :raise ConfigurationError: if storage is incorrectly configured (and no fallback is enabled)
        """
        if self.enabled:
            self.logger.debug(
                f"Starting to check in-memory backend storage: {self._storage}"
            )
            if self._storage.check():
                self.logger.debug(
                    f"In-memory backend storage operating correctly: {self._storage}"
                )
            else:
                if self._in_memory_fallback_enabled:
                    self.logger.error(
                        f"Storage schema inaccessible - falling back to {self._in_memory_fallback}"
                    )
                else:
                    self.logger.critical(
                        f"Invalid or inaccessible storage configuration: {self._storage}"
                    )
                    raise ConfigurationError(
                        "Invalid or inaccessible storage configuration"
                    )
