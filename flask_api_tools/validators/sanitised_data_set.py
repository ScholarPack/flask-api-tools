import bleach

from .data_set import DataSet
from .validator import Validator
from cerberus import DocumentError
from copy import copy
from typing import Dict


class SanitisedDataSet(DataSet):

    _validator: Validator = Validator()
    _validator_config: Dict = copy(_validator._config)

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
        Validate and clean the data against the defined schema.
        :param request_data: The user request data.
        :return: Validated data.
        """
        return cls.validate_object(request_data)

    def _sanitise_value(self, value):
        """
        Sanitise the passed value to prevent malicious string values.
        :param value: The value to be sanitised
        """
        if type(value) == str:
            return bleach.clean(value)
        return value
