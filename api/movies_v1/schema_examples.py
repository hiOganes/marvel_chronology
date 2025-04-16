from rest_framework import status
from drf_spectacular.utils import OpenApiParameter, OpenApiExample

from api.movies_v1.serializers import MoviesSerializer


# description
GET_LIST_MOVIES_DESCRIPTION = '''
    This endpoint is needed to get a list of movies. 
    The list is divided into pages, 10 movies on one page. 
    There is also a search by movie title, in Russian and English.
    '''

POST_LIST_MOVIES_DESCRIPTION = '''
    Create new movie.
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


# responses
GET_LIST_MOVIES_STATUS_RESPONSES = {
    status.HTTP_200_OK: MoviesSerializer,
}


# examples
GET_LIST_MOVIES_EXAMPLES = [
    OpenApiExample(
        "Movies example",
        description="Test example for the post",
        value=
        {
            "links": {
                "next": "http://127.0.0.1:8000/api/movies_v1/list/?page=2",
                "previous": 'null'
            },
            "count": 20,
            "results": [
                {
                    "position": 1,
                    "title_ru": "Первый мститель",
                    "title_en": "Captain America: The First Avenger",
                    "release_date": "2011-07-28T00:00:00Z",
                    "timing": 124,
                    "director": "Джо Джонстон",
                    "trailer": "https://www.youtube.com/watch?v=FxTlOl03x9c",
                    "description": "Стив Роджерс добровольно соглашается принять участие в эксперименте, который превратит его в суперсолдата, известного как Первый мститель. Роджерс вступает в вооруженные силы США вместе с Баки Барнсом и Пегги Картер, чтобы бороться с враждебной организацией ГИДРА, которой управляет безжалостный Красный Череп.",
                    "poster": "/media/posters/2025/04/09/3840x.webp",
                    "content": "MOVIE"
                }
            ]
        },
         status_codes=[str(status.HTTP_200_OK)],
    ),
]