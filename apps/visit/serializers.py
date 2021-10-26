from typing import List

from django.core.validators import URLValidator
from rest_framework import serializers


class VisitCreateSerialiser(serializers.Serializer):  # NOQA

    links = serializers.ListSerializer(allow_empty=False, child=serializers.CharField(),
                                       write_only=True)

    @staticmethod
    def validate_links(values: List[str]):
        """
        Function that validates every resource in links array.

        Args:
            values (<List>) - array that contains resource urls
        """

        for value in values: URLValidator()(value)  # NOQA
        return values


class VisitListSerializer(serializers.Serializer):  # NOQA

    start = serializers.IntegerField(write_only=True)
    end = serializers.IntegerField(write_only=True)
