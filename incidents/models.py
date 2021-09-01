from django.db import models
from hubs.models import Hub, Module
from datetime import datetime


class Incident(models.Model):
    timestamp = models.DateTimeField(default=datetime.now)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    payload = models.BinaryField(max_length=50)
