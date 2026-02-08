import json
from jsonschema import validate
import allure
from reqres_tests.utils.path import schema_path


@allure.step('Валидация JSON schema')
def validate_schema(response, schema_file_name):
    schema = json.load(open(schema_path(schema_file_name)))
    validate(response, schema)
