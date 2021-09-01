from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, mixins, status
from rest_framework.response import Response

from . import serializers
from . import models


class IncidentList(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = serializers.IncidentSerializer
    queryset = models.Incident.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        try:
            return self.create(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
