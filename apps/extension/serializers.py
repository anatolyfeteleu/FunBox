from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class EmptySerializer(serializers.Serializer):  # NOQA
    """Empty serializer"""


class StatusSerializer(serializers.Serializer):  # NOQA
    """Swagger API serializer class"""

    STATUS_CHOICES = (
        ('ok', _('ok')),
        ('not ok', _('not ok'))
    )

    status = serializers.ChoiceField(choices=STATUS_CHOICES)


class DomainSerializer(StatusSerializer):  # NOQA
    """Swagger API serializer class"""

    STATUS_CHOICES = (
        ('ok', _('ok')),
    )

    domains = serializers.ListSerializer(child=serializers.CharField())
