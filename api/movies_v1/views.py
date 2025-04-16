from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from api.movies_v1.paginations import ListMoviesPagination
from rest_framework import filters
from django.contrib.postgres.search import TrigramSimilarity
from django.core.cache import cache


from apps.movies.models import Movies
from api.movies_v1.serializers import MoviesSerializer
from api.movies_v1 import schema_examples


tags = ['Movies']

class ListMoviesAPIView(APIView):
    model = Movies
    serializer_class = MoviesSerializer
    pagination_class = ListMoviesPagination

    def get_objects(self, search=None):
        if search:
            queryset = self.model.objects.annotate(
                similarity=(TrigramSimilarity('title_ru', search) +
                            TrigramSimilarity('title_en', search))
            ).filter(
                similarity__gte=0.1
            ).order_by('-similarity').select_related('director')
            return queryset
        else:
            return self.model.objects.all().select_related('director')

    @extend_schema(
        summary='This endpoint returns a list of movies.',
        description=schema_examples.GET_LIST_MOVIES_DESCRIPTION,
        tags=tags,
        parameters=schema_examples.GET_LIST_MOVIES_SEARCH_PARAMETERS,
        responses=schema_examples.GET_LIST_MOVIES_STATUS_RESPONSES,
        examples=schema_examples.GET_LIST_MOVIES_EXAMPLES,
    )
    def get(self, request):
        full_path = request.get_full_path()
        movies = self.get_objects(request.query_params.get('search'))
        cached_queryset = cache.get(full_path, None)
        if cached_queryset is None:
            cache.set(full_path, movies, timeout=5)
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(movies, request)
        else:
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(
                cached_queryset,
                request
            )
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary='This endpoint create a new movie.',
        description=schema_examples.POST_LIST_MOVIES_DESCRIPTION,
        tags=tags,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.data)
        if serializer.is_valid():
            movie = self.model.objects.create(**serializer.validated_data)
            serializer = serializer_class(movie)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
