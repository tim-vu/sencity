import time

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from hubs.models import Hub, ModuleSetting, Module


class HubSerializer(serializers.ModelSerializer):

    modules = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Hub
        fields = ['id', 'location_name', 'longitude', 'latitude', 'guid', 'modules']
        validators = [
            UniqueTogetherValidator(
                queryset=Hub.objects.all(),
                fields=['longitude', 'latitude'],
                message='The hub location must be unique'
            )
        ]


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'name', 'guid']


class ModuleSettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModuleSetting
        fields = ['id', 'module', 'hub', 'key', 'value']
        read_only_fields = ['id']
        validators = [
            UniqueTogetherValidator(
                queryset=ModuleSetting.objects.all(),
                fields=['key', 'hub', 'module'],
                message='The key must be unique for a given module'
            )
        ]

    def create(self, validated_data):
        unix_timestamp = int(time.time())
        validated_data['timestamp'] = unix_timestamp
        return ModuleSetting.objects.create(**validated_data)


class ModuleSettingDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModuleSetting
        fields = ['id', 'key', 'value']


class ModuleSettingChangedSerializer(serializers.ModelSerializer):

    module_guid = serializers.UUIDField(read_only=True, source='module.guid')
    hub_guid = serializers.UUIDField(read_only=True, source='hub.guid')

    class Meta:
        model = ModuleSetting
        fields = ['module_guid', 'hub_guid', 'key', 'value']
        read_only_fields = ['key', 'value']
