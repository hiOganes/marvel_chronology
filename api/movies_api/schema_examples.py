from rest_framework import status
from drf_spectacular.utils import (
    OpenApiParameter, OpenApiExample, OpenApiRequest
)

from api.movies_api.serializers import MoviesSerializer


value = {
    "position": 1,
    "title_ru": "Первый мститель",
     "title_en": "Captain America: The First Avenger",
     "release_date": "2011-07-28T00:00:00Z",
     "timing": 124,
     "director": "Джо Джонстон",
     "trailer": "https://www.youtube.com/watch?v=FxTlOl03x9c",
     "description": 'Стив Роджерс добровольно соглашается принять участие в '
         'эксперименте, который превратит его в суперсолдата, '
         'известного как Первый мститель. '
         'Роджерс вступает в вооруженные силы США вместе с '
         'Баки Барнсом и Пегги Картер, чтобы бороться с враждебной '
         'организацией ГИДРА, которой управляет '
         'безжалостный Красный Череп.',
     "poster": "/media/posters/2025/04/09/3840x.webp",
     "content": "MOVIE"
}


# description
GET_LIST_MOVIES_DESCRIPTION = '''
    This endpoint is needed to get a list of movies. 
    The list is divided into pages, 10 movies on one page. 
    There is also a search by movie title, in Russian and English.
    '''

POST_LIST_MOVIES_DESCRIPTION = '''
    Create new movie.
    '''

GET_DETAIL_MOVIES_DESCRIPTION = '''
    By the movie ID you can get detailed information about it
    '''

PUT_DETAIL_MOVIES_DESCRIPTION = '''
    By the movie ID you can update detailed information about it
    '''

DELETE_DETAIL_MOVIES_DESCRIPTION = '''
    By the movie ID you can delete movie
    '''

# parameters
GET_LIST_MOVIES_SEARCH_PARAMETERS = [
    OpenApiParameter(
        'search',
        str,
        description='Search by Russian or English movie title',
        required=False
    )
]


# request


# responses
GET_LIST_MOVIES_STATUS_RESPONSES = {
    status.HTTP_200_OK: MoviesSerializer,
}

POST_LIST_MOVIES_STATUS_RESPONSES = {
    status.HTTP_201_CREATED: MoviesSerializer,
    status.HTTP_400_BAD_REQUEST: MoviesSerializer,
}

GET_DETAIL_MOVIES_STATUS_RESPONSES = {
    status.HTTP_200_OK: MoviesSerializer,
    status.HTTP_404_NOT_FOUND: MoviesSerializer,
}

PUT_DETAIL_MOVIES_STATUS_RESPONSES = {
    status.HTTP_200_OK: MoviesSerializer,
    status.HTTP_400_BAD_REQUEST: MoviesSerializer,
    status.HTTP_404_NOT_FOUND: MoviesSerializer,
}

DELETE_DETAIL_MOVIES_STATUS_RESPONSES = {
    status.HTTP_200_OK: MoviesSerializer,
    status.HTTP_404_NOT_FOUND: MoviesSerializer,
}

# examples
GET_LIST_MOVIES_EXAMPLES = [
    OpenApiExample(
        "Movies example",
        description="Test example for the post",
        value={
            "links": {
                "next": "http://127.0.0.1:8000/api/movies_v1/list/?page=3",
                "previous": "http://127.0.0.1:8000/api/movies_v1/list/?page=1"
            },
            "count": 20,
            "results": [
                value
            ]
        },
         status_codes=[str(status.HTTP_200_OK)],
    ),
]

POST_LIST_MOVIES_EXAMPLES_RESPONSE = [
    OpenApiExample(
        "Movies example",
        description="Test example for the post",
        response_only=True,
        value=value,
        status_codes=[str(status.HTTP_201_CREATED)],
    ),
]


GET_DETAIL_MOVIES_EXAMPLES = [
    OpenApiExample(
        "Movie example",
        description="Result when the server responds successfully",
        value=value,
         status_codes=[str(status.HTTP_200_OK)],
    ),
    OpenApiExample(
        "Movie   example",
        description="Result if object is not in database",
        value={
            "detail": "No Movies matches the given query."
        },
         status_codes=[str(status.HTTP_404_NOT_FOUND)],
    ),
]

PUT_DETAIL_MOVIES_EXAMPLES = [
    OpenApiExample(
        "Movie example",
        description="Result when the server responds successfully",
        value=value,
         status_codes=[str(status.HTTP_200_OK)],
    ),
    OpenApiExample(
        "Movie   example",
        description="Result if object is not in database",
        value={
            "detail": "JSON parse error - Expecting value: line # column #(char #)"
        },
         status_codes=[str(status.HTTP_400_BAD_REQUEST)],
    ),
    OpenApiExample(
        "Movie   example",
        description="Result if object is not in database",
        value={
            "detail": "No Movies matches the given query."
        },
         status_codes=[str(status.HTTP_404_NOT_FOUND)],
    ),
]

DELETE_DETAIL_MOVIES_EXAMPLES = [
    OpenApiExample(
        "Movie example",
        description="Result when the server responds successfully",
        value={'result': 'The movie has been removed.'},
         status_codes=[str(status.HTTP_200_OK)],
    ),
    OpenApiExample(
        "Movie   example",
        description="Result if object is not in database",
        value={
            "detail": "No Movies matches the given query."
        },
         status_codes=[str(status.HTTP_404_NOT_FOUND)],
    ),
]