import re
import json
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import renderers, parsers
from rest_framework.exceptions import ParseError


def snake_to_camel(name):
    """Convert snake_case to camelCase."""
    if not name:
        return name

    # Handle edge cases
    if "_" not in name:
        return name

    # Split by underscore and capitalize each word except the first
    components = name.split("_")
    return components[0] + "".join(word.capitalize() for word in components[1:])


def camel_to_snake(name):
    """Convert camelCase to snake_case."""
    if not name:
        return name

    # Insert underscore before uppercase letters (except at the start)
    # and convert to lowercase
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def convert_keys_to_camel(data):
    """
    Recursively convert all dictionary keys from snake_case to camelCase.
    Handles nested dictionaries, lists, and other data structures.
    """
    if isinstance(data, dict):
        return {
            snake_to_camel(key): convert_keys_to_camel(value)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [convert_keys_to_camel(item) for item in data]
    elif isinstance(data, tuple):
        return tuple(convert_keys_to_camel(item) for item in data)
    else:
        return data


def convert_keys_to_snake(data):
    """
    Recursively convert all dictionary keys from camelCase to snake_case.
    Handles nested dictionaries, lists, and other data structures.
    """
    if isinstance(data, dict):
        return {
            camel_to_snake(key): convert_keys_to_snake(value)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [convert_keys_to_snake(item) for item in data]
    elif isinstance(data, tuple):
        return tuple(convert_keys_to_snake(item) for item in data)
    else:
        return data


def success_response(data=None, message="Success", status=HTTP_200_OK):
    return Response(
        {"success": True, "message": message, "data": data, "errors": None},
        status=status,
    )


def error_response(
    errors=None, message="Something went wrong", status=HTTP_400_BAD_REQUEST
):
    return Response(
        {
            "success": False,
            "message": message,
            "data": None,
            "errors": errors if errors is not None else {},
        },
        status=status,
    )


class CamelCaseJSONRenderer(renderers.JSONRenderer):
    """
    Renderer that converts snake_case field names to camelCase.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, converting snake_case keys to camelCase.
        """
        if data is None:
            return b""

        # Convert snake_case keys to camelCase
        camel_case_data = convert_keys_to_camel(data)

        # Use the parent class to handle the actual JSON rendering
        return super().render(camel_case_data, accepted_media_type, renderer_context)


class CamelCaseJSONParser(parsers.JSONParser):
    """
    Parser that converts camelCase field names to snake_case.
    """

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parse the request body and convert camelCase keys to snake_case.
        """
        parser_context = parser_context or {}
        encoding = parser_context.get("encoding", "utf-8")

        try:
            data = stream.read().decode(encoding)
            parsed_data = json.loads(data) if data else {}

            # Convert camelCase keys to snake_case
            snake_case_data = convert_keys_to_snake(parsed_data)

            return snake_case_data
        except ValueError as exc:
            raise ParseError("JSON parse error - %s" % str(exc))
