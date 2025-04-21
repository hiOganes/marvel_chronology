from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.contrib.postgres.search import TrigramSimilarity
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.movies.models import Movies
from api.movies_v1.serializers import MoviesSerializer, ViewedAPIView
from api.movies_v1 import schema_examples
from api.movies_v1.paginations import ListMoviesPagination
from api.movies_v1.permissions import MoviesPermission


tags = ['Movies']


class ListMoviesAPIView(APIView):
    model = Movies
    serializer_class = MoviesSerializer
    pagination_class = ListMoviesPagination
    permission_classes = [MoviesPermission]

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
        responses=schema_examples.POST_LIST_MOVIES_STATUS_RESPONSES,
        examples=schema_examples.POST_LIST_MOVIES_EXAMPLES_RESPONSE,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            movie = self.model.objects.create(**serializer.validated_data)
            serializer = self.serializer_class(movie)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        cache.clear()
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class DetailMoviesAPIView(APIView):
    model = Movies
    serializer_class = MoviesSerializer
    permission_classes = [MoviesPermission]

    def get_object(self, *args, **kwargs):
        return get_object_or_404(self.model, pk=kwargs['pk'])

    @extend_schema(
        summary='This endpoint return movie.',
        description=schema_examples.GET_DETAIL_MOVIES_DESCRIPTION,
        tags=tags,
        responses=schema_examples.GET_DETAIL_MOVIES_STATUS_RESPONSES,
        examples=schema_examples.GET_DETAIL_MOVIES_EXAMPLES,
    )
    def get(self, request, *args, **kwargs):
        movie = self.get_object(*args, **kwargs)
        serializer = self.serializer_class(movie)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='This endpoint update movie.',
        description=schema_examples.PUT_DETAIL_MOVIES_DESCRIPTION,
        tags=tags,
        responses=schema_examples.PUT_DETAIL_MOVIES_STATUS_RESPONSES,
        examples=schema_examples.PUT_DETAIL_MOVIES_EXAMPLES,
    )
    def put(self, request, *args, **kwargs):
        movie = self.get_object(*args, **kwargs)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            for key, value in serializer.validated_data.items():
                if getattr(movie, key) != value:
                    setattr(movie, key, value)
            movie.save()
            serializer = self.serializer_class(movie)
            cache.clear()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        summary='This endpoint delete movie.',
        description=schema_examples.DELETE_DETAIL_MOVIES_DESCRIPTION,
        tags=tags,
        responses=schema_examples.DELETE_DETAIL_MOVIES_STATUS_RESPONSES,
        examples=schema_examples.DELETE_DETAIL_MOVIES_EXAMPLES,
    )
    def delete(self, request, *args, **kwargs):
        movie = self.get_object(*args, **kwargs)
        movie.delete()
        cache.clear()
        return Response(
            data={'result': 'The movie has been removed.'},
            status=status.HTTP_200_OK
        )


class ViewedAPIView(APIView):
    model = Movies
    serializer_class = ViewedAPIView
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='This endpoint changes the movie viewing status',
        tags=tags,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            movie = self.model.objects.get(pk=serializer.validated_data['id'])
            try:
                request.user.viewed.get(id=movie.id)
                request.user.viewed.remove(movie)
                return Response(data='Movie removed')
            except self.model.DoesNotExist:
                movie.user_set.add(request.user)
            return Response(data='Movie status is changed')
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )