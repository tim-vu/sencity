from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from hubs.models import Hub, Module, ModuleSetting
from hubs.serializers import HubSerializer, ModuleSerializer, ModuleSettingSerializer, ModuleSettingDetailSerializer, ModuleSettingChangedSerializer
from rest_framework import generics, mixins, status


class HubList(generics.ListCreateAPIView):
    queryset = Hub.objects.all()
    serializer_class = HubSerializer


class HubDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hub.objects.all()
    serializer_class = HubSerializer


class ModuleList(generics.ListCreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


class HubEnabledModules(APIView):

    hub_pk_parameter = openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER)
    module_pk_parameter = openapi.Parameter('module_pk', openapi.IN_PATH, type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(responses={200: HubSerializer()}, manual_parameters=[hub_pk_parameter, module_pk_parameter])
    def put(self, request, *args, **kwargs):
        hub = get_object_or_404(Hub.objects.prefetch_related('modules'), pk=kwargs.get('id'))
        module = get_object_or_404(Module.objects, pk=kwargs.get('module_pk'))

        if hub.modules.filter(pk=module.id).exists():
            return Response({'detail': "The hub already has this module"}, status=status.HTTP_400_BAD_REQUEST)

        hub.modules.add(module)
        hub.save()

        serializer = HubSerializer(hub)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: HubSerializer()}, manual_parameters=[hub_pk_parameter, module_pk_parameter])
    def delete(self, request, *args, **kwargs):
        module_pk = kwargs.get("module_pk")
        hub = get_object_or_404(Hub.objects.prefetch_related('modules'), pk=kwargs.get('id'))
        module = get_object_or_404(Module.objects, pk=module_pk)

        if not hub.modules.filter(pk=module_pk).exists():
            return Response({'detail': "The hub does not have this module"}, status=status.HTTP_400_BAD_REQUEST)

        hub.modules.remove(module)
        hub.save()

        serializer = HubSerializer(hub)
        return Response(serializer.data)


class ModuleSettingList(generics.ListCreateAPIView):
    queryset = ModuleSetting.objects.all()
    serializer_class = ModuleSettingSerializer


class ModuleSettingDetail(generics.GenericAPIView,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin):
    queryset = ModuleSetting.objects.all()
    serializer_class = ModuleSettingDetailSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ModuleSettingChanged(generics.ListAPIView):
    serializer_class = ModuleSettingChangedSerializer

    def get_queryset(self):
        timestamp = self.kwargs['unix_timestamp']
        return list(ModuleSetting.objects.select_related('module').filter(timestamp__gte=timestamp))

