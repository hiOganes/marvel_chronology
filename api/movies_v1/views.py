from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from api.movies_v1.paginations import ListMoviesPagination
from rest_framework import filters
from django.contrib.postgres.search import TrigramSimilarity


from apps.movies.models import Movies
from api.movies_v1.serializers import MoviesSerializer
from api.movies_v1 import schema_examples


tags = ['Movies']

class ListMoviesAPIView(APIView):
    model = Movies
    serializer_class = MoviesSerializer
    pagination_class = ListMoviesPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title_ru', 'title_en']

    def get_objects(self, search=None):
        if search:
            form = self.form_class(self.request.GET)
            if form.is_valid():
                search = form.cleaned_data.get('search')
                queryset = self.model.objects.annotate(
                    similarity=TrigramSimilarity('title_ru', search) +
                               TrigramSimilarity('title_en', search)
                ).filter(
                    similarity__gte=0.1).order_by(
                    '-similarity'
                ).select_related('director')
            return queryset
        else:
            return self.model.objects.all(
            ).select_related('director')

    @extend_schema(
        summary='This endpoint returns a list of movies.',
        tags=tags,
        parameters=schema_examples.SEARCH_PARAMETERS
    )
    def get(self, request):
        movies = self.model.objects.all()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(movies, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

