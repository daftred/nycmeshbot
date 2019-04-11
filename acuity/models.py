from django.conf import settings
from django.db import models
from django.utils import timezone
import requests, logging, datetime

logger = logging.getLogger(__name__)

class Appointment(models.Model):
    apptId = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=25)
    dateTime = models.DateTimeField(blank=True, null=True)
    apptType = models.CharField(max_length=20)
    duration = models.DurationField()
    nodeNumber = models.SmallIntegerField()
    address = models.CharField(max_length=255)
    notes = models.TextField()

    def __str__(self):
        return "{} - {}".format(self.nodeNumber, self.apptId)

