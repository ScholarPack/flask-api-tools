# Flask API Tools - Validators
A set of validation utilities for handling API response data and user input data.

# Installation/Setup
See [README.md](https://github.com/ScholarPack/flask-api-tools/blob/master/README.md#installation)

## Data Set Validation
### Validator basics
The schema can define the following types of fields by default:
* string - ```{ "type": "string", "coerce": "to_string" }```
* integer - ```{ "type": "integer", "coerce": "to_integer" }```
* bool - ```{ "type": "boolean", "coerce": "to_bool" }```
* uuid - ```{ "type": "string", "check_with": "uuid" }```

An example schema would be:

```python
schema = {
    "string": { "type": "string", "coerce": "to_string" },
    "integer": { "type": "integer", "coerce": "to_integer" },
    "bool": { "type": "boolean", "coerce": "to_bool" },
    "uuid": { "type": "string", "check_with": "uuid" },
}
```

### DataSet
The ```DataSet``` class is a friendly wrapper for the ```Validator``` class.
This class is intended to be used for ensuring data that comes from another API matches a given format.

Basic usage:
```python
from flask_api_tools.validators import DataSet

class ValidDataSet(DataSet):
    schema = {
        "message": { "type": "string", "coerce": "to_string" }
    }

validated_response = ValidDataSet.validate_object(api_response)
```

If the schema provided includes a field not present in the object validated, it will raise a ```DocumentError``` (from ```cerberus```). If a field is not present in the schema, it is not validated.

It is also possible to validate a list of objects:

```python
from flask_api_tools.validators import DataSet

class ValidDataSet(DataSet):
    schema = {
        "message": { "type": "string", "coerce": "to_string" }
    }


validated_response = ValidDataSet.validate_objects(api_response)
```

If the API response is in the format:

```json
{
    "data": [
        {
            "message": "Hello world"
        }
    ]
}
```

```.validate_one``` and ```.validate_many``` should be used instead.

### SanitisedDataSet
The ```SanitisedDataSet``` class is a friendly wrapper for a dictionary.
It is intented to be used for sanitising user inputted strings.

Basic usage:

```python
from flask_api_tools.validators import SanitisedDataSet

class ValidDataSet(SanitisedDataSet):
    schema = {
        "message": { "type": "string", "coerce": "to_string" }
    }

validated_response = ValidDataSet.validate(user_input)
```

If the schema provided includes a field not present in the object validated, it will raise a ```DocumentError``` (from ```cerberus```). If a field is not present in the schema, it is not validated.

```bleach``` is used to sanitised the inputs.
