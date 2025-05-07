from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser

from apps.directors.models import Directors
from api.directors_v1.serializers import DirectorsSerializer
from api.directors_v1 import schema_examples


tags=['Directors']


class CreateDirectorsAPIView(APIView):
    model = Directors
    serializer_class = DirectorsSerializer
    permission_classes = [IsAdminUser]

    @extend_schema(
        summary='This endpoint create a new director.',
        description=schema_examples.POST_CREATE_DIRECTORS_DESCRIPTION,
        tags=tags,
        responses=schema_examples.POST_CREATE_DIRECTORS_STATUS_RESPONSES,
        examples=schema_examples.POST_CREATE_DIRECTORS_EXAMPLES,
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
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class DeleteDirectorsAPIView(APIView):
    model = Directors
    permission_classes = [IsAdminUser]

    @extend_schema(
        summary='This endpoint delete a director.',
        description=schema_examples.DELETE_DIRECTORS_DESCRIPTION,
        tags=tags,
        responses=schema_examples.DELETE_DIRECTORS_STATUS_RESPONSES,
        examples=schema_examples.DELETE_DIRECTORS_EXAMPLES,
    )
    def delete(self, request, *args, **kwargs):
        director = get_object_or_404(self.model, pk=kwargs.get('pk'))
        director.delete()
        return Response(
            data={'result': 'Director has been deleted'},
            status=status.HTTP_204_NO_CONTENT
        )