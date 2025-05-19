from rest_framework import serializers

from apps.directors.models import Directors


class DirectorsSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()