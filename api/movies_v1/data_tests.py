import io
from PIL import Image
from datetime import datetime

from apps.directors.models import Directors
from apps.movies.models import Movies


def generete_image():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, format='PNG')
    file.name = 'test.png'
    file.seek(0)
    return file

def new_movie():
    return {
        "position": 1,
        "title_ru": "строка",
        "title_en": "string",
        "release_date": datetime.now().date(),
        "timing": 120,
        "director": Directors.objects.all()[0].id,
        "trailer": "https://www.youtube.com/watch?v=KN0FHCErJjo",
        "description": "string",
        "poster": generete_image(),
        "content": Movies.MediaContent.MOVIE
    }