import pytest
from cerberus import DocumentError
from flask_api_tools.validators import DataSet, SanitisedDataSet, Validator


class ExampleSanitisedDataSet(SanitisedDataSet):

    schema = {
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
    }


class TestSanitisedDataSet:

    input = {
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

    output = {
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

    def test_full_valid_data_set(self):
        validated = ExampleSanitisedDataSet.validate(self.input)
        assert validated == self.output

        validated = ExampleSanitisedDataSet.validate_object(self.input)
        assert validated == self.output

        validated = ExampleSanitisedDataSet.validate_objects([self.input])
        assert validated == [self.output]

        validated = ExampleSanitisedDataSet.validate_one({"data": [self.input]})
        assert validated == self.output

        validated = ExampleSanitisedDataSet.validate_many(
            {"data": [self.input, self.input]}
        )
        assert validated == [self.output, self.output]

    def test_a_simple_validation_failure(self):
        class Example(SanitisedDataSet):
            schema = {
                "string_1": {"type": "string"},
            }

        data = {
            "string_1": 1337,
        }

        with pytest.raises(DocumentError):
            validated = Example.validate(data)

        with pytest.raises(DocumentError):
            validated = Example.validate_object(data)

        with pytest.raises(DocumentError):
            validated = Example.validate_objects([data])

        with pytest.raises(DocumentError):
            validated = Example.validate_one({"data": [data]})

        with pytest.raises(DocumentError):
            validated = Example.validate_many({"data": [data, data]})

    def test_update_constructor(self):
        data = SanitisedDataSet({"name": "<script><!-- comment -->script</script>"})

        assert data.get("name") == "&lt;script&gt;script&lt;/script&gt;"

    def test_set_item(self):
        data = SanitisedDataSet()
        data["name"] = "<script><!-- comment -->script</script>"
        data["age"] = 25

        assert data["name"] == "&lt;script&gt;script&lt;/script&gt;"
        assert data["age"] == 25

    def test_update_method(self):
        data = SanitisedDataSet()
        data.update({"name": "<script><!-- comment -->script</script>"})
        data.update(age=25)
        data.update()

        assert data["name"] == "&lt;script&gt;script&lt;/script&gt;"
        assert data["age"] == 25

    def test_setdefault_method(self):
        data = SanitisedDataSet()
        data.setdefault("name", "<script><!-- comment -->script</script>")

        assert data["name"] == "&lt;script&gt;script&lt;/script&gt;"

    def test_a_validator_can_be_set_without_affecting_a_child_class(self):
        DataSet.set_validator(Validator(require_all=True))

        class Example1(DataSet):
            schema = {
                "string_1": {"type": "string", "coerce": "to_string"},
                "string_2": {"type": "string", "coerce": "to_string"},
            }

        class Example2(SanitisedDataSet):
            schema = {
                "string_1": {"type": "string", "coerce": "to_string"},
                "string_2": {"type": "string", "coerce": "to_string"},
            }

        data = {
            "string_1": "Lorem ipsum",
        }
        result = {
            "string_1": "Lorem ipsum",
        }

        with pytest.raises(DocumentError):
            validated = Example1.validate_object(data)

        validated = Example2.validate(data)
        assert validated == result

    def test_a_validator_can_be_set_without_affecting_the_base_class(self):
        DataSet.set_validator(
            Validator()
        )  # Revert the validator set in the test above.
        SanitisedDataSet.set_validator(Validator(require_all=True))

        class Example1(DataSet):
            schema = {
                "string_1": {"type": "string", "coerce": "to_string"},
                "string_2": {"type": "string", "coerce": "to_string"},
            }

        class Example2(SanitisedDataSet):
            schema = {
                "string_1": {"type": "string", "coerce": "to_string"},
                "string_2": {"type": "string", "coerce": "to_string"},
            }

        data = {
            "string_1": "Lorem ipsum",
        }
        result = {
            "string_1": "Lorem ipsum",
        }

        with pytest.raises(DocumentError):
            validated = Example2.validate(data)

        validated = Example1.validate_object(data)
        assert validated == result
