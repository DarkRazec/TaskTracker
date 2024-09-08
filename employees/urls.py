from django.urls import path
from rest_framework.routers import DefaultRouter

from employees.apps import EmployeesConfig
from employees.views import EmployeesViewSet, BusyEmployeesListAPIView

app_name = EmployeesConfig.name

router = DefaultRouter()
router.register(r'employees', EmployeesViewSet, basename='employees')

urlpatterns = [
                  path('employees/busy/', BusyEmployeesListAPIView.as_view(), name='busy employees')
              ] + router.urls
