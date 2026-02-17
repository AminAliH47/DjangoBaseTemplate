import json
from rest_framework import serializers
from django.utils.translation import gettext as _
from djangorestframework_camel_case.util import underscoreize
import ast

from common.utils import get_hex_id


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(
    *,
    fields: dict,
    data: dict | None = None,
    **kwargs,
) -> serializers.Serializer:
    serializer_class = create_serializer_class(
        name=str(get_hex_id()),
        fields=fields,
    )

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)


class JSONStringField(serializers.Field):
    def __init__(self, nested_serializer: serializers.Serializer, *args, **kwargs):
        self.nested_serializer = nested_serializer
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        try:
            json_data = underscoreize(ast.literal_eval(data))
        except ValueError as e:
            try:
                json_data = json.loads(data)
            except ValueError:
                raise serializers.ValidationError(f"Invalid JSON format: {str(e)}")

        many = True if isinstance(json_data, list) else False

        serializer = self.nested_serializer(data=json_data, many=many)
        serializer.is_valid(raise_exception=True)

        return serializer.validated_data

    def to_representation(self, value):
        if isinstance(value, dict) or isinstance(value, list):
            return json.dumps(value)

        serializer = self.nested_serializer(value, many=True)
        return serializer.data


class LimitOffsetPaginationParamsSerializer(serializers.Serializer):
    limit = serializers.IntegerField(
        min_value=1,
        required=False,
        help_text=_('Limit the number of items to return.'),
    )
    offset = serializers.IntegerField(
        min_value=0,
        required=False,
        help_text=_('Offset the number of items to return.'),
    )
