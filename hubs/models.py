from django.db import models


class Module(models.Model):
    name = models.CharField(max_length=200, unique=True)
    guid = models.UUIDField(unique=True)


class Hub(models.Model):
    location_name = models.CharField(max_length=200, unique=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    guid = models.UUIDField(unique=True)
    modules = models.ManyToManyField(Module)


class ModuleSetting(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=200)
    timestamp = models.IntegerField()


