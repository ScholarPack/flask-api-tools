from cerberus import DocumentError
from datetime import date, datetime
from flask_api_tools.validators import Validator
import pytest


class TestValidator:
    def test_uuids(self):
        schema = {
            "string_1": {"type": "string", "check_with": "uuid"},
        }
        data = {
            "string_1": "7c674878-e544-431c-8c11-f11565299cac",
        }
        result = {
            "string_1": "7c674878-e544-431c-8c11-f11565299cac",
        }

        validator = Validator(schema=schema)
        assert validator.validate(data), validator.errors
        assert validator.document == result

    def test_to_string(self):
        schema = {
            "string_1": {"type": "string", "coerce": "to_string"},
            "string_2": {"type": "string", "coerce": "to_string"},
            "string_3": {"type": "string", "coerce": "to_string"},
        }
        data = {
            "string_1": "This is a normal string",
            "string_2": "None",
            "string_3": None,
        }
        result = {
            "string_1": "This is a normal string",
            "string_2": "",
            "string_3": "",
        }

        validator = Validator(schema=schema)
        assert validator.validate(data), validator.errors
        assert validator.document == result

    def test_to_nullable_string(self):
        schema = {
            "string_1": {
                "type": "string",
                "nullable": True,
                "coerce": "to_nullable_string",
            },
            "string_2": {
                "type": "string",
                "nullable": True,
                "coerce": "to_nullable_string",
            },
            "string_3": {
                "type": "string",
                "nullable": True,
                "coerce": "to_nullable_string",
            },
            "string_4": {
                "type": "string",
                "nullable": True,
                "coerce": "to_nullable_string",
            },
        }
        data = {
            "string_1": "This is a normal string",
            "string_2": "None",
            "string_3": None,
            "string_4": "",
        }
        result = {
            "string_1": "This is a normal string",
            "string_2": None,
            "string_3": None,
            "string_4": None,
        }

        validator = Validator(schema=schema)
        assert validator.validate(data), validator.errors
        assert validator.document == result

    def test_to_integer(self):
        schema = {
            "integer_1": {"type": "integer", "coerce": "to_integer"},
            "integer_2": {"type": "integer", "coerce": "to_integer"},
            "integer_3": {"type": "integer", "coerce": "to_integer"},
        }
        data = {
            "integer_1": 12345,
            "integer_2": "None",
            "integer_3": None,
        }
        result = {
            "integer_1": 12345,
            "integer_2": 0,
            "integer_3": 0,
        }

        validator = Validator(schema=schema)
        assert validator.validate(data), validator.errors
        assert validator.document == result

    def test_to_nullable_integer(self):
        schema = {
            "integer_1": {
                "type": "integer",
                "nullable": True,
                "coerce": "to_nullable_integer",
            },
            "integer_2": {
                "type": "integer",
                "nullable": True,
                "coerce": "to_nullable_integer",
            },
            "integer_3": {
                "type": "integer",
                "nullable": True,
                "coerce": "to_nullable_integer",
            },
            "integer_4": {
                "type": "integer",
                "nullable": True,
                "coerce": "to_nullable_integer",
            },
        }
        data = {
            "integer_1": 12345,
            "integer_2": "None",
            "integer_3": None,
            "integer_4": "",
        }
        result = {
            "integer_1": 12345,
            "integer_2": None,
            "integer_3": None,
            "integer_4": None,
        }

        validator = Validator(schema=schema)
        assert validator.validate(data), validator.errors
        assert validator.document == result

    def test_to_boolean(self):
        schema = {
            "boolean_1": {"type": "boolean", "coerce": "to_bool"},
            "boolean_2": {"type": "boolean", "coerce": "to_bool"},
            "boolean_3": {"type": "boolean", "coerce": "to_bool"},
            "boolean_4": {"type": "boolean", "coerce": "to_bool"},
            "boolean_5": {"type": "boolean", "coerce": "to_bool"},
            "boolean_6": {"type": "boolean", "coerce": "to_bool"},
            "boolean_7": {"type": "boolean", "coerce": "to_bool"},
        }
        data = {
            "boolean_1": True,
            "boolean_2": "True",
            "boolean_3": "",
            "boolean_4": "False",
            "boolean_5": False,
            "boolean_6": "None",
            "boolean_7": None,
        }
        result = {
            "boolean_1": True,
            "boolean_2": True,
            "boolean_3": False,
            "boolean_4": False,
            "boolean_5": False,
            "boolean_6": False,
            "boolean_7": False,
        }

        validator = Validator(schema=schema)
        assert validator.validate(data), validator.errors
        assert validator.document == result

    def test_to_float(self):
        schema = {
            "float_1": {"type": "float", "coerce": "to_float"},
            "float_2": {"type": "float", "coerce": "to_float"},
            "float_3": {"type": "float", "coerce": "to_float"},
            "float_4": {"type": "float", "coerce": "to_float"},
        }
        data = {
            "float_1": 0.0005,
            "float_2": "",
            "float_3": "None",
            "float_4": None,
        }
        result = {
            "float_1": 0.0005,
            "float_2": 0.0,
            "float_3": 0.0,
            "float_4": 0.0,
        }

        validator = Validator(schema=schema)
        assert validator.validate(data), validator.errors
        assert validator.document == result

    def test_to_nullable_float(self):
        schema = {
            "float_1": {
                "type": "float",
                "nullable": True,
                "coerce": "to_nullable_float",
            },
            "float_2": {
                "type": "float",
                "nullable": True,
                "coerce": "to_nullable_float",
            },
            "float_3": {
                "type": "float",
                "nullable": True,
                "coerce": "to_nullable_float",
            },
            "float_4": {
                "type": "float",
                "nullable": True,
                "coerce": "to_nullable_float",
            },
        }
        data = {
            "float_1": 0.0005,
            "float_2": "",
            "float_4": "None",
            "float_3": None,
        }
        result = {
            "float_1": 0.0005,
            "float_2": None,
            "float_3": None,
            "float_4": None,
        }

        validator = Validator(schema=schema)
        assert validator.validate(data), validator.errors
        assert validator.document == result

    def test_to_date(self):
        schema = {
            "string_1": {"type": "date", "nullable": True, "coerce": "to_date"},
            "string_2": {"type": "date", "coerce": "to_date"},
        }
        data = {
            "string_1": "This is a normal string",
            "string_2": "1900-01-31",
        }
        result = {
            "string_1": None,
            "string_2": date.fromisoformat("1900-01-31"),
        }

        validator = Validator(schema=schema)
        assert validator.validate(data), validator.errors
        assert validator.document == result

    def test_to_datetime(self):
        schema = {
            "string_1": {"type": "datetime", "nullable": True, "coerce": "to_datetime"},
            "string_2": {"type": "datetime", "coerce": "to_datetime"},
        }
        data = {
            "string_1": "This is a normal string",
            "string_2": "1900-01-31T09:30:00.532649",
        }
        result = {
            "string_1": None,
            "string_2": datetime.fromisoformat("1900-01-31T09:30:00.532649"),
        }

        validator = Validator(schema=schema)
        assert validator.validate(data), validator.errors
        assert validator.document == result
