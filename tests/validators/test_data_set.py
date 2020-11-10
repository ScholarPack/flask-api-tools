from cerberus import DocumentError
from datetime import date, datetime
from flask_api_tools.validators import DataSet, Validator
import pytest


class TestDataSet:
    def test_validate_object(self):
        class Example(DataSet):
            schema = {
                "string_1": {"type": "string", "check_with": "uuid"},
                "string_2": {"type": "string", "coerce": "to_string"},
                "string_3": {
                    "type": "string",
                    "nullable": True,
                    "coerce": "to_nullable_string",
                },
                "integer_1": {"type": "integer", "coerce": "to_integer"},
                "integer_2": {
                    "type": "integer",
                    "nullable": True,
                    "coerce": "to_nullable_integer",
                },
                "boolean_1": {"coerce": "to_bool"},
                "float_1": {"type": "float", "coerce": "to_float"},
                "float_2": {
                    "type": "float",
                    "nullable": True,
                    "coerce": "to_nullable_float",
                },
            }

        data = {
            "string_1": "7c674878-e544-431c-8c11-f11565299cac",
            "string_2": None,
            "string_3": None,
            "integer_1": None,
            "integer_2": None,
            "boolean_1": 1,
            "float_1": None,
            "float_2": None,
        }
        result = {
            "string_1": "7c674878-e544-431c-8c11-f11565299cac",
            "string_2": "",
            "string_3": None,
            "integer_1": 0,
            "integer_2": None,
            "boolean_1": True,
            "float_1": 0.0,
            "float_2": None,
        }

        validated = Example.validate_object(data)
        assert validated == result

    def test_validate_objects(self):
        class Example(DataSet):
            schema = {
                "string_1": {"type": "string", "check_with": "uuid"},
                "string_2": {"type": "string", "coerce": "to_string"},
                "string_3": {
                    "type": "string",
                    "nullable": True,
                    "coerce": "to_nullable_string",
                },
                "integer_1": {"type": "integer", "coerce": "to_integer"},
                "integer_2": {
                    "type": "integer",
                    "nullable": True,
                    "coerce": "to_nullable_integer",
                },
                "boolean_1": {"coerce": "to_bool"},
                "float_1": {"type": "float", "coerce": "to_float"},
                "float_2": {
                    "type": "float",
                    "nullable": True,
                    "coerce": "to_nullable_float",
                },
            }

        data = {
            "string_1": "7c674878-e544-431c-8c11-f11565299cac",
            "string_2": None,
            "string_3": None,
            "integer_1": None,
            "integer_2": None,
            "boolean_1": 1,
            "float_1": None,
            "float_2": None,
        }
        result = {
            "string_1": "7c674878-e544-431c-8c11-f11565299cac",
            "string_2": "",
            "string_3": None,
            "integer_1": 0,
            "integer_2": None,
            "boolean_1": True,
            "float_1": 0.0,
            "float_2": None,
        }

        validated = Example.validate_objects([data])
        assert validated == [result]

    def test_validate_one(self):
        class Example(DataSet):
            schema = {
                "string_1": {"type": "string", "check_with": "uuid"},
            }

        data = {
            "data": [
                {"string_1": "7c674878-e544-431c-8c11-f11565299cac"},
                {"string_1": "7c674878-e544-431c-8c11-f11565299cac"},
            ]
        }
        result = {
            "string_1": "7c674878-e544-431c-8c11-f11565299cac",
        }

        validated = Example.validate_one(data)
        assert validated == result

    def test_validate_one_no_data(self):
        class Example(DataSet):
            schema = {
                "string_1": {"type": "string", "check_with": "uuid"},
            }

        data = {}
        result = {}

        validated = Example.validate_one(data)
        assert validated == result

    def test_validate_many(self):
        class Example(DataSet):
            schema = {
                "string_1": {"type": "string", "check_with": "uuid"},
            }

        data = {
            "data": [
                {"string_1": "7c674878-e544-431c-8c11-f11565299cac"},
                {"string_1": "7c674878-e544-431c-8c11-f11565299cac"},
            ]
        }
        result = [
            {"string_1": "7c674878-e544-431c-8c11-f11565299cac"},
            {"string_1": "7c674878-e544-431c-8c11-f11565299cac"},
        ]

        validated = Example.validate_many(data)
        assert validated == result

    def test_validate_many_no_data(self):
        class Example(DataSet):
            schema = {
                "string_1": {"type": "string", "check_with": "uuid"},
            }

        data = {}
        result = []

        validated = Example.validate_many(data)
        assert validated == result

    def test_a_simple_validation_failure(self):
        class Example(DataSet):
            schema = {
                "string_1": {"type": "string"},
            }

        data = {
            "string_1": 1337,
        }

        with pytest.raises(DocumentError):
            validated = Example.validate_object(data)

        with pytest.raises(DocumentError):
            validated = Example.validate_objects([data])

        with pytest.raises(DocumentError):
            validated = Example.validate_one({"data": [data]})

        with pytest.raises(DocumentError):
            validated = Example.validate_many({"data": [data, data]})

    def test_validate_object_unknown_key(self):
        class Example(DataSet):
            schema = {
                "string_1": {"type": "string", "check_with": "uuid"},
            }

        data = {
            "string_2": "7c674878-e544-431c-8c11-f11565299cac",
        }
        result = {
            "string_2": "7c674878-e544-431c-8c11-f11565299cac",
        }

        with pytest.raises(DocumentError):
            validated = Example.validate_object(data)

        Example.allow_unknown = True
        validated = Example.validate_object(data)
        assert validated == result

    def test_validate_objects_unknown_key(self):
        class Example(DataSet):
            schema = {
                "string_1": {"type": "string", "check_with": "uuid"},
            }

        data = {
            "string_2": "7c674878-e544-431c-8c11-f11565299cac",
        }
        result = {
            "string_2": "7c674878-e544-431c-8c11-f11565299cac",
        }

        with pytest.raises(DocumentError):
            validated = Example.validate_objects([data])

        Example.allow_unknown = True
        validated = Example.validate_objects([data])
        assert validated == [result]

    def test_local_config_updates_validator(self):
        class Example1(DataSet):
            allow_unknown = True
            ignore_none_values = True
            purge_readonly = True
            purge_unknown = True
            require_all = False
            schema = {
                "string_1": {"type": "string", "check_with": "uuid"},
            }

        class Example2(DataSet):
            schema = {
                "string_1": {"type": "string", "check_with": "uuid"},
            }

        assert not Example1._validator.allow_unknown
        assert not Example1._validator.ignore_none_values
        assert not Example1._validator.purge_readonly
        assert not Example1._validator.purge_unknown
        assert not Example1._validator.require_all

        assert not Example2._validator.allow_unknown
        assert not Example2._validator.ignore_none_values
        assert not Example2._validator.purge_readonly
        assert not Example2._validator.purge_unknown
        assert not Example2._validator.require_all

        data = {
            "string_2": "7c674878-e544-431c-8c11-f11565299cac",
        }
        result = {
            "string_2": "7c674878-e544-431c-8c11-f11565299cac",
        }

        validated = Example1.validate_object(data)

        assert not Example1._validator.allow_unknown
        assert not Example1._validator.ignore_none_values
        assert not Example1._validator.purge_readonly
        assert not Example1._validator.purge_unknown
        assert not Example1._validator.require_all

        with pytest.raises(DocumentError):
            validated = Example2.validate_object(data)

        assert not Example2._validator.allow_unknown
        assert not Example2._validator.ignore_none_values
        assert not Example2._validator.purge_readonly
        assert not Example2._validator.purge_unknown
        assert not Example2._validator.require_all

    def test_local_config_only_affects_local_dataset(self):
        class Example1(DataSet):
            schema = {
                "string_1": {"type": "string", "check_with": "uuid"},
            }

        class Example2(DataSet):
            schema = {
                "string_1": {"type": "string", "check_with": "uuid"},
            }

        data = {
            "string_2": "7c674878-e544-431c-8c11-f11565299cac",
        }
        result = {
            "string_2": "7c674878-e544-431c-8c11-f11565299cac",
        }

        with pytest.raises(DocumentError):
            validated = Example1.validate_object(data)

        with pytest.raises(DocumentError):
            validated = Example2.validate_object(data)

        Example1.allow_unknown = True
        validated = Example1.validate_object(data)
        assert validated == result

        with pytest.raises(DocumentError):
            validated = Example2.validate_object(data)

    def test_replacing_validator(self):
        DataSet.set_validator(Validator(allow_unknown=True))

        class Example(DataSet):
            schema = {
                "string_1": {"type": "string", "check_with": "uuid"},
            }

        assert Example._validator.allow_unknown
        assert not Example._validator.ignore_none_values
        assert not Example._validator.purge_readonly
        assert not Example._validator.purge_unknown
        assert not Example._validator.require_all

        data = {
            "string_2": "7c674878-e544-431c-8c11-f11565299cac",
        }
        result = {
            "string_2": "7c674878-e544-431c-8c11-f11565299cac",
        }

        validated = Example.validate_object(data)
        assert validated == result
