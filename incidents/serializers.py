from rest_framework import serializers
from django.shortcuts import get_object_or_404
from incidents.models import *
import base64


class Base64Field(serializers.Field):

    def to_representation(self, value):
        return base64.b64encode(value).decode('utf-8')

    def to_internal_value(self, data):
        return base64.b64decode(data.encode('utf-8'))


class IncidentSerializer(serializers.ModelSerializer):
    payload = Base64Field()
    hub_guid = serializers.UUIDField(write_only=True)
    module_guid = serializers.UUIDField(write_only=True)

    class Meta:
        model = Incident
        fields = ['id', 'hub', 'hub_guid', 'module_guid', 'module', 'payload', 'timestamp']
        read_only_fields = ['hub', 'module', 'timestamp']

    def create(self, validated_data):
        module = Module.objects.get(guid__exact=validated_data['module_guid'])
        hub = Hub.objects.get(guid__exact=validated_data['hub_guid'])

        validated_data.pop('module_guid', None)
        validated_data.pop('hub_guid', None)
        validated_data['module'] = module
        validated_data['hub'] = hub
        return Incident.objects.create(**validated_data)
