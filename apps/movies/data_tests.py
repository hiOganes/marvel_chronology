from datetime import datetime

from apps.directors.models import Directors


new_movie = {
        'position': 1,
        'title_ru': 'Фильм',
        'title_en': 'Film',
        'release_date': datetime.now(),
        'timing': 100,
        'director_id': Directors.objects.all()[0],
        'trailer': 'https://www.youtube.com/watch?v=FxTlOl03x9c',
        'description': 'description',
        'poster': 'posters/2025/04/09/3840x.webp',
        'content': 'MOVIE'
    }

invalid_new_movie = {
        'position': 'string',
        'title_ru': 'Фильм',
        'title_en': 'Film',
        'release_date': datetime.now(),
        'timing': '100',
        'director_id': Directors.objects.all()[0],
        'trailer': 'https://www.youtube.com/watch?v=FxTlOl03x9c',
        'description': 'description',
        'poster': 'posters/2025/04/09/3840x.webp',
        'content': 'MOVIES'
    }