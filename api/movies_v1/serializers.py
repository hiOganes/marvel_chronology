from rest_framework import serializers

from apps.movies.models import Movies

from apps.directors.models import Directors


class MoviesSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    title_ru = serializers.CharField()
    title_en = serializers.CharField()
    release_date = serializers.DateField()
    timing = serializers.IntegerField()
    director = serializers.PrimaryKeyRelatedField(
        queryset=Directors.objects.all()
    )
    trailer = serializers.URLField()
    description = serializers.CharField()
    poster = serializers.ImageField()
    content = serializers.ChoiceField(choices=Movies.MediaContent.choices)