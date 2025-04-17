from rest_framework import status
from drf_spectacular.utils import OpenApiExample

from api.directors_v1.serializers import DirectorsSerializer


# description
POST_CREATE_DIRECTORS_DESCRIPTION = '''
    Create new movie.
    '''

DELETE_DIRECTORS_DESCRIPTION = '''
    By the director ID you can delete director
    '''


# responses
POST_CREATE_DIRECTORS_STATUS_RESPONSES = {
    status.HTTP_201_CREATED: DirectorsSerializer,
    status.HTTP_400_BAD_REQUEST: DirectorsSerializer,
}

DELETE_DIRECTORS_STATUS_RESPONSES = {
    status.HTTP_200_OK: DirectorsSerializer,
    status.HTTP_404_NOT_FOUND: DirectorsSerializer,
}

# examples
POST_CREATE_DIRECTORS_EXAMPLES = [
    OpenApiExample(
        "Movies example",
        description="Test example for the post",
        response_only=True,
        value={
            'first_name': 'Джон',
            'last_name': 'Джонстон'
        },
        status_codes=[str(status.HTTP_201_CREATED)],
    ),
    OpenApiExample(
        "Movies example",
        description="Test example for the post",
        response_only=True,
        value={
            "detail": "JSON parse error - "
                      "Expecting value: line # column # (char #)"
        },
        status_codes=[str(status.HTTP_400_BAD_REQUEST)],
    ),
]

DELETE_DIRECTORS_EXAMPLES = [
    OpenApiExample(
        "Movie example",
        description="Result when the server responds successfully",
        value={'result': 'The director has been removed.'},
         status_codes=[str(status.HTTP_200_OK)],
    ),
    OpenApiExample(
        "Movie   example",
        description="Result if object is not in database",
        value={
            "detail": "No Directors matches the given query."
        },
         status_codes=[str(status.HTTP_404_NOT_FOUND)],
    ),
]