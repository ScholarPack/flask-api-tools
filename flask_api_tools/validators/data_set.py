from typing import Dict, List
from cerberus import DocumentError
from .validator import Validator


class DataSet(dict):

    _allow_unknown: bool = False
    _ignore_none_values: bool = False
    _purge_readonly: bool = False
    _purge_unknown: bool = False
    _require_all: bool = False
    schema: Dict = {}

    def __init__(self, *args, **kwargs):
        """
        DataSet inherits from dict so it behaves exactly like one.
        """
        super(DataSet, self).__init__(*args, **kwargs)

    @classmethod
    def validate_object(cls, data: Dict) -> Dict:
        """
        Validates a dictionary against the defined schema
        :param data: A dictionary.
        :return: Validated data
        """
        return cls.validate_one({"data": [data]})

    @classmethod
    def validate_objects(cls, data: List) -> List:
        """
        Validates a list of dictionaries against the defined schema
        :param data: A list of dictionaries.
        :return: Validated data
        """
        return cls.validate_many({"data": data})

    @classmethod
    def validate_one(cls, response: Dict) -> Dict:
        """
        Static constructor that checks that we got data from an API and that
        data validates against the defined schema.
        :param response: An api client response.
        :return: Validated data
        """
        data = response.get("data", [])

        if not data:
            return {}

        validator = Validator(
            schema=cls.schema,
            allow_unknown=cls._allow_unknown,
            ignore_none_values=cls._ignore_none_values,
            purge_readonly=cls._purge_readonly,
            purge_unknown=cls._purge_unknown,
            require_all=cls._require_all,
        )

        if not validator.validate(data[0]):
            raise DocumentError(validator.errors)

        return cls(validator.document)

    @classmethod
    def validate_many(cls, response: Dict) -> List:
        """
        Static constructor that checks that we got data from an API and that
        data validates against the defined schema.
        :param response: An api client response.
        :return: Validated data
        """

        data = response.get("data", [])
        collection: List = []

        if not data:
            return collection

        validator = Validator(
            schema=cls.schema,
            allow_unknown=cls._allow_unknown,
            ignore_none_values=cls._ignore_none_values,
            purge_readonly=cls._purge_readonly,
            purge_unknown=cls._purge_unknown,
            require_all=cls._require_all,
        )

        for d in data:
            if validator.validate(d):
                collection.append(cls(validator.document))
            else:
                raise DocumentError(validator.errors)

        return collection
