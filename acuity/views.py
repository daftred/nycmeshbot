#Framework/Python Imports
from django.conf import settings
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.reverse import reverse
import logging, requests, datetime, json

#Models Import
from .models import Appointment

#Serializers Import
from .serializers import AppointmentSerializer, AcuitySerializer

logger = logging.getLogger(__name__)

class AppointmentsView(ViewSet):
    serializer_class = AppointmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = AppointmentSerializer

        if request.META.get('HTTP_X_ACUITY_SIGNATURE'):
            input_data = AcuitySerializer(data=request.data.copy())
            input_data.is_valid(raise_exception=True)

            appt = self.getById(input_data.validated_data.get('id'))
            try:
                apptExist = Appointment.objects.get(apptId=appt['apptId'])
                if apptExist:
                    appt['id'] = apptExist.id
            except Appointment.DoesNotExist:
                validAppt = AppointmentSerializer(data=appt)
                validAppt.is_valid(raise_exception=True)
                validAppt.save()
            else:
                if appt['id']:
                    theid = appt.pop('id', None)
                    apptId = appt.pop('apptId')
                    apptModel, created = Appointment.objects.update_or_create(pk=theid, apptId=apptId, defaults=appt)
                else:
                    raise Exception("Something went wrong...")

            return Response(status=204)
        else:
            return Response(status=401)

    def list(self, request):
        queryset = Appointment.objects.all()
        serializer = AppointmentSerializer
        return Response(serializer.data)


    def getById(self, apptId):
        try:
            acuityRecord = self.refreshFromAcuity(apptId)
        except Exception as e:
            logger.error(e)
        try:
            if acuityRecord:
                sqlFind = acuityRecord
            else:
                sqlFind, created = Appointment.objects.get(apptId=apptId)
        except Exception as e:
            logger.error(e)

        return sqlFind


    def refreshFromAcuity(self, apptId):
        response = requests.get(
            "https://acuityscheduling.com/api/v1/appointments/" + str(apptId),
            auth=(settings.BOT['ACUITY_USER_ID'], settings.BOT['ACUITY_API_KEY']),
        )

        '''Takes a requests.response object. Returns the contents of the object in JSON format if the status_code is "200"
        if status_code is any other code it raises an exception detailing the errors as returned from the server.  '''
        if str(response.status_code) == '200':
            response_data = json.loads(response.content.decode())
        else:
            raise Exception('\n' + datetime.datetime.now().isoformat() + ' \n Server responded with ' + response.status_code + '. \n error: ' + response.json())

        for form in response_data['forms']:
            for field in form['values']:
                if field['name'] == "Node Number":
                    node_number = field['value']
                elif field['name'] == "Address and Apartment #":
                    address = field['value']
                elif field['name'] == "Notes":
                    notes = field['value']

        appt_data = {
                'apptId': response_data['id'],
                'name': response_data['firstName'] + " " + response_data['lastName'],
                'phone': response_data['phone'],
                'dateTime': response_data['datetime'],
                'apptType': response_data['type'],
                'duration': datetime.timedelta(minutes=int(response_data['duration'])),
                'nodeNumber': node_number,
                'address': address,
                'notes': notes
            }

        return appt_data
