from rest_framework import serializers
from .models import Appointment
import logging

logger = logging.getLogger(__name__)

class AcuitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField(max_length=25)

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ("id", "apptId", "name", "phone", "dateTime", "apptType", "duration", "nodeNumber", "address", "notes")

