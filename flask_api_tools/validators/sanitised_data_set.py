import bleach

from typing import Dict
from cerberus import DocumentError
from .validator import Validator


class SanitisedDataSet(dict):

    schema: Dict = {}

    def __init__(self, *args, **kwargs):
        """
        SanitisedDataSet inherits from dict so it behaves exactly like one.
        :param *args: args.
        :param **kwargs: kwargs.
        """
        self.store = dict()
        self.update(dict(*args, **kwargs))

    def __setitem__(self, key, value):
        """
        Override the standard __setitem__ method to sanitise all data being set.
        :param key: The key.
        :param value: The value.
        """
        super(SanitisedDataSet, self).__setitem__(key, self._sanitise_value(value))

    def update(self, mapping={}, **kwargs):
        """
        Override the standard update method to sanitise all data being set.
        :param mapping: A mapping to be set.
        :param **kwargs: kwargs.
        """
        for key, value in mapping.items():
            self.__setitem__(key, value)

        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def setdefault(self, key, value=None):
        """
        Override the setdefault update method to sanitise all data being set.
        :param key: The key of the value to be retrieved.
        :param value: A default if the value is not found.
        """
        return super(SanitisedDataSet, self).setdefault(
            key, self._sanitise_value(value)
        )

    @classmethod
    def validate(cls, request_data):
        """
        Static constructor for validating the data against the defined schema.
        :param request_data: The request from parents app.
        :return: Validated data.
        """
        validator = Validator()

        if not validator.validate(request_data, cls.schema):
            raise DocumentError(validator.errors)

        return cls(validator.document)

    def _sanitise_value(self, value):
        """
        Sanitise the passed value to prevent malicious string values.
        :param value: The value to be sanitised
        """
        if type(value) == str:
            return bleach.clean(value)
        return value
