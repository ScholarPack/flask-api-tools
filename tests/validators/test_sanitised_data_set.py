import pytest
from cerberus import DocumentError

from .example_data_sets import ExampleSanitisedDataSet


class TestSanitisedDataSet:
    def test_full_valid_data_set(self):
        example_raw_data = {
            "key_string": "<script>",
            "key_none_string": None,
            "key_nullable_string": "",
            "key_uuid_string": "7c674878-e544-431c-8c11-f11565299cac",
            "key_integer": 5,
            "key_none_integer": None,
            "key_nullable_integer": "",
            "key_bool": "True",
            "key_none_bool": None,
        }
        expected_data = {
            "key_string": "&lt;script&gt;",
            "key_none_string": "",
            "key_nullable_string": None,
            "key_uuid_string": "7c674878-e544-431c-8c11-f11565299cac",
            "key_integer": 5,
            "key_none_integer": 0,
            "key_nullable_integer": None,
            "key_bool": True,
            "key_none_bool": False,
        }
        validated_data_set = ExampleSanitisedDataSet.validate(example_raw_data)
        assert validated_data_set == expected_data

    def test_partial_valid_data_set(self):
        example_raw_data = {
            "key_string": "abc",
        }
        expected_data = {
            "key_string": "abc",
        }
        validated_data_set = ExampleSanitisedDataSet.validate(example_raw_data)
        assert validated_data_set == expected_data

    def test_unknown_key(self):
        example_raw_data = {
            "unknown_key": "",
        }
        with pytest.raises(DocumentError):
            ExampleSanitisedDataSet.validate(example_raw_data)
