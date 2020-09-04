from flask_api_tools.validators import DataSet, SanitisedDataSet

_shared_schema = {
    "key_string": {"type": "string", "coerce": "to_string"},
    "key_none_string": {
        "type": "string",
        "nullable": True,
        "coerce": "to_string",
    },
    "key_nullable_string": {
        "type": "string",
        "nullable": True,
        "coerce": "to_nullable_string",
    },
    "key_uuid_string": {"type": "string", "check_with": "uuid"},
    "key_integer": {"type": "integer", "coerce": "to_integer"},
    "key_none_integer": {
        "type": "integer",
        "nullable": True,
        "coerce": "to_integer",
    },
    "key_nullable_integer": {
        "type": "integer",
        "nullable": True,
        "coerce": "to_nullable_integer",
    },
    "key_bool": {"type": "boolean", "coerce": "to_bool"},
    "key_none_bool": {"type": "boolean", "nullable": True, "coerce": "to_bool"},
    "key_float": {"type": "float", "coerce": "to_float"},
    "key_none_float": {"type": "float", "coerce": "to_float"},
    "key_nullable_float": {
        "type": "float",
        "nullable": True,
        "coerce": "to_nullable_float",
    },
}


class ExampleDataSet(DataSet):
    schema = _shared_schema


class ExampleSanitisedDataSet(SanitisedDataSet):
    schema = _shared_schema
