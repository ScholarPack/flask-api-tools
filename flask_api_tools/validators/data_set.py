from .validator import Validator
from cerberus import DocumentError
from copy import copy
from typing import Dict, List, Optional


class DataSet(dict):

    schema: Dict = {}

    allow_unknown: Optional[bool] = None
    ignore_none_values: Optional[bool] = None
    purge_readonly: Optional[bool] = None
    purge_unknown: Optional[bool] = None
    require_all: Optional[bool] = None

    _validator: Validator = Validator()
    _validator_config: Dict = copy(_validator._config)

    def __init__(self, *args, **kwargs):
        """
        DataSet inherits from dict so it behaves exactly like one.
        """
        super(DataSet, self).__init__(*args, **kwargs)

    @classmethod
    def validate_object(cls, obj: Dict) -> Dict:
        """
        Validates a dictionary against the defined schema
        :param data: A dictionary.
        :return: Validated data
        """
        validator = cls._configure_validator()

        if not validator.validate(obj):
            raise DocumentError(validator.errors)

        cls._reset_validator()

        return cls(validator.document)

    @classmethod
    def validate_objects(cls, objs: List) -> List:
        """
        Validates a list of dictionaries against the defined schema
        :param data: A list of dictionaries.
        :return: Validated data
        """
        collection: List = []

        if not objs:
            return collection

        validator = cls._configure_validator()

        for o in objs:
            if validator.validate(o):
                collection.append(cls(validator.document))
            else:
                raise DocumentError(validator.errors)

        cls._reset_validator()

        return collection

    @classmethod
    def validate_one(cls, response: Dict) -> Dict:
        """
        Gets the first data object from an API request and makes sure that
        data validates against the defined schema.
        :param response: An api client response.
        :return: Validated data
        """
        data = response.get("data", [])
        if not data:
            return {}
        return cls.validate_object(data[0])

    @classmethod
    def validate_many(cls, response: Dict) -> List:
        """
        Gets data objects from an API request and makes sure that
        data validates against the defined schema.
        :param response: An api client response.
        :return: Validated data
        """
        return cls.validate_objects(response.get("data", []))

    @classmethod
    def set_validator(cls, validator: Validator) -> None:
        """
        Set a validator instance for use by the dataset. This is setting it
        globally for all datasets that extend this class.
        :param validator: The validator.
        """
        cls._validator = validator
        cls._validator_config = copy(cls._validator._config)

    @classmethod
    def _reset_validator(cls) -> None:
        """
        Reset validator's config to how the instance was first created.
        """
        cls._validator._config = copy(cls._validator_config)

    @classmethod
    def _configure_validator(cls) -> Validator:
        """
        Configure and return the validator.
        :returns: A Validator.
        """
        cls._reset_validator()
        cls._validator.schema = cls.schema

        # Only override the above config settings if a boolean is set. This is
        # to prevent the dataset from overriding the above config all the time.
        if cls.allow_unknown != None:
            cls._validator.allow_unknown = cls.allow_unknown

        if cls.ignore_none_values != None:
            cls._validator.ignore_none_values = cls.ignore_none_values

        if cls.purge_readonly != None:
            cls._validator.purge_readonly = cls.purge_readonly

        if cls.purge_unknown != None:
            cls._validator.purge_unknown = cls.purge_unknown

        if cls.require_all != None:
            cls._validator.require_all = cls.require_all

        return cls._validator
