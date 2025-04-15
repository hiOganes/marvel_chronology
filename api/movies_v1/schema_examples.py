from drf_spectacular.utils import OpenApiParameter


SEARCH_PARAMETERS = [
    OpenApiParameter(
        'search',
        str,
        description='Искать по русскому названию фильма',
        required=False
    )
]