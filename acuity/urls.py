from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AppointmentsView

router = DefaultRouter()
router.register('', AppointmentsView, base_name="acuity-appointments")

urlpatterns = router.urls
